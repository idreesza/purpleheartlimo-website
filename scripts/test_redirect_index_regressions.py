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
from email.message import Message
from html.parser import HTMLParser
from unittest.mock import patch


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from server import Handler, REDIRECTS_EXACT, _redirect_destination
from scripts.gen_htaccess import build_htaccess, parse_blocks

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

# Owner-approved retirement after original-content and equivalence audit.
RETIRED_ARTICLES = {
    "/blog/a-comprehensive-guide-to-transportation-services-in-austin--texas",
    "/blog/exploring-advanced-limousine-booking-systems--a-look-at-purple-heart-limo-s-technology",
    "/blog/how-purple-heart-limousine-uses-ai-for-seamless-booking-experiences",
    "/blog/the-future-of-transportation-booking-systems--how-innovations-are-changing-the-game",
    "/blog/case-study--success-stories-from-austin-s-prom-season-limo-bookings",
    "/blog/why-austin-locals-love-purple-heart-limousine-services",
    "/blog/why-purple-heart-limousine-stands-out-among-austin-s-limo-services",
}

RESTORED_ARTICLES = {
    "/blog/prom-night-perfection--tips-for-booking-a-limo-in-austin",
    "/blog/prom-season-limo-booking-tips-for-austin-teens-and-parents",
}

LINK_FIXES = {
    "blog/arlington-entertainment-district-cowboys-games/index.html":
        ("/blog/arlington-entertainment.html", "/blog/arlington-entertainment"),
    "blog/prom-limo-rental-dallas-tx/index.html":
        ("/blog/dfw-quinceaneara-limo.html", "/blog/dfw-quinceaneara-limo"),
}

DISCOVERY_LINKS = {
    "blog/the-ultimate-guide-to-booking-a-limo-service-in-austin/index.html": (
        "/blog/frequently-asked-questions-about-hiring-a-limo-service-in-austin/",
        "/blog/how-dynamic-map-integration-enhances-your-limo-experience/",
    ),
    "blog/frequently-asked-questions-about-hiring-a-limo-service-in-austin/index.html": (
        "/blog/the-ultimate-guide-to-booking-a-limo-service-in-austin/",
    ),
    "blog/things-to-do-in-austin-texas-weekend-guide/index.html": (
        "/blog/top-5-destinations-to-visit-with-a-limo-in-austin/",
        "/blog/how-to-plan-the-perfect-night-out-with-a-limo-in-austin/",
    ),
    "blog/seasonal-events-in-austin--why-a-limo-service-is-your-best-choice/index.html": (
        "/blog/sxsw-limo-service-austin-transportation-guide/",
    ),
    "blog/airport-transfers-made-easy-stress-free-travel-with-limo-services/index.html": (
        "/blog/navigating-austin-s-traffic--why-a-limo-service-is-your-best-choice/",
    ),
    "blog/index.html": (
        "/blog/how-dynamic-maps-enhance-limousine-services-in-austin/",
        "/blog/how-dynamic-map-integration-enhances-your-limo-experience/",
    ),
}


class _BodyLinks(HTMLParser):
    """Static discovery edges, excluding global chrome and script strings."""
    def __init__(self):
        super().__init__()
        self.stack = []
        self.hrefs = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        marker = attrs.get("class", "") + " " + attrs.get("id", "")
        excluded = tag in ("head", "header", "nav", "footer", "script", "style", "template")
        excluded = excluded or bool(re.search(r"\b(?:navbar|footer|header|mobile-nav)\b", marker))
        blocked = excluded or (self.stack[-1][1] if self.stack else False)
        if tag == "a" and not blocked and attrs.get("href"):
            self.hrefs.add(attrs["href"])
        if tag not in ("area", "base", "br", "col", "embed", "hr", "img", "input",
                       "link", "meta", "param", "source", "track", "wbr"):
            self.stack.append((tag, blocked))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                self.stack = self.stack[:index]
                break


def _canonical(html):
    match = re.search(
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', html, re.I
    )
    return match.group(1) if match else None


def _redirects():
    config = tomllib.loads((ROOT / "netlify.toml").read_text(encoding="utf-8"))
    return {
        rule["from"]: rule
        for rule in config.get("redirects", [])
        if "from" in rule
    }


