---
name: Live deploy host reality
description: Where purpleheartlimo.com actually serves from, and how its DNS/email are wired.
---

The live custom domain **purpleheartlimo.com now serves from Netlify** (project
`purpleheartlimo`, subdomain `purpleheartlimo.netlify.app`, auto-deploys from the
GitHub repo `idreesza/purpleheartlimo-website` main branch). The DNS cutover is
done: the domain uses **Netlify DNS** (nameservers `dns{1..4}.p01.nsone.net`),
apex is the primary domain, and `www` redirects to apex. Let's Encrypt SSL is
issued and valid.

**Why it matters:** `netlify.toml` is now the LIVE, authoritative config for
redirects/headers — it is no longer dormant. The old Replit static deployment
(`purpleheartlimo-website.replit.app`, deploymentTarget="static") still exists but
is NOT what the domain points at. Edit `netlify.toml` for any redirect/header
change and it takes effect on the live domain after a GitHub push + Netlify build.

**Code reaches the live site only via GitHub.** Replit checkpoint commits are NOT
auto-pushed; you must push to GitHub `origin/main` for Netlify to rebuild. (Main
agent cannot push — guide the user, or they push from the Replit Git pane.)

**Email is on Netlify DNS — protect it.** Because nameservers point to Netlify,
ALL DNS (including mail) lives in the Netlify DNS zone. The domain uses **Namecheap
Private Email**; required records were re-added manually after the cutover:
MX `@ -> mx1.privateemail.com` / `mx2.privateemail.com` (pri 10), TXT SPF
`v=spf1 include:spf.privateemail.com ~all`. DKIM (`default._domainkey` TXT, unique
per account) was deferred. **Any future DNS change must keep these MX/TXT records
or the business email breaks.**
