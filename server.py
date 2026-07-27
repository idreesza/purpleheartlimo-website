import os
import json
import urllib.request
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
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
            self.end_headers()
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

        return super().do_GET()

    def end_headers(self):
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
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        print(format % args)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f'Serving on port {port}')
    server.serve_forever()
