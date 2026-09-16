---
name: Google autocomplete constraints
description: Browser-key scope, modern Places API, and lazy Maps loader requirements
---
Use Places API (New) with a website-restricted browser key, separate from any server-side routing credential. Keep Maps loading deferred until address-field focus and use a single loader shared by all fields.

**Why:** The user requested Google address suggestions only, not changes to mileage or fare calculation. Browser keys are necessarily visible to visitors; website/API restrictions provide protection. Duplicate Maps library loading caused runtime conflicts during integration testing.

**How to apply:** Preserve existing pricing and manual entry if Google denies requests. A successful Maps JavaScript bootstrap does not establish Places authorization: verify the actual autocomplete RPC and a selected address with coordinates. Never log keyed URLs or credential values while diagnosing authorization.