---
name: Homepage loading
description: Why not to reintroduce a blocking brand splash on the homepage.
---
Do not hide the homepage behind a timed logo intro.

**Why:** The September 12, 2026 mobile PageSpeed report measured 6.2s LCP and identified the navigation logo as the LCP element; the timed intro added avoidable render delay.

**How to apply:** Keep branding visible in the header without blocking initial content. The user's later PageSpeed brief explicitly requests deferred Analytics transport: preserve the immediate dataLayer queue and load the transport after load/idle or first interaction. Do not require interaction exclusively.

Keep the default booking layout present before JavaScript and avoid late font replacement on slow connections.

**Why:** After removing the splash, Google's mobile report attributed 0.247 CLS to the hero/booking region and flagged web fonts. Revealing a previously empty booking bar compounds font-driven movement.

**How to apply:** Mode switching may redistribute fields, but the first paint should match the default mode. Keep the chosen optional-font strategy unless replacement fonts have matched fallback metrics.