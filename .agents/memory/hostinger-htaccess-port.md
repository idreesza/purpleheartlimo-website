---
name: Hostinger .htaccess port
description: How the Apache .htaccess for Hostinger is produced from netlify.toml and the gotchas that matter.
---

# Hostinger / Apache `.htaccess`

Hostinger shared hosting runs **Apache and ignores `netlify.toml`**. The site's
redirects/clean-URLs only work there via a root `.htaccess`.

**`.htaccess` is generated, not hand-edited.** `netlify.toml` is the single
source of truth; `scripts/gen_htaccess.py` parses every `[[redirects]]` +
`[[headers]]` block and emits the Apache equivalent. Edit the toml and re-run
`python3 scripts/gen_htaccess.py`.

## Translation rules that matter
- Netlify default (non-force) redirects are "shadowed" by existing files; force=true
  wins over a file. Most non-force `from` paths here are pretty URLs with no real
  file, so unconditional Apache rules are equivalent — except param/catch rules,
  which get `!-f`/`!-d` guards.
- `status=200` → internal rewrite `[L]` (NOT a redirect). `status=410` → `[G,L]`.
  `/*`→404 catch-all → `ErrorDocument 404`, not a rewrite.
- **`:param` rules (e.g. `/blog/:slug`→`/blog/:slug/`) must become capture groups**
  (`^blog/([^/]+)$ /blog/$1/`) — a literal `:slug` is a dead rule. Anchor with `$`
  (no optional trailing slash) + `!-f`/`!-d` guards, or the slashed target re-matches
  and loops.
- Pretty URLs: redirect `*.html`/`index.html`→clean via `THE_REQUEST`, then serve
  extensionless via internal rewrite to `.html` (loop-safe because the redirect only
  fires on the original browser request).
- Host canonical (HTTPS + strip www) is one block at the top; skip the three
  per-scheme host `[[redirects]]` (covered by it).

## Not portable
- Netlify Functions (`/api/distance` → `/.netlify/functions/distance`) do **not**
  exist on Hostinger. The distance lookup needs a separate backend (PHP endpoint or
  direct third-party API). The generator emits a NOTE comment and skips it.
