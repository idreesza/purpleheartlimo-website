---
name: Live deploy host reality
description: Where purpleheartlimo.com actually serves from, and which redirect config is authoritative.
---

**As of July 2026, purpleheartlimo.com serves from the Replit STATIC deployment**
(`purpleheartlimo-website.replit.app`, custom domain attached, `via: 1.1 google`
response header). It is NOT on Netlify and NOT on Hostinger anymore — verify with
`getDeploymentInfo()` and live response headers before trusting any host assumption.

**Why it matters:**
- `netlify.toml` and `.htaccess` are IGNORED by the live host. They are kept in the
  repo (and `.htaccess` regenerated via `scripts/gen_htaccess.py`) only as portable
  configs in case of a future host move.
- Replit static deployments support ONLY `[[deployment.rewrites]]` in `.replit`
  (200 rewrites, no 301s). Legacy-URL fixes (e.g. /about-us, dead blog slugs) live
  there; SEO consolidation relies on canonical tags on the target pages.
- Netlify Functions (`netlify/functions/*`) do NOT run in production — anything
  needing a backend (e.g. /api/distance) has no live endpoint on a static deploy.

**How to apply:** any redirect/header change must be added to `.replit`
`[[deployment.rewrites]]` (and optionally mirrored into netlify.toml → gen_htaccess
for portability). Changes go live only after the user republishes the deployment.

## Update (2026-08-17)
Deployment config switched to **Autoscale** running `python3 server.py` (takes effect on next republish).
- server.py now handles: www→apex 301 (Host header check, before all routing), legacy-slug 301/410s parsed from netlify.toml at startup, custom 404.html, env-aware cache headers (`REPLIT_DEPLOYMENT` ⇒ prod caching; dev stays no-store).
- **Why:** static deploys can't 301 and never run server.py; user needed a server-level www redirect (DNS redirects can't do HTTPS).
- **How to apply:** add/change redirects in netlify.toml (single source of truth) and restart/republish — do NOT add `.replit [[deployment.rewrites]]` anymore. Stale `/es → /es/limo-service-dallas-tx/` rules were removed when the real /es/ homepage shipped.

## Update (2026-09-06)
Treat Autoscale `server.py` as the active response layer for compression and HTTP headers.

**Why:** live headers showed that HTML/CSS/JS were uncompressed; manually declaring
`Content-Encoding: gzip` in `netlify.toml` would be ignored by Replit and would corrupt
uncompressed responses on any host that did apply it.

**How to apply:** implement and verify content negotiation in the Python server, including
`Vary: Accept-Encoding` for resolved directory indexes and explicit encoding opt-outs.
