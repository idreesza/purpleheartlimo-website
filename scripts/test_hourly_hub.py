#!/usr/bin/env python3
"""Focused tests for the server-only hourly hub availability endpoint."""
import json
from http.client import HTTPConnection
from pathlib import Path
import sys
import threading
import unittest
from urllib.parse import parse_qs, urlsplit
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import server
from server import Handler
from http.server import ThreadingHTTPServer


class _GoogleResponse:
    status = 200

    def __init__(self, payload):
        self.payload = payload

    def read(self):
        return json.dumps(self.payload).encode('utf-8')

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False


def _distance_matrix(austin_meters, dallas_meters):
    return {
        'status': 'OK',
        'rows': [{
            'elements': [
                {'status': 'OK', 'distance': {'value': austin_meters}},
                {'status': 'OK', 'distance': {'value': dallas_meters}},
            ],
        }],
    }


class HourlyHubEndpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join(timeout=2)

    def setUp(self):
        Handler._hourly_hub_cache.clear()
        self.env_patch = mock.patch.dict(
            server.os.environ,
            {'GOOGLE_MAPS_API_KEY': 'test-server-key'},
            clear=False,
        )
        self.env_patch.start()
        self.urlopen_patch = mock.patch('server.urllib.request.urlopen')
        self.env = self.urlopen_patch.start()
        self.addCleanup(self.urlopen_patch.stop)
        self.addCleanup(self.env_patch.stop)

    def get(self, path):
        connection = HTTPConnection('127.0.0.1', self.httpd.server_port, timeout=3)
        connection.request('GET', path)
        response = connection.getresponse()
        body = response.read()
        connection.close()
        try:
            decoded = json.loads(body) if body else None
        except json.JSONDecodeError:
            decoded = body
        return response.status, decoded

    def test_google_success_selects_nearest_internally_and_exposes_only_flag(self):
        self.env_response = _GoogleResponse(_distance_matrix(18000, 9000))
        self.env.side_effect = lambda *_args, **_kwargs: self.env_response

        status, body = self.get('/api/hourly-hub?pickup=5200%20N%20Lamar%20Blvd%2C%20Austin%2C%20TX')

        self.assertEqual(status, 200)
        self.assertEqual(body, {'available': True})
        self.assertEqual(set(body), {'available'})
        cached_key = server._normalize_hourly_request(
            '5200 N Lamar Blvd, Austin, TX'
        )[2]
        self.assertEqual(Handler._hourly_hub_cache.get(cached_key), 'dallas')
        request = self.env.call_args.args[0]
        self.assertIn('distancematrix/json', request.full_url)
        self.assertNotIn('GOOGLE_MAPS_BROWSER_API_KEY', request.full_url)
        query = parse_qs(urlsplit(request.full_url).query)
        self.assertEqual(
            query['destinations'],
            ['3100 Esperanza Crossing, Austin, TX 78758|777 S Central Expy, Richardson, TX 75080'],
        )
        self.assertEqual(query['mode'], ['driving'])

    def test_success_is_cached_for_normalized_address_and_coordinates(self):
        self.env.side_effect = lambda *_args, **_kwargs: _GoogleResponse(
            _distance_matrix(1000, 2000)
        )
        first = self.get(
            '/api/hourly-hub?pickup=%205200%20N%20Lamar%20Blvd%20&lat=30&lon=-97'
        )
        second = self.get(
            '/api/hourly-hub?pickup=5200%20n%20lamar%20blvd&lat=30.00000000&lon=-97.0'
        )

        self.assertEqual(first, (200, {'available': True}))
        self.assertEqual(second, (200, {'available': True}))
        self.assertEqual(self.env.call_count, 1)

    def test_google_failure_returns_false_and_short_failure_is_cached(self):
        self.env.side_effect = OSError('provider unavailable')

        first = self.get('/api/hourly-hub?pickup=Somewhere%2C%20Austin%2C%20TX')
        second = self.get('/api/hourly-hub?pickup=Somewhere%2C%20Austin%2C%20TX')

        self.assertEqual(first, (200, {'available': False}))
        self.assertEqual(second, (200, {'available': False}))
        self.assertEqual(self.env.call_count, 1)

    def test_cache_is_bounded_and_expiry_differs_for_failures(self):
        now = [0.0]
        cache = server._BoundedTTLCache(
            max_entries=1,
            success_ttl=30,
            failure_ttl=2,
            clock=lambda: now[0],
        )
        cache.set('failed', None)
        now[0] = 1.9
        self.assertIsNone(cache.get('failed'))
        now[0] = 2.1
        self.assertIs(cache.get('failed'), server.HOURLY_HUB_CACHE_MISS)
        cache.set('one', 'austin')
        cache.set('two', 'dallas')
        self.assertEqual(len(cache), 1)
        self.assertIs(cache.get('one'), server.HOURLY_HUB_CACHE_MISS)
        self.assertEqual(cache.get('two'), 'dallas')

    def test_validation_rejects_missing_or_partial_coordinates(self):
        status, body = self.get('/api/hourly-hub')
        self.assertEqual(status, 400)
        self.assertEqual(body, {'error': 'pickup is required'})

        status, body = self.get('/api/hourly-hub?pickup=Address&lat=30')
        self.assertEqual(status, 400)
        self.assertEqual(body, {'error': 'lat and lon must be supplied together'})
        self.assertFalse(self.env.called)

    def test_source_files_are_not_public_static_assets(self):
        for path in (
            '/server.py',
            '/scripts/test_server_compression.py',
            '/attached_assets/Pasted-Here-s-your-complete-Replit-implementation-prompt-Purpl_1789527886501.txt',
        ):
            status, _body = self.get(path)
            self.assertEqual(status, 404, path)


if __name__ == '__main__':
    unittest.main()