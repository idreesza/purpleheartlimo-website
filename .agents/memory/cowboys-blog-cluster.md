---
name: Cowboys 2026 blog cluster
description: Rules for the Cowboys/AT&T Stadium 2026 blog cluster and Spanish blog post handling
---
- The blog renderer hardcodes `<html lang="en">`; the Spanish post `blog/transporte-juegos-dallas-cowboys-arlington/` must be re-patched to `lang="es"` **after every run of scripts/build_blog.py** (build overwrites it). No hreflang added on purpose — there is no English twin (see hreflang reciprocity rule).
- **Why:** template has no lang support; adding fake hreflang alternates would violate reciprocity.
- "60-minute free wait" is an **airport-pickup-only** claim (per scripts/data/SPEC.md). Never apply it to stadium/post-game/concert exits — use "chauffeur staged before the final whistle" / "flat rate covers overtime and slow exits" phrasing instead. A code review caught this over-claim once already.
- Verified 2026 AT&T Stadium dates used across the cluster came from attstadium.com (July 2026): home opener vs Commanders Sept 20, Thanksgiving vs Eagles Nov 26, R&B Tour Sept 10/12/13, Karol G Oct 15, Ed Sheeran Oct 24.
