---
name: AI-readiness (isitagentready) fixes
description: What was already in place and the right pattern for AI-discovery edits on purpleheartlimo.com.
---

# AI-readiness (isitagentready.com) fixes

State of the site (so a future agent doesn't re-create or overwrite):
- **llms.txt already exists** at root and is canonical-correct + far richer than any
  template prompt. Do NOT overwrite it from an external prompt.
- **robots.txt already allows** the major AI crawlers (GPTBot, ChatGPT-User,
  OAI-SearchBot, PerplexityBot, ClaudeBot, Claude-Web, Google-Extended,
  Applebot-Extended, CCBot, anthropic-ai, cohere-ai) and has the Sitemap line.
  Content-Signal lines (ai-train/search/ai-input) live at the very top.

Patterns / decisions:
- **Headers go in netlify.toml, NOT a `_headers` file.** netlify.toml is the single
  source of truth for headers+redirects here. Adding `_headers` would split config.
- **Do NOT advertise `Link: </.well-known/api-catalog>`** — no API catalog exists;
  a broken Link header is worse than none. API/OAuth/MCP items are out of scope for
  this limo business site.
- Existing global security headers set `X-Frame-Options: SAMEORIGIN` — don't override
  to DENY.

**Why:** External "AI fix" prompts for this site shipped WRONG business data — phone
(833) 400-7007 and a bare moovs booking URL. Site truth is **(833) 740-0700** and
**/booking.html** (737+ occurrences). Always verify contact data against the site
before writing it into discovery files; never copy a prompt's contact block blindly.
