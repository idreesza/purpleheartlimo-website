import os
import json
import tomllib
import urllib.request
import urllib.parse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

IS_PROD = bool(os.environ.get('REPLIT_DEPLOYMENT'))

def _load_redirects():
    """Load path-based redirect rules from netlify.toml (single source of
    truth for legacy-slug 301s). Host-based rules (www) are handled in code;
    status-200 rewrites are covered by the extensionless handler or native
    /api endpoints; the /* -> /404.html catch-all is handled as a custom
    error page."""
    exact, prefixes = {}, []
    try:
        with open(os.path.join(os.path.dirname(__file__), 'netlify.toml'), 'rb') as f:
            rules = tomllib.load(f).get('redirects', [])
    except Exception as e:
        print('WARNING: could not load netlify.toml redirects:', e)
        return exact, prefixes
    for r in rules:
        frm, to, status = r.get('from', ''), r.get('to', ''), int(r.get('status', 301))
        if frm.startswith('http') or status not in (301, 410) or frm == '/*':
            continue
        if frm.endswith('/*'):
            prefixes.append((frm[:-1], to, status))  # keep trailing slash on prefix
        else:
            exact[frm] = (to, status)
    return exact, prefixes

REDIRECTS_EXACT, REDIRECT_PREFIXES = _load_redirects()

