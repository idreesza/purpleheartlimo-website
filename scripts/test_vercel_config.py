#!/usr/bin/env python3
"""vercel.json must be current, redirect in one hop, and rewrite to real files;
the Vercel function must restore the original request path."""
from pathlib import Path
import importlib.util
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import gen_vercel  # noqa: E402

spec = importlib.util.spec_from_file_location("vercel_fn", ROOT / "api" / "index.py")
vercel_fn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vercel_fn)


class VercelConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = gen_vercel.build_config()

    def test_committed_config_is_current(self):
        committed = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
        self.assertEqual(committed, json.loads(json.dumps(self.config)))

    def test_redirects_are_single_hop_301s(self):
        sources = {r["source"] for r in self.config["redirects"]}
        for rule in self.config["redirects"]:
            self.assertEqual(rule["statusCode"], 301)
            self.assertNotIn(rule["destination"], sources, rule)

    def test_static_rewrites_point_at_existing_files(self):
        for rule in self.config["rewrites"]:
            dest = rule["destination"]
            if dest.startswith("/api/index"):
                continue
            self.assertTrue((ROOT / dest.lstrip("/")).is_file(), rule)

    def test_sitemap_urls_are_not_redirected(self):
        xml = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        sources = {r["source"] for r in self.config["redirects"]}
        for url in xml.split("<loc>")[1:]:
            path = url.split("</loc>")[0].replace("https://purpleheartlimo.com", "")
            self.assertNotIn(path, sources)

    def test_dynamic_endpoints_reach_the_function(self):
        rewritten = {r["source"] for r in self.config["rewrites"]
                     if r["destination"].startswith("/api/index")}
        for path in gen_vercel.DYNAMIC:
            self.assertIn(path, rewritten)

    def test_function_restores_original_path(self):
        restore = vercel_fn.restore_original_path
        self.assertEqual(restore("/api/index?__path=/api/distance&origin=a%20b"),
                         "/api/distance?origin=a+b")
        self.assertEqual(restore("/api/index?__path=/config.js"), "/config.js")
        self.assertEqual(restore("/api/index"), "/api/index")
        self.assertEqual(restore("/api/index?__path=http://evil"), "/api/index?__path=http://evil")


if __name__ == "__main__":
    unittest.main()
