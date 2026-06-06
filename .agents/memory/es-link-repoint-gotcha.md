---
name: es/ link repoint gotcha
description: Blanket-replacing English link paths inside /es/ pages silently breaks the language toggle.
---

When adding inbound links / localizing Spanish pages, do NOT blanket-replace
`href="/fleet.html"` → `href="/es/fleet.html"` (or booking) across an `es/` file.

**Why:** Each `es/` page has three links that must stay pointing at the English
page: the nav-links `🌐 English` link, the `id="lang-toggle"` `🌐 EN` button, and
the mobile-menu `🌐 English` link. A blind replace repoints those to the Spanish
URL, so the language switcher just reloads the same Spanish page. Caught by code
review after the first pass.

**How to apply:** When repointing content/CTA links to `/es/...`, exclude any
anchor whose text is `🌐 English` / `🌐 EN` or whose `id="lang-toggle"`. Leave the
`rel="alternate"` hreflang `<link>`s (full https URLs) untouched too — they
already encode the correct EN/ES/x-default targets.
