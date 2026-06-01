---
name: Booking form → contact function field contract
description: The Netlify contact function and the on-page booking forms use different field names; forms must map before POST or bookings silently fail.
---

# Booking form field-mapping contract

City/landing booking forms use input names: `first_name`, `last_name`,
`pickup_address`, `dropoff_address`, `pickup_date`, `pickup_time`, `notes`
(plus `email`, `phone`, `service`, `vehicle`, `passengers`, `city`).

`netlify/functions/contact.js` expects: `name` (REQUIRED), `pickup`, `dropoff`,
`date`, `time`, `message` (plus email/phone/service/vehicle/passengers).

**Why:** If a form POSTs the raw `Object.fromEntries(new FormData(form))` it omits
`name` entirely → function returns 400 → booking silently fails with no user error.
This bug existed in all 6 city hubs (EN+ES) and was easy to miss because the form
"submits" without throwing.

**How to apply:** Any new or edited booking form must build a mapped `data` object
(join first+last → `name`, `pickup_address`→`pickup`, `notes`→`message`, etc.)
BEFORE `JSON.stringify`. The landing-page generator (`scripts/gen_landing.py`)
already does this correctly; mirror it.
