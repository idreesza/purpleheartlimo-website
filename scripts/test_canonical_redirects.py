#!/usr/bin/env python3
"""Duplicate URL forms must 301 (one hop) to the page's own canonical URL,
canonical URLs must never redirect, and internal links must use canonicals."""
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server import _canonical_redirect_target  # noqa: E402

DUPLICATES = {
    "/limo-service-dallas-tx/index.html": "/limo-service-dallas-tx/",
    "/es/index.html": "/es/",
    "/blog/index.html": "/blog/",
    "/blog/dfw-airport-limo-guide": "/blog/dfw-airport-limo-guide.html",
    "/blog/dfw-wedding-venues": "/blog/dfw-wedding-venues.html",
    "/blog/addison-restaurant-row/": "/blog/addison-restaurant-row",
    "/blog/addison-restaurant-row.html": "/blog/addison-restaurant-row",
    "/blog/how-much-to-tip-limo-driver-texas/index.html":
        "/blog/how-much-to-tip-limo-driver-texas/",
    "/es/index.html?utm_source=x": "/es/?utm_source=x",
}


def sitemap_paths():
    xml = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    return [u.replace("https://purpleheartlimo.com", "")
            for u in re.findall(r"<loc>([^<]+)</loc>", xml)]


class CanonicalRedirectTests(unittest.TestCase):
    def test_duplicates_redirect_to_canonical(self):
        for source, target in DUPLICATES.items():
            with self.subTest(source=source):
                self.assertEqual(_canonical_redirect_target(str(ROOT), source), target)

    def test_canonical_urls_never_redirect(self):
        for path in sitemap_paths():
            with self.subTest(path=path):
                self.assertIsNone(_canonical_redirect_target(str(ROOT), path))

    def test_redirect_targets_are_themselves_final(self):
        for target in DUPLICATES.values():
            path = target.split("?")[0]
            self.assertIsNone(_canonical_redirect_target(str(ROOT), path), target)

    def test_unknown_and_api_paths_untouched(self):
        for path in ("/nope-xyz", "/api/hourly-hub", "/css/global.css", "/../server.py"):
            self.assertIsNone(_canonical_redirect_target(str(ROOT), path), path)

    def test_internal_links_use_canonical_urls(self):
        bad = []
        for page in ROOT.rglob("*.html"):
            parts = page.relative_to(ROOT).parts
            if parts[0] in {"exports", "reports", "screenshots", "attached_assets",
                            "compiled-static", "node_modules"} or parts[0].startswith("."):
                continue
            for href in re.findall(r'href="(/[^"#?]*)', page.read_text(encoding="utf-8")):
                if _canonical_redirect_target(str(ROOT), href):
                    bad.append(f"{page.relative_to(ROOT).as_posix()}: {href}")
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
