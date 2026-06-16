---
name: csel bar dropdowns detach to body
description: why bar time/AMPM dropdown lists must be styled via .csel-list[data-owner], not an ancestor selector
---

The custom select (`csel`) lists inside the home hero booking bar (`.bk-bar`) are
**moved to `document.body`** when opened (`cselToggle` does `appendChild(list)` and
sets a `data-owner` attribute) so they escape the bar's `backdrop-filter`
containing block.

**Consequence:** any selector that relies on a `.bk-bar` / `#home-page` ancestor
(e.g. `#home-page .bk-bar .csel-list`) will **not** match the open list — it has
been re-parented to `<body>`. Such rules silently do nothing; the list falls back
to the global light `.csel-list` style.

**How to apply:** style open bar dropdowns via `.csel-list[data-owner]` (and
`.csel-list[data-owner] .csel-opt`). `data-owner` is set ONLY on the detached
`.bk-bar` lists, so this is effectively scoped to the home booking bar without
needing an ancestor. The closed/in-place lists (e.g. Ride Type / Passengers in
`.bk-details`, which are NOT detached) are still styled normally via
`#home-page .bk-details .csel-list`.

**Why:** booking-form theming changes kept "not applying" to the time dropdowns
because the ancestor-scoped rules couldn't reach the body-level node.
