---
name: Live deploy host reality
description: Where purpleheartlimo.com actually serves from vs. what the repo implies.
---

The repo contains `netlify.toml` and a GitHub Action (`.github/workflows/deploy.yml`)
that deploy to Netlify, but the **live custom domain has been served from a Replit
static deployment** (deploymentTarget="static", publicDir="."). The Netlify config
is dormant until DNS is repointed.

**Why it matters:** Host-level Semrush issues (gzip/brotli compression, cache
headers, www→apex redirect, SSL on www) are controlled by whoever actually serves
the domain. They can't be fixed by editing `netlify.toml` while Replit static is
live — Replit static serves uncompressed and ignores netlify.toml. The chosen
remedy was to switch the live domain to Netlify (user repoints DNS); the repo's
netlify.toml/functions were prepared for that cutover.

**How to apply:** Before "fixing" compression/caching/redirect audit findings,
confirm which platform is actually answering for the domain (getDeploymentInfo +
response headers like `via: 1.1 google`). Edit the config of the *live* host, or
plan a host switch — don't assume netlify.toml is in effect.
