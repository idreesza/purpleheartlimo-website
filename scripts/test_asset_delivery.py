import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from email.message import Message

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server


class AssetDeliveryTests(unittest.TestCase):
    def headers_for(self, path):
        handler = object.__new__(server.Handler)
        handler.path = path
        values = {}
        handler.send_header = lambda key, value: values.update({key: value})
        with patch.object(server, 'IS_PROD', True), patch.object(server.SimpleHTTPRequestHandler, 'end_headers'):
            handler.end_headers()
        return values

    def test_versioned_assets_are_immutable(self):
        for suffix in ('css', 'js', 'webp', 'woff2'):
            self.assertEqual(self.headers_for('/asset.' + suffix + '?v=abc')['Cache-Control'],
                             'public, max-age=31536000, immutable')

    def test_unversioned_assets_and_html_revalidate(self):
        for path in ('/', '/booking.html', '/js/pricing.js'):
            self.assertEqual(self.headers_for(path)['Cache-Control'],
                             'public, max-age=0, must-revalidate')

    def test_html_charset(self):
        handler = object.__new__(server.Handler)
        self.assertEqual(handler.guess_type('index.html'), 'text/html; charset=utf-8')

    def test_build_and_tools_not_public(self):
        for path in ('/compiled-static/index.html', '/node_modules/esbuild/package.json',
                     '/generated-artifacts/lighthouse-after-mobile.json'):
            self.assertTrue(server.Handler._private_static_path(path))


if __name__ == '__main__':
    unittest.main()
