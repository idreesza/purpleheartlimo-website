---
name: Contact form + flight tracker backend wiring
description: How forms send email and how the flight tracker looks up flights — mixed EmailJS / Netlify-function setup that is easy to get wrong
---

# Contact form & flight tracker backends

Two email paths coexist on purpose:
- **EmailJS (client-side, inline public keys)**: index.html, booking.html, es/booking.html call `emailjs.send('service_53lh00r','template_xwek3ac', …)` with public key `coK69SSFSbc1x8dc6`. EmailJS public keys are meant to be public; these are restricted in the EmailJS dashboard.
- **SendGrid Netlify function** `/.netlify/functions/contact` (needs env `SENDGRID_API_KEY`, optional `NOTIFY_EMAIL`): used by the city landing pages (`limo-service-*-tx`, `es/…`) and the two contact pages (contact.html, es/contact.html). POST JSON `{name,email,phone,service,message,…}`; returns `{success:true}` on 200. Sends a rich business email + email-to-SMS to the owner + a customer auto-reply.

**Flight tracker** (flight-tracker.html): looks up flights via `/.netlify/functions/flights?flight=IATA` which proxies AviationStack using env `AVIATIONSTACK_API_KEY`. The key must stay server-side — never put it in client JS. Proxy soft-fails to `{data:[]}` so the page falls back to airline deep links; it also blocks foreign-Referer hotlinking to curb billable-quota abuse.

**Why:** A stray `/config.js` (never committed) used to supply `window.AVIATION_KEY` + `window.EJS_*`; its absence 404'd (SEMrush "broken internal JS") AND broke the flight tracker + contact pages. Removed entirely.

**How to apply:** Don't reintroduce `/config.js` or client-side AviationStack calls. New booking/contact forms should POST to `/.netlify/functions/contact`. If contact emails stop sending, check `SENDGRID_API_KEY` in Netlify; if the flight tracker stops, check `AVIATIONSTACK_API_KEY`.
