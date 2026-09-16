---
name: Booking delivery verification
description: Verify real email submission on the Python host, not just a UI success state
---
Booking confirmation must use the existing EmailJS service, not SendGrid. Verify actual provider acceptance, not just a mocked browser response.

**Why:** The user corrected the provider choice after SendGrid configuration blocked submissions: EmailJS was already used by the homepage. Previously the booking confirmation displayed success without sending a request. A passing visual flow therefore does not demonstrate delivery.

**How to apply:** Require provider acceptance before showing success, preserve details on errors, and use mocked transport for tests to avoid sending test leads. The EmailJS template's recipient setting must consume the recipient parameter; client-side parameters alone do not prove that both destinations will receive mail. Do not revert booking confirmation to SendGrid while working on unrelated contact routes.