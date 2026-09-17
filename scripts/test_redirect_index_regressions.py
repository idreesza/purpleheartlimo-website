#!/usr/bin/env python3
"""Regression checks for the focused legacy blog redirect cleanup.

These checks intentionally use the repository's source of truth rather than
guessing from a running server: every destination must have a real HTML file,
an indexable robots directive, and a canonical URL matching the destination.
"""
from pathlib import Path
import re
import sys
import tomllib
import unittest


ROOT = Path(__file__).resolve().parent.parent
BASE = "https://purpleheartlimo.com"

# Only redirects with a substantive equivalent are listed here. The remaining
# legacy ARTICLE rules that still point to /blog/ are deliberately retained
# until an equivalent article exists; they must not be guessed into a weaker
# destination merely to remove a generic redirect.
UPDATED = {
    "/blog/how-to-use-transportation-booking-systems-for-stress-free-travel":
        "/blog/the-ultimate-guide-to-booking-a-limo-service-in-austin/",
    "/blog/how-to-choose-the-perfect-limousine-for-your-wedding-day":
        "/blog/how-to-choose-the-perfect-limousine-for-your-wedding/",
    "/blog/choosing-the-right-limo-service--austin-prestige-limo-vs-alternatives":
        "/blog/comparing-purple-heart-limo-with-other-austin-limo-services/",
    "/blog/how-to-simplify-your-multi-step-limo-booking-experience":
        "/blog/the-ultimate-guide-to-booking-a-limo-service-in-austin/",
}

# No equivalent substantive article was found for these audit entries. Their
# generic destination is intentionally unchanged rather than inventing a
# topical redirect. They are still legacy sources and must stay out of the
# sitemap.
RETAINED_GENERIC = {
    "/blog/a-comprehensive-guide-to-transportation-services-in-austin--texas",
    "/blog/exploring-advanced-limousine-booking-systems--a-look-at-purple-heart-limo-s-technology",
    "/blog/how-purple-heart-limousine-uses-ai-for-seamless-booking-experiences",
    "/blog/the-future-of-transportation-booking-systems--how-innovations-are-changing-the-game",
}

LINK_FIXES = {
    "blog/arlington-entertainment-district-cowboys-games/index.html":
        ("/blog/arlington-entertainment.html", "/blog/arlington-entertainment"),
    "blog/prom-limo-rental-dallas-tx/index.html":
        ("/blog/dfw-quinceaneara-limo.html", "/blog/dfw-quinceaneara-limo"),
}


def _redirects():
    config = tomllib.loads((ROOT / "netlify.toml").read_text(encoding="utf-8"))
    return {
        rule["from"]: rule
        for rule in config.get("redirects", [])
        if "from" in rule
    }


def _target_file(url_path):
    relative = url_path.lstrip("/")
    if relative.endswith("/"):
        return ROOT / relative / "index.html"
    candidate = ROOT / relative
    if candidate.is_file():
        return candidate
    return ROOT / (relative + ".html")


class RedirectIndexRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.redirects = _redirects()
        cls.sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    def test_updated_redirects_have_indexable_canonical_200_targets(self):
        for source, destination in UPDATED.items():
            with self.subTest(source=source):
                rule = self.redirects.get(source)
                self.assertIsNotNone(rule, f"missing redirect for {source}")
                self.assertEqual(rule.get("status"), 301)
                self.assertEqual(rule.get("to"), destination)
                self.assertNotEqual(destination, "/blog/")

                target = _target_file(destination)
                self.assertTrue(target.is_file(), f"destination has no file: {target}")
                html = target.read_text(encoding="utf-8")
                self.assertNotRegex(html, r'(?i)<meta[^>]+name=["\']robots["\'][^>]+noindex')
                canonical = re.search(
                    r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)',
                    html,
                    re.I,
                )
                self.assertIsNotNone(canonical, f"missing canonical in {target}")
                self.assertEqual(canonical.group(1), BASE + destination)

    def test_legacy_sources_are_not_in_sitemap(self):
        for source in set(UPDATED) | RETAINED_GENERIC:
            with self.subTest(source=source):
                self.assertNotIn(BASE + source, self.sitemap)
                self.assertNotIn(BASE + source + "/", self.sitemap)

    def test_unmatched_audit_articles_remain_explicitly_generic(self):
        for source in RETAINED_GENERIC:
            with self.subTest(source=source):
                self.assertEqual(self.redirects[source].get("status"), 301)
                self.assertEqual(self.redirects[source].get("to"), "/blog/")

    def test_listed_internal_links_use_clean_targets(self):
        for filename, (legacy, clean) in LINK_FIXES.items():
            with self.subTest(filename=filename):
                html = (ROOT / filename).read_text(encoding="utf-8")
                self.assertNotIn(f'href="{legacy}"', html)
                self.assertIn(f'href="{clean}"', html)


if __name__ == "__main__":
    sys.exit(unittest.main())