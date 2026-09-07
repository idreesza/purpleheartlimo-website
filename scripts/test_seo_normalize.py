#!/usr/bin/env python3
"""Focused regression tests for sitewide SEO normalization helpers."""
import unittest

import seo_normalize


class AssetNormalizationTests(unittest.TestCase):
    def test_preserves_nojs_stylesheet_fallback(self):
        url = "https://fonts.example/family.css"
        source = (
            "<head>"
            f'<link href="{url}" media="print" '
            'onload="this.media=\'all\'" rel="stylesheet">'
            f'<noscript><link href="{url}" rel="stylesheet"></noscript>'
            "</head>"
        )
        normalized = seo_normalize.dedupe_asset_references(source)
        self.assertEqual(normalized.count(url), 2)

    def test_restores_non_adjacent_async_stylesheet_fallbacks(self):
        first = "https://fonts.example/first.css"
        second = "https://fonts.example/second.css"
        source = (
            "<head>"
            f'<link href="{first}" media="print" '
            'onload="this.media=\'all\'" rel="stylesheet">'
            f'<link href="{second}" media="print" '
            'onload="this.media=\'all\'" rel="stylesheet">'
            f'<noscript><link href="{second}" rel="stylesheet"></noscript>'
            "<noscript></noscript>"
            "</head>"
        )
        restored = seo_normalize.restore_nojs_stylesheet_fallbacks(source)
        self.assertEqual(restored.count(first), 2)
        self.assertEqual(restored.count(second), 2)
        self.assertNotIn("<noscript></noscript>", restored)

    def test_removes_only_unconditional_duplicate_assets(self):
        source = (
            "<head>"
            '<link href="/site.css" rel="stylesheet">'
            '<link href="/site.css" rel="stylesheet">'
            '<script defer src="/site.js"></script>'
            '<script defer src="/site.js"></script>'
            "</head>"
        )
        normalized = seo_normalize.dedupe_asset_references(source)
        self.assertEqual(normalized.count("/site.css"), 1)
        self.assertEqual(normalized.count("/site.js"), 1)


if __name__ == "__main__":
    unittest.main()