class Handler(SimpleHTTPRequestHandler):
    def _www_redirect(self):
        """301 www.purpleheartlimo.com -> purpleheartlimo.com, preserving
        the full path + query string. Runs before any other routing."""
        host = (self.headers.get('Host') or '').split(':')[0].strip().lower()
        if host == 'www.purpleheartlimo.com':
            self.send_response(301)
            self.send_header('Location', 'https://purpleheartlimo.com' + self.path)
            self.send_header('Cache-Control', 'max-age=3600')
            SimpleHTTPRequestHandler.end_headers(self)
            return True
        return False

    def send_error(self, code, message=None, explain=None):
        # Custom branded 404 page (parity with the old static deployment's
        # /* -> /404.html rule).
        if code == 404 and os.path.isfile('404.html'):
            try:
                with open('404.html', 'rb') as f:
                    body = f.read()
                self.send_response(404)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                SimpleHTTPRequestHandler.end_headers(self)
                if self.command != 'HEAD':
                    self.wfile.write(body)
                return
            except Exception:
                pass
        return SimpleHTTPRequestHandler.send_error(self, code, message, explain)

    def do_HEAD(self):
        # HEAD must mirror GET exactly (same status + headers, no body), so
        # it goes through the same routing; body writes are gated on
        # self.command inside the handlers.
        return self._route()

    def _legacy_redirect(self):
        """Legacy-slug 301s/410s ported from netlify.toml (the static
        deployment's rewrites don't apply once a server handles requests)."""
        parsed = urllib.parse.urlparse(self.path)
        path, query = parsed.path, parsed.query
        hit = REDIRECTS_EXACT.get(path) or (path != '/' and REDIRECTS_EXACT.get(path.rstrip('/'))) or None
        if hit is None:
            for prefix, to, status in REDIRECT_PREFIXES:
                if path.startswith(prefix):
                    hit = (to, status)
                    break
        if hit is None:
            return False
        to, status = hit
        if status == 410:
            self.send_response(410)
            SimpleHTTPRequestHandler.end_headers(self)
            return True
        self.send_response(301)
        self.send_header('Location', to + ('?' + query if query else ''))
        self.send_header('Cache-Control', 'max-age=3600')
        SimpleHTTPRequestHandler.end_headers(self)
        return True

    def do_GET(self):
        return self._route()

    def _route(self):
        """Shared routing for GET and HEAD."""
        if self._www_redirect():
            return
        if self._legacy_redirect():
            return
        if self.path == '/config.js':
            key = os.environ.get('AVIATIONSTACK_API_KEY', '')
            ejs_pub  = os.environ.get('EMAILJS_PUBLIC_KEY', '')
            ejs_svc  = os.environ.get('EMAILJS_SERVICE_ID', '')
            ejs_tpl  = os.environ.get('EMAILJS_TEMPLATE_ID', '')
            js = (f'window.AVIATION_KEY = "{key}";'
                  f'window.EJS_PUBLIC_KEY = "{ejs_pub}";'
                  f'window.EJS_SERVICE_ID = "{ejs_svc}";'
                  f'window.EJS_TEMPLATE_ID = "{ejs_tpl}";')
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(js.encode())))
            self.end_headers()
            if self.command != 'HEAD':
                self.wfile.write(js.encode())
            return

        if self.path.startswith('/api/positioning'):
            # Hub positioning: pick the anchor hub for a trip and return the
            # real driving distance/time from that hub to the far end.
            try:
                qs = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(qs)
                pickup = params.get('pickup', [''])[0]
                dropoff = params.get('dropoff', [''])[0]
                if not pickup:
                    return self._json({'error': 'missing pickup'}, 400)
                result = self._hub_positioning(pickup, dropoff)
                if result is None:
                    return self._json({'error': 'no_route'}, 400)
                return self._json(result)
            except Exception as e:
                return self._json({'error': str(e)}, 500)

        if self.path.startswith('/api/distance'):
            try:
                qs = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(qs)
                origin = params.get('origin', [''])[0]
                destination = params.get('destination', [''])[0]
                if not (origin and destination):
                    return self._json({'error': 'missing params'}, 400)
                result = self._google_route(origin, destination)
                if result is None:
                    # Google Routes API unavailable (not enabled on the
                    # project yet) — fall back to free OpenStreetMap routing.
                    result = self._osrm_route(origin, destination)
                if result is None:
                    return self._json({'error': 'no_route'}, 400)
                return self._json(result)
            except Exception as e:
                return self._json({'error': str(e)}, 500)

        # Netlify-style pretty URLs: serve /blog/foo from /blog/foo.html
        # so the dev preview matches production (extensionless canonicals).
        clean = urllib.parse.urlparse(self.path).path
        if clean and not clean.endswith('/'):
            fs_path = clean.lstrip('/')
            if not os.path.isfile(fs_path) and os.path.isfile(fs_path + '.html'):
                self.path = clean + '.html'

        if self.command == 'HEAD':
            return super().do_HEAD()
        return super().do_GET()

    def end_headers(self):
        if IS_PROD:
            # Production: cache static assets, always revalidate HTML.
            p = urllib.parse.urlparse(self.path).path.lower()
            if p.endswith(('.css', '.js', '.webp', '.png', '.jpg', '.jpeg', '.svg', '.ico', '.woff', '.woff2', '.mp4')):
                self.send_header('Cache-Control', 'public, max-age=86400')
            else:
                self.send_header('Cache-Control', 'no-cache')
        else:
            # Dev preview: never cache, so edits show up on refresh.
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        SimpleHTTPRequestHandler.end_headers(self)

    def _google_route(self, origin, destination):
        gkey = os.environ.get('GOOGLE_MAPS_API_KEY', '')
        if not gkey:
            return None
        try:
            url = 'https://routes.googleapis.com/directions/v2:computeRoutes'
            body = json.dumps({
                'origin': {'address': origin},
                'destination': {'address': destination},
                'travelMode': 'DRIVE',
                'routingPreference': 'TRAFFIC_AWARE',
                'units': 'IMPERIAL',
            }).encode()
            req = urllib.request.Request(url, data=body, method='POST', headers={
                'Content-Type': 'application/json',
                'X-Goog-Api-Key': gkey,
                'X-Goog-FieldMask': 'routes.distanceMeters,routes.duration',
            })
            with urllib.request.urlopen(req, timeout=12) as r:
                data = json.loads(r.read().decode())
            routes = data.get('routes') or []
            if not routes:
                return None
            rt = routes[0]
            meters = rt.get('distanceMeters', 0)
            dur = str(rt.get('duration', '0s'))
            ds = dur[:-1] if dur.endswith('s') else dur
            try:
                seconds = int(round(float(ds)))
            except Exception:
                seconds = 0
            return {
                'meters': meters,
                'miles': round(meters / 1609.34, 1),
                'seconds': seconds,
                'minutes': round(seconds / 60),
                'source': 'google',
            }
        except Exception:
            return None

    # Operating hubs: every vehicle starts and ends its day at one of these.
    HUBS = [
        ('Austin',            -97.7431, 30.2672),
        ('Dallas\u2013Fort Worth', -96.7970, 32.7767),
        ('Houston',           -95.3698, 29.7604),
    ]
    HUB_FREE_MILES = 60
    _geo_cache = {}

    @staticmethod
    def _haversine_miles(a, b):
        import math
        lon1, lat1, lon2, lat2 = map(math.radians, (float(a[0]), float(a[1]), float(b[0]), float(b[1])))
        h = (math.sin((lat2 - lat1) / 2) ** 2 +
             math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
        return 3958.8 * 2 * math.asin(math.sqrt(h))

    def _hub_positioning(self, pickup, dropoff):
        p = self._geocode(pickup)
        if not p:
            return None
        d = None
        if dropoff:
            d = self._geocode(dropoff)
            if not d:
                # A drop-off was given but couldn't be located — fail loudly
                # rather than quietly pricing from the pickup alone.
                return None
        # Anchor hub: the hub nearest to either end of the trip. A trip that
        # touches a hub metro naturally selects that hub; a remote trip gets
        # whichever hub is closest overall.
        best = None
        for name, lon, lat in self.HUBS:
            hp = self._haversine_miles((lon, lat), p)
            hd = self._haversine_miles((lon, lat), d) if d else hp
            score = min(hp, hd)
            if best is None or score < best[0]:
                best = (score, name, (lon, lat), hp, hd)
        _, hub_name, hub_pt, hp, hd = best
        # Far end of the trip relative to the anchor hub
        far_pt = d if (d and hd > hp) else p
        route = self._route_coords(hub_pt, far_pt)
        if route is None:
            return None
        route['hub'] = hub_name
        route['free_miles'] = self.HUB_FREE_MILES
        return route

    def _route_coords(self, a, b):
        try:
            url = (f'https://router.project-osrm.org/route/v1/driving/'
                   f'{a[0]},{a[1]};{b[0]},{b[1]}?overview=false')
            req = urllib.request.Request(url, headers={
                'User-Agent': 'PurpleHeartLimo/1.0 (purpleheartlimo.com)',
            })
            with urllib.request.urlopen(req, timeout=12) as r:
                data = json.loads(r.read().decode())
            routes = data.get('routes') or []
            if not routes:
                return None
            meters = routes[0].get('distance', 0)
            seconds = int(round(routes[0].get('duration', 0)))
            return {
                'meters': int(meters),
                'miles': round(meters / 1609.34, 1),
                'seconds': seconds,
                'minutes': round(seconds / 60),
                'source': 'osrm',
            }
        except Exception:
            return None

    def _geocode(self, q):
        cached = Handler._geo_cache.get(q)
        if cached is not None:
            return cached
        url = ('https://nominatim.openstreetmap.org/search?format=json&limit=1'
               '&countrycodes=us&q=' + urllib.parse.quote(q))
        req = urllib.request.Request(url, headers={
            'User-Agent': 'PurpleHeartLimo/1.0 (purpleheartlimo.com)',
            'Accept-Language': 'en',
        })
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
        if not data:
            return None
        result = (data[0]['lon'], data[0]['lat'])
        Handler._geo_cache[q] = result
        return result

    def _osrm_route(self, origin, destination):
        try:
            a = self._geocode(origin)
            b = self._geocode(destination)
            if not a or not b:
                return None
            url = (f'https://router.project-osrm.org/route/v1/driving/'
                   f'{a[0]},{a[1]};{b[0]},{b[1]}?overview=false')
            req = urllib.request.Request(url, headers={
                'User-Agent': 'PurpleHeartLimo/1.0 (purpleheartlimo.com)',
            })
            with urllib.request.urlopen(req, timeout=12) as r:
                data = json.loads(r.read().decode())
            routes = data.get('routes') or []
            if not routes:
                return None
            meters = routes[0].get('distance', 0)
            seconds = int(round(routes[0].get('duration', 0)))
            return {
                'meters': int(meters),
                'miles': round(meters / 1609.34, 1),
                'seconds': seconds,
                'minutes': round(seconds / 60),
                'source': 'osrm',
            }
        except Exception:
            return None

    def _json(self, obj, status=200):
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(body)

    def log_message(self, format, *args):
        print(format % args)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    server = ThreadingHTTPServer(('0.0.0.0', port), Handler)
    print(f'Serving on port {port} ({"production" if IS_PROD else "dev"}; '
          f'{len(REDIRECTS_EXACT)} exact + {len(REDIRECT_PREFIXES)} prefix redirects loaded)')
    server.serve_forever()