def _target_file(url_path):
    if url_path == "/":
        return ROOT / "index.html"
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
        for source in set(UPDATED) | RETIRED_ARTICLES:
            with self.subTest(source=source):
                self.assertNotIn(BASE + source, self.sitemap)
                self.assertNotIn(BASE + source + "/", self.sitemap)

    def test_unmatched_audit_articles_are_gone(self):
        apache = (ROOT / ".htaccess").read_text()
        for source in RETIRED_ARTICLES:
            with self.subTest(source=source):
                self.assertEqual(self.redirects[source].get("status"), 410)
                self.assertEqual(self.redirects[source].get("to"), "/404.html")
                self.assertIn(f"RewriteRule ^{re.escape(source.lstrip('/'))}/?$ - [G,L]", apache)
                for suffix in ("", "/", "?utm_source=test", "/?utm_source=test"):
                    self.assertEqual(_redirect_destination(source + suffix), ("/404.html", 410))

    def test_restored_articles_have_canonical_discoverable_targets(self):
        index = (ROOT / "blog/index.html").read_text()
        apache = (ROOT / ".htaccess").read_text()
        for source in RESTORED_ARTICLES:
            with self.subTest(source=source):
                target = source + "/"
                self.assertEqual(_redirect_destination(source), (target, 301))
                self.assertIsNone(_redirect_destination(target))
                self.assertFalse(self.redirects[source].get("force", False))
                html = _target_file(target).read_text()
                self.assertEqual(_canonical(html), BASE + target)
                self.assertNotRegex(html, r'(?i)<meta[^>]+name=["\']robots["\'][^>]+noindex')
                self.assertIn(BASE + target + "</loc>", self.sitemap)
                self.assertIn(f'href="{target}"', index)
                self.assertIn(f"RewriteRule ^{re.escape(source.lstrip('/'))}$ {target} [R=301,L]", apache)

    def test_retired_articles_get_and_head_never_redirect_even_on_www(self):
        from io import BytesIO
        for source in RETIRED_ARTICLES:
            for suffix in ("", "/", "?utm_source=test", "/?utm_source=test"):
                for method in ("GET", "HEAD"):
                    for host in ("purpleheartlimo.com", "www.purpleheartlimo.com"):
                        handler = object.__new__(Handler)
                        handler.path = source + suffix
                        handler.command = method
                        handler.headers = Message()
                        handler.headers["Host"] = host
                        handler.wfile = BytesIO()
                        with self.subTest(path=handler.path, method=method, host=host), \
                             patch.object(handler, "send_response") as status, \
                             patch.object(handler, "send_header") as header, \
                             patch("http.server.SimpleHTTPRequestHandler.end_headers"):
                            self.assertFalse(handler._www_redirect())
                            self.assertTrue(handler._legacy_redirect())
                            status.assert_called_once_with(410)
                            self.assertNotIn("Location", [c.args[0] for c in header.call_args_list])
                            if method == "HEAD":
                                self.assertEqual(handler.wfile.getvalue(), b"")

    def test_listed_internal_links_use_clean_targets(self):
        for filename, (legacy, clean) in LINK_FIXES.items():
            with self.subTest(filename=filename):
                html = (ROOT / filename).read_text(encoding="utf-8")
                self.assertNotIn(f'href="{legacy}"', html)
                self.assertIn(f'href="{clean}"', html)


