#!/usr/bin/env python3
"""Idempotently rework legacy flat blog pages that have no generator source.

This intentionally targets only the two confirmed flat-only legacy posts. Run it
explicitly after review; it preserves canonical URLs and does not discover or
modify any other rendered pages.
"""
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent

POSTS = {
    "blog/addison-restaurant-row.html": {
        "title": "Addison Restaurant Row Limo Service | Purple Heart",
        "meta": (
            "Book Addison Restaurant Row limo service for dinner groups, "
            "corporate hosting, airport arrivals, and a safe ride home."
        ),
        "headline": "Addison Restaurant Row Limo Service",
        "intro": (
            "Plan a chauffeured Addison Restaurant Row evening with pickup, "
            "multi-stop dinner routing, and a dedicated ride home for your group."
        ),
        "article": """<h2>Addison Restaurant Row Chauffeur Service</h2>
<p>Purple Heart Limo plans dinner transportation around your reservation times rather than parking availability. Reserve a sedan for a couple, an SUV for a business dinner or family group, or a Sprinter when several guests want to travel together. Your chauffeur can wait while you move from cocktails to dinner to dessert, so no one has to relocate cars or serve as the designated driver.</p>
<h2>Useful Addison Dinner Logistics</h2>
<ul><li><strong>Reservation-first pickup:</strong> Share the restaurant, reservation time, pickup address, passenger count, and luggage or mobility notes when booking.</li><li><strong>Multi-stop routing:</strong> Add a hotel, cocktail bar, Addison Improv, or a final home drop-off before departure; we build the route around the group's plan.</li><li><strong>Airport and hotel arrivals:</strong> Guests arriving through DFW or Love Field can reserve <a href="/services.html#airport" style="color:#C9A84C">airport chauffeur service</a> directly to Addison.</li><li><strong>Business hosting:</strong> Use our <a href="/services.html#corporate" style="color:#C9A84C">corporate transportation</a> for client dinners, executive arrivals, and account-team outings.</li></ul>
<h2>Restaurant Row Transportation for Celebrations</h2>
<p>Anniversaries, birthdays, bachelor or bachelorette dinners, and visiting-family evenings benefit from a single vehicle and a known pickup plan. For larger celebration groups, ask about a Sprinter or <a href="/services.html#nightout" style="color:#C9A84C">private party transportation</a>. We coordinate the vehicle around your itinerary, not a rideshare queue after dinner.</p>
<div class="cta"><h3>Book Your Addison Chauffeur</h3><p>Call <a href="tel:+18337400700" style="color:#C9A84C">(833) 740-0700</a> for timing help, or reserve online for Addison dinner, airport, and group transportation.</p><a href="/booking.html">Book Your Ride &rarr;</a></div>
<h2>Dallas-Area Limo Service</h2>
<p>See our <a href="/limo-service-dallas-tx/" style="color:#C9A84C">Dallas limo service</a> options for vehicle and service-area details. Purple Heart Limo provides scheduled, professional transportation for Addison and throughout DFW.</p>""",
    },
    "blog/dallas-luxury-shopping.html": {
        "title": "Dallas Mall Limo Service | Purple Heart",
        "meta": (
            "Reserve Dallas mall limo service for NorthPark, Highland Park "
            "Village, Galleria, shopping groups, airport arrivals, and events."
        ),
        "headline": "Dallas Mall Limo Service and Shopping Transportation",
        "intro": (
            "Book a private chauffeur for Dallas mall pickups, shopping-day "
            "routing, bag space, airport arrivals, and a relaxed ride between stops."
        ),
        "article": """<h2>Dallas Mall Limo Service</h2>
<p>Purple Heart Limo provides scheduled transportation for shopping days at NorthPark Center, Highland Park Village, Galleria Dallas, Legacy West, and other DFW retail destinations. A chauffeur handles curbside pickup, parking circulation, and the drive between stores while you keep purchases secure in the vehicle and stay on your own schedule.</p>
<h2>Plan Your Shopping Transportation</h2>
<ul><li><strong>Choose the right vehicle:</strong> A sedan suits one or two shoppers; an SUV provides extra passenger and bag room; and a Sprinter keeps a larger group together.</li><li><strong>Build a multi-stop itinerary:</strong> Share your first pickup, planned malls, lunch or dinner reservation, and final drop-off so the chauffeur can plan timing.</li><li><strong>Coordinate airport arrivals:</strong> Book <a href="/services.html#airport" style="color:#C9A84C">airport transportation</a> from DFW or Love Field to a hotel, mall, or appointment.</li><li><strong>Host clients without parking hassles:</strong> Our <a href="/services.html#corporate" style="color:#C9A84C">corporate chauffeur service</a> supports executive shopping appointments and visitor itineraries.</li></ul>
<h2>Shopping Days, Events, and Group Rides</h2>
<p>For birthday shopping, holiday outings, fashion appointments, or a dinner after the mall, reserve a dedicated chauffeur instead of splitting the group among cars. Larger celebration groups can ask about <a href="/services.html#nightout" style="color:#C9A84C">private party transportation</a> and Sprinter availability.</p>
<div class="cta"><h3>Reserve Dallas Shopping Transportation</h3><p>Call <a href="tel:+18337400700" style="color:#C9A84C">(833) 740-0700</a> to discuss your stops and pickup timing, or book a chauffeur online.</p><a href="/booking.html">Book Your Ride &rarr;</a></div>
<h2>Dallas Chauffeur Service Details</h2>
<p>Visit our <a href="/limo-service-dallas-tx/" style="color:#C9A84C">Dallas limo service</a> page for DFW coverage and vehicle options. We provide professional, prearranged transportation for shopping, airport, corporate, and event itineraries.</p>""",
    },
}


def replace_once(text, pattern, replacement, page):
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise ValueError(f"Expected one {page} source fragment for {pattern!r}")
    return updated


def rework(path, post):
    if len(post["title"]) > 60:
        raise ValueError(f"Title exceeds 60 characters: {path}")
    if len(post["meta"]) > 155:
        raise ValueError(f"Meta description exceeds 155 characters: {path}")
    html = path.read_text(encoding="utf-8")
    if post["headline"] in html and post["article"] in html:
        return False
    html = replace_once(html, r"<title>.*?</title>", f"<title>{post['title']}</title>", path)
    html = replace_once(
        html, r'<meta name="description" content=".*?">', f'<meta name="description" content="{post["meta"]}">', path
    )
    html = replace_once(html, r'("headline":")[^"]*', r"\g<1>" + post["headline"], path)
    html = replace_once(html, r'("description":")[^"]*', r"\g<1>" + post["meta"], path)
    html = replace_once(html, r"<h1>.*?</h1>", f"<h1>{post['headline']}</h1>", path)
    html = replace_once(html, r'<p class="intro">.*?</p>', f'<p class="intro">{post["intro"]}</p>', path)
    html = replace_once(html, r'<article class="body">.*?</article>', f'<article class="body">\n{post["article"]}\n</article>', path)
    path.write_text(html, encoding="utf-8")
    return True


if __name__ == "__main__":
    for relative_path, post in POSTS.items():
        changed = rework(ROOT / relative_path, post)
        print(f"{'Updated' if changed else 'Already updated'} {relative_path}")