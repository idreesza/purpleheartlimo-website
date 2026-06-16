---
name: global.css !important overrides
description: How to win style overrides against css/global.css on the home page (load order + specificity).
---

`index.html` links `css/global.css` AFTER its inline `<style>` block, and global.css
is minified and littered with `!important` (e.g. `.nav-links>li>a{background:#fff!important;...}`,
`.nav-phone` gold).

**Rule:** An inline rule cannot beat a later-loaded `!important` rule of equal specificity.
To restyle anything global.css owns, the inline rule must use HIGHER specificity AND `!important`.
Example that works for nav pills: `.navbar .nav-links > li > a { ... !important }` beats
global's `.nav-links > li > a { ... !important }`.

**Why:** load order + `!important` mean equal-specificity inline loses; only greater
specificity (or also !important at higher specificity) wins.

**How to apply:** when a home-page restyle "doesn't take", check global.css for an
`!important` rule on the same selector; bump the inline selector's specificity (prefix
with `.navbar`, `#home-page`, etc.) and add `!important`, rather than editing the shared
minified global.css.
