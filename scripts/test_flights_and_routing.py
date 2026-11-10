#!/usr/bin/env python3
"""Flight tracker proxy keeps the AviationStack key server-side; hub
positioning prefers Google and falls back to the free services."""
from pathlib import Path
import io
import json
import os
import sys
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import server  # noqa: E402


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def opener_returning(*payloads):
    calls = []

    def opener(url, timeout=None):
        calls.append(url)
        return FakeResponse(json.dumps(payloads[len(calls) - 1]).encode())
    opener.calls = calls
    return opener


class FlightLookupTests(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch.dict(os.environ, {'AVIATIONSTACK_API_KEY': 'secret-key'})
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_returns_first_flight(self):
        opener = opener_returning({'data': [{'flight': {'iata': 'AA1234'}}]})
        body, status = server._flight_lookup('aa1234', 'https://purpleheartlimo.com/flight-tracker.html', opener)
        self.assertEqual((status, body['data'][0]['flight']['iata']), (200, 'AA1234'))
        self.assertTrue(opener.calls[0].startswith('https://api.aviationstack.com/'))

    def test_free_plan_retries_over_http(self):
        opener = opener_returning({'error': {'code': 'https_access_restricted'}}, {'data': [{'x': 1}]})
        body, status = server._flight_lookup('UA100', '', opener)
        self.assertEqual((status, body), (200, {'data': [{'x': 1}]}))
        self.assertTrue(opener.calls[1].startswith('http://'))

    def test_invalid_number_and_foreign_referer(self):
        self.assertEqual(server._flight_lookup('drop table', '', opener_returning())[1], 400)
        self.assertEqual(server._flight_lookup('AA1', 'https://evil.example/', opener_returning())[1], 403)

    def test_vercel_preview_referer_allowed(self):
        opener = opener_returning({'data': []})
        self.assertEqual(server._flight_lookup('AA1', 'https://purpleheartlimo.vercel.app/x', opener)[1], 200)

    def test_provider_error_fails_soft_without_leaking_key(self):
        opener = opener_returning({'error': {'code': 'invalid_access_key'}})
        body, status = server._flight_lookup('AA1', '', opener)
        self.assertEqual(status, 200)
        self.assertEqual(body['data'], [])
        self.assertNotIn('secret-key', json.dumps(body))

    def test_no_key_returns_empty(self):
        with mock.patch.dict(os.environ, {'AVIATIONSTACK_API_KEY': ''}):
            self.assertEqual(server._flight_lookup('AA1', ''), ({'data': []}, 200))


class RoutingFallbackTests(unittest.TestCase):
    def handler(self):
        return server.Handler.__new__(server.Handler)

    def test_route_prefers_google(self):
        h = self.handler()
        google = {'miles': 10, 'source': 'google'}
        with mock.patch.object(h, '_google_route', return_value=google) as g, \
             mock.patch.object(h, '_osrm_route_coords') as osrm:
            self.assertEqual(h._route_coords((-97.7, 30.2), (-96.8, 32.7)), google)
        g.assert_called_once_with('', '', (30.2, -97.7), (32.7, -96.8))
        osrm.assert_not_called()

    def test_route_falls_back_to_osrm(self):
        h = self.handler()
        with mock.patch.object(h, '_google_route', return_value=None), \
             mock.patch.object(h, '_osrm_route_coords', return_value={'source': 'osrm'}):
            self.assertEqual(h._route_coords((0, 0), (1, 1)), {'source': 'osrm'})

    def test_geocode_falls_back_to_nominatim(self):
        h = self.handler()
        with mock.patch.dict(server.Handler._geo_cache, clear=True), \
             mock.patch.object(server.Handler, '_google_geocode', return_value=None), \
             mock.patch.object(h, '_nominatim_geocode', return_value=('-97.0', '32.0')) as nom:
            self.assertEqual(h._geocode('Dallas'), ('-97.0', '32.0'))
            nom.assert_called_once()

    def test_config_js_no_longer_exposes_aviation_key(self):
        source = (ROOT / 'server.py').read_text(encoding='utf-8')
        start = source.index("if self.path == '/config.js':")
        block = source[start:source.index('self.send_response(200)', start)]
        self.assertNotIn('AVIATION', block.split('# Only browser-safe values.')[1].split('\n', 3)[-1])


if __name__ == '__main__':
    unittest.main()
