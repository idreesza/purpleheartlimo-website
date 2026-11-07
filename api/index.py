"""Vercel Python function: runs the existing server.py request handler for the
dynamic endpoints (booking/contact email, quotes, hourly hub, maps key,
config.js, retired 410 URLs).

vercel.json rewrites each dynamic path to /api/index?__path=<original path>,
so the handler sees the same URL it would on a normal server and server.py
stays the single source of truth for this logic (and its tests).
"""
import os
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.chdir(ROOT)  # server.py resolves 404.html and netlify.toml relative to cwd
os.environ.setdefault('PRODUCTION', '1')

from server import Handler  # noqa: E402


class handler(Handler):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('directory', ROOT)
        super().__init__(*args, **kwargs)

    def parse_request(self):
        ok = super().parse_request()
        if ok:
            self.path = restore_original_path(self.path)
        return ok


def restore_original_path(path):
    """/api/index?__path=/api/distance&origin=x -> /api/distance?origin=x"""
    parsed = urllib.parse.urlsplit(path)
    pairs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    original = [value for key, value in pairs if key == '__path']
    if not original or not original[0].startswith('/'):
        return path
    rest = urllib.parse.urlencode([(k, v) for k, v in pairs if k != '__path'])
    return original[0] + ('?' + rest if rest else '')
