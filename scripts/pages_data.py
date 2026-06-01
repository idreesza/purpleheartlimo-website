#!/usr/bin/env python3
"""Per-page content for the landing-page generator.

Each page targets a real keyword cluster from the SEMrush gap analysis where
purpleheartlimo.com ranked 0 while competitors ranked. Content is unique and
localized per page to avoid thin/doorway content.
"""


def build_pages(STD_WHY, AUSTIN_AREAS, DALLAS_AREAS):
    AUS_HUB = ("limo-service-austin-tx", "Limo Service Austin")
    DAL_HUB = ("limo-service-dallas-tx", "Limo Service Dallas-Fort Worth")

    austin_related = [
        ("/car-service-austin-tx/", "Austin Car Service"),
        ("/austin-airport-limo/", "Austin Airport Limo"),
        ("/austin-chauffeur-service/", "Austin Chauffeur Service"),
        ("/austin-limo-rental/", "Austin Limo Rental"),
        ("/austin-wedding-limo/", "Austin Wedding Limo"),
        ("/austin-sprinter-van-rental/", "Austin Sprinter Van"),
        ("/limo-service-austin-tx/", "Austin Limo Service"),
    ]
    dallas_related = [
        ("/dallas-corporate-car-service/", "Dallas Corporate Car Service"),
        ("/car-service-dallas-love-field/", "Dallas Love Field Car Service"),
        ("/dfw-airport-car-service/", "DFW Airport Car Service"),
        ("/dallas-wedding-transportation/", "Dallas Wedding Transportation"),
        ("/dallas-party-bus/", "Dallas Party Bus"),
        ("/limo-service-dallas-tx/", "Dallas Limo Service"),
    ]

    def rel(items, exclude):
        return [x for x in items if x[0] != exclude]

    pages = []

    # ---------------- AUSTIN ----------------

    # 1. Car Service Austin (black car) — car service austin / austin tx
    pages.append({
        "slug": "car-service-austin-tx",
        "title": "Car Service Austin TX | Black Car & Executive Sedan | Purple Heart Limo",
        "meta": "Professional car service in Austin, TX. Black car & executive sedan service for airport, business and point-to-point trips. Flat rates, no surge, 24/7. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 Car Service Austin TX",
        "image": "sedan-cadillac.webp",
        "areas": AUSTIN_AREAS, "locality": "Austin", "reviews": 214,
        "hub_slug": AUS_HUB[0], "hub_name": AUS_HUB[1], "crumb": "Car Service Austin TX",
        "badge": "\U0001F396\uFE0F Texan-Owned \u00b7 Austin, TX",
        "h1_main": "Car Service", "h1_em": "Austin, TX",
        "hero_p": "Reliable black car and executive sedan service across Austin \u2014 airport runs, business meetings, and point-to-point trips with a professional chauffeur. Flat rates, zero surge pricing, available 24/7 throughout the Austin metro.",
        "stats": [("4.9\u2605", "Average Rating"), ("214+", "Austin Reviews"), ("24/7", "Available"), ("$0", "Surge Fees")],
        "svc_label": "Austin Car Service", "svc_title": "Black Car Service for Every Austin Trip",
        "svc_desc": "From AUS airport transfers to downtown business meetings, our Austin car service delivers a polished, on-time ride every time.",
        "cards": [
            ("\u2708\uFE0F", "Airport Car Service", "Flat-rate sedans to and from Austin-Bergstrom (AUS), flight-monitored."),
            ("\U0001F4BC", "Corporate Travel", "Executive sedans for client pickups, meetings and roadshows."),
            ("\U0001F4CD", "Point-to-Point", "Fixed-price rides anywhere in Austin \u2014 no metering, no surprises."),
            ("\u23F1\uFE0F", "Hourly Hire", "Keep a car and chauffeur on call by the hour for multi-stop days."),
            ("\U0001F37E", "Night Out", "Safe, stylish rides to 6th Street, the Domain and Rainey Street."),
            ("\U0001F698", "Luxury SUV", "Cadillac Escalade and Suburban for groups, luggage and comfort."),
        ],
        "body": [
            ("Austin's Trusted Black Car Service", [
                "When you search for a dependable car service in Austin, you want more than a rideshare \u2014 you want a professional chauffeur, a spotless vehicle, and a price that doesn't change because it's rush hour or a festival weekend. Purple Heart Limo provides exactly that: flat-rate black car service across Austin and the surrounding Hill Country, operated by a veteran-owned team that treats punctuality as a mission.",
                "Our Austin car service is built for business travelers, families and visitors who need to be somewhere on time. Every booking is confirmed with a real person, every chauffeur is professionally dressed and background-checked, and every airport pickup is matched to your live flight status so your driver is waiting when you land at AUS.",
            ]),
            ("Where We Drive in Austin", [
                "We cover the entire Austin metro \u2014 downtown, the Domain, the University of Texas, the Arboretum and the tech corridor \u2014 plus surrounding cities:",
                '<ul><li>Round Rock, Cedar Park &amp; Leander</li><li>Georgetown &amp; Pflugerville</li><li>Lakeway, Bee Cave &amp; West Lake Hills</li><li>Kyle, Buda &amp; San Marcos</li></ul>',
                "Need a ride to the airport, a corporate event, or a night out? Our <a href=\"/austin-airport-limo/\">Austin airport limo service</a> and <a href=\"/austin-chauffeur-service/\">private chauffeur service</a> are just a call away.",
            ]),
            ("Why Flat Rates Matter", [
                "Rideshare apps surge during ACL, SXSW, UT football weekends and every storm. Our car service quotes a flat rate when you book, so a 6 a.m. airport run costs the same whether it's a quiet Tuesday or a packed festival Saturday. That predictability is why Austin businesses and families keep us on speed dial.",
            ]),
        ],
        "form_title": "Book Austin Car Service", "form_btn": "Request Austin Car Service",
        "service_opts": ["Airport Car Service (AUS)", "Corporate / Executive", "Point-to-Point", "Hourly Charter", "Night Out / Event", "Wedding", "Other"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Stretch Limousine", "Executive Sprinter", "Party Bus"],
        "pickup_ph": "123 Congress Ave, Austin TX or AUS Airport", "city_val": "Austin TX",
        "why_title": "Austin's Texan-Owned Choice", "why": STD_WHY,
        "faq_title": "Austin Car Service FAQ",
        "faqs": [
            ("How much does car service in Austin cost?", "We quote a flat rate at the time of booking based on your pickup, destination and vehicle \u2014 no surge pricing and no hidden fees. Call (833) 740-0700 for an exact quote."),
            ("Do you offer black car service to Austin-Bergstrom Airport (AUS)?", "Yes. We provide flight-monitored black car and SUV service to and from AUS, with meet-and-greet pickup and flat-rate pricing."),
            ("Can I book a car service by the hour in Austin?", "Absolutely. Hourly charter keeps a chauffeur and vehicle dedicated to you for multi-stop business days, events or nights out across the Austin metro."),
            ("How far in advance should I book?", "We recommend booking 24\u201348 hours ahead, but we accommodate same-day and last-minute Austin car service requests whenever a vehicle is available."),
        ],
        "related": rel(austin_related, "/car-service-austin-tx/"),
    })

    # 2. Austin Airport Limo
    pages.append({
        "slug": "austin-airport-limo",
        "title": "Austin Airport Limo Service (AUS) | Flat-Rate Black Car | Purple Heart Limo",
        "meta": "Austin airport limo & car service to and from Austin-Bergstrom (AUS). Flight-monitored, meet & greet, flat rates, 24/7. Sedans, SUVs & Sprinters. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 Austin Airport Limo Service",
        "image": "luxsuv-escalade.webp",
        "areas": AUSTIN_AREAS, "locality": "Austin", "reviews": 214,
        "hub_slug": AUS_HUB[0], "hub_name": AUS_HUB[1], "crumb": "Austin Airport Limo",
        "badge": "\u2708\uFE0F Austin-Bergstrom (AUS)",
        "h1_main": "Austin Airport", "h1_em": "Limo Service",
        "hero_p": "Flight-monitored limo and car service to and from Austin-Bergstrom International Airport (AUS). Meet-and-greet pickups, flat rates with zero surge, and chauffeurs who track your flight so they're waiting the moment you land.",
        "stats": [("4.9\u2605", "Average Rating"), ("AUS", "Airport Served"), ("24/7", "Available"), ("$0", "Surge Fees")],
        "svc_label": "AUS Airport Transfers", "svc_title": "Stress-Free Rides To & From AUS",
        "svc_desc": "Whether you're catching a 5 a.m. departure or landing after midnight, our Austin airport limo service is ready around the clock.",
        "cards": [
            ("\U0001F6EC", "Arrivals Meet & Greet", "Your chauffeur tracks your flight and meets you at baggage claim."),
            ("\U0001F6EB", "Departures On Time", "Early, monitored pickups so you never rush to make your flight."),
            ("\U0001F4BC", "Corporate Airport Travel", "Executive sedans and SUVs for business travelers and teams."),
            ("\U0001F46A", "Family & Groups", "Sprinter vans with room for luggage, car seats and the whole party."),
            ("\U0001F4F1", "Flight Monitoring", "Delays and early landings handled automatically \u2014 no extra fees."),
            ("\U0001F4B5", "Flat Airport Rates", "One fixed price to AUS, quoted up front, no surge ever."),
        ],
        "body": [
            ("Austin-Bergstrom Airport Limo & Car Service", [
                "A great trip starts and ends with a ride you can count on. Purple Heart Limo's Austin airport limo service takes the stress out of getting to and from Austin-Bergstrom International Airport (AUS) \u2014 no parking, no surge pricing, no wondering whether your driver will show. We monitor your flight in real time, so if you land early or your flight is delayed, your chauffeur adjusts automatically.",
                "Arriving passengers get meet-and-greet service: your professionally dressed chauffeur greets you, helps with luggage, and walks you to a spotless sedan, SUV or Sprinter. Departing? We arrive early, every time, and keep you ahead of Austin traffic so you reach your gate relaxed.",
            ]),
            ("Airport Transfers Across the Austin Metro", [
                "We provide flat-rate AUS transfers from anywhere in the region \u2014 downtown hotels, the Domain, UT, the tech corridor, and surrounding suburbs including Round Rock, Cedar Park, Georgetown, Lakeway and Kyle. Traveling for business? Pair your transfer with our <a href=\"/austin-corporate-car-service/\">corporate car service</a> or keep a car on call with our <a href=\"/austin-chauffeur-service/\">chauffeur service</a>.",
            ]),
            ("Choose the Right Vehicle", [
                "Solo or a couple? An executive sedan is perfect. Traveling with luggage or a small group? A luxury SUV gives you room to spread out. Flying with a team, a family, or lots of bags? Our <a href=\"/austin-sprinter-van-rental/\">executive Sprinter van</a> seats up to 12 in comfort.",
            ]),
        ],
        "form_title": "Book Austin Airport Limo", "form_btn": "Request AUS Airport Transfer",
        "service_opts": ["AUS Airport Arrival", "AUS Airport Departure", "Round-Trip Airport", "Corporate Airport Travel", "Group / Family Airport", "Other"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Executive Sprinter", "Stretch Limousine"],
        "pickup_ph": "AUS Airport or 123 Main St, Austin TX", "city_val": "Austin TX",
        "why_title": "Austin's Texan-Owned Airport Choice", "why": STD_WHY,
        "faq_title": "Austin Airport Limo FAQ",
        "faqs": [
            ("Do you monitor my flight for delays?", "Yes. Every AUS pickup is matched to your live flight status, so your chauffeur adjusts automatically to early or delayed arrivals at no extra charge."),
            ("Where do you meet me at Austin-Bergstrom (AUS)?", "For arrivals we offer meet-and-greet service \u2014 your chauffeur meets you at baggage claim and helps with your luggage. Curbside pickup is also available on request."),
            ("How much is a limo to Austin airport?", "Airport transfers are flat-rate and quoted up front based on your location and vehicle. There is never surge pricing. Call (833) 740-0700 for your exact fare."),
            ("Can you handle very early or late-night flights?", "Yes \u2014 our Austin airport limo service operates 24/7, including pre-dawn departures and overnight arrivals."),
        ],
        "related": rel(austin_related, "/austin-airport-limo/"),
    })

    # 3. Austin Chauffeur Service (private / family / black car)
    pages.append({
        "slug": "austin-chauffeur-service",
        "title": "Austin Chauffeur Service | Private & Personal Drivers | Purple Heart Limo",
        "meta": "Private chauffeur service in Austin, TX. Personal & family chauffeurs, executive black car, hourly hire. Professional, discreet, 24/7. Texan-owned. Flat rates.",
        "schema_name": "Purple Heart Limo \u2014 Austin Chauffeur Service",
        "image": "sedan-cadillac.webp",
        "areas": AUSTIN_AREAS, "locality": "Austin", "reviews": 214,
        "hub_slug": AUS_HUB[0], "hub_name": AUS_HUB[1], "crumb": "Austin Chauffeur Service",
        "badge": "\U0001F454 Private Chauffeurs \u00b7 Austin",
        "h1_main": "Austin", "h1_em": "Chauffeur Service",
        "hero_p": "Professional private chauffeur service in Austin \u2014 personal drivers, family chauffeurs and executive black car service by the hour or the day. Discreet, punctual and flat-rate, available 24/7 across the Austin metro.",
        "stats": [("4.9\u2605", "Average Rating"), ("214+", "Austin Reviews"), ("24/7", "On Call"), ("$0", "Surge Fees")],
        "svc_label": "Private Chauffeurs", "svc_title": "Your Personal Driver in Austin",
        "svc_desc": "From a full day of meetings to errands, school runs and special occasions, your dedicated chauffeur handles the driving so you don't have to.",
        "cards": [
            ("\U0001F454", "Personal Chauffeur", "A dedicated professional driver for your day, by the hour."),
            ("\U0001F46A", "Family Chauffeur", "Safe, reliable rides for kids, parents and busy households."),
            ("\U0001F4BC", "Executive Black Car", "Polished sedans and SUVs for business and client travel."),
            ("\u23F1\uFE0F", "Hourly Hire", "Keep your chauffeur and vehicle on call for multi-stop days."),
            ("\U0001F377", "Hill Country Tours", "Private wine-country and Hill Country day trips with a driver."),
            ("\U0001F512", "Discreet & Vetted", "Background-checked, professionally dressed, confidential."),
        ],
        "body": [
            ("Private Chauffeur Service in Austin", [
                "A chauffeur is more than a driver \u2014 it's having a trusted professional handle the road while you focus on what matters. Purple Heart Limo's Austin chauffeur service pairs you with discreet, background-checked drivers in immaculate vehicles, available by the hour or for the full day across Austin and the Hill Country.",
                "Whether you need an executive black car for back-to-back meetings, a personal chauffeur for errands and appointments, or a family chauffeur to handle school runs and activities safely, we tailor the service to your schedule. You get the same driver experience the city's executives rely on, at honest flat rates.",
            ]),
            ("Who Uses an Austin Chauffeur?", [
                '<ul><li><strong>Executives</strong> who want to work or take calls between meetings</li><li><strong>Families</strong> who need a safe, consistent driver for children or elderly parents</li><li><strong>Visitors</strong> exploring Austin, the Domain and Hill Country wineries</li><li><strong>Event guests</strong> who want a dedicated driver for the evening</li></ul>',
                "Need airport transfers too? See our <a href=\"/austin-airport-limo/\">Austin airport limo service</a>, or browse all <a href=\"/limo-service-austin-tx/\">Austin limo services</a>.",
            ]),
            ("Hourly & Full-Day Chauffeur Hire", [
                "Our hourly chauffeur service is ideal when your day has multiple stops. Your driver waits, anticipates your schedule, and keeps everything running on time \u2014 no re-booking, no waiting for the next rideshare. Book a few hours or reserve a chauffeur for the entire day.",
            ]),
        ],
        "form_title": "Book an Austin Chauffeur", "form_btn": "Request Chauffeur Service",
        "service_opts": ["Personal Chauffeur (Hourly)", "Family Chauffeur", "Executive Black Car", "Full-Day Chauffeur", "Hill Country Tour", "Other"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Executive Sprinter", "Stretch Limousine"],
        "pickup_ph": "123 Main St, Austin TX", "city_val": "Austin TX",
        "why_title": "Austin's Texan-Owned Chauffeurs", "why": STD_WHY,
        "faq_title": "Austin Chauffeur Service FAQ",
        "faqs": [
            ("What is the difference between a chauffeur and a rideshare driver?", "A chauffeur is a professional, background-checked driver dedicated to you \u2014 in a luxury vehicle, professionally dressed, and reserved for your schedule. There's no surge pricing and no rotating strangers."),
            ("Can I hire a private chauffeur by the hour in Austin?", "Yes. Hourly chauffeur hire keeps a driver and vehicle dedicated to you for multi-stop days, events, or business. Book a few hours or the full day."),
            ("Do you offer family chauffeur service?", "We do. Many Austin families rely on us for safe, consistent rides for children, teens and elderly parents with vetted, professional drivers."),
            ("Are your chauffeurs background-checked?", "Every Purple Heart Limo chauffeur is background-checked, professionally trained, and discreet. Confidentiality and safety are core to our service."),
        ],
        "related": rel(austin_related, "/austin-chauffeur-service/"),
    })

    # 4. Austin Limo Rental
    pages.append({
        "slug": "austin-limo-rental",
        "title": "Austin Limo Rental | Stretch Limousine & SUV Hire | Purple Heart Limo",
        "meta": "Austin limo rental \u2014 stretch limousines, limo SUVs & party-ready vehicles for weddings, proms, nights out & events. Hourly packages, flat rates, 24/7. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 Austin Limo Rental",
        "image": "stretch-limo.webp",
        "areas": AUSTIN_AREAS, "locality": "Austin", "reviews": 214,
        "hub_slug": AUS_HUB[0], "hub_name": AUS_HUB[1], "crumb": "Austin Limo Rental",
        "badge": "\U0001F695 Stretch Limos \u00b7 Austin",
        "h1_main": "Austin", "h1_em": "Limo Rental",
        "hero_p": "Rent a stretch limousine or limo SUV in Austin for weddings, proms, nights out and special events. Flat-rate hourly packages, a polished chauffeur, and zero surge pricing \u2014 available 24/7 across the Austin metro.",
        "stats": [("4.9\u2605", "Average Rating"), ("214+", "Austin Reviews"), ("8\u201312", "Passengers"), ("$0", "Surge Fees")],
        "svc_label": "Limo Rentals", "svc_title": "The Right Limo for Every Austin Occasion",
        "svc_desc": "Celebrate in style with a chauffeur-driven stretch limousine or limo SUV, booked by the hour with transparent flat pricing.",
        "cards": [
            ("\U0001F48D", "Weddings", "Stretch limos for the couple and the bridal party. Full-day packages."),
            ("\U0001F393", "Prom & Graduation", "Safe, parent-approved limo rentals with professional chauffeurs."),
            ("\U0001F377", "Wine Tours", "Hill Country winery day trips by the hour, no driving required."),
            ("\U0001F389", "Birthdays & Bachelorette", "Make a night of it with a party-ready stretch limo."),
            ("\U0001F37E", "Nights Out", "Downtown, Rainey Street and the Domain in limousine style."),
            ("\u23F1\uFE0F", "Hourly Packages", "Flexible hourly rentals with flat, all-in pricing."),
        ],
        "body": [
            ("Stretch Limousine & Limo SUV Rentals in Austin", [
                "Some occasions deserve more than a sedan. Purple Heart Limo's Austin limo rental service puts a chauffeur-driven stretch limousine or limo SUV at your door for weddings, proms, milestone birthdays, bachelorette parties and big nights out. You ride; we handle the driving, the parking and the logistics.",
                "Every limo rental comes with a professional, background-checked chauffeur and honest flat-rate pricing \u2014 the quote you get at booking is the price you pay, even on festival weekends. Reserve by the hour and build the package around your event.",
            ]),
            ("Popular Reasons to Rent a Limo in Austin", [
                '<ul><li><strong>Weddings</strong> \u2014 elegant arrivals and bridal-party transport (see our <a href="/austin-wedding-limo/">Austin wedding limo</a> service)</li><li><strong>Prom &amp; homecoming</strong> \u2014 safe, supervised group transportation</li><li><strong>Wine tours</strong> \u2014 Hill Country and Driftwood wineries</li><li><strong>Birthdays &amp; bachelorette parties</strong> \u2014 celebrate without a designated driver</li><li><strong>Concerts &amp; sports</strong> \u2014 ACL, Moody Center and Q2 Stadium</li></ul>',
            ]),
            ("How Limo Rental Pricing Works", [
                "Limo rentals are typically booked by the hour with a small minimum, depending on the date and vehicle. We quote one flat, all-in rate up front \u2014 no surge, no fuel surprises. Larger group? Consider our <a href=\"/austin-sprinter-van-rental/\">Sprinter van rental</a> for up to 12 passengers.",
            ]),
        ],
        "form_title": "Book an Austin Limo Rental", "form_btn": "Request Limo Rental Quote",
        "service_opts": ["Wedding", "Prom / Graduation", "Wine Tour", "Birthday / Bachelorette", "Night Out", "Concert / Sports", "Other"],
        "vehicle_opts": ["Stretch Limousine", "Stretch SUV Limo", "Luxury SUV", "Executive Sprinter", "Party Bus"],
        "pickup_ph": "123 Main St, Austin TX", "city_val": "Austin TX",
        "why_title": "Austin's Texan-Owned Limo Choice", "why": STD_WHY,
        "faq_title": "Austin Limo Rental FAQ",
        "faqs": [
            ("How much does it cost to rent a limo in Austin?", "Limo rentals are booked by the hour and quoted as one flat, all-in rate based on the date, duration and vehicle. There is no surge pricing. Call (833) 740-0700 for a quote."),
            ("How many people fit in your limos?", "Our stretch limousines seat up to 8\u201310 passengers; for larger groups our executive Sprinter and party bus options seat up to 12 or more."),
            ("Is there a minimum rental time?", "Most limo rentals have a modest hourly minimum that varies by date and event. We'll confirm the exact terms when you book."),
            ("Do you provide limos for proms?", "Yes \u2014 safe, parent-approved prom and graduation limo rentals with professional chauffeurs are one of our most popular Austin services."),
        ],
        "related": rel(austin_related, "/austin-limo-rental/"),
    })

    # 5. Austin Wedding Limo
    pages.append({
        "slug": "austin-wedding-limo",
        "title": "Austin Wedding Limo Service | Bridal Party Transportation | Purple Heart Limo",
        "meta": "Austin wedding limo & transportation \u2014 stretch limousines, SUVs & Sprinters for the couple, bridal party & guests. Hill Country venues, flat rates. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 Austin Wedding Limo Service",
        "image": "stretch-limo.webp",
        "areas": AUSTIN_AREAS, "locality": "Austin", "reviews": 214,
        "hub_slug": AUS_HUB[0], "hub_name": AUS_HUB[1], "crumb": "Austin Wedding Limo",
        "badge": "\U0001F48D Weddings \u00b7 Austin & Hill Country",
        "h1_main": "Austin", "h1_em": "Wedding Limo",
        "hero_p": "Elegant wedding limo and transportation in Austin \u2014 for the couple, the bridal party and your guests. Stretch limousines, luxury SUVs and Sprinters for Hill Country venues and city ceremonies, with flat rates and a chauffeur who keeps your day on schedule.",
        "stats": [("4.9\u2605", "Average Rating"), ("214+", "Austin Reviews"), ("100%", "On-Time"), ("$0", "Surge Fees")],
        "svc_label": "Wedding Transportation", "svc_title": "Transportation That Makes the Day Effortless",
        "svc_desc": "From the first-look to the send-off, we handle every transfer so you and your guests arrive relaxed and on time.",
        "cards": [
            ("\U0001F48D", "Couple's Limo", "A stunning stretch limousine for the newlyweds' grand entrance and exit."),
            ("\U0001F470", "Bridal Party", "SUVs and Sprinters to keep the wedding party together and on time."),
            ("\U0001F3F0", "Hill Country Venues", "Reliable transfers to Driftwood, Dripping Springs and Wimberley."),
            ("\U0001F68C", "Guest Shuttles", "Sprinter shuttles between hotels, ceremony and reception."),
            ("\U0001F4C5", "Full-Day Packages", "Multi-vehicle, multi-stop coordination for the entire celebration."),
            ("\u2708\uFE0F", "Out-of-Town Guests", "AUS airport transfers for arriving family and guests."),
        ],
        "body": [
            ("Austin Wedding Limo & Transportation", [
                "Your wedding day runs on timing, and transportation is the thread that holds it together. Purple Heart Limo provides elegant, dependable wedding limo service across Austin and the Hill Country \u2014 a show-stopping stretch limousine for the couple, comfortable SUVs and Sprinters for the bridal party, and guest shuttles that keep everyone moving between venues.",
                "We specialize in Austin's most popular wedding regions, including the Driftwood, Dripping Springs and Wimberley venues where reliable transportation makes all the difference. Your chauffeur arrives early, dresses for the occasion, and follows a timeline built around your day \u2014 so no one is ever left waiting.",
            ]),
            ("Wedding Packages Built Around You", [
                "Every wedding is different, so we tailor the vehicles and timeline to your plan:",
                '<ul><li>Couple\u2019s stretch limousine for the ceremony exit and photos</li><li>Bridal-party SUVs and Sprinter vans</li><li>Guest shuttles between hotels, ceremony and reception</li><li><a href="/austin-airport-limo/">AUS airport transfers</a> for out-of-town family</li></ul>',
                "Planning other celebrations too? Explore our full <a href=\"/austin-limo-rental/\">Austin limo rental</a> options.",
            ]),
            ("Why Couples Choose Purple Heart", [
                "Veteran-owned and detail-obsessed, we treat your timeline like a mission. Flat rates mean no surprise charges on your big day, and our chauffeurs coordinate directly with your planner so transportation is one less thing to worry about.",
            ]),
        ],
        "form_title": "Book Austin Wedding Transportation", "form_btn": "Request Wedding Quote",
        "service_opts": ["Couple's Wedding Limo", "Bridal Party Transport", "Guest Shuttle", "Full Wedding Package", "Engagement / Rehearsal", "Other"],
        "vehicle_opts": ["Stretch Limousine", "Luxury SUV", "Executive Sprinter", "Party Bus", "Executive Sedan"],
        "pickup_ph": "Hotel or venue, Austin / Hill Country TX", "city_val": "Austin TX",
        "why_title": "Austin's Texan-Owned Wedding Choice", "why": STD_WHY,
        "faq_title": "Austin Wedding Limo FAQ",
        "faqs": [
            ("Do you provide transportation to Hill Country wedding venues?", "Yes \u2014 we regularly serve Driftwood, Dripping Springs, Wimberley and other Hill Country venues, plus city ceremonies throughout the Austin metro."),
            ("Can you transport the whole bridal party and guests?", "Absolutely. We combine stretch limos, luxury SUVs and Sprinter shuttles to move the couple, the wedding party and guests on a single coordinated timeline."),
            ("Do you offer full-day wedding packages?", "We do. Full-day packages cover multiple vehicles, multiple stops and direct coordination with your planner so every transfer runs on schedule."),
            ("How early should we book wedding transportation?", "Wedding dates book quickly, especially in spring and fall. We recommend reserving as early as possible \u2014 call (833) 740-0700 to check your date."),
        ],
        "related": rel(austin_related, "/austin-wedding-limo/"),
    })

    # 6. Austin Sprinter Van Rental
    pages.append({
        "slug": "austin-sprinter-van-rental",
        "title": "Austin Sprinter Van Rental | Group & Corporate Travel | Purple Heart Limo",
        "meta": "Austin Sprinter van rental with chauffeur \u2014 luxury group travel for up to 12. Corporate roadshows, wine tours, airport groups & events. Flat rates, 24/7. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 Austin Sprinter Van Rental",
        "image": "sprinter.webp",
        "areas": AUSTIN_AREAS, "locality": "Austin", "reviews": 214,
        "hub_slug": AUS_HUB[0], "hub_name": AUS_HUB[1], "crumb": "Austin Sprinter Van Rental",
        "badge": "\U0001F690 Group Travel \u00b7 Austin",
        "h1_main": "Austin", "h1_em": "Sprinter Van Rental",
        "hero_p": "Chauffeur-driven Mercedes Sprinter van rental in Austin for groups of up to 12. Perfect for corporate roadshows, wine tours, airport groups, and events \u2014 with flat rates, real comfort, and zero surge pricing.",
        "stats": [("4.9\u2605", "Average Rating"), ("12", "Passengers"), ("24/7", "Available"), ("$0", "Surge Fees")],
        "svc_label": "Sprinter Vans", "svc_title": "Keep Your Group Together in Comfort",
        "svc_desc": "One vehicle, one chauffeur, one flat rate \u2014 the easiest way to move a team, a family or a celebration around Austin.",
        "cards": [
            ("\U0001F4BC", "Corporate Roadshows", "Move your team between meetings, sites and the airport on schedule."),
            ("\U0001F377", "Wine & Brewery Tours", "Hill Country and Driftwood tours with a designated chauffeur."),
            ("\u2708\uFE0F", "Airport Groups", "AUS transfers for teams and families with room for every bag."),
            ("\U0001F389", "Group Celebrations", "Bachelor/ette parties, birthdays and nights out for the whole crew."),
            ("\U0001F46A", "Family Travel", "Comfortable, safe group rides with space for luggage and car seats."),
            ("\U0001F4C5", "Events & Conferences", "SXSW, ACL and conference shuttles with flat, pre-booked pricing."),
        ],
        "body": [
            ("Luxury Sprinter Van Rental in Austin", [
                "When you're moving a group, splitting into multiple cars is a headache \u2014 and rideshares rarely keep everyone together. Purple Heart Limo's Austin Sprinter van rental solves that with a chauffeur-driven Mercedes-Benz Sprinter that seats up to 12 in real comfort, with room for luggage, gear and golf clubs.",
                "It's the go-to choice for corporate roadshows, Hill Country wine tours, airport groups, conference shuttles and group celebrations. Your team stays together, your chauffeur handles the route and parking, and you get one transparent flat rate instead of a dozen surge-priced fares.",
            ]),
            ("Built for Austin Groups", [
                '<ul><li><strong>Corporate</strong> \u2014 roadshows, client tours and team airport runs (see <a href="/austin-corporate-car-service/">corporate car service</a>)</li><li><strong>Wine tours</strong> \u2014 Driftwood, Dripping Springs and Hill Country wineries</li><li><strong>Airport groups</strong> \u2014 <a href="/austin-airport-limo/">AUS transfers</a> with luggage space</li><li><strong>Celebrations</strong> \u2014 bachelor/ette parties, birthdays and reunions</li></ul>',
            ]),
            ("Comfortable, Professional, On Time", [
                "Our Sprinters are clean, climate-controlled and driven by professional chauffeurs \u2014 not a self-drive rental you have to navigate and park yourself. Book by the hour or for a full day, and we'll tailor the route to your itinerary.",
            ]),
        ],
        "form_title": "Book an Austin Sprinter Van", "form_btn": "Request Sprinter Van Quote",
        "service_opts": ["Corporate / Roadshow", "Wine Tour", "Airport Group Transfer", "Group Celebration", "Conference Shuttle", "Other"],
        "vehicle_opts": ["Executive Sprinter (up to 12)", "Party Bus", "Luxury SUV", "Stretch Limousine"],
        "pickup_ph": "123 Main St, Austin TX or AUS Airport", "city_val": "Austin TX",
        "why_title": "Austin's Texan-Owned Group Travel", "why": STD_WHY,
        "faq_title": "Austin Sprinter Van Rental FAQ",
        "faqs": [
            ("How many passengers fit in your Sprinter vans?", "Our executive Mercedes Sprinter vans seat up to 12 passengers comfortably, with dedicated space for luggage and gear."),
            ("Does the Sprinter come with a chauffeur?", "Yes. Every Sprinter van rental is chauffeur-driven by a professional, background-checked driver \u2014 it is not a self-drive rental."),
            ("Can I use a Sprinter for an Austin wine tour?", "Definitely. Hill Country and Driftwood wine tours are one of the most popular uses for our Sprinter vans \u2014 everyone rides together with a designated driver."),
            ("Do you offer Sprinter airport transfers?", "Yes \u2014 we provide AUS airport group transfers with plenty of room for passengers and luggage, at a flat rate with no surge."),
        ],
        "related": rel(austin_related, "/austin-sprinter-van-rental/"),
    })

    # 7. Austin Corporate Car Service (supports corporate/exec + transportation services austin)
    pages.append({
        "slug": "austin-corporate-car-service",
        "title": "Austin Corporate Car Service | Executive Transportation | Purple Heart Limo",
        "meta": "Corporate car & executive transportation in Austin, TX. Client pickups, roadshows, airport travel & corporate accounts. Flat rates, billing, 24/7. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 Austin Corporate Car Service",
        "image": "luxsuv-escalade.webp",
        "areas": AUSTIN_AREAS, "locality": "Austin", "reviews": 214,
        "hub_slug": AUS_HUB[0], "hub_name": AUS_HUB[1], "crumb": "Austin Corporate Car Service",
        "badge": "\U0001F4BC Corporate \u00b7 Austin",
        "h1_main": "Austin Corporate", "h1_em": "Car Service",
        "hero_p": "Executive corporate transportation in Austin \u2014 client pickups, roadshows, conferences and airport travel with professional chauffeurs, corporate accounts and consolidated billing. Flat rates, on-time, 24/7.",
        "stats": [("4.9\u2605", "Average Rating"), ("214+", "Austin Reviews"), ("24/7", "Available"), ("$0", "Surge Fees")],
        "svc_label": "Corporate Travel", "svc_title": "Executive Transportation for Austin Business",
        "svc_desc": "Impress clients, keep your team on schedule and simplify expense reporting with a dedicated corporate car service.",
        "cards": [
            ("\U0001F91D", "Client Pickups", "Make a polished first impression with executive sedans and SUVs."),
            ("\U0001F5FA\uFE0F", "Roadshows", "Multi-stop, multi-day itineraries handled by one reliable provider."),
            ("\u2708\uFE0F", "Airport Travel", "Flight-monitored AUS transfers for executives and visiting teams."),
            ("\U0001F3DB\uFE0F", "Conferences", "Group shuttles and on-call cars for offsites and conventions."),
            ("\U0001F4C4", "Corporate Accounts", "Consolidated billing, priority booking and account management."),
            ("\U0001F507", "Discreet Service", "Quiet, professional rides where you can work or take calls."),
        ],
        "body": [
            ("Corporate & Executive Car Service in Austin", [
                "Business travel runs on reliability. Purple Heart Limo's Austin corporate car service gives companies a single, dependable transportation partner for client pickups, executive travel, roadshows, conferences and airport runs \u2014 with professional chauffeurs, immaculate vehicles and flat-rate pricing that makes budgeting simple.",
                "We set up corporate accounts with consolidated billing and priority booking, so your assistants and travelers can reserve in seconds and your finance team gets clean, itemized invoices. Whether it's a single VIP client pickup or a week-long roadshow across the Austin tech corridor, we handle the logistics so your team stays focused.",
            ]),
            ("Designed for Austin Companies", [
                '<ul><li><strong>Client &amp; VIP transport</strong> \u2014 executive sedans and SUVs</li><li><strong>Roadshows</strong> \u2014 multi-stop itineraries with the same chauffeur</li><li><strong>Airport travel</strong> \u2014 flight-monitored <a href="/austin-airport-limo/">AUS transfers</a></li><li><strong>Group offsites</strong> \u2014 <a href="/austin-sprinter-van-rental/">Sprinter van</a> shuttles for teams</li></ul>',
            ]),
            ("Corporate Accounts & Billing", [
                "Set up a corporate account for priority access, negotiated flat rates and consolidated monthly billing. Need a dedicated driver for the day? Our <a href=\"/austin-chauffeur-service/\">chauffeur service</a> keeps a car on call for back-to-back meetings.",
            ]),
        ],
        "form_title": "Book Austin Corporate Transport", "form_btn": "Request Corporate Service",
        "service_opts": ["Client / VIP Pickup", "Executive Roadshow", "Corporate Airport Travel", "Conference / Offsite", "Open Corporate Account", "Other"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Executive Sprinter", "Stretch Limousine"],
        "pickup_ph": "Office address, Austin TX or AUS Airport", "city_val": "Austin TX",
        "why_title": "Austin's Texan-Owned Corporate Choice", "why": STD_WHY,
        "faq_title": "Austin Corporate Car Service FAQ",
        "faqs": [
            ("Do you offer corporate accounts with monthly billing?", "Yes. We set up corporate accounts with priority booking, negotiated flat rates and consolidated, itemized monthly invoices for easy expense reporting."),
            ("Can you handle multi-day executive roadshows?", "Absolutely. We coordinate multi-stop, multi-day roadshows across the Austin metro \u2014 often with the same dedicated chauffeur throughout."),
            ("What vehicles are available for corporate travel?", "Executive sedans and luxury SUVs for individuals and VIPs, and executive Sprinter vans for teams and group transfers."),
            ("Do you provide corporate airport transfers?", "Yes \u2014 flight-monitored, flat-rate transfers to and from Austin-Bergstrom (AUS) for executives and visiting teams, available 24/7."),
        ],
        "related": rel(austin_related, "/austin-corporate-car-service/"),
    })

    # ---------------- DALLAS ----------------

    # 8. Dallas Corporate / Executive Car Service
    pages.append({
        "slug": "dallas-corporate-car-service",
        "title": "Dallas Corporate & Executive Car Service | Purple Heart Limo",
        "meta": "Executive & corporate car service in Dallas, TX. Client pickups, roadshows, DFW & Love Field airport travel, corporate accounts. Flat rates, 24/7. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 Dallas Corporate Car Service",
        "image": "luxsuv-escalade.webp",
        "areas": DALLAS_AREAS, "locality": "Dallas", "reviews": 188,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "Dallas Corporate Car Service",
        "badge": "\U0001F4BC Corporate \u00b7 Dallas-Fort Worth",
        "h1_main": "Dallas Corporate", "h1_em": "Car Service",
        "hero_p": "Executive corporate transportation across Dallas-Fort Worth \u2014 client pickups, roadshows, conferences and airport travel with professional chauffeurs, corporate accounts and consolidated billing. Flat rates, on-time, 24/7.",
        "stats": [("4.9\u2605", "Average Rating"), ("188+", "Dallas Reviews"), ("24/7", "Available"), ("$0", "Surge Fees")],
        "svc_label": "Corporate Travel", "svc_title": "Executive Transportation for DFW Business",
        "svc_desc": "From Uptown boardrooms to Las Colinas and the airport, give your executives and clients a polished, reliable ride.",
        "cards": [
            ("\U0001F91D", "Client Pickups", "Executive sedans and SUVs that make the right first impression."),
            ("\U0001F5FA\uFE0F", "Roadshows", "Multi-stop DFW itineraries handled by one dependable provider."),
            ("\u2708\uFE0F", "Airport Travel", "Flight-monitored DFW and Love Field transfers for your team."),
            ("\U0001F3DB\uFE0F", "Conventions", "Group transport for events at KBHCCD and Las Colinas."),
            ("\U0001F4C4", "Corporate Accounts", "Consolidated billing, priority booking and account management."),
            ("\U0001F507", "Discreet Service", "Quiet, professional rides where executives can work en route."),
        ],
        "body": [
            ("Corporate & Executive Car Service in Dallas-Fort Worth", [
                "Dallas runs on business, and business runs on being on time. Purple Heart Limo's Dallas corporate car service gives companies across DFW a single, reliable transportation partner for client pickups, executive travel, roadshows, conventions and airport runs \u2014 with professional chauffeurs, spotless vehicles and flat-rate pricing that keeps budgets predictable.",
                "We serve Uptown, Downtown, Las Colinas, Plano, Frisco and the wider Metroplex, with corporate accounts that include consolidated billing and priority booking. From a single VIP client pickup to a multi-day roadshow, we handle the routing, the parking and the timing so your team can focus on the deal.",
            ]),
            ("Built for DFW Companies", [
                '<ul><li><strong>Client &amp; VIP transport</strong> \u2014 executive sedans and SUVs</li><li><strong>Roadshows</strong> \u2014 multi-stop itineraries with a consistent chauffeur</li><li><strong>Airport travel</strong> \u2014 <a href="/dfw-airport-car-service/">DFW</a> and <a href="/car-service-dallas-love-field/">Love Field</a> transfers</li><li><strong>Group offsites</strong> \u2014 Sprinter shuttles for teams and conventions</li></ul>',
            ]),
            ("Corporate Accounts & Billing", [
                "Open a corporate account for negotiated flat rates, priority access and consolidated monthly invoices. We make business travel across the Metroplex effortless \u2014 explore all our <a href=\"/limo-service-dallas-tx/\">Dallas limo services</a>.",
            ]),
        ],
        "form_title": "Book Dallas Corporate Transport", "form_btn": "Request Corporate Service",
        "service_opts": ["Client / VIP Pickup", "Executive Roadshow", "DFW Airport Travel", "Love Field Travel", "Convention / Offsite", "Open Corporate Account", "Other"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Executive Sprinter", "Stretch Limousine"],
        "pickup_ph": "Office address, Dallas TX or DFW Airport", "city_val": "Dallas TX",
        "why_title": "DFW's Texan-Owned Corporate Choice", "why": STD_WHY,
        "faq_title": "Dallas Corporate Car Service FAQ",
        "faqs": [
            ("Do you offer corporate accounts in Dallas?", "Yes. We set up corporate accounts across DFW with priority booking, negotiated flat rates and consolidated, itemized monthly billing for simple expense reporting."),
            ("Do you serve both DFW and Dallas Love Field?", "We do \u2014 flight-monitored executive transfers to and from both DFW International and Dallas Love Field (DAL), 24/7."),
            ("Can you cover multi-day roadshows across the Metroplex?", "Absolutely. We coordinate multi-stop, multi-day executive roadshows across Dallas, Fort Worth, Plano, Frisco, Irving and Las Colinas."),
            ("What areas of Dallas-Fort Worth do you serve?", "The entire Metroplex \u2014 Dallas, Fort Worth, Plano, Frisco, Irving, Las Colinas, Arlington, University Park and Highland Park."),
        ],
        "related": rel(dallas_related, "/dallas-corporate-car-service/"),
    })

    # 9. Car Service Dallas Love Field (DAL)
    pages.append({
        "slug": "car-service-dallas-love-field",
        "title": "Car Service Dallas Love Field (DAL) | Flat-Rate Black Car | Purple Heart Limo",
        "meta": "Car service to & from Dallas Love Field (DAL). Flight-monitored black car & SUV, meet & greet, flat rates, 24/7. Perfect for Southwest travelers. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 Car Service Dallas Love Field",
        "image": "sedan-cadillac.webp",
        "areas": DALLAS_AREAS, "locality": "Dallas", "reviews": 188,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "Dallas Love Field Car Service",
        "badge": "\u2708\uFE0F Dallas Love Field (DAL)",
        "h1_main": "Car Service", "h1_em": "Dallas Love Field",
        "hero_p": "Flight-monitored car service to and from Dallas Love Field (DAL) \u2014 meet-and-greet black car and SUV pickups, flat rates with zero surge, and chauffeurs who track your flight. Ideal for Southwest Airlines travelers and busy professionals.",
        "stats": [("4.9\u2605", "Average Rating"), ("DAL", "Airport Served"), ("24/7", "Available"), ("$0", "Surge Fees")],
        "svc_label": "Love Field Transfers", "svc_title": "Smooth Rides To & From DAL",
        "svc_desc": "Skip the parking and the rideshare scramble at Love Field \u2014 your chauffeur is tracking your flight and ready when you land.",
        "cards": [
            ("\U0001F6EC", "Arrivals Meet & Greet", "Your chauffeur tracks your flight and meets you inside the terminal."),
            ("\U0001F6EB", "On-Time Departures", "Early pickups that beat Dallas traffic to DAL."),
            ("\U0001F4BC", "Corporate Love Field", "Executive sedans and SUVs for business travelers."),
            ("\U0001F46A", "Family & Groups", "Roomy SUVs and Sprinters with space for luggage."),
            ("\U0001F4F1", "Flight Monitoring", "Delays and early landings handled automatically, no extra fees."),
            ("\U0001F4B5", "Flat DAL Rates", "One fixed price to Love Field, quoted up front, no surge."),
        ],
        "body": [
            ("Dallas Love Field (DAL) Car Service", [
                "Dallas Love Field is fast, close to downtown, and the home of Southwest Airlines \u2014 but parking and rideshare pickups can still turn a quick trip into a hassle. Purple Heart Limo's Dallas Love Field car service gives you a flight-monitored, flat-rate black car or SUV with a professional chauffeur who's ready the moment you land at DAL.",
                "For arrivals, we offer meet-and-greet service \u2014 your chauffeur greets you, helps with luggage and walks you to the vehicle. For departures, we arrive early and beat the traffic so you reach your gate relaxed. It's the stress-free way to fly out of Love Field.",
            ]),
            ("Love Field Transfers Across DFW", [
                "We provide flat-rate DAL transfers from anywhere in the Metroplex \u2014 Uptown, Downtown, Las Colinas, Plano, Frisco and beyond. Flying out of the other airport instead? See our <a href=\"/dfw-airport-car-service/\">DFW Airport car service</a>. Traveling for work? Pair it with our <a href=\"/dallas-corporate-car-service/\">Dallas corporate car service</a>.",
            ]),
            ("Perfect for Southwest Travelers", [
                "Because Love Field is Southwest's hub, many of our DAL clients are frequent flyers who value speed and consistency. We track your inbound flight, adjust for delays automatically, and never add surge pricing \u2014 so your airport ride is one less thing to think about.",
            ]),
        ],
        "form_title": "Book Love Field Car Service", "form_btn": "Request DAL Airport Transfer",
        "service_opts": ["Love Field Arrival (DAL)", "Love Field Departure (DAL)", "Round-Trip Airport", "Corporate Airport Travel", "Group / Family Airport", "Other"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Executive Sprinter", "Stretch Limousine"],
        "pickup_ph": "Dallas Love Field (DAL) or 123 Main St, Dallas TX", "city_val": "Dallas TX",
        "why_title": "DFW's Texan-Owned Airport Choice", "why": STD_WHY,
        "faq_title": "Dallas Love Field Car Service FAQ",
        "faqs": [
            ("Do you track my flight into Dallas Love Field?", "Yes \u2014 every DAL pickup is matched to your live flight status, so your chauffeur adjusts to early or delayed arrivals at no extra charge."),
            ("Where do you meet me at Love Field (DAL)?", "We offer meet-and-greet service for arrivals \u2014 your chauffeur meets you inside the terminal and helps with luggage. Curbside pickup is also available."),
            ("How much is car service to Dallas Love Field?", "Love Field transfers are flat-rate and quoted up front based on your location and vehicle, with no surge pricing. Call (833) 740-0700 for your fare."),
            ("Do you serve early-morning Southwest departures?", "Yes \u2014 our Love Field car service runs 24/7, including pre-dawn departures and late-night arrivals."),
        ],
        "related": rel(dallas_related, "/car-service-dallas-love-field/"),
    })

    # 10. DFW Airport Car Service
    pages.append({
        "slug": "dfw-airport-car-service",
        "title": "DFW Airport Car Service | Dallas Airport Limo & Shuttle | Purple Heart Limo",
        "meta": "DFW Airport car service & limo \u2014 flight-monitored black car, SUV & Sprinter transfers to/from Dallas Fort Worth International. Meet & greet, flat rates, 24/7. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 DFW Airport Car Service",
        "image": "luxsuv-escalade.webp",
        "areas": DALLAS_AREAS, "locality": "Dallas", "reviews": 188,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "DFW Airport Car Service",
        "badge": "\u2708\uFE0F DFW International Airport",
        "h1_main": "DFW Airport", "h1_em": "Car Service",
        "hero_p": "Flight-monitored car service and airport transportation to and from Dallas Fort Worth International Airport (DFW). Meet-and-greet pickups, flat rates with no surge, and sedans, SUVs and Sprinters for every group size. Available 24/7.",
        "stats": [("4.9\u2605", "Average Rating"), ("DFW", "Airport Served"), ("24/7", "Available"), ("$0", "Surge Fees")],
        "svc_label": "DFW Airport Transfers", "svc_title": "Reliable Rides To & From DFW",
        "svc_desc": "DFW is huge \u2014 your ride shouldn't be complicated. We handle the terminals, the timing and the traffic.",
        "cards": [
            ("\U0001F6EC", "Arrivals Meet & Greet", "Your chauffeur tracks your flight and meets you at your terminal."),
            ("\U0001F6EB", "On-Time Departures", "Early, monitored pickups so you stay ahead of DFW traffic."),
            ("\U0001F4BC", "Corporate DFW Travel", "Executive sedans and SUVs for business travelers and teams."),
            ("\U0001F46A", "Family & Groups", "Sprinter vans with space for luggage, car seats and the crew."),
            ("\U0001F4F1", "Flight Monitoring", "Delays and early landings handled automatically, no surprises."),
            ("\U0001F4B5", "Flat DFW Rates", "One fixed price to DFW, quoted up front, no surge ever."),
        ],
        "body": [
            ("DFW International Airport Car Service", [
                "Dallas Fort Worth International is one of the busiest airports in the world, with five terminals spread across thousands of acres \u2014 not the place you want to be circling for a rideshare. Purple Heart Limo's DFW airport car service gives you a flight-monitored, flat-rate ride with a professional chauffeur who knows exactly which terminal and door to meet you at.",
                "Arriving travelers get meet-and-greet service and luggage help; departing travelers get early, traffic-aware pickups that keep them ahead of schedule. Whether you need a single executive sedan or a Sprinter for a whole team, we make DFW simple.",
            ]),
            ("DFW Transfers Across the Metroplex", [
                "We serve the entire Dallas-Fort Worth area \u2014 Downtown, Uptown, Las Colinas, Plano, Frisco, Arlington and Fort Worth. Flying Southwest out of the close-in airport instead? See our <a href=\"/car-service-dallas-love-field/\">Dallas Love Field car service</a>. Need it for business? Our <a href=\"/dallas-corporate-car-service/\">corporate car service</a> adds accounts and billing.",
            ]),
            ("Choose the Right Vehicle for DFW", [
                "Solo travelers and couples ride comfortably in an executive sedan; small groups and luggage-heavy trips suit a luxury SUV; teams, families and tour groups fit our executive Sprinter for up to 12. Every option is flat-rate and flight-monitored.",
            ]),
        ],
        "form_title": "Book DFW Airport Car Service", "form_btn": "Request DFW Airport Transfer",
        "service_opts": ["DFW Airport Arrival", "DFW Airport Departure", "Round-Trip Airport", "Corporate Airport Travel", "Group / Family Airport", "Other"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Executive Sprinter", "Stretch Limousine"],
        "pickup_ph": "DFW Airport or 123 Main St, Dallas TX", "city_val": "Dallas TX",
        "why_title": "DFW's Texan-Owned Airport Choice", "why": STD_WHY,
        "faq_title": "DFW Airport Car Service FAQ",
        "faqs": [
            ("Do you monitor flights into DFW?", "Yes. Every DFW pickup is matched to your live flight status, so your chauffeur adjusts to early or delayed arrivals automatically, with no extra charge."),
            ("Will my chauffeur meet me inside the DFW terminal?", "For arrivals we offer meet-and-greet service \u2014 your chauffeur meets you at your terminal and helps with luggage. Curbside pickup is also available on request."),
            ("How much does a car to DFW airport cost?", "DFW transfers are flat-rate and quoted up front based on your pickup location and vehicle. There is never surge pricing. Call (833) 740-0700 for a quote."),
            ("Can you transport a group to DFW?", "Yes \u2014 our executive Sprinter vans seat up to 12 with room for luggage, ideal for teams, families and tour groups heading to DFW."),
        ],
        "related": rel(dallas_related, "/dfw-airport-car-service/"),
    })

    # 11. Dallas Wedding Transportation
    pages.append({
        "slug": "dallas-wedding-transportation",
        "title": "Dallas Wedding Transportation | Bridal Party Limos & Shuttles | Purple Heart Limo",
        "meta": "Dallas wedding transportation \u2014 stretch limos, SUVs & Sprinter shuttles for the couple, bridal party & guests across DFW. Flat rates, on-time, 24/7. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 Dallas Wedding Transportation",
        "image": "stretch-limo.webp",
        "areas": DALLAS_AREAS, "locality": "Dallas", "reviews": 188,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "Dallas Wedding Transportation",
        "badge": "\U0001F48D Weddings \u00b7 Dallas-Fort Worth",
        "h1_main": "Dallas Wedding", "h1_em": "Transportation",
        "hero_p": "Elegant wedding transportation across Dallas-Fort Worth \u2014 stretch limousines for the couple, SUVs for the bridal party, and Sprinter shuttles for your guests. Flat rates and a chauffeur who keeps your timeline flawless.",
        "stats": [("4.9\u2605", "Average Rating"), ("188+", "Dallas Reviews"), ("100%", "On-Time"), ("$0", "Surge Fees")],
        "svc_label": "Wedding Transportation", "svc_title": "Transportation That Makes the Day Effortless",
        "svc_desc": "From the ceremony to the reception to the send-off, we coordinate every transfer so you and your guests arrive on time.",
        "cards": [
            ("\U0001F48D", "Couple's Limo", "A stunning stretch limousine for the newlyweds' entrance and exit."),
            ("\U0001F470", "Bridal Party", "Luxury SUVs and Sprinters keep the wedding party together."),
            ("\U0001F3F0", "Venue Transfers", "Reliable rides between ceremony, photos and reception venues."),
            ("\U0001F68C", "Guest Shuttles", "Sprinter shuttles between hotels and your venues."),
            ("\U0001F4C5", "Full-Day Packages", "Multi-vehicle coordination for the entire celebration."),
            ("\u2708\uFE0F", "Out-of-Town Guests", "DFW and Love Field airport transfers for arriving guests."),
        ],
        "body": [
            ("Dallas-Fort Worth Wedding Transportation", [
                "A wedding is a tightly choreographed day, and transportation keeps it on beat. Purple Heart Limo provides elegant, dependable wedding transportation across Dallas-Fort Worth \u2014 a head-turning stretch limousine for the couple, comfortable SUVs for the bridal party, and Sprinter shuttles that keep your guests moving between hotels, the ceremony and the reception.",
                "We serve venues across the Metroplex, from Uptown and Downtown Dallas to Fort Worth, Plano, Frisco and the surrounding countryside. Your chauffeur arrives early, dresses for the occasion, and follows a timeline built around your day so no one is ever left waiting.",
            ]),
            ("Wedding Packages Built Around You", [
                "We tailor the vehicles and schedule to your celebration:",
                '<ul><li>Couple\u2019s stretch limousine for the exit and photos</li><li>Bridal-party SUVs and Sprinter vans</li><li>Guest shuttles between hotels and venues</li><li><a href="/dfw-airport-car-service/">DFW</a> and <a href="/car-service-dallas-love-field/">Love Field</a> transfers for out-of-town guests</li></ul>',
            ]),
            ("Why Dallas Couples Choose Purple Heart", [
                "Veteran-owned and detail-driven, we treat your wedding timeline like a mission. Flat rates mean no surprise charges on your big day, and we coordinate directly with your planner. Explore more <a href=\"/limo-service-dallas-tx/\">Dallas limo services</a>.",
            ]),
        ],
        "form_title": "Book Dallas Wedding Transportation", "form_btn": "Request Wedding Quote",
        "service_opts": ["Couple's Wedding Limo", "Bridal Party Transport", "Guest Shuttle", "Full Wedding Package", "Engagement / Rehearsal", "Other"],
        "vehicle_opts": ["Stretch Limousine", "Luxury SUV", "Executive Sprinter", "Party Bus", "Executive Sedan"],
        "pickup_ph": "Hotel or venue, Dallas-Fort Worth TX", "city_val": "Dallas TX",
        "why_title": "DFW's Texan-Owned Wedding Choice", "why": STD_WHY,
        "faq_title": "Dallas Wedding Transportation FAQ",
        "faqs": [
            ("Do you cover wedding venues across Dallas-Fort Worth?", "Yes \u2014 we serve venues throughout the Metroplex, including Dallas, Fort Worth, Plano, Frisco, Irving and surrounding areas."),
            ("Can you transport the bridal party and guests together?", "Absolutely. We combine stretch limos, luxury SUVs and Sprinter shuttles to move the couple, the wedding party and guests on one coordinated timeline."),
            ("Do you offer full-day wedding packages?", "We do \u2014 full-day packages cover multiple vehicles, multiple stops and direct coordination with your planner so every transfer runs on schedule."),
            ("How far ahead should we book?", "Popular wedding dates book early, especially in spring and fall. Reserve as soon as your date is set \u2014 call (833) 740-0700 to check availability."),
        ],
        "related": rel(dallas_related, "/dallas-wedding-transportation/"),
    })

    # 12. Dallas Party Bus & Holiday Lights Tours
    pages.append({
        "slug": "dallas-party-bus",
        "title": "Dallas Party Bus Rental | Christmas Lights Tours & Group Fun | Purple Heart Limo",
        "meta": "Dallas party bus rental for birthdays, bachelorette parties, nights out & Christmas lights tours. Group-ready, flat rates, professional chauffeur, 24/7. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 Dallas Party Bus Rental",
        "image": "partybus-ford.webp",
        "areas": DALLAS_AREAS, "locality": "Dallas", "reviews": 188,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "Dallas Party Bus",
        "badge": "\U0001F389 Party Bus \u00b7 Dallas-Fort Worth",
        "h1_main": "Dallas Party Bus", "h1_em": "& Holiday Lights Tours",
        "hero_p": "Rent a party bus in Dallas for birthdays, bachelorette parties, nights out and festive Christmas lights tours. Keep your whole group together with a professional chauffeur, flat-rate pricing and zero surge \u2014 the party starts the moment you step on board.",
        "stats": [("4.9\u2605", "Average Rating"), ("188+", "Dallas Reviews"), ("Groups", "Welcome"), ("$0", "Surge Fees")],
        "svc_label": "Party Bus & Tours", "svc_title": "Group Celebrations On Wheels",
        "svc_desc": "One bus, one chauffeur, one flat rate \u2014 the easiest way to keep the whole crew together and the night going.",
        "cards": [
            ("\U0001F384", "Christmas Lights Tours", "Tour DFW's best holiday light displays in warm, festive comfort."),
            ("\U0001F389", "Birthdays", "Celebrate milestone birthdays with the whole group on board."),
            ("\U0001F478", "Bachelorette & Bachelor", "Hit multiple venues without splitting up or finding parking."),
            ("\U0001F37E", "Nights Out", "Deep Ellum, Uptown and Fort Worth bar crawls, safely."),
            ("\U0001F3C8", "Game Day & Concerts", "Group transport to Cowboys, Rangers, Mavs and big shows."),
            ("\U0001F46A", "Group Outings", "Reunions, corporate parties and special celebrations."),
        ],
        "body": [
            ("Dallas Party Bus Rental", [
                "When the whole group is celebrating, splitting into separate cars kills the vibe \u2014 and finding parking kills the night. Purple Heart Limo's Dallas party bus rental keeps everyone together with a professional chauffeur handling the driving, so you can focus on the fun. It's perfect for birthdays, bachelorette and bachelor parties, nights out, game days and group celebrations across Dallas-Fort Worth.",
                "Every party bus rental comes with flat-rate pricing \u2014 no surge, no surprises \u2014 and a vetted, professional chauffeur. Book by the hour and build the night around your itinerary, hitting as many stops as you like without anyone worrying about driving.",
            ]),
            ("DFW Christmas Lights Tours", [
                "Around the holidays, our most-requested party bus experience is the Dallas Christmas lights tour. Gather your family or friends and we'll drive you through the Metroplex's most spectacular light displays \u2014 from neighborhood favorites to the big seasonal attractions \u2014 all in warm, festive comfort. It's a stress-free holiday tradition with no driving, no parking and no cold walks between stops.",
            ]),
            ("Great for Every Group Occasion", [
                '<ul><li><strong>Birthdays &amp; milestone celebrations</strong></li><li><strong>Bachelorette &amp; bachelor parties</strong> \u2014 multi-venue nights</li><li><strong>Holiday lights tours</strong> across DFW</li><li><strong>Game days &amp; concerts</strong> \u2014 Cowboys, Rangers, Mavs and more</li></ul>',
                "Planning a wedding or corporate event instead? See our <a href=\"/dallas-wedding-transportation/\">Dallas wedding transportation</a> and <a href=\"/dallas-corporate-car-service/\">corporate car service</a>.",
            ]),
        ],
        "form_title": "Book a Dallas Party Bus", "form_btn": "Request Party Bus Quote",
        "service_opts": ["Christmas Lights Tour", "Birthday Party", "Bachelorette / Bachelor", "Night Out / Bar Crawl", "Game Day / Concert", "Group Outing", "Other"],
        "vehicle_opts": ["Party Bus", "Executive Sprinter", "Stretch Limousine", "Stretch SUV Limo"],
        "pickup_ph": "123 Main St, Dallas TX", "city_val": "Dallas TX",
        "why_title": "DFW's Texan-Owned Party Choice", "why": STD_WHY,
        "faq_title": "Dallas Party Bus FAQ",
        "faqs": [
            ("How much does a party bus cost in Dallas?", "Party bus rentals are booked by the hour and quoted as one flat, all-in rate based on the date, duration and group size, with no surge pricing. Call (833) 740-0700 for a quote."),
            ("Do you offer Christmas lights tours by party bus?", "Yes \u2014 festive DFW Christmas lights tours are one of our most popular seasonal party bus experiences, with a chauffeur guiding you to the best displays."),
            ("How many people fit on the party bus?", "Our party-ready vehicles accommodate groups comfortably; tell us your headcount and we'll match you to the right vehicle, from a large Sprinter to a party bus."),
            ("Can we make multiple stops during the night?", "Absolutely \u2014 book by the hour and your chauffeur will take your group to as many venues or light displays as your itinerary allows."),
        ],
        "related": rel(dallas_related, "/dallas-party-bus/"),
    })

    return pages
