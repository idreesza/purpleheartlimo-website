---
name: Booking carousel event ownership
description: Legacy event listeners can conflict with the final booking vehicle layer
---
When replacing a booking carousel control's behavior, remove legacy listeners rather than only assigning a new onclick handler.

**Why:** Expand Rides was toggled twice by old and new handlers, making it appear unresponsive. Legacy transforms and selected-card realignment also competed with native scrolling.

**How to apply:** Give the final interaction layer sole ownership of controls and scrolling. Verify selected radio and visible card agree after repeated navigation, and expanded state changes exactly once per click.