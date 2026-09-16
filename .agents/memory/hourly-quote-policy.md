---
name: Hourly quote policy
description: User-approved scope of hourly hub pricing versus existing transfer fares
---
Austin and Dallas use the same existing hourly rates. Round the customer's requested start/end duration upward only for Hourly service; airport and point-to-point fare rules are not replaced.

**Why:** The user explicitly narrowed the uploaded all-trip hourly pricing proposal to Hourly service and confirmed rates already exist.

**How to apply:** If Google's backend hub check fails, show a contact-for-quote message rather than a guessed default price. Hub addresses must remain backend-only, including protection against static access to backend source and uploaded specifications. Do not reuse the website-restricted browser autocomplete key for server calls.