#!/usr/bin/env python3
"""Sync SEO-only price markup from the canonical rate table in js/pricing.js.

Search engines read the raw HTML, not JS-rendered values, so prices baked into
JSON-LD / meta tags / no-JS fallback spans can drift after a rate change in
js/pricing.js. Run this script after ANY rate edit in js/pricing.js:

    python3 scripts/sync_seo_prices.py          # rewrite files
    python3 scripts/sync_seo_prices.py --check  # exit 1 if anything is stale

It regenerates:
  1. es/fleet.html   — Vehicle JSON-LD "offers" prices (live classes only)
  2. rates.html      — FAQPage JSON-LD answer text ($ sedan flat / SUV flat)
  3. fleet.html      — meta description ("Flat rates from $X")
  4. all three pages — static fallback text inside data-phl-from/flat/hourly
                       spans (the no-JS / crawler-visible values)

Price semantics (mirrors js/price-sync.js):
  from   = min(flat, hourly)
  flat   = flat rate
  hourly = hourly rate
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRICING_JS = ROOT / "js" / "pricing.js"

# JSON-LD Vehicle name → pricing.js class id (live-priced classes only;
# stretch/sprinter/party-bus offers are quoted rates, not in pricing.js).
ES_FLEET_JSONLD_CLASSES = {
    "Executive Sedan — Cadillac CTS": "business-sedan",
    "Luxury Sedan — Mercedes-Benz S-Class": "luxury-sedan",
    "Executive SUV — GMC Yukon Denali": "business-suv",
    "Luxury SUV — Cadillac Escalade": "luxury-suv",
}


def parse_classes():
    """Extract {id: {flat, hourly}} from window.PHL_CLASSES in js/pricing.js."""
    src = PRICING_JS.read_text(encoding="utf-8")
    m = re.search(r"window\.PHL_CLASSES\s*=\s*\[(.*?)\];", src, re.S)
    if not m:
        sys.exit("ERROR: could not find window.PHL_CLASSES in js/pricing.js")
    classes = {}
    for entry in re.finditer(
        r"id:\s*'([^']+)'.*?flat:\s*(\d+)\s*,\s*hourly:\s*(\d+)", m.group(1), re.S
    ):
        cid, flat, hourly = entry.group(1), int(entry.group(2)), int(entry.group(3))
        classes[cid] = {"flat": flat, "hourly": hourly, "from": min(flat, int(hourly))}
    if not classes:
        sys.exit("ERROR: no classes parsed from js/pricing.js")
    return classes


def sub_checked(pattern, repl, text, label, count=1, flags=0):
    new, n = re.subn(pattern, repl, text, count=count, flags=flags)
    if n == 0:
        sys.exit(f"ERROR: pattern not found for {label}: {pattern}")
    return new


def sync_fallback_spans(html, classes):
    """Update static text inside <span data-phl-from|flat|hourly="id">NNN</span>."""
    for attr, key in (("data-phl-from", "from"), ("data-phl-flat", "flat"),
                      ("data-phl-hourly", "hourly")):
        def repl(m, key=key):
            cid = m.group(2)
            if cid not in classes:
                return m.group(0)
            return f"{m.group(1)}{classes[cid][key]}{m.group(3)}"
        html = re.sub(rf'(<span {attr}="([^"]+)"[^>]*>)\d+(</span>)', repl, html)
    return html


def sync_es_fleet(html, classes):
    """Rewrite Vehicle JSON-LD offer prices in es/fleet.html."""
    m = re.search(
        r'(<script type="application/ld\+json">)(\{"@context":"https://schema\.org","@type":"ItemList".*?\})(</script>)',
        html, re.S)
    if not m:
        sys.exit("ERROR: ItemList JSON-LD not found in es/fleet.html")
    data = json.loads(m.group(2))
    for li in data.get("itemListElement", []):
        item = li.get("item", {})
        cid = ES_FLEET_JSONLD_CLASSES.get(item.get("name", ""))
        if cid and cid in classes and "offers" in item:
            item["offers"]["price"] = str(classes[cid]["from"])
    new_json = json.dumps(data, ensure_ascii=True, separators=(",", ":"))
    return html[: m.start()] + m.group(1) + new_json + m.group(3) + html[m.end():]


def sync_rates(html, classes):
    """Rewrite FAQPage JSON-LD answer prices in rates.html."""
    sedan_flat = classes["business-sedan"]["flat"]
    suv_flat = classes["luxury-suv"]["flat"]
    html = sub_checked(
        r"(Executive sedan airport transfers start at \$)\d+( flat)",
        rf"\g<1>{sedan_flat}\g<2>", html, "rates.html sedan FAQ price")
    html = sub_checked(
        r"(Luxury SUVs start at \$)\d+",
        rf"\g<1>{suv_flat}", html, "rates.html SUV FAQ price")
    return html


def sync_fleet_meta(html, classes):
    """Rewrite 'Flat rates from $X' in fleet.html meta description."""
    lowest = min(c["from"] for c in classes.values())
    return sub_checked(
        r"(Flat rates from \$)\d+", rf"\g<1>{lowest}", html,
        "fleet.html meta description")


def main():
    check_only = "--check" in sys.argv
    classes = parse_classes()
    targets = {
        ROOT / "es" / "fleet.html": (sync_es_fleet, sync_fallback_spans),
        ROOT / "rates.html": (sync_rates, sync_fallback_spans),
        ROOT / "fleet.html": (sync_fleet_meta, sync_fallback_spans),
    }
    stale = []
    for path, funcs in targets.items():
        original = path.read_text(encoding="utf-8")
        updated = original
        for fn in funcs:
            updated = fn(updated, classes)
        if updated != original:
            stale.append(path)
            if not check_only:
                path.write_text(updated, encoding="utf-8")
                print(f"updated  {path.relative_to(ROOT)}")
        else:
            print(f"in sync  {path.relative_to(ROOT)}")
    if check_only and stale:
        print("STALE — run: python3 scripts/sync_seo_prices.py")
        sys.exit(1)


if __name__ == "__main__":
    main()
