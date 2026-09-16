#!/usr/bin/env python3
"""Focused checks for the Places API (New) address integration."""
import json
import os
from email.message import Message
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server import Handler  # noqa: E402


class GooglePlacesIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.helper = (ROOT / "js/google-places-autocomplete.js").read_text()
        cls.server = (ROOT / "server.py").read_text()

    def test_helper_uses_places_new_sessions_and_coordinates(self):
        self.assertIn("places.AutocompleteSuggestion", self.helper)
        self.assertIn("fetchAutocompleteSuggestions(", self.helper)
        self.assertIn("new places.AutocompleteSessionToken()", self.helper)
        self.assertIn("place.fetchFields({ fields: ['formattedAddress', 'location', 'displayName'] })", self.helper)
        self.assertIn("Powered by Google", self.helper)
        self.assertIn("powered_by_google_on_white.png", self.helper)
        self.assertIn("https://maps.googleapis.com/maps/api/js?", self.helper)
        self.assertIn("key=' + encodeURIComponent(browserKey)", self.helper)
        self.assertIn("&v=weekly&libraries=", self.helper)
        self.assertEqual(self.helper.count("https://maps.googleapis.com/maps/api/js?"), 1)
        self.assertIn("Google Maps authentication failed", self.helper)
        self.assertIn("Google Maps library unavailable", self.helper)
        self.assertNotIn("google.maps.places.Autocomplete", self.helper)
        self.assertNotIn("nominatim.openstreetmap.org", self.helper)

    def test_no_competing_maps_javascript_loader_in_pages(self):
        page_files = list(ROOT.rglob("*.html"))
        for page in page_files:
            text = page.read_text()
            self.assertNotIn("maps.googleapis.com/maps/api/js", text, page.name)
            self.assertNotIn("maps.google.com/maps/api/js", text, page.name)
            self.assertNotIn("google.maps.places.Autocomplete", text, page.name)
        for script in ROOT.rglob("*.js"):
            if script == ROOT / "js/google-places-autocomplete.js":
                continue
            text = script.read_text()
            self.assertNotIn("/maps/api/js", text, script.name)

    def test_pages_use_one_shared_helper(self):
        for relative in ("index.html", "booking.html", "es/booking.html"):
            text = (ROOT / relative).read_text()
            self.assertIn("/js/google-places-autocomplete.js", text)
            self.assertNotIn("nominatim.openstreetmap.org", text)
            self.assertNotIn("initNominatimAutocomplete", text)

    @staticmethod
    def _request():
        handler = object.__new__(Handler)
        handler.headers = Message()
        handler.path = "/api/google-maps-browser-key"
        handler.command = "GET"
        handler.response_status = None
        handler.response_headers = {}
        handler.response_body = b""
        handler.send_response = lambda status: setattr(handler, "response_status", status)
        handler.send_header = lambda name, value: handler.response_headers.__setitem__(name, value)
        handler.end_headers = lambda: None
        handler._write_body = lambda body: setattr(handler, "response_body", body)
        return handler

    def test_browser_key_route_returns_only_public_key_and_no_store(self):
        def fake_get(name, default=None):
            return "test-restricted-browser-key" if name == "GOOGLE_MAPS_BROWSER_API_KEY" else default

        with patch.object(os.environ, "get", side_effect=fake_get):
            handler = self._request()
            handler._route()

        self.assertEqual(handler.response_status, 200)
        self.assertEqual(json.loads(handler.response_body), {"key": "test-restricted-browser-key"})
        self.assertEqual(handler.response_headers["Cache-Control"], "no-store")
        self.assertNotIn("GOOGLE_MAPS_API_KEY", handler.response_body.decode())

    def test_browser_key_route_fails_explicitly_when_not_configured(self):
        def fake_get(name, default=None):
            return default

        with patch.object(os.environ, "get", side_effect=fake_get):
            handler = self._request()
            handler._route()

        self.assertEqual(handler.response_status, 503)
        self.assertEqual(
            json.loads(handler.response_body),
            {"error": "Google Maps address search unavailable"},
        )


if __name__ == "__main__":
    unittest.main()