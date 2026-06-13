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

        if self.path.startswith('/api/distance'):
            try:
                qs = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(qs)
                origin = params.get('origin', [''])[0]
                destination = params.get('destination', [''])[0]
                gkey = os.environ.get('GOOGLE_MAPS_API_KEY', '')
                if not (origin and destination and gkey):
                    return self._json({'error': 'missing params or key'}, 400)
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
                try:
                    with urllib.request.urlopen(req, timeout=12) as r:
                        data = json.loads(r.read().decode())
                except urllib.error.HTTPError as he:
                    msg = he.read().decode(errors='ignore')[:400]
                    return self._json({'error': f'HTTP {he.code}', 'message': msg}, 400)
                routes = data.get('routes') or []
                if not routes:
                    return self._json({'error': 'no_route'}, 400)
                rt = routes[0]
                meters = rt.get('distanceMeters', 0)
                dur = rt.get('duration', '0s')
                ds = str(dur).rstrip('s') if str(dur).endswith('s') else str(dur)
                try: seconds = int(round(float(ds)))
                except Exception: seconds = 0
                return self._json({
                    'meters': meters,
                    'miles': round(meters / 1609.34, 1),
                    'seconds': seconds,
                    'minutes': round(seconds / 60),
                })
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
