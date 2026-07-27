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
