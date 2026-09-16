---
name: Booking delivery verification
description: Verify real email submission on the Python host, not just a UI success state
---
Verify quote delivery against the active Python runtime, not just Netlify function source or a mocked browser response.

**Why:** The previous booking confirmation displayed success without sending a request, and the Python host did not implement the legacy contact function URL. A passing visual flow therefore did not demonstrate delivery.

**How to apply:** Require provider acceptance before showing success, preserve details on errors, and test the server route with a mocked delivery transport to avoid sending test leads. Missing delivery configuration must be reported explicitly.