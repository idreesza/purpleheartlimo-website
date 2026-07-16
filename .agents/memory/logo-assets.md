---
name: Logo assets & typo-fix recipe
description: Which logo file plays which role, and how the banner typo was fixed
---
Roles: `images/logo-banner.webp` = header banner (1416x320, "PURPLE HEART LIMO" ribbon, transparent), `/logo.webp` = footer square, `images/logo-badge.webp` = splash intro only. `images/logo-heart-limo.webp` is retired (no HTML refs).

**Why:** AI image regeneration is unreliable for text (it produced the "PURPE" typo). Fixing typos in generated lettering works better as pixel surgery: transplant a matching glyph from elsewhere in the same image, feather-paste (~6px alpha ramp) over a background strip sampled near the word, then border flood-fill bg removal + 1px alpha blur.

**How to apply:** If a logo needs text changes, edit pixels rather than regenerate; keep glyph crops wide enough to include serif feet or the feather ramp eats them.