class CurrentGscRoutingRegressions(unittest.TestCase):
    def test_root_aliases_redirect_to_existing_canonical_pages(self):
        for source, destination in {
            "/index.html": "/",
            "/about": "/about.html",
            "/cancellation-policy": "/cancellation-policy.html",
        }.items():
            with self.subTest(source=source):
                self.assertEqual(_redirect_destination(source), (destination, 301))
                self.assertIsNone(_redirect_destination(destination))
                html = _target_file(destination).read_text(encoding="utf-8")
                self.assertIn(f'href="{BASE + destination}"', html)

    def test_flat_blog_aliases_keep_extensionless_canonicals(self):
        for slug in ("july-4th-dfw", "best-restaurants-dfw", "plano-frisco-guide"):
            with self.subTest(slug=slug):
                self.assertEqual(
                    _redirect_destination(f"/blog/{slug}.html"),
                    (f"/blog/{slug}", 301),
                )
                self.assertIsNone(_redirect_destination(f"/blog/{slug}"))

    def test_live_folder_targets_do_not_loop(self):
        for slug in (
            "world-cup-2026-dallas-limo-service-guide",
            "how-dynamic-maps-enhance-limousine-services-in-austin",
            "best-day-trips-from-dallas-by-limo",
            "top-5-reasons-to-hire-a-limo-for-your-austin-event",
            "top-5-destinations-to-visit-with-a-limo-in-austin",
            "things-to-do-in-austin-texas-weekend-guide",
        ):
            path = "/blog/" + slug
            with self.subTest(slug=slug):
                self.assertEqual(_redirect_destination(path), (path + "/", 301))
                self.assertIsNone(_redirect_destination(path + "/"))

    def test_deliberate_consolidations_keep_existing_winners(self):
        for source, destination in {
            "/blog/best-wedding-venues-in-dallas-dfw-limo-service":
                "/blog/dfw-wedding-venues.html",
            "/blog/limo-service-dfw-airport-complete-guide":
                "/blog/dfw-airport-limo-guide.html",
            "/blog/comparing-austin-s-top-limo-services--what-sets-purple-heart-apart-":
                "/blog/comparing-purple-heart-limo-with-other-austin-limo-services/",
        }.items():
            with self.subTest(source=source):
                self.assertEqual(_redirect_destination(source), (destination, 301))
                self.assertEqual(_redirect_destination(source + "/"), (destination, 301))
                self.assertIsNone(_redirect_destination(destination))

    def test_retired_pagination_is_removed_from_both_blog_url_forms(self):
        for path in ("/blog", "/blog/"):
            for query in ("q=&p=1", "q=&p=4", "q=&p=5", "p=1", "q="):
                with self.subTest(path=path, query=query):
                    self.assertEqual(
                        _redirect_destination(path + "?" + query), ("/blog/", 301)
                    )
        self.assertEqual(
            _redirect_destination("/blog/?q=&p=1&utm_source=test"),
            ("/blog/?utm_source=test", 301),
        )
        self.assertIsNone(_redirect_destination("/blog/?utm_source=test"))

    def test_www_alias_combines_host_and_path_in_one_hop_for_get_and_head(self):
        for command in ("GET", "HEAD"):
            for source, destination in (
                ("/about?utm_source=test", "/about.html?utm_source=test"),
                ("/blog?q=&p=4", "/blog/"),
                ("/blog/how-to-plan-the-perfect-night-out-with-a-limo-in-austin",
                 "/blog/how-to-plan-the-perfect-night-out-with-a-limo-in-austin/"),
            ):
                handler = object.__new__(Handler)
                handler.path = source
                handler.command = command
                handler.headers = Message()
                handler.headers["Host"] = "www.purpleheartlimo.com"
                with self.subTest(command=command, source=source), \
                     patch.object(handler, "send_response") as status, \
                     patch.object(handler, "send_header") as header, \
                     patch("server.SimpleHTTPRequestHandler.end_headers"):
                    self.assertTrue(handler._www_redirect())
                    status.assert_called_once_with(301)
                    header.assert_any_call("Location", BASE + destination)

    def test_live_rates_service_areas_and_unknown_blog_are_not_redirected(self):
        for path in (
            "/rates.html", "/service-areas.html", "/blog/not-a-real-gsc-post",
            "/blog/not-a-real-gsc-post/", "/blog/", "/es/",
        ):
            with self.subTest(path=path):
                self.assertIsNone(_redirect_destination(path))

    def test_gone_and_unrelated_query_strings_are_preserved(self):
        self.assertEqual(_redirect_destination("/html/head/title"), ("/404.html", 410))
        self.assertEqual(
            _redirect_destination("/about?x=a%2Fb"), ("/about.html?x=a%2Fb", 301)
        )

    def test_every_configured_path_redirect_resolves_without_a_chain(self):
        for source in REDIRECTS_EXACT:
            with self.subTest(source=source):
                hit = _redirect_destination(source)
                self.assertIsNotNone(hit)
                if hit[1] == 301:
                    self.assertIsNone(_redirect_destination(hit[0]))

    def test_future_redirect_cycle_is_not_exposed_to_browsers(self):
        with patch.dict(REDIRECTS_EXACT, {
            "/cycle-a": ("/cycle-b", 301), "/cycle-b": ("/cycle-a", 301)
        }):
            self.assertIsNone(_redirect_destination("/cycle-a"))

    def test_apache_does_not_strip_html_from_live_root_pages(self):
        apache = (ROOT / ".htaccess").read_text(encoding="utf-8")
        self.assertIn(r"RewriteRule ^about/?$ /about.html [R=301,L]", apache)
        self.assertNotIn(r"\s/+([^.\s?]+)\.html[\s?]", apache)
        self.assertIn(r"RewriteRule ^es$ /es/ [R=301,L]", apache)
        self.assertIn(r"RewriteRule ^blog$ /blog/ [R=301,L]", apache)

    def test_apache_generation_is_reproducible(self):
        redirects, headers = parse_blocks(
            (ROOT / "netlify.toml").read_text(encoding="utf-8")
        )
        generated, _ = build_htaccess(redirects, headers)
        self.assertEqual(
            generated, (ROOT / ".htaccess").read_text(encoding="utf-8")
        )

    def test_apache_slash_rules_do_not_match_their_own_targets(self):
        redirects, headers = parse_blocks(
            (ROOT / "netlify.toml").read_text(encoding="utf-8")
        )
        generated, _ = build_htaccess(redirects, headers)
        for rule in redirects:
            source, target = rule.get("from", ""), rule.get("to", "")
            if rule.get("status") != 301 or target != source.rstrip("/") + "/":
                continue
            norm = source.rstrip("/").lstrip("/")
            matching_rules = [
                line.split()[1]
                for line in generated.splitlines()
                if line.startswith("RewriteRule ")
                and f" {target} [R=301,L]" in line
            ]
            with self.subTest(source=source):
                self.assertTrue(any(re.fullmatch(p, norm) for p in matching_rules))
                self.assertFalse(any(re.fullmatch(p, norm + "/") for p in matching_rules))


