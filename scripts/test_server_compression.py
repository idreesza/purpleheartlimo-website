#!/usr/bin/env python3
"""Focused tests for HTTP content-encoding negotiation."""
from email.message import Message
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from server import Handler


class EncodingQualityTests(unittest.TestCase):
    def quality(self, header, encoding):
        handler = object.__new__(Handler)
        handler.headers = Message()
        if header is not None:
            handler.headers["Accept-Encoding"] = header
        return handler._encoding_quality(encoding)

    def test_identity_is_default_without_header(self):
        self.assertEqual(self.quality(None, "identity"), 1.0)
        self.assertEqual(self.quality(None, "gzip"), 0.0)

    def test_explicit_gzip_optout_overrides_wildcard(self):
        header = "gzip;q=0, *;q=1"
        self.assertEqual(self.quality(header, "gzip"), 0.0)
        self.assertEqual(self.quality(header, "identity"), 1.0)

    def test_rejects_both_available_representations(self):
        header = "gzip;q=0, identity;q=0"
        self.assertEqual(self.quality(header, "gzip"), 0.0)
        self.assertEqual(self.quality(header, "identity"), 0.0)

    def test_unsupported_encoding_can_reject_identity(self):
        header = "br, identity;q=0"
        self.assertEqual(self.quality(header, "gzip"), 0.0)
        self.assertEqual(self.quality(header, "identity"), 0.0)


if __name__ == "__main__":
    unittest.main()