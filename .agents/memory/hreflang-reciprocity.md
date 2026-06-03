---
name: hreflang reciprocity (purpleheartlimo.com)
description: Why the homepage intentionally has no Spanish (es) hreflang alternate
---

The homepage (`index.html`) intentionally carries only `hreflang="en"` and `hreflang="x-default"`, both pointing to `https://purpleheartlimo.com/`. It must NOT declare an `es` alternate.

**Why:** There is no Spanish homepage (`es/index.html` does not exist). The `/es/<page>/` directories are Spanish twins of specific English city pages (e.g. `/es/limo-service-austin-tx/` ↔ `/limo-service-austin-tx/`), and those clusters reciprocate correctly. A previous homepage `es` link to `/es/limo-service-austin-tx/` was non-reciprocal (that page points its en/x-default back to `/limo-service-austin-tx/`, not `/`), which Semrush flagged as "incorrect hreflang links".

**How to apply:** Only add an `es` hreflang to the homepage if a real `/es/` homepage is created — and then add reciprocal en/es/x-default tags on BOTH homepage variants in the same release. Each en page's `es` alternate must point to a Spanish page whose `en`/`x-default` points back to that same en page.