class ContextualDiscoveryRegressions(unittest.TestCase):
    def assert_public_indexable_canonical(self, filename):
        html = filename.read_text(encoding="utf-8")
        canonical = _canonical(html)
        self.assertIsNotNone(canonical)
        self.assertTrue(canonical.startswith(BASE + "/"))
        path = canonical.removeprefix(BASE)
        self.assertIsNone(_redirect_destination(path))
        self.assertFalse(Handler._private_static_path(path))
        self.assertEqual(_target_file(path).resolve(), filename.resolve())
        self.assertNotRegex(html, r'(?i)<meta[^>]+name=["\']robots["\'][^>]+noindex')
        self.assertIn(canonical, (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        return html, canonical

    def test_contextual_links_are_static_and_point_to_public_canonical_articles(self):
        for source, targets in DISCOVERY_LINKS.items():
            with self.subTest(source=source):
                html, source_canonical = self.assert_public_indexable_canonical(ROOT / source)
                links = _BodyLinks()
                links.feed(html)
                for target in targets:
                    self.assertIn(target, links.hrefs)
                    _, target_canonical = self.assert_public_indexable_canonical(_target_file(target))
                    self.assertEqual(target_canonical, BASE + target)
                    self.assertNotEqual(source_canonical, target_canonical)

    def test_all_eight_weak_articles_have_multiple_distinct_body_link_sources(self):
        destinations = {target for targets in DISCOVERY_LINKS.values() for target in targets}
        inbound = {target: set() for target in destinations}
        for source in (ROOT / "blog").rglob("*.html"):
            html = source.read_text(encoding="utf-8")
            canonical = _canonical(html)
            if not canonical or not canonical.startswith(BASE + "/"):
                continue
            path = canonical.removeprefix(BASE)
            if _redirect_destination(path) or _target_file(path).resolve() != source.resolve():
                continue
            if re.search(r'(?i)<meta[^>]+name=["\']robots["\'][^>]+noindex', html):
                continue
            links = _BodyLinks()
            links.feed(html)
            for target in destinations & links.hrefs:
                if path != target:
                    inbound[target].add(canonical)
        self.assertEqual(len(destinations), 8)
        for target, sources in inbound.items():
            with self.subTest(target=target):
                self.assertGreaterEqual(len(sources), 2, f"weak discovery: {target}: {sources}")

    def test_blog_routing_resources_are_outside_generated_listing(self):
        html = (ROOT / "blog/index.html").read_text(encoding="utf-8")
        resources = re.search(
            r'<section class="related-guides" aria-labelledby="routing-resources-title".*?</section>',
            html, re.S,
        )
        self.assertIsNotNone(resources)
        for target in DISCOVERY_LINKS["blog/index.html"]:
            self.assertIn(f'href="{target}"', resources.group())
        self.assertNotIn('class="post-card"', resources.group())

    def test_existing_generator_inputs_do_not_overwrite_manual_source_articles(self):
        # These legacy Austin folder posts are maintained directly as HTML.
        # If they gain a JSON regeneration source, preserve the discovery links
        # in that source too rather than silently dropping them on rebuild.
        import json
        for data_file in (ROOT / "scripts/data").glob("*.json"):
            post = json.loads(data_file.read_text(encoding="utf-8"))
            source = post.get("path", "").lstrip("/")
            if source in DISCOVERY_LINKS:
                generated_source = json.dumps(post)
                for target in DISCOVERY_LINKS[source]:
                    self.assertIn(target, generated_source, f"missing regeneration link in {data_file}")


if __name__ == "__main__":
    sys.exit(unittest.main())