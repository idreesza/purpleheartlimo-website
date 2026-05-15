import os
import json
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
        else:
            super().do_GET()

    def log_message(self, format, *args):
        print(format % args)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f'Serving on port {port}')
    server.serve_forever()
