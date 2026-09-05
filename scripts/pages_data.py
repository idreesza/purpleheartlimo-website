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
        ("/prom-limo-rental-dallas-tx/", "Dallas Prom Limo"),
        ("/limo-service-addison-tx/", "Addison Limo Service"),
        ("/limo-service-dallas-tx/", "Dallas Limo Service"),
    ]
    dallas_cities = [
        ("/car-service-arlington-tx/", "Arlington Car Service"),
        ("/car-service-plano-tx/", "Plano Car Service"),
        ("/car-service-frisco-tx/", "Frisco Car Service"),
        ("/car-service-irving-tx/", "Irving Car Service"),
        ("/car-service-mckinney-tx/", "McKinney Car Service"),
        ("/limo-service-fort-worth-tx/", "Fort Worth Limo Service"),
        ("/limo-service-university-park-tx/", "University Park Limo Service"),
        ("/limo-service-highland-park-tx/", "Highland Park Limo Service"),
        ("/limo-service-dallas-tx/", "Dallas Limo Service"),
        ("/dfw-airport-car-service/", "DFW Airport Car Service"),
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
                "We provide flat-rate DAL transfers from anywhere in the Metroplex \u2014 Uptown, Downtown, Las Colinas, Plano, Frisco and beyond. Whether you search for DAL car service or Dallas Love Field car service, you get the same thing: a flight-tracked, flat-rate ride that's on time. Flying out of the other airport instead? See our <a href=\"/dfw-airport-car-service/\">DFW Airport car service</a>. Traveling for work? Pair it with our <a href=\"/dallas-corporate-car-service/\">Dallas corporate car service</a>.",
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
                "We serve the entire Dallas-Fort Worth area \u2014 Downtown, Uptown, Las Colinas, Plano, Frisco, Arlington and Fort Worth. Think of us as a private airport shuttle service in Dallas, TX: door-to-door, on your schedule, with no shared stops or waiting. Flying Southwest out of the close-in airport instead? See our <a href=\"/car-service-dallas-love-field/\">Dallas Love Field car service</a>. Need it for business? Our <a href=\"/dallas-corporate-car-service/\">corporate car service</a> adds accounts and billing.",
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
        "hero_p": "Elegant wedding transportation in Dallas, TX and across Dallas-Fort Worth \u2014 stretch limousines for the couple, SUVs for the bridal party, and Sprinter shuttles for your guests. Flat rates and a chauffeur who keeps your timeline flawless.",
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

    # ---------------- DALLAS-AREA CITIES ----------------

    # 13. Car Service Arlington TX
    pages.append({
        "slug": "car-service-arlington-tx",
        "title": "Car Service Arlington TX | Cowboys & Rangers Game Day, Airport | Purple Heart Limo",
        "meta": "Car service in Arlington, TX \u2014 black car & limo for AT&T Stadium, Globe Life Field, Six Flags, DFW airport & corporate travel. Flat rates, no surge, 24/7. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 Car Service Arlington TX",
        "image": "luxsuv-escalade.webp",
        "areas": ["Arlington", "Grand Prairie", "Mansfield", "Dallas", "Fort Worth", "Irving"],
        "locality": "Arlington", "reviews": 96,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "Arlington Car Service",
        "badge": "\U0001F3C8 Entertainment District \u00b7 Arlington, TX",
        "h1_main": "Car Service", "h1_em": "Arlington, TX",
        "hero_p": "Professional car service in Arlington, TX \u2014 flat-rate black car, SUV and limo rides for AT&T Stadium game days, Globe Life Field, Six Flags, concerts at Texas Live!, DFW airport transfers and corporate travel. A chauffeur who knows the Entertainment District, with zero surge pricing, 24/7.",
        "stats": [("4.9\u2605", "Average Rating"), ("DFW", "Airport Served"), ("24/7", "Available"), ("$0", "Surge Fees")],
        "svc_label": "Arlington Car Service", "svc_title": "Rides for Every Arlington Occasion",
        "svc_desc": "From a Cowboys kickoff to a 6 a.m. flight, our Arlington car service gets your group there on time and stress-free.",
        "cards": [
            ("\U0001F3C8", "Cowboys Game Day", "Drop-off and pickup at AT&T Stadium \u2014 no parking, no tailgate hassle."),
            ("\u26BE", "Rangers at Globe Life", "Flat-rate rides to Globe Life Field and Texas Live! after the game."),
            ("\U0001F3A2", "Six Flags & Family", "Roomy SUVs and Sprinters for Six Flags and Hurricane Harbor trips."),
            ("\u2708\uFE0F", "DFW Airport Transfers", "Flight-monitored airport car service from anywhere in Arlington."),
            ("\U0001F4BC", "Corporate Travel", "Executive sedans for meetings across the Mid-Cities and Metroplex."),
            ("\U0001F37E", "Concerts & Nights Out", "Group transport to big shows and Arlington's bars and venues."),
        ],
        "body": [
            ("Arlington's Texan-Owned Car Service", [
                "Arlington sits right in the middle of the Metroplex, halfway between Dallas and Fort Worth, and it's the beating heart of Texas sports and entertainment \u2014 AT&T Stadium, Globe Life Field, Texas Live!, Six Flags Over Texas and Hurricane Harbor. On game days and concert nights, parking is brutal and rideshare surges hard. Purple Heart Limo's Arlington car service skips all of that with a flat-rate, chauffeur-driven ride that drops you at the gate and picks you up when it's over.",
                "We're a veteran-owned team that treats your schedule like a mission. Whether it's a Cowboys home game, a Rangers playoff push, a family day at Six Flags or an early flight out of DFW, your chauffeur arrives early, tracks traffic and gets your whole group there together.",
            ]),
            ("Game Day & Event Transportation", [
                "Tailgating and driving don't mix \u2014 let us handle the wheel. We provide door-to-gate transportation to AT&T Stadium and Globe Life Field, then pick you up at a set meeting point so you never wait in the post-game crush. Book by the hour and we'll add stops at Texas Live!, dinner or a hotel.",
                "Need a bigger ride? Our luxury SUVs, executive Sprinters and party buses keep groups of friends, families or corporate suites together for the whole event.",
            ]),
            ("DFW Airport & Corporate Trips From Arlington", [
                "Because Arlington is minutes from DFW International, we're a popular choice for flight-monitored <a href=\"/dfw-airport-car-service/\">DFW airport car service</a> and executive travel. Pair it with our <a href=\"/dallas-corporate-car-service/\">Dallas corporate car service</a> for account billing, or explore all our <a href=\"/limo-service-dallas-tx/\">Dallas-Fort Worth limo services</a>.",
            ]),
        ],
        "form_title": "Book Arlington Car Service", "form_btn": "Request Arlington Car Service",
        "service_opts": ["Cowboys / AT&T Stadium", "Rangers / Globe Life Field", "Concert / Event", "DFW Airport Transfer", "Corporate / Executive", "Six Flags / Family", "Other"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Executive Sprinter", "Stretch Limousine", "Party Bus"],
        "pickup_ph": "123 Main St, Arlington TX or AT&T Stadium", "city_val": "Arlington TX",
        "why_title": "Arlington's Texan-Owned Choice", "why": STD_WHY,
        "faq_title": "Arlington Car Service FAQ",
        "faqs": [
            ("How much is car service in Arlington, TX?", "We quote a flat rate up front based on your pickup, destination and vehicle \u2014 no surge pricing, even on game days. Call (833) 740-0700 for an exact fare."),
            ("Do you provide rides to AT&T Stadium and Globe Life Field?", "Yes \u2014 game-day and concert transportation to AT&T Stadium and Globe Life Field is one of our most popular Arlington services, with door-to-gate drop-off and a set pickup point afterward."),
            ("Can you take us to DFW Airport from Arlington?", "Absolutely. Arlington is minutes from DFW, and we offer flight-monitored, flat-rate airport transfers 24/7 in sedans, SUVs and Sprinters."),
            ("Do you handle large groups for events?", "Yes \u2014 our luxury SUVs, executive Sprinters and party buses keep groups together for games, concerts and family outings across Arlington and the Metroplex."),
        ],
        "related": rel(dallas_cities, "/car-service-arlington-tx/") + [("/dallas-corporate-car-service/", "Dallas Corporate Car Service")],
    })

    # 14. Car Service Plano TX
    pages.append({
        "slug": "car-service-plano-tx",
        "title": "Car Service Plano TX | Corporate Black Car & DFW Airport | Purple Heart Limo",
        "meta": "Car service in Plano, TX \u2014 executive black car for corporate travel, Legacy West, DFW & Love Field airport transfers and events. Flat rates, no surge, 24/7. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 Car Service Plano TX",
        "image": "sedan-cadillac.webp",
        "areas": ["Plano", "Frisco", "Allen", "Richardson", "McKinney", "Dallas"],
        "locality": "Plano", "reviews": 96,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "Plano Car Service",
        "badge": "\U0001F4BC Corporate Corridor \u00b7 Plano, TX",
        "h1_main": "Car Service", "h1_em": "Plano, TX",
        "hero_p": "Executive car service in Plano, TX \u2014 flat-rate black car and SUV travel for corporate trips, Legacy West and The Shops at Legacy, client roadshows, and DFW or Love Field airport transfers. Professional chauffeurs, account billing available, zero surge pricing, 24/7.",
        "stats": [("4.9\u2605", "Average Rating"), ("DFW", "Airport Served"), ("24/7", "Available"), ("$0", "Surge Fees")],
        "svc_label": "Plano Car Service", "svc_title": "Executive Transportation for Plano",
        "svc_desc": "Plano runs on business \u2014 our car service keeps executives, teams and visitors moving on schedule.",
        "cards": [
            ("\U0001F4BC", "Corporate Travel", "Executive sedans for HQ visits, meetings and client roadshows."),
            ("\u2708\uFE0F", "DFW & Love Field", "Flight-monitored airport transfers to both Dallas airports."),
            ("\U0001F3E2", "Legacy West", "Polished rides to Legacy West offices, dining and hotels."),
            ("\U0001F465", "Group & Team Travel", "Executive Sprinters for teams, conferences and offsites."),
            ("\U0001F37D\uFE0F", "Dinner & Events", "Evening car service to The Shops at Legacy and beyond."),
            ("\U0001F698", "Luxury SUV", "Escalade and Suburban for executives, families and luggage."),
        ],
        "body": [
            ("Plano's Corporate Car Service", [
                "Plano is one of the country's great corporate addresses \u2014 home to major headquarters and the Legacy West and Shops at Legacy business district. That means a steady stream of executives, clients and teams who need transportation that's as professional as they are. Purple Heart Limo's Plano car service delivers flat-rate, chauffeur-driven black cars and SUVs that show up early, look immaculate and get you to the meeting on time.",
                "We're veteran-owned, which means punctuality and presentation aren't optional. Whether you're hosting a client roadshow, moving a team between offices, or sending a visitor back to the airport, we make your company look good.",
            ]),
            ("Airport Transfers From Plano", [
                "Plano sits between DFW International and Dallas Love Field, so we handle flight-monitored transfers to both. Your chauffeur tracks the flight, adjusts for delays automatically and never adds surge pricing. See our <a href=\"/dfw-airport-car-service/\">DFW airport car service</a> and <a href=\"/car-service-dallas-love-field/\">Love Field car service</a> for details.",
            ]),
            ("Business Accounts & Group Travel", [
                "For companies that book regularly, we offer account billing and priority scheduling through our <a href=\"/dallas-corporate-car-service/\">Dallas corporate car service</a>. Need to move a whole team? Our executive Sprinters seat up to 12 with room for luggage \u2014 ideal for conferences and offsites across the Metroplex.",
            ]),
        ],
        "form_title": "Book Plano Car Service", "form_btn": "Request Plano Car Service",
        "service_opts": ["Corporate / Executive", "DFW Airport Transfer", "Love Field Transfer", "Group / Team Travel", "Dinner / Event", "Hourly Charter", "Other"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Executive Sprinter", "Stretch Limousine"],
        "pickup_ph": "Legacy West or 123 Main St, Plano TX", "city_val": "Plano TX",
        "why_title": "Plano's Texan-Owned Choice", "why": STD_WHY,
        "faq_title": "Plano Car Service FAQ",
        "faqs": [
            ("How much does car service in Plano cost?", "Plano rides are flat-rate and quoted up front based on your pickup, destination and vehicle, with no surge pricing. Call (833) 740-0700 for a quote."),
            ("Do you offer corporate accounts in Plano?", "Yes \u2014 we offer billing accounts, priority scheduling and reporting for Plano companies through our Dallas corporate car service. Frequent travel is easy to manage."),
            ("Which airports do you serve from Plano?", "We provide flight-monitored, flat-rate transfers to both DFW International and Dallas Love Field, 24/7, in sedans, SUVs and Sprinters."),
            ("Can you move a team or conference group?", "Absolutely \u2014 our executive Sprinter vans seat up to 12 with luggage space, perfect for team travel, conferences and offsites around Legacy West and the Metroplex."),
        ],
        "related": rel(dallas_cities, "/car-service-plano-tx/") + [("/dallas-corporate-car-service/", "Dallas Corporate Car Service")],
    })

    # 15. Car Service Frisco TX
    pages.append({
        "slug": "car-service-frisco-tx",
        "title": "Car Service Frisco TX | The Star, Corporate & DFW Airport | Purple Heart Limo",
        "meta": "Car service in Frisco, TX \u2014 executive black car for The Star, corporate travel, Stonebriar, sporting events and DFW airport transfers. Flat rates, no surge, 24/7. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 Car Service Frisco TX",
        "image": "luxsuv-escalade.webp",
        "areas": ["Frisco", "Plano", "The Colony", "Little Elm", "McKinney", "Dallas"],
        "locality": "Frisco", "reviews": 96,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "Frisco Car Service",
        "badge": "\U0001F3DF\uFE0F Sports City USA \u00b7 Frisco, TX",
        "h1_main": "Car Service", "h1_em": "Frisco, TX",
        "hero_p": "Professional car service in Frisco, TX \u2014 flat-rate black car and SUV travel for The Star, corporate trips, Toyota Stadium and PGA events, Stonebriar shopping, and DFW or Love Field airport transfers. Veteran-owned, zero surge pricing, available 24/7.",
        "stats": [("4.9\u2605", "Average Rating"), ("DFW", "Airport Served"), ("24/7", "Available"), ("$0", "Surge Fees")],
        "svc_label": "Frisco Car Service", "svc_title": "Rides Built for Frisco",
        "svc_desc": "From corporate campuses to The Star to the airport, our Frisco car service keeps you on schedule in style.",
        "cards": [
            ("\U0001F4BC", "Corporate Travel", "Executive sedans for Frisco's corporate campuses and HQs."),
            ("\U0001F3C8", "The Star & Events", "Rides to The Star, Toyota Stadium and PGA Frisco events."),
            ("\u2708\uFE0F", "DFW Airport Transfers", "Flight-monitored, flat-rate transfers to DFW and Love Field."),
            ("\U0001F6CD\uFE0F", "Stonebriar & Dining", "Evening car service to Stonebriar Centre and The Star District."),
            ("\U0001F465", "Group & Team Travel", "Executive Sprinters for teams, conferences and offsites."),
            ("\U0001F698", "Luxury SUV", "Escalade and Suburban for executives, families and luggage."),
        ],
        "body": [
            ("Frisco's Texan-Owned Car Service", [
                "Frisco has exploded into one of Texas's most dynamic cities \u2014 corporate headquarters, The Star (the Dallas Cowboys' world headquarters), Toyota Stadium, PGA of America's home, and the upscale Stonebriar Centre. All that growth means a constant need for dependable, professional transportation. Purple Heart Limo's Frisco car service answers it with flat-rate, chauffeur-driven black cars and SUVs that arrive early and look the part.",
                "As a veteran-owned company, we hold ourselves to a military standard of punctuality and presentation \u2014 ideal for executives, event guests and families who expect their ride to be the easy part of the day.",
            ]),
            ("Events at The Star & Beyond", [
                "Frisco is built for events, and parking near The Star, Toyota Stadium or a PGA Frisco tournament can be a headache. We drop you at the entrance and pick you up after, so you skip the lots and the crowds. Book by the hour for multi-stop nights that include dinner at The Star District or drinks afterward.",
            ]),
            ("Airport & Corporate Travel From Frisco", [
                "We provide flight-monitored, flat-rate transfers from Frisco to both <a href=\"/dfw-airport-car-service/\">DFW International</a> and <a href=\"/car-service-dallas-love-field/\">Dallas Love Field</a>. For regular business travel, our <a href=\"/dallas-corporate-car-service/\">Dallas corporate car service</a> adds account billing and priority scheduling.",
            ]),
        ],
        "form_title": "Book Frisco Car Service", "form_btn": "Request Frisco Car Service",
        "service_opts": ["Corporate / Executive", "The Star / Event", "DFW Airport Transfer", "Love Field Transfer", "Group / Team Travel", "Dinner / Shopping", "Other"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Executive Sprinter", "Stretch Limousine", "Party Bus"],
        "pickup_ph": "The Star or 123 Main St, Frisco TX", "city_val": "Frisco TX",
        "why_title": "Frisco's Texan-Owned Choice", "why": STD_WHY,
        "faq_title": "Frisco Car Service FAQ",
        "faqs": [
            ("How much is car service in Frisco, TX?", "Frisco rides are flat-rate and quoted up front based on your pickup, destination and vehicle, with no surge pricing. Call (833) 740-0700 for a quote."),
            ("Do you provide transportation to The Star and Frisco events?", "Yes \u2014 we offer door-to-entrance rides to The Star, Toyota Stadium and PGA Frisco events, with a set pickup point afterward so you skip the parking lots."),
            ("Which airports do you serve from Frisco?", "We provide flight-monitored, flat-rate transfers to both DFW International and Dallas Love Field, available 24/7 in sedans, SUVs and Sprinters."),
            ("Do you offer corporate car service in Frisco?", "Absolutely \u2014 executive travel for Frisco's corporate campuses is a core service, with account billing and group Sprinter options available."),
        ],
        "related": rel(dallas_cities, "/car-service-frisco-tx/") + [("/dallas-corporate-car-service/", "Dallas Corporate Car Service")],
    })

    # 16. Limo Service University Park TX
    pages.append({
        "slug": "limo-service-university-park-tx",
        "title": "Limo Service University Park TX | Park Cities Black Car & Chauffeur | Purple Heart Limo",
        "meta": "Limo & car service in University Park, TX (Park Cities) \u2014 black car, airport transfers, weddings, galas & SMU events with a professional chauffeur. Flat rates, 24/7. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 Limo Service University Park TX",
        "image": "sedan-cadillac.webp",
        "areas": ["University Park", "Highland Park", "Dallas", "Preston Hollow", "Plano", "Irving"],
        "locality": "University Park", "reviews": 96,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "University Park Limo Service",
        "badge": "\U0001F396\uFE0F Park Cities \u00b7 University Park, TX",
        "h1_main": "Limo Service", "h1_em": "University Park, TX",
        "hero_p": "Premium limo and car service for University Park and the Park Cities \u2014 black car airport transfers, wedding and gala transportation, SMU family weekends and nights out, all with a professional chauffeur. Flat rates, zero surge, and the discretion University Park families expect, 24/7.",
        "stats": [("4.9\u2605", "Average Rating"), ("Park Cities", "Specialists"), ("24/7", "Available"), ("$0", "Surge Fees")],
        "svc_label": "University Park Limo Service", "svc_title": "Refined Transportation for the Park Cities",
        "svc_desc": "Discreet, polished and always on time \u2014 the limo service University Park trusts for airports, events and celebrations.",
        "cards": [
            ("\u2708\uFE0F", "Airport Transfers", "Flat-rate black car to DFW and Love Field, flight-monitored."),
            ("\U0001F37E", "Galas & Charity Events", "Arrive in style at Dallas galas, benefits and society events."),
            ("\U0001F393", "SMU & Family Weekends", "Reliable rides for SMU parents, graduations and reunions."),
            ("\U0001F48D", "Weddings", "Stretch limos and luxury SUVs for Park Cities weddings."),
            ("\U0001F4BC", "Executive Car Service", "Discreet corporate travel for executives and professionals."),
            ("\U0001F377", "Nights Out", "Safe, elegant transportation to dinner, the arts and downtown."),
        ],
        "body": [
            ("Limo & Black Car Service for University Park", [
                "University Park is the heart of the Park Cities \u2014 tree-lined streets, stately homes, Snider Plaza, SMU and a community that expects a certain standard. Purple Heart Limo provides limo and black car service tailored to that standard: a professionally dressed chauffeur, an immaculate vehicle, flat-rate pricing and the quiet discretion you'd want at your front door. Whether it's a charity gala, a wedding, an SMU family weekend or a 5 a.m. flight, we make the transportation effortless.",
                "We're veteran-owned, and we treat punctuality and presentation as a point of honor. Your chauffeur arrives early, knows the neighborhood, and handles the details so you never think twice about the ride.",
            ]),
            ("Where We Drive in the Park Cities", [
                "We serve University Park, Highland Park and the surrounding Dallas neighborhoods \u2014 Preston Hollow, Uptown, Downtown and beyond \u2014 with seamless connections to both airports and every major venue:",
                '<ul><li>DFW &amp; Dallas Love Field airport transfers</li><li>Galas, benefits and society events</li><li>SMU graduations, family weekends and reunions</li><li>Weddings, anniversaries and milestone celebrations</li></ul>',
                "Looking for more? Explore our <a href=\"/limo-service-highland-park-tx/\">Highland Park limo service</a> and our full range of <a href=\"/limo-service-dallas-tx/\">Dallas-Fort Worth limo services</a>.",
            ]),
            ("Discretion University Park Families Expect", [
                "From standing weekly chauffeur arrangements to one-off black-tie events, our University Park clients value reliability and privacy above all. Flat rates mean no surge surprises, professional chauffeurs mean no awkward rideshare moments, and our <a href=\"/dfw-airport-car-service/\">airport car service</a> means you're never scrambling before a flight.",
            ]),
        ],
        "form_title": "Book University Park Limo Service", "form_btn": "Request University Park Service",
        "service_opts": ["Airport Transfer (DFW/DAL)", "Gala / Charity Event", "Wedding", "SMU / Family Weekend", "Corporate / Executive", "Night Out", "Other"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Stretch Limousine", "Executive Sprinter", "Party Bus"],
        "pickup_ph": "Snider Plaza or 123 Main St, University Park TX", "city_val": "University Park TX",
        "why_title": "The Park Cities' Texan-Owned Choice", "why": STD_WHY,
        "faq_title": "University Park Limo Service FAQ",
        "faqs": [
            ("How much is limo service in University Park, TX?", "Our University Park rides are flat-rate and quoted up front based on your pickup, destination and vehicle, with no surge pricing. Call (833) 740-0700 for a quote."),
            ("Do you provide airport transfers from University Park?", "Yes \u2014 we offer flight-monitored, flat-rate black car and SUV transfers to both DFW International and Dallas Love Field, 24/7."),
            ("Can you handle weddings and galas in the Park Cities?", "Absolutely \u2014 stretch limousines, luxury SUVs and Sprinters for weddings, charity galas and society events across University Park and Highland Park."),
            ("Do you offer standing or recurring chauffeur service?", "Yes \u2014 many Park Cities families book recurring chauffeur arrangements for school runs, standing appointments and regular airport travel. Call us to set one up."),
        ],
        "related": rel(dallas_cities, "/limo-service-university-park-tx/") + [("/dallas-wedding-transportation/", "Dallas Wedding Transportation")],
    })

    # 17. Limo Service Highland Park TX
    pages.append({
        "slug": "limo-service-highland-park-tx",
        "title": "Limo Service Highland Park TX | Luxury Black Car & Chauffeur | Purple Heart Limo",
        "meta": "Limo & car service in Highland Park, TX \u2014 luxury black car, airport transfers, weddings, galas & executive travel with a professional chauffeur. Flat rates, 24/7. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 Limo Service Highland Park TX",
        "image": "stretch-limo.webp",
        "areas": ["Highland Park", "University Park", "Dallas", "Preston Hollow", "Uptown", "Irving"],
        "locality": "Highland Park", "reviews": 96,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "Highland Park Limo Service",
        "badge": "\U0001F48E Park Cities \u00b7 Highland Park, TX",
        "h1_main": "Limo Service", "h1_em": "Highland Park, TX",
        "hero_p": "Luxury limo and car service for Highland Park \u2014 discreet black car airport transfers, wedding and gala transportation, executive travel and elegant nights out, all with a professional chauffeur. Flat rates, zero surge, and white-glove service, available 24/7.",
        "stats": [("4.9\u2605", "Average Rating"), ("Park Cities", "Specialists"), ("24/7", "Available"), ("$0", "Surge Fees")],
        "svc_label": "Highland Park Limo Service", "svc_title": "White-Glove Transportation for Highland Park",
        "svc_desc": "The discreet, dependable limo service Highland Park relies on for airports, galas, weddings and executive travel.",
        "cards": [
            ("\u2708\uFE0F", "Airport Transfers", "Flat-rate black car to DFW and Love Field, flight-monitored."),
            ("\U0001F377", "Galas & Society Events", "Arrive in style at Dallas galas, benefits and openings."),
            ("\U0001F48D", "Weddings", "Stretch limousines and luxury SUVs for elegant celebrations."),
            ("\U0001F4BC", "Executive Car Service", "Discreet, professional travel for executives and VIPs."),
            ("\U0001F6CD\uFE0F", "Highland Park Village", "Polished rides to luxury shopping and fine dining."),
            ("\U0001F3AD", "Arts & Dining", "Evening transportation to the Arts District and beyond."),
        ],
        "body": [
            ("Luxury Limo & Black Car Service for Highland Park", [
                "Highland Park sets the standard for elegance in Dallas \u2014 from Highland Park Village's luxury boutiques to the galas, weddings and society events that fill the calendar. Purple Heart Limo provides white-glove limo and black car service to match: an impeccably presented chauffeur, a spotless vehicle, flat-rate pricing and total discretion. Whether you're attending a charity benefit, hosting out-of-town guests or catching a flight, we make the journey as refined as the destination.",
                "Veteran-owned and detail-driven, we treat reliability and privacy as non-negotiable. Your chauffeur arrives early, dresses for the occasion and anticipates the details \u2014 the way Highland Park expects.",
            ]),
            ("Service Across Highland Park & the Park Cities", [
                "We cover Highland Park, neighboring University Park, and the surrounding Dallas neighborhoods, with seamless connections to airports, venues and downtown:",
                '<ul><li>DFW &amp; Dallas Love Field airport transfers</li><li>Charity galas, benefits and gallery openings</li><li>Weddings, anniversaries and milestone events</li><li>Executive and VIP corporate travel</li></ul>',
                "See also our <a href=\"/limo-service-university-park-tx/\">University Park limo service</a> and our complete <a href=\"/limo-service-dallas-tx/\">Dallas-Fort Worth limo services</a>.",
            ]),
            ("Discretion & Reliability, Every Time", [
                "Our Highland Park clients value a ride that's private, punctual and effortless. Flat rates remove any surge surprises, professional chauffeurs replace unpredictable rideshares, and our <a href=\"/dallas-wedding-transportation/\">wedding transportation</a> and <a href=\"/dfw-airport-car-service/\">airport car service</a> are tailored to the occasion.",
            ]),
        ],
        "form_title": "Book Highland Park Limo Service", "form_btn": "Request Highland Park Service",
        "service_opts": ["Airport Transfer (DFW/DAL)", "Gala / Society Event", "Wedding", "Corporate / Executive", "Shopping / Dining", "Night Out", "Other"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Stretch Limousine", "Executive Sprinter", "Party Bus"],
        "pickup_ph": "Highland Park Village or 123 Main St, Highland Park TX", "city_val": "Highland Park TX",
        "why_title": "The Park Cities' Texan-Owned Choice", "why": STD_WHY,
        "faq_title": "Highland Park Limo Service FAQ",
        "faqs": [
            ("How much is limo service in Highland Park, TX?", "Highland Park rides are flat-rate and quoted up front based on your pickup, destination and vehicle, with no surge pricing. Call (833) 740-0700 for a quote."),
            ("Do you offer discreet executive and VIP service?", "Yes \u2014 discretion is central to our Highland Park service. Professional, background-checked chauffeurs and immaculate vehicles for executives, VIPs and private clients."),
            ("Can you provide wedding and gala transportation?", "Absolutely \u2014 stretch limousines, luxury SUVs and Sprinter shuttles for weddings, charity galas and society events throughout the Park Cities."),
            ("Do you serve both Dallas airports from Highland Park?", "Yes \u2014 flight-monitored, flat-rate transfers to both DFW International and Dallas Love Field, available 24/7."),
        ],
        "related": rel(dallas_cities, "/limo-service-highland-park-tx/") + [("/dallas-wedding-transportation/", "Dallas Wedding Transportation")],
    })

    # 18. Car Service Irving TX
    pages.append({
        "slug": "car-service-irving-tx",
        "title": "Car Service Irving TX | Las Colinas Corporate Black Car & DFW | Purple Heart Limo",
        "meta": "Car service in Irving & Las Colinas, TX \u2014 executive black car for corporate travel, DFW airport transfers, Toyota Music Factory & events. Flat rates, no surge, 24/7. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 Car Service Irving TX",
        "image": "sedan-cadillac.webp",
        "areas": ["Irving", "Las Colinas", "Coppell", "Grapevine", "Dallas", "Fort Worth"],
        "locality": "Irving", "reviews": 88,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "Irving Car Service",
        "badge": "\U0001F4BC Las Colinas \u00b7 Irving, TX",
        "h1_main": "Car Service", "h1_em": "Irving, TX",
        "hero_p": "Executive car service in Irving and Las Colinas, TX \u2014 flat-rate black car and SUV travel for corporate trips, DFW airport transfers, the Irving Convention Center and Toyota Music Factory events. Professional chauffeurs, account billing available, zero surge pricing, 24/7.",
        "stats": [("4.9\u2605", "Average Rating"), ("DFW", "Airport Served"), ("24/7", "Available"), ("$0", "Surge Fees")],
        "svc_label": "Irving Car Service", "svc_title": "Executive Transportation for Irving & Las Colinas",
        "svc_desc": "From Las Colinas boardrooms to DFW departures, our Irving car service keeps business travelers on schedule.",
        "cards": [
            ("\U0001F4BC", "Corporate Travel", "Executive sedans for Las Colinas HQs, meetings and roadshows."),
            ("\u2708\uFE0F", "DFW Airport Transfers", "Minutes from DFW \u2014 flight-monitored, flat-rate airport rides."),
            ("\U0001F3B5", "Toyota Music Factory", "Group transport to concerts, dining and nightlife."),
            ("\U0001F3E2", "Convention Center", "Reliable rides for Irving Convention Center events and guests."),
            ("\U0001F465", "Group & Team Travel", "Executive Sprinters for teams, conferences and offsites."),
            ("\U0001F698", "Luxury SUV", "Escalade and Suburban for executives, families and luggage."),
        ],
        "body": [
            ("Irving & Las Colinas Car Service", [
                "Irving \u2014 and especially the Las Colinas business district \u2014 is one of the densest corporate hubs in Texas, packed with headquarters, hotels and the Irving Convention Center. Add the Toyota Music Factory's concerts and restaurants and you have a city that never stops needing dependable transportation. Purple Heart Limo's Irving car service delivers flat-rate, chauffeur-driven black cars and SUVs that arrive early, look immaculate and get you where you need to be.",
                "As a veteran-owned company, we treat punctuality and presentation as a standard, not an upsell \u2014 exactly what Las Colinas executives, event guests and visiting teams expect.",
            ]),
            ("Minutes From DFW Airport", [
                "Irving borders Dallas Fort Worth International, making it one of the easiest cities for flight-monitored airport transfers. Your chauffeur tracks the flight, adjusts for delays automatically and never adds surge pricing. See our <a href=\"/dfw-airport-car-service/\">DFW airport car service</a>, or fly Southwest from <a href=\"/car-service-dallas-love-field/\">Dallas Love Field</a> instead.",
            ]),
            ("Corporate Accounts & Group Travel", [
                "For companies that book regularly, we offer account billing and priority scheduling through our <a href=\"/dallas-corporate-car-service/\">Dallas corporate car service</a>. Moving a team? Our executive Sprinters seat up to 12 with luggage space \u2014 ideal for conferences at the Irving Convention Center and offsites across the Metroplex.",
            ]),
        ],
        "form_title": "Book Irving Car Service", "form_btn": "Request Irving Car Service",
        "service_opts": ["Corporate / Executive", "DFW Airport Transfer", "Convention / Event", "Toyota Music Factory", "Group / Team Travel", "Hourly Charter", "Other"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Executive Sprinter", "Stretch Limousine", "Party Bus"],
        "pickup_ph": "Las Colinas or 123 Main St, Irving TX", "city_val": "Irving TX",
        "why_title": "Irving's Texan-Owned Choice", "why": STD_WHY,
        "faq_title": "Irving Car Service FAQ",
        "faqs": [
            ("How much is car service in Irving, TX?", "Irving and Las Colinas rides are flat-rate and quoted up front based on your pickup, destination and vehicle, with no surge pricing. Call (833) 740-0700 for a quote."),
            ("Do you serve DFW Airport from Irving?", "Yes \u2014 Irving borders DFW International, so we offer fast, flight-monitored, flat-rate transfers 24/7 in sedans, SUVs and Sprinters."),
            ("Do you offer corporate accounts in Las Colinas?", "Absolutely \u2014 billing accounts, priority scheduling and reporting are available for Las Colinas companies through our Dallas corporate car service."),
            ("Can you handle convention and event groups?", "Yes \u2014 our executive Sprinter vans seat up to 12 with luggage room, ideal for Irving Convention Center events, conferences and Toyota Music Factory outings."),
        ],
        "related": rel(dallas_cities, "/car-service-irving-tx/") + [("/dallas-corporate-car-service/", "Dallas Corporate Car Service")],
    })

    # 19. Car Service McKinney TX
    pages.append({
        "slug": "car-service-mckinney-tx",
        "title": "Car Service McKinney TX | Black Car, Airport & Events | Purple Heart Limo",
        "meta": "Car service in McKinney, TX \u2014 black car for DFW airport transfers, corporate travel, weddings, wine tours & Historic Downtown nights out. Flat rates, no surge, 24/7. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 Car Service McKinney TX",
        "image": "luxsuv-escalade.webp",
        "areas": ["McKinney", "Frisco", "Allen", "Plano", "Prosper", "Dallas"],
        "locality": "McKinney", "reviews": 88,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "McKinney Car Service",
        "badge": "\U0001F3DB\uFE0F Collin County \u00b7 McKinney, TX",
        "h1_main": "Car Service", "h1_em": "McKinney, TX",
        "hero_p": "Professional car service in McKinney, TX \u2014 flat-rate black car and SUV travel for DFW airport transfers, corporate trips, weddings, wine tours and Historic Downtown McKinney nights out. Veteran-owned, zero surge pricing, available 24/7 across Collin County.",
        "stats": [("4.9\u2605", "Average Rating"), ("DFW", "Airport Served"), ("24/7", "Available"), ("$0", "Surge Fees")],
        "svc_label": "McKinney Car Service", "svc_title": "Rides for Every McKinney Occasion",
        "svc_desc": "From an early flight to a night on the Square, our McKinney car service gets you there on time and in comfort.",
        "cards": [
            ("\u2708\uFE0F", "DFW Airport Transfers", "Flight-monitored, flat-rate rides to DFW and Love Field."),
            ("\U0001F4BC", "Corporate Travel", "Executive sedans for Collin County business trips and meetings."),
            ("\U0001F48D", "Weddings", "Stretch limos and luxury SUVs for McKinney-area weddings."),
            ("\U0001F377", "Wine & Brewery Tours", "Safe, chauffeured tours of local wineries and breweries."),
            ("\U0001F37E", "Historic Downtown", "Nights out on McKinney's Square without driving or parking."),
            ("\U0001F465", "Group Travel", "Executive Sprinters for families, teams and celebrations."),
        ],
        "body": [
            ("McKinney's Texan-Owned Car Service", [
                "McKinney blends fast-growing Collin County business with one of the most charming historic downtowns in Texas \u2014 a Square full of restaurants, shops and venues. That mix means residents and visitors need everything from early-morning airport runs to elegant wedding transportation to safe nights out. Purple Heart Limo's McKinney car service covers all of it with flat-rate, chauffeur-driven black cars, SUVs and limousines.",
                "We're veteran-owned, so reliability and presentation come standard. Your chauffeur arrives early, knows the area, and handles the details \u2014 whether it's a business trip, a celebration or a flight to catch.",
            ]),
            ("Airport Transfers From McKinney", [
                "McKinney is an easy run to both Dallas airports. We provide flight-monitored, flat-rate transfers to <a href=\"/dfw-airport-car-service/\">DFW International</a> and <a href=\"/car-service-dallas-love-field/\">Dallas Love Field</a>, tracking your flight and adjusting for delays automatically \u2014 with no surge pricing, ever.",
            ]),
            ("Weddings, Tours & Nights Out", [
                "Collin County is full of wedding venues, wineries and breweries, and Historic Downtown McKinney is a destination in its own right. Book by the hour for a chauffeured wine tour, a multi-stop celebration or a night on the Square. Planning a wedding? See our <a href=\"/dallas-wedding-transportation/\">Dallas-Fort Worth wedding transportation</a>.",
            ]),
        ],
        "form_title": "Book McKinney Car Service", "form_btn": "Request McKinney Car Service",
        "service_opts": ["DFW Airport Transfer", "Love Field Transfer", "Corporate / Executive", "Wedding", "Wine / Brewery Tour", "Night Out / Event", "Other"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Executive Sprinter", "Stretch Limousine", "Party Bus"],
        "pickup_ph": "Historic Downtown or 123 Main St, McKinney TX", "city_val": "McKinney TX",
        "why_title": "McKinney's Texan-Owned Choice", "why": STD_WHY,
        "faq_title": "McKinney Car Service FAQ",
        "faqs": [
            ("How much is car service in McKinney, TX?", "McKinney rides are flat-rate and quoted up front based on your pickup, destination and vehicle, with no surge pricing. Call (833) 740-0700 for a quote."),
            ("Do you provide airport transfers from McKinney?", "Yes \u2014 flight-monitored, flat-rate transfers to both DFW International and Dallas Love Field, available 24/7 in sedans, SUVs and Sprinters."),
            ("Can you do wine tours or brewery tours?", "Absolutely \u2014 book by the hour and your chauffeur will take your group safely to Collin County wineries, breweries and Historic Downtown McKinney."),
            ("Do you offer wedding transportation in McKinney?", "Yes \u2014 stretch limousines, luxury SUVs and Sprinter shuttles for weddings and celebrations at McKinney-area venues across Collin County."),
        ],
        "related": rel(dallas_cities, "/car-service-mckinney-tx/") + [("/dallas-wedding-transportation/", "Dallas Wedding Transportation")],
    })

    # 20. Limo Service Fort Worth TX
    pages.append({
        "slug": "limo-service-fort-worth-tx",
        "title": "Limo Service Fort Worth TX | Stockyards, Weddings & Airport | Purple Heart Limo",
        "meta": "Limo & car service in Fort Worth, TX \u2014 stretch limos, black car & party buses for the Stockyards, Sundance Square, weddings, nights out & DFW airport. Flat rates, 24/7. Texan-owned.",
        "schema_name": "Purple Heart Limo \u2014 Limo Service Fort Worth TX",
        "image": "stretch-limo.webp",
        "areas": ["Fort Worth", "Arlington", "Grapevine", "Southlake", "Dallas", "Irving"],
        "locality": "Fort Worth", "reviews": 124,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "Fort Worth Limo Service",
        "badge": "\U0001F920 Cowtown \u00b7 Fort Worth, TX",
        "h1_main": "Limo Service", "h1_em": "Fort Worth, TX",
        "hero_p": "Limo and car service across Fort Worth, TX \u2014 stretch limousines, executive black cars and party buses for the Stockyards, Sundance Square, weddings, nights out, Dickies Arena events and DFW airport transfers. Flat rates, zero surge, professional chauffeurs, 24/7.",
        "stats": [("4.9\u2605", "Average Rating"), ("124+", "Fort Worth Reviews"), ("24/7", "Available"), ("$0", "Surge Fees")],
        "svc_label": "Fort Worth Limo Service", "svc_title": "Limos & Black Cars for All of Cowtown",
        "svc_desc": "From the Stockyards to Sundance Square to a flight out of DFW, our Fort Worth limo service does it in style.",
        "cards": [
            ("\U0001F920", "Stockyards Nights", "Limos and party buses for the Stockyards and Cowtown bars."),
            ("\U0001F3D9\uFE0F", "Sundance Square", "Elegant rides to dining, Bass Hall and downtown events."),
            ("\U0001F48D", "Weddings", "Stretch limousines and SUVs for Fort Worth-area weddings."),
            ("\u2708\uFE0F", "DFW Airport Transfers", "Flight-monitored, flat-rate airport car service."),
            ("\U0001F3DF\uFE0F", "Dickies Arena & Events", "Group transport to concerts, rodeos and big shows."),
            ("\U0001F4BC", "Corporate Travel", "Executive sedans for downtown Fort Worth business."),
        ],
        "body": [
            ("Fort Worth Limo & Car Service", [
                "Fort Worth is where Texas keeps its cowboy soul \u2014 the Stockyards, the rodeo, Billy Bob's \u2014 right alongside a polished downtown of Sundance Square, Bass Performance Hall and Dickies Arena. Whatever the occasion, Purple Heart Limo's Fort Worth limo service shows up ready: stretch limousines for a night out or a wedding, executive black cars for business, and party buses to keep a whole group together. Flat-rate pricing, professional chauffeurs and zero surge, every time.",
                "We're veteran-owned and built on punctuality. Your chauffeur arrives early, dresses for the occasion and knows Cowtown \u2014 from the Stockyards to TCU to the Cultural District.",
            ]),
            ("Nights Out, Weddings & Events", [
                "Fort Worth knows how to celebrate, and we keep the group together for all of it:",
                '<ul><li>Stockyards and Sundance Square nights out</li><li>Weddings, anniversaries and quincea\u00f1eras</li><li>Concerts, rodeos and shows at Dickies Arena</li><li>Bachelorette and bachelor parties by limo or party bus</li></ul>',
                "Need transportation for the whole wedding? See our <a href=\"/dallas-wedding-transportation/\">DFW wedding transportation</a> and <a href=\"/dallas-party-bus/\">party bus rentals</a>.",
            ]),
            ("Airport & Corporate Travel in Fort Worth", [
                "We provide flight-monitored, flat-rate transfers from Fort Worth to <a href=\"/dfw-airport-car-service/\">DFW International</a>, plus discreet executive travel for downtown business through our <a href=\"/dallas-corporate-car-service/\">corporate car service</a>. Explore all our <a href=\"/limo-service-dallas-tx/\">Dallas-Fort Worth limo services</a>.",
            ]),
        ],
        "form_title": "Book Fort Worth Limo Service", "form_btn": "Request Fort Worth Service",
        "service_opts": ["Night Out / Stockyards", "Wedding", "DFW Airport Transfer", "Concert / Event", "Corporate / Executive", "Party Bus / Group", "Other"],
        "vehicle_opts": ["Stretch Limousine", "Executive Sedan", "Luxury SUV", "Executive Sprinter", "Party Bus"],
        "pickup_ph": "Sundance Square or 123 Main St, Fort Worth TX", "city_val": "Fort Worth TX",
        "why_title": "Fort Worth's Texan-Owned Choice", "why": STD_WHY,
        "faq_title": "Fort Worth Limo Service FAQ",
        "faqs": [
            ("How much is limo service in Fort Worth, TX?", "Fort Worth rides are flat-rate and quoted up front based on your pickup, destination, vehicle and hours, with no surge pricing. Call (833) 740-0700 for a quote."),
            ("Do you serve the Stockyards and Sundance Square?", "Yes \u2014 nights out in the Stockyards and Sundance Square are among our most popular Fort Worth services, by stretch limo or party bus."),
            ("Do you provide DFW airport transfers from Fort Worth?", "Absolutely \u2014 flight-monitored, flat-rate transfers to DFW International, available 24/7 in sedans, SUVs and Sprinters."),
            ("Can you handle Fort Worth weddings and large groups?", "Yes \u2014 stretch limousines, luxury SUVs, Sprinters and party buses for weddings, quincea\u00f1eras and group celebrations across Fort Worth and the Metroplex."),
        ],
        "related": rel(dallas_cities, "/limo-service-fort-worth-tx/") + [("/dallas-wedding-transportation/", "Dallas Wedding Transportation")],
    })

    # 21. Prom & special-event limo Dallas
    pages.append({
        "slug": "prom-limo-rental-dallas-tx",
        "title": "Prom Limo Rental Dallas TX | Safe Group Rides | PHL",
        "meta": "Prom limo rental in Dallas with professional chauffeurs, parent-ready trip plans, stretch limos, SUVs, Sprinters and party buses. Call for a flat-rate quote.",
        "schema_name": "Purple Heart Limo — Prom Limo Rental Dallas",
        "image": "stretch-limo.webp", "areas": DALLAS_AREAS,
        "locality": "Dallas", "reviews": 214,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "Dallas Prom Limo",
        "badge": "🎓 Prom & Special Events · Dallas-Fort Worth",
        "h1_main": "Prom Limo Rental", "h1_em": "Dallas, TX",
        "hero_p": "Safe, polished prom transportation across Dallas-Fort Worth with professional chauffeurs, confirmed pickup plans, and the right vehicle for couples or full groups. Choose a stretch limousine, luxury SUV, executive Sprinter, or party bus and get a clear quote before the big night.",
        "stats": [("4.9★", "Average Rating"), ("24/7", "Reservations"), ("5–30", "Group Sizes"), ("$0", "Surge Fees")],
        "svc_label": "Dallas Prom Transportation", "svc_title": "A Vehicle for Every Prom Group",
        "svc_desc": "We match passenger count, formalwear comfort, photo plans, luggage, and after-prom stops to a confirmed vehicle.",
        "cards": [
            ("✨", "Stretch Limousine", "Classic prom arrival for couples and small groups with coordinated pickup timing."),
            ("🚌", "Party Bus", "Keep larger friend groups together between photos, dinner, the venue, and home."),
            ("🚐", "Executive Sprinter", "Comfortable group seating with easier entry, climate control, and room for formalwear."),
            ("🚙", "Luxury SUV", "Discreet, polished transportation for couples, parents, and smaller groups."),
            ("📸", "Photo & Dinner Stops", "Build planned stops into the itinerary without splitting the group between cars."),
            ("🛡️", "Parent-Ready Plan", "Confirmed chauffeur, vehicle, pickup contacts, addresses, and return schedule."),
        ],
        "body": [
            ("Prom Transportation Built Around Safety", [
                "A Dallas prom night can involve school photos, dinner, the dance, an after-prom event, and several home addresses spread across the Metroplex. Purple Heart Limo turns that complicated evening into one confirmed transportation plan. Parents receive a professional point of contact, the vehicle and chauffeur are scheduled before the event, and the group stays together instead of relying on multiple teen drivers or last-minute rideshares.",
                "Our team helps choose realistic pickup times around Dallas traffic and venue arrival windows. We serve schools and families in Dallas, Plano, Frisco, Addison, Arlington, Richardson, McKinney, Irving, Fort Worth, and surrounding DFW communities. Every quote is based on the actual itinerary, passenger count, vehicle, and reservation duration, with no rideshare-style surge pricing.",
            ]),
            ("Choosing the Right Prom Vehicle", [
                "A stretch limousine works well for the traditional prom experience and elegant arrival photos. An executive Sprinter is often more practical for a larger group because passengers can enter more easily and formal clothing has more room. Party buses suit groups that want everyone together for multiple stops, while a Cadillac Escalade or similar luxury SUV is ideal for a couple or small party.",
                "Passenger capacity is only one part of the decision. Tell us about dresses, jackets, photo props, coolers, and any items that need extra space. Browse the <a href=\"/fleet.html\">Purple Heart Limo fleet</a>, then call so we can confirm which vehicle best fits the group instead of squeezing the reservation into the wrong layout.",
            ]),
            ("Planning the Dallas Prom Itinerary", [
                "The best prom schedules include complete addresses, one lead contact, enough time for group photos, a firm dinner reservation, the school venue's arrival instructions, and a clear return plan. If several families are involved, select one or two central pickup points to reduce delays. We can also plan an hourly charter when the group needs the vehicle to remain available through several stops.",
                "Reserve early for April and May weekends because stretch limousines and party buses are limited. For other milestone events, explore our <a href=\"/dallas-party-bus/\">Dallas party bus service</a> and <a href=\"/dallas-wedding-transportation/\">Dallas wedding transportation</a>. Ready to plan? <a href=\"/booking.html\">Request a quote</a> or call <a href=\"tel:+18337400700\">(833) 740-0700</a>.",
            ]),
        ],
        "form_title": "Request a Dallas Prom Limo Quote", "form_btn": "Plan Prom Transportation",
        "service_opts": ["Prom", "Homecoming", "Graduation", "Quinceañera", "Birthday", "Other Special Event"],
        "vehicle_opts": ["Stretch Limousine", "Luxury SUV", "Executive Sprinter", "Party Bus", "Executive Sedan"],
        "pickup_ph": "School, home, or photo location in DFW", "city_val": "Dallas TX",
        "why_title": "Why Dallas Families Choose Purple Heart", "why": STD_WHY,
        "faq_title": "Dallas Prom Limo FAQ",
        "faqs": [
            ("How far ahead should we reserve a Dallas prom limo?", "Reserve as early as possible for April and May weekends because stretch limousines, Sprinters, and party buses are limited."),
            ("Can parents receive the chauffeur and trip details?", "Yes. We confirm the reservation contact, vehicle, pickup plan, addresses, and schedule before service."),
            ("Can the group stop for photos and dinner?", "Yes. Include every planned stop when requesting the quote so the itinerary and reservation time are accurate."),
            ("Which vehicle is best for a prom group?", "It depends on passenger count and space needs. We offer stretch limousines, SUVs, Sprinters, and party buses."),
        ],
        "related": rel(dallas_related, "/prom-limo-rental-dallas-tx/") + [("/fleet.html", "View Our Fleet")],
    })

    # 22. Addison limo service
    pages.append({
        "slug": "limo-service-addison-tx",
        "title": "Limo Service Addison TX | Airport & Event Rides | PHL",
        "meta": "Limo service in Addison, TX for DFW and Love Field transfers, Restaurant Row, corporate travel, weddings and groups. Professional chauffeurs, 24/7 reservations.",
        "schema_name": "Purple Heart Limo — Limo Service Addison TX",
        "image": "luxsuv-escalade.webp",
        "areas": ["Addison", "Dallas", "Richardson", "Plano", "Farmers Branch", "Carrollton"],
        "locality": "Addison", "reviews": 132,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "Addison Limo Service",
        "badge": "📍 Addison · North Dallas",
        "h1_main": "Limo Service", "h1_em": "Addison, TX",
        "hero_p": "Professional limo and black car service in Addison for airport transfers, Restaurant Row dinners, corporate meetings, weddings, and group events. Get a confirmed chauffeur, vehicle, and flat-rate quote with 24/7 reservation support.",
        "stats": [("4.9★", "Average Rating"), ("DFW + DAL", "Airports"), ("24/7", "Reservations"), ("$0", "Surge Fees")],
        "svc_label": "Addison Chauffeured Transportation", "svc_title": "Airport, Business & Event Service",
        "svc_desc": "From Addison Airport and Restaurant Row to DFW, Love Field, and North Dallas offices, every trip is planned in advance.",
        "cards": [
            ("✈️", "DFW Airport Service", "Flight-monitored pickups and flat-rate transfers between Addison and DFW."),
            ("🛬", "Love Field Transfers", "Prearranged car service to DAL with luggage-ready sedans and SUVs."),
            ("🍽️", "Restaurant Row", "Dinner, celebration, and nightlife transportation without parking concerns."),
            ("💼", "Corporate Travel", "Executive sedans and SUVs for Addison offices, hotels, and client pickups."),
            ("💍", "Weddings & Events", "Limos, Sprinters, and group transportation for North Dallas venues."),
            ("🚐", "Group Transportation", "Keep teams and families together with Sprinters and party buses."),
        ],
        "body": [
            ("Addison's Professional Limo and Car Service", [
                "Addison sits at the center of North Dallas business, dining, hotels, and event traffic. A short trip can still become unpredictable when the Tollway backs up, Restaurant Row fills for the evening, or a flight arrival changes. Purple Heart Limo provides prearranged Addison transportation with a professional chauffeur, a confirmed vehicle, and a schedule built around the real pickup and destination.",
                "We serve Addison Circle, Belt Line Road, the Dallas North Tollway corridor, Addison Airport, local hotels, offices, and nearby communities including Farmers Branch, Carrollton, Richardson, Plano, and Dallas. Reservations are supported 24/7 for early flights, late dinners, executive travel, and special events.",
            ]),
            ("Addison Airport and Commercial Airport Transfers", [
                "Travelers can reserve service between Addison and <a href=\"/dfw-airport-car-service/\">Dallas Fort Worth International Airport</a> or <a href=\"/car-service-dallas-love-field/\">Dallas Love Field</a>. We monitor commercial flight timing, select vehicles based on passengers and luggage, and provide pickup instructions before the trip. Private aviation passengers can also schedule direct transportation to or from Addison Airport.",
                "A sedan suits one or two business travelers, while a luxury SUV adds luggage room for families and small groups. Executive Sprinters are available when a team needs to travel together. The quote is established from the itinerary rather than changing with app demand.",
            ]),
            ("Restaurant Row, Corporate Travel, and Events", [
                "Addison's restaurants and hotels make it a natural meeting point for client dinners, birthdays, anniversaries, and nights out. Hourly service keeps the chauffeur available through multiple stops, while point-to-point service works for a defined pickup and return. Companies can use our <a href=\"/dallas-corporate-car-service/\">Dallas corporate car service</a> for executive arrivals, roadshows, group meetings, and recurring reservations.",
                "For weddings and celebrations, we coordinate passenger counts, venue access, photo timing, and return transportation. Review <a href=\"/fleet.html\">sedans, SUVs, stretch limousines, Sprinters, and party buses</a>, then <a href=\"/booking.html\">request a quote</a>. For immediate planning help, call <a href=\"tel:+18337400700\">(833) 740-0700</a>.",
            ]),
        ],
        "form_title": "Request Addison Limo Service", "form_btn": "Get an Addison Quote",
        "service_opts": ["DFW Airport Transfer", "Love Field Transfer", "Addison Airport", "Corporate / Executive", "Restaurant / Night Out", "Wedding / Event", "Group Transportation"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Stretch Limousine", "Executive Sprinter", "Party Bus"],
        "pickup_ph": "Addison Circle, hotel, office, or home", "city_val": "Addison TX",
        "why_title": "Why Addison Riders Choose Purple Heart", "why": STD_WHY,
        "faq_title": "Addison Limo Service FAQ",
        "faqs": [
            ("Do you provide Addison to DFW Airport car service?", "Yes. We offer 24/7, flight-monitored transfers between Addison and DFW in sedans, SUVs, and Sprinters."),
            ("Do you serve Dallas Love Field from Addison?", "Yes. Love Field transfers are available with a confirmed vehicle and pickup plan."),
            ("Can we book a limo for Addison Restaurant Row?", "Yes. Point-to-point or hourly service is available for dinners, celebrations, and nights out."),
            ("What vehicles are available in Addison?", "Choose executive sedans, luxury SUVs, stretch limousines, Sprinters, or party buses based on the group and itinerary."),
        ],
        "related": rel(dallas_related, "/limo-service-addison-tx/") + [("/car-service-plano-tx/", "Plano Car Service"), ("/car-service-frisco-tx/", "Frisco Car Service")],
    })

    # 23. Limo Service Lewisville TX
    pages.append({
        "slug": "limo-service-lewisville-tx",
        "title": "Limo Service Lewisville TX | Airport, Weddings & Events | Purple Heart Limo",
        "meta": "Lewisville limo service for DFW airport, weddings, Lake Lewisville outings and business travel. Sedans, SUVs, Sprinters and limos with flat-rate pricing, 24/7.",
        "schema_name": "Purple Heart Limo — Limo Service Lewisville TX",
        "image": "stretch-limo.webp",
        "areas": ["Lewisville", "Flower Mound", "Highland Village", "The Colony", "Coppell", "Carrollton"],
        "locality": "Lewisville", "reviews": 96,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "Lewisville Limo Service",
        "badge": "🌊 Lake Lewisville · Lewisville, TX",
        "h1_main": "Limo Service", "h1_em": "Lewisville, TX",
        "hero_p": "Professional Lewisville limo service for DFW airport transfers, Lake Lewisville celebrations, Old Town evenings, weddings and corporate travel. Reserve a sedan, luxury SUV, stretch limousine or Sprinter with a punctual chauffeur and an upfront flat rate.",
        "stats": [("4.9★", "Average Rating"), ("DFW", "Airport Access"), ("24/7", "Reservations"), ("$0", "Surge Fees")],
        "svc_label": "Lewisville Limousine Service", "svc_title": "Airport, Lake and Event Transportation",
        "svc_desc": "A locally planned ride for every Lewisville itinerary, from an early flight on SH 121 to a full evening around the lake.",
        "cards": [
            ("✈️", "DFW Airport Limo", "Flight-monitored service via SH 121 with room selected for travelers and bags."),
            ("🌊", "Lake Lewisville Outings", "Chauffeured transportation for marina gatherings, dinners and group celebrations."),
            ("💍", "Wedding Limos", "Coordinated arrivals for Lewisville, Flower Mound and Highland Village venues."),
            ("🏛️", "Old Town Evenings", "Point-to-point or hourly rides for dining, live music and special occasions."),
            ("💼", "Corporate Black Car", "Quiet sedans and SUVs for offices along I-35E and the Sam Rayburn corridor."),
            ("🚐", "Group Transportation", "Sprinters and party buses for families, teams and larger event groups."),
        ],
        "body": [
            ("Lewisville Limo Rental With Local Route Knowledge", [
                "Lewisville connects the I-35E corridor, SH 121, Lake Lewisville and communities across southern Denton County. That location is convenient, but construction, lake-weekend traffic and airport congestion can make an ordinary trip unpredictable. Purple Heart Limo plans the pickup, route and vehicle before departure, giving riders a dependable alternative to on-demand transportation.",
                "Our Lewisville limousine service covers Old Town Lewisville, Music City Mall, Castle Hills, Vista Ridge, the lake marinas and nearby Flower Mound, Highland Village, Coppell, Carrollton and The Colony. Whether the search is for a luxury limo in Lewisville, Lewisville car service or a private black car service, every reservation includes a professional chauffeur and confirmed pricing.",
            ]),
            ("Lewisville to DFW Airport Transportation", [
                "DFW International Airport is a natural connection from Lewisville by SH 121. Our <a href=\"/dfw-airport-car-service/\">DFW airport car service</a> monitors arriving flights and builds departure pickups around terminal, traffic and check-in needs. We also provide prearranged trips to <a href=\"/car-service-dallas-love-field/\">Dallas Love Field</a> via I-35E and the Dallas North Tollway corridor.",
                "Choose an executive sedan for one or two travelers, a luxury SUV for extra luggage or family space, and an executive Sprinter when a group needs one vehicle. Airport limo rental from Lewisville is available around the clock, including early departures and late arrivals.",
            ]),
            ("Weddings, Lake Days and Lewisville Celebrations", [
                "A stretch limousine adds a classic arrival for a wedding, prom or anniversary, while SUVs and Sprinters keep wedding parties and guests together. For Lake Lewisville outings, birthdays or an Old Town dinner, hourly service lets the chauffeur remain available between planned stops. Larger celebrations can use a party bus so no one has to coordinate parking or a designated driver.",
                "Explore <a href=\"/dallas-wedding-transportation/\">DFW wedding transportation</a>, compare options on our <a href=\"/fleet.html\">fleet page</a>, or consider nearby <a href=\"/limo-service-grapevine-tx/\">Grapevine limo service</a> for a wine-country itinerary.",
            ]),
            ("Planning a Lewisville Route That Works", [
                "A useful reservation starts with the actual itinerary, not just a pickup address. Tell us whether the ride begins near Old Town, Castle Hills, Vista Ridge or a Lake Lewisville marina; whether there are timed stops; and whether passengers will have checked bags, coolers or event items. For DFW departures, we plan the SH 121 approach around the airline terminal and build in a sensible buffer for corridor congestion. For Love Field, we review the longer southbound route rather than assuming the same timing will work.",
                "Lake plans deserve their own conversation. A marina pickup, restaurant reservation and home return can be held under one hourly charter so the group is not trying to summon separate rides between stops. For a concert, wedding, or school formal, share the venue, pickup sequence and final release time. The chauffeur can follow a confirmed schedule while the host has one transportation contact instead of coordinating every guest independently.",
            ]),
            ("Lewisville Fleet and Capacity Guidance", [
                "An executive sedan is the streamlined option for one or two airport travelers with ordinary luggage. Reserve a luxury SUV when a family, a couple with several bags, or a client pickup needs more passenger and cargo room. An executive Sprinter is often the better value for six to twelve guests traveling together to a lake event, wedding, airport, or dinner itinerary because it keeps the party in one vehicle. A stretch limousine is chosen for the formal experience; a party bus is best discussed for larger celebrations that need shared transportation.",
                "Capacity is only one part of the recommendation. Golf bags, strollers, garment bags, instruments and airport luggage change what will be comfortable. Include the passenger count, bag count, child-seat needs and any mobility considerations in the quote request. We will recommend a vehicle that fits the trip instead of promising a tight fit that makes the ride less enjoyable.",
            ]),
            ("Lewisville Pricing and Reservation Expectations", [
                "Lewisville limo service is quoted before the reservation is confirmed. The quote reflects the date, pickup and destination, vehicle, passenger needs, planned stops and, for hourly service, the reserved time. Airport trips are generally priced as a transfer; a multi-stop lake day, wedding schedule or evening out is usually better planned as an hourly charter. Flat-rate quoting means local demand, a concert crowd or a late finish does not create rideshare-style surge pricing.",
                "For the most accurate quote, provide flight numbers for airport trips and a complete timeline for events. Reserve important dates early, especially spring and fall weddings, prom weekends, holiday events and major lake weekends. Last-minute requests are welcome when a suitable vehicle is available, but advance booking gives the best chance to match the exact vehicle and pickup plan you want.",
            ]),
        ],
        "form_title": "Request Lewisville Limo Service", "form_btn": "Get a Lewisville Quote",
        "service_opts": ["DFW Airport Transfer", "Love Field Transfer", "Wedding / Anniversary", "Lake Lewisville Outing", "Corporate / Black Car", "Prom / Night Out", "Group Transportation"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Stretch Limousine", "Executive Sprinter", "Party Bus"],
        "pickup_ph": "Old Town, Lake Lewisville, home, hotel, or office", "city_val": "Lewisville TX",
        "why_title": "Why Lewisville Riders Choose Purple Heart", "why": STD_WHY,
        "faq_title": "Lewisville Limo Service FAQ",
        "faqs": [
            ("Do you provide limo service from Lewisville to DFW Airport?", "Yes. We provide 24/7, flight-monitored transfers between Lewisville and every DFW terminal, with sedans, SUVs and Sprinters selected for your party and luggage."),
            ("Can I rent a limo for a Lake Lewisville outing?", "Yes. Hourly limo, SUV, Sprinter and party bus service is available for marina gatherings, birthdays, dinners and other lake-area occasions."),
            ("What vehicle is best for a Lewisville wedding?", "A stretch limousine is ideal for the couple, while luxury SUVs or Sprinters work well for wedding parties and guest transfers. We can coordinate multiple vehicles on one timeline."),
            ("How is Lewisville limo service priced?", "We quote a flat rate from the date, route, duration and vehicle before booking. There is no rideshare-style surge pricing."),
            ("Should Lake Lewisville transportation be booked as a transfer or by the hour?", "A single direct trip can be quoted point-to-point. If your group will visit a marina, restaurant or several stops and wants the chauffeur available between them, hourly service is usually the more practical arrangement. Share the itinerary so we can quote the right format."),
            ("What details should I include for a Lewisville airport reservation?", "Please provide the airline, flight number, terminal if known, passenger and luggage count, pickup address and requested pickup time. That lets us monitor an arrival or plan a departure route and recommend the appropriate sedan, SUV or Sprinter."),
        ],
        "related": rel(dallas_related, "/limo-service-lewisville-tx/") + [("/limo-service-denton-tx/", "Denton Limo Service"), ("/limo-service-grapevine-tx/", "Grapevine Limo Service"), ("/car-service-frisco-tx/", "Frisco Car Service")],
    })

    # 24. Limo Service Denton TX
    pages.append({
        "slug": "limo-service-denton-tx",
        "title": "Limo Service Denton TX | DFW Airport, UNT & Weddings | Purple Heart Limo",
        "meta": "Denton limo service for DFW airport, UNT and TWU events, weddings, concerts and group travel. Flat-rate sedans, SUVs, limos and Sprinters available 24/7.",
        "schema_name": "Purple Heart Limo — Limo Service Denton TX",
        "image": "luxsuv-escalade.webp",
        "areas": ["Denton", "Corinth", "Lake Dallas", "Argyle", "Krum", "Aubrey"],
        "locality": "Denton", "reviews": 96,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "Denton Limo Service",
        "badge": "🎓 North Texas · Denton, TX",
        "h1_main": "Limo Service", "h1_em": "Denton, TX",
        "hero_p": "Denton limo and black car service for DFW flights, UNT and TWU occasions, courthouse-square nights, weddings and North Texas group travel. Ride with a professional chauffeur in a vehicle matched to your guests, luggage and schedule.",
        "stats": [("4.9★", "Average Rating"), ("2", "University Campuses"), ("24/7", "Available"), ("Flat", "Quoted Rates")],
        "svc_label": "Denton Limo Rental", "svc_title": "Made for Denton's Flights and Milestones",
        "svc_desc": "From commencement morning to an airport departure down I-35W, each reservation is planned around Denton's routes and timing.",
        "cards": [
            ("🎓", "UNT & TWU Events", "Transportation for commencements, family weekends, speakers and university guests."),
            ("✈️", "Airport Transportation", "Scheduled trips to DFW and Love Field with real-time flight monitoring."),
            ("💍", "Weddings in Denton County", "Limos and group vehicles for venues in Denton, Argyle and Aubrey."),
            ("🎵", "Square & Concert Nights", "Hourly service for the courthouse square, dining and live-music stops."),
            ("💼", "Executive Car Service", "Professional black cars for university, healthcare and business appointments."),
            ("🚌", "Prom & Group Rides", "Sprinters and party buses that keep students, families or teams together."),
        ],
        "body": [
            ("A Denton Limousine Company for North Texas Travel", [
                "Denton has its own rhythm: two university campuses, an active courthouse square, a renowned music community and fast-growing neighborhoods along I-35. A local itinerary may cross UNT, TWU and downtown before continuing south toward DFW. Purple Heart Limo provides scheduled Denton limo service with route planning, direct communication and a chauffeur who arrives early.",
                "Coverage includes Rayzor Ranch, Southridge, the Denton Square, the University of North Texas, Texas Woman's University and nearby Corinth, Lake Dallas, Argyle, Krum and Aubrey. Customers looking for Denton limo rental, luxury car service in Denton or a Denton party bus receive a real fleet recommendation rather than a one-size-fits-all ride.",
            ]),
            ("Airport Car Service From Denton", [
                "Trips from Denton to DFW typically use I-35W, while Love Field travel may continue through the I-35E corridor. We account for distance, terminal requirements and peak traffic when setting the pickup time. Commercial arrivals are flight-monitored, so the chauffeur can respond when a flight reaches the airport early or late.",
                "For an airport run, an executive sedan is efficient for a solo traveler or couple. A luxury SUV offers more bag space, and a Sprinter is the practical choice for university groups, wedding guests or families with substantial luggage. Learn more about <a href=\"/dfw-airport-car-service/\">DFW airport transportation</a> and <a href=\"/car-service-dallas-love-field/\">Love Field car service</a>.",
            ]),
            ("University Events, Weddings and Nights on the Square", [
                "Commencement, homecoming and family weekends bring concentrated traffic around UNT and TWU. Prearranged black car or Sprinter service gives families and official guests a defined pickup plan. For weddings in Denton, Argyle and the surrounding countryside, stretch limousines create the formal entrance while SUVs and Sprinters handle attendants or hotel shuttles.",
                "Hourly chauffeured service also works for dinner and live music around the Denton Square, proms and milestone birthdays. Browse <a href=\"/dallas-party-bus/\">Dallas party bus options</a>, plan <a href=\"/dallas-wedding-transportation/\">wedding transportation</a>, or connect a southern pickup through our <a href=\"/limo-service-lewisville-tx/\">Lewisville limo service</a>.",
            ]),
            ("Denton Route Planning Beyond the Map", [
                "Denton airport and event transportation should account for the city’s north-of-metro location. A departure to DFW generally follows I-35W, while Love Field may require the I-35E side of the corridor; the better choice depends on the pickup location, time of day and destination. We discuss the flight, airline and requested arrival window before confirming a pickup time. That preparation is particularly important for early flights, university move-in periods and busy Friday afternoon travel.",
                "For UNT and TWU events, a meeting point matters as much as the vehicle. Families may prefer a hotel or designated campus-adjacent pickup rather than trying to load on a congested street. A speaker, visiting administrator or prospective student can book a quiet point-to-point black car; a commencement group can reserve one vehicle for a coordinated hotel-to-campus-to-restaurant schedule. The plan is tailored to the use case rather than treating every campus trip like an airport run.",
            ]),
            ("Vehicle Selection for Denton Groups and Gear", [
                "An executive sedan suits a solo faculty visitor, a business traveler or a couple headed to the airport. A luxury SUV provides additional space for parents, graduation guests and luggage. For six to twelve passengers, an executive Sprinter keeps a band, athletic family, wedding party or university group together with more practical room for bags than several separate cars. A stretch limousine is intended for a formal arrival, while a party bus may suit a larger prom, birthday or concert group.",
                "Please count more than seats when choosing a vehicle. Graduation flowers, formalwear, instrument cases, carry-on bags and car seats all affect the comfortable configuration. Give us the number of passengers, luggage pieces, pickup order and accessibility needs during booking. We can then suggest a capacity that feels appropriate for a ride from Denton rather than merely meeting a maximum number.",
            ]),
            ("Denton Quotes, Timing and Booking", [
                "Your Denton limo quote is set from the date, route, vehicle, duration and itinerary. A direct airport ride is normally quoted as a transfer, while a Denton Square evening, campus schedule, wedding or multiple-stop outing is commonly reserved by the hour. The price is communicated in advance; it is not recalculated because rideshare demand rises after a show or during a university weekend.",
                "For flights, submit the airline and flight number so arrival service can be monitored and departure timing can be planned. For ceremonies and formal events, include venue addresses, the desired arrival time and any return or shuttle windows. Advance reservations are wise for commencements, homecoming, prom and wedding dates. If your trip is sooner, contact us anyway: we will clearly confirm availability and the vehicle options before you commit.",
            ]),
        ],
        "form_title": "Book Denton Limo Service", "form_btn": "Request a Denton Quote",
        "service_opts": ["DFW Airport Transfer", "Love Field Transfer", "UNT / TWU Event", "Wedding Transportation", "Corporate / Black Car", "Prom / Graduation", "Concert / Night Out"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Stretch Limousine", "Executive Sprinter", "Party Bus"],
        "pickup_ph": "Denton Square, UNT, TWU, venue, home, or hotel", "city_val": "Denton TX",
        "why_title": "Dependable Chauffeured Travel in Denton", "why": STD_WHY,
        "faq_title": "Denton Limo Service FAQ",
        "faqs": [
            ("How far ahead should I reserve a Denton airport limo?", "Advance reservations are recommended because Denton is north of both major airports. Share the flight and luggage details so we can set an appropriate pickup time and vehicle."),
            ("Do you serve UNT and Texas Woman's University?", "Yes. We provide sedans, SUVs, limos and Sprinters for commencements, family weekends, official visitors and other UNT or TWU events."),
            ("Can you provide wedding transportation outside central Denton?", "Yes. Service extends to venues in Argyle, Aubrey and other Denton County communities, including coordinated vehicles for couples, wedding parties and guests."),
            ("Do you offer a Denton party bus for prom or a night out?", "Yes. Party buses and Sprinters are available based on group size and date; a professional chauffeur manages every planned stop and the return."),
            ("Which airport should a Denton traveler use for car service?", "We serve both DFW International Airport and Dallas Love Field. DFW is commonly reached via I-35W, while Love Field requires a longer trip through the metro. Provide your airline and flight schedule so the pickup plan reflects the correct airport and travel window."),
            ("Can one reservation cover UNT or TWU commencement, dinner and the return trip?", "Yes. An hourly charter can keep the same vehicle and chauffeur assigned through a campus event, photos, dinner and the final drop-off. Send the expected stop sequence and timing so we can recommend the right vehicle and reservation length."),
        ],
        "related": rel(dallas_related, "/limo-service-denton-tx/") + [("/limo-service-lewisville-tx/", "Lewisville Limo Service"), ("/car-service-frisco-tx/", "Frisco Car Service"), ("/limo-service-fort-worth-tx/", "Fort Worth Limo Service")],
    })

    # 25. Limo Service Grapevine TX
    pages.append({
        "slug": "limo-service-grapevine-tx",
        "title": "Limo Service Grapevine TX | DFW Airport, Wine Tours & Events | Purple Heart Limo",
        "meta": "Grapevine limo service for DFW airport, Main Street wine tours, Gaylord Texan events and weddings. Flat-rate cars, SUVs, limos and group vehicles, 24/7.",
        "schema_name": "Purple Heart Limo — Limo Service Grapevine TX",
        "image": "stretch-limo.webp",
        "areas": ["Grapevine", "Southlake", "Colleyville", "Coppell", "Euless", "Irving"],
        "locality": "Grapevine", "reviews": 96,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "Grapevine Limo Service",
        "badge": "🍇 Main Street · Grapevine, TX",
        "h1_main": "Limo Service", "h1_em": "Grapevine, TX",
        "hero_p": "Grapevine limo service for DFW airport arrivals, Historic Main Street wine tours, Gaylord Texan conferences, weddings and lakefront celebrations. Enjoy a locally planned itinerary, a polished chauffeur and transparent flat-rate pricing.",
        "stats": [("4.9★", "Average Rating"), ("DFW", "Next Door"), ("24/7", "Airport Service"), ("100%", "Chauffeured")],
        "svc_label": "Grapevine Luxury Transportation", "svc_title": "From the Terminal to Texas Wine Country",
        "svc_desc": "Airport pickups, resort conferences and Main Street celebrations are easier with one confirmed vehicle and chauffeur.",
        "cards": [
            ("🛬", "DFW Airport Pickup", "Fast local access to all terminals with flight monitoring and pickup instructions."),
            ("🍷", "Winery & Main Street Tours", "Hourly limousine service for tasting rooms, dining and Historic Main Street."),
            ("🏨", "Gaylord Texan & Resorts", "Executive and group transportation for conventions, guests and resort stays."),
            ("💍", "Weddings & Rehearsals", "Formal limos and guest shuttles for Grapevine-area celebrations."),
            ("🌊", "Lake Grapevine Events", "SUVs, Sprinters and chauffeured group rides for waterfront occasions."),
            ("🎄", "Christmas Capital Tours", "Private seasonal transportation for lights, ICE! and holiday gatherings."),
        ],
        "body": [
            ("Grapevine Limo Service With a True Local Itinerary", [
                "Grapevine combines DFW International Airport access with Historic Main Street, wineries, major resorts and Lake Grapevine. Visitors often need more than a simple pickup: a terminal arrival may continue to the Gaylord Texan, a convention dinner and several downtown tasting rooms. Purple Heart Limo coordinates those details as one clear chauffeured itinerary.",
                "Our Grapevine car and limo service covers Historic Main Street, Grapevine Mills, Gaylord Texan Resort, Great Wolf Lodge, Hotel Vin, Lake Grapevine and neighboring Southlake, Colleyville, Coppell and Irving. The service naturally fits searches for a Grapevine airport limo, Grapevine wine tour limousine, luxury black car or party bus rental.",
            ]),
            ("The Convenient Grapevine Connection to DFW", [
                "Grapevine borders the north side of DFW Airport, but terminal loops, flight changes and resort transfer timing still reward advance planning. Our <a href=\"/dfw-airport-car-service/\">DFW car service</a> monitors the flight and communicates where to meet. A sedan works for executive arrivals, SUVs accommodate families and luggage, and Sprinters move convention teams without splitting the group.",
                "For meetings beyond Grapevine, reserve <a href=\"/dallas-corporate-car-service/\">corporate transportation</a> by the transfer or hour. We can connect Gaylord Texan, Las Colinas, downtown Dallas and Fort Worth on a single roadshow schedule using SH 114 and TX 121.",
            ]),
            ("Wine Tours, Resort Events and Holiday Traditions", [
                "An hourly stretch limo, SUV or Sprinter gives a Grapevine wine tour its own pace while the chauffeur handles each Main Street stop. Couples can pair a formal limousine with guest shuttle vehicles for winery, hotel or lakeside weddings. During the Christmas Capital of Texas season, a private car or group vehicle avoids repeated parking while visiting Main Street lights and resort attractions.",
                "Smaller parties may prefer a luxury SUV; six to twelve guests often fit an executive Sprinter; larger celebrations can request a party bus. Explore <a href=\"/dallas-party-bus/\">DFW party bus rental</a>, <a href=\"/dallas-wedding-transportation/\">wedding transportation</a>, or neighboring <a href=\"/limo-service-southlake-tx/\">Southlake limo service</a>.",
            ]),
            ("Grapevine Routes: Airport, Resort and Main Street", [
                "Grapevine is close to DFW, but “close” does not remove the need for a pickup plan. Airport arrivals need the airline, flight number and destination hotel or residence; departures need the terminal if known and a pickup time that accounts for the route into the airport. For a Gaylord Texan conference, we can plan a terminal-to-resort transfer, an evening dinner run and a return pickup as separate transfers or as one hourly schedule. That is simpler than asking every guest to navigate terminal and resort traffic on their own.",
                "Historic Main Street itineraries work best when stops are named in advance. A wine-tasting group may want a pickup at Hotel Vin, a sequence of tasting rooms, dinner and a final destination; a holiday group may combine Main Street lights with a resort attraction. The chauffeur follows the confirmed route while the group can enjoy the occasion without moving cars or assigning a driver. We can also connect Grapevine to Southlake, Las Colinas, downtown Dallas or Fort Worth through the SH 114 and TX 121 corridors.",
            ]),
            ("Capacity Advice for Grapevine Visitors and Groups", [
                "Choose an executive sedan for an individual executive or couple with light luggage. A luxury SUV is a comfortable choice for a family arriving at DFW, a small wedding party or a tasting group that needs more room. An executive Sprinter generally suits six to twelve people and is especially useful for convention teams, airport groups and winery itineraries because the passengers and their belongings stay together. Stretch limousines add a formal or celebratory feel; larger parties should ask whether a party bus is the better fit.",
                "Let us know about checked luggage, strollers, mobility needs, presentation materials, golf clubs or event supplies. Those details matter as much as the passenger total when matching a vehicle. We will provide capacity guidance before booking so a resort arrival or winery day begins with enough room, not a last-minute vehicle compromise.",
            ]),
            ("Grapevine Pricing and Peak-Date Reservations", [
                "We quote the trip in advance using the route, date, vehicle, number of stops and expected duration. A DFW-to-hotel ride is normally a flat transfer; a tasting itinerary, conference day or holiday lights outing is often more suitable for hourly service. The agreed price is transparent and does not rise simply because airport or holiday demand is high.",
                "Share arrival flights, hotel names, event agendas and desired pickup windows when requesting a quote. Christmas Capital dates, large Gaylord Texan conventions, wedding weekends and holiday evenings can have limited vehicle availability, so early reservations are prudent. For a spontaneous dinner or delayed travel plan, contact us for current availability and a clear quote before the reservation is finalized.",
            ]),
        ],
        "form_title": "Plan Grapevine Limo Service", "form_btn": "Get a Grapevine Quote",
        "service_opts": ["DFW Airport Transfer", "Wine / Main Street Tour", "Gaylord Texan / Convention", "Wedding Transportation", "Christmas Lights Tour", "Corporate / Hourly", "Lake / Group Event"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Stretch Limousine", "Executive Sprinter", "Party Bus"],
        "pickup_ph": "DFW terminal, Main Street, Gaylord Texan, or hotel", "city_val": "Grapevine TX",
        "why_title": "Why Grapevine Guests Ride With Us", "why": STD_WHY,
        "faq_title": "Grapevine Limo Service FAQ",
        "faqs": [
            ("Do you pick up at DFW Airport for Grapevine hotels?", "Yes. We monitor the flight, provide terminal pickup instructions and serve Grapevine hotels and resorts 24/7."),
            ("Can I book a Grapevine wine tour limo by the hour?", "Yes. Hourly service lets your group visit Main Street tasting rooms and dining stops with the same chauffeur and vehicle."),
            ("Do you provide group transportation to the Gaylord Texan?", "Yes. Executive Sprinters and larger vehicles are available for convention teams, resort guests and event groups, while sedans and SUVs suit individual arrivals."),
            ("Are Christmas lights and holiday tours available?", "Yes. Seasonal chauffeured tours can include Historic Main Street and Grapevine resort attractions. Early booking is recommended for peak holiday dates."),
            ("How should a Grapevine wine tour be booked?", "Wine tours are usually reserved by the hour so the same chauffeur and vehicle remain with the group between tasting rooms, dining and the final drop-off. Send the guest count, preferred stops and approximate timing so we can recommend an SUV, Sprinter, limousine or larger vehicle."),
            ("Can you coordinate DFW arrivals for a Gaylord Texan convention group?", "Yes. Provide each flight number, arrival window, passenger count and luggage estimate. We can plan individual executive pickups or group transfers and can also arrange scheduled transportation between the resort, dinners and off-site meetings."),
        ],
        "related": rel(dallas_related, "/limo-service-grapevine-tx/") + [("/limo-service-southlake-tx/", "Southlake Limo Service"), ("/limo-service-lewisville-tx/", "Lewisville Limo Service"), ("/car-service-irving-tx/", "Irving Car Service")],
    })

    # 26. Limo Service Southlake TX
    pages.append({
        "slug": "limo-service-southlake-tx",
        "title": "Limo Service Southlake TX | DFW Airport & Luxury Car Service | Purple Heart Limo",
        "meta": "Southlake limo and black car service for DFW airport, Town Square, weddings, executive travel and events. Luxury fleet, professional chauffeurs and flat rates.",
        "schema_name": "Purple Heart Limo — Limo Service Southlake TX",
        "image": "sedan-cadillac.webp",
        "areas": ["Southlake", "Westlake", "Grapevine", "Colleyville", "Keller", "Trophy Club"],
        "locality": "Southlake", "reviews": 96,
        "hub_slug": DAL_HUB[0], "hub_name": DAL_HUB[1], "crumb": "Southlake Limo Service",
        "badge": "✨ Town Square · Southlake, TX",
        "h1_main": "Limo Service", "h1_em": "Southlake, TX",
        "hero_p": "Discreet Southlake limo and black car service for DFW airport, executive schedules, Town Square dining, weddings and family occasions. Choose a refined sedan, luxury SUV, stretch limousine or Sprinter with 24/7 reservation support.",
        "stats": [("4.9★", "Average Rating"), ("DFW", "Airport Transfers"), ("24/7", "Support"), ("10+", "Minutes Early")],
        "svc_label": "Southlake Chauffeured Service", "svc_title": "Polished Transportation, Planned Around You",
        "svc_desc": "A quiet airport sedan, spacious family SUV or coordinated event fleet—matched to the Southlake trip rather than assigned at random.",
        "cards": [
            ("✈️", "DFW Airport Black Car", "Flight-aware transfers using SH 114 with vehicle choice based on luggage."),
            ("💼", "Executive Chauffeur", "Discreet hourly and point-to-point service for leaders, clients and roadshows."),
            ("🛍️", "Town Square Dining", "Door-to-door transportation for dinners, shopping and private celebrations."),
            ("💍", "Wedding Transportation", "Stretch limos, SUVs and Sprinters coordinated for couples and guests."),
            ("👨‍👩‍👧‍👦", "Family & School Occasions", "Professional rides for graduations, proms, galas and family airport travel."),
            ("🚐", "Private Group Travel", "Executive Sprinters for golf outings, events and multi-stop itineraries."),
        ],
        "body": [
            ("Southlake's Private Limo and Black Car Service", [
                "Southlake riders expect transportation to be punctual, presentable and unobtrusive. Purple Heart Limo provides that consistency for airport departures, executive calendars, formal occasions and evenings at Southlake Town Square. The chauffeur receives the itinerary in advance, the selected vehicle arrives prepared, and the quoted price does not change because local demand spikes.",
                "Service extends along Southlake Boulevard and SH 114 to Westlake, Trophy Club, Keller, Colleyville and Grapevine. Customers can reserve a Southlake limo rental for a celebration, luxury car service for a client, or private chauffeur service by the hour for a day containing several appointments.",
            ]),
            ("Southlake Airport Transportation for DFW and Love Field", [
                "Southlake's SH 114 access makes DFW International the closest major airport, and our <a href=\"/dfw-airport-car-service/\">DFW airport limo service</a> supports departures and flight-monitored arrivals at every terminal. Trips to <a href=\"/car-service-dallas-love-field/\">Dallas Love Field</a> are also available, with pickup timing planned around the longer route and expected traffic.",
                "Executive sedans are suited to solo passengers and couples. Luxury SUVs provide a more flexible choice for families, golf clubs and additional bags. A Sprinter keeps larger parties together and leaves more room than booking several cars. Meet-and-greet or other pickup details can be discussed when reserving.",
            ]),
            ("Executive Schedules, Weddings and Southlake Events", [
                "Hourly chauffeur service works well for board meetings, client dinners and roadshows that move between Southlake, Westlake, Las Colinas and Dallas. For weddings, charity events, prom and homecoming, a stretch limousine creates the occasion while SUVs and Sprinters solve wedding-party or guest logistics. Town Square dinners and milestone celebrations can be booked point-to-point or with the driver waiting.",
                "Review our <a href=\"/fleet.html\">chauffeured fleet</a>, arrange <a href=\"/dallas-corporate-car-service/\">corporate car service</a>, or expand an itinerary with <a href=\"/limo-service-grapevine-tx/\">Grapevine limousine service</a>. Larger celebrations can also use a <a href=\"/dallas-party-bus/\">DFW party bus</a>.",
            ]),
            ("Southlake Route Planning for Airport and Executive Days", [
                "For a Southlake airport departure, we start with the airline, flight number, terminal if known and the time you want to reach the airport. DFW is typically accessed along SH 114, while Love Field requires a longer cross-metro plan; neither trip is scheduled by a generic rideshare estimate. For arrivals, flight monitoring lets the chauffeur adjust to the actual landing rather than asking a passenger to coordinate while collecting bags. Pickup instructions and meet-and-greet preferences are confirmed in advance.",
                "A multi-stop executive day needs the same level of detail. A Westlake meeting, Town Square lunch, Las Colinas presentation and Dallas dinner may be best served by one hourly chauffeur rather than a chain of point-to-point bookings. Share addresses, appointment times, passenger changes and waiting periods. The chauffeur has a working itinerary, while the client has a quiet, consistent vehicle throughout the day.",
            ]),
            ("Southlake Fleet Recommendations and Practical Capacity", [
                "An executive sedan fits a solo airport traveler, a couple or a discreet client transfer. A luxury SUV provides useful room for family luggage, golf clubs, shopping bags or three to five passengers who want a more spacious ride. An executive Sprinter is the practical option for six to twelve people headed to a corporate dinner, golf outing, wedding or airport; it keeps the group together and reduces the need to coordinate multiple arrival times. A stretch limousine suits a formal entrance, while a larger celebration may call for a party bus.",
                "Before reserving, include passenger count, luggage, equipment, car seats and mobility needs. A capacity maximum is not always a comfortable airport configuration, especially after an international arrival or a family trip. We use those details to recommend the vehicle that fits the actual Southlake itinerary and explain alternatives if the preferred vehicle is not the best match.",
            ]),
            ("Southlake Booking and Flat-Rate Expectations", [
                "A Southlake limo or black car quote is based on the date, route, vehicle, number of stops and duration. Direct airport, office or restaurant transportation can be quoted as a transfer. A roadshow, shopping afternoon, wedding timeline or evening with a waiting chauffeur is generally quoted hourly. Pricing is confirmed before the ride, without rideshare-style surge changes caused by a busy Town Square evening, weather or a local event.",
                "Reserve early for weddings, gala dates, prom, graduation and peak travel periods if a specific vehicle matters to you. For airport service, add the flight information and luggage count; for formal events, add the timeline, venues and return window. Same-day availability can be checked, but we will give a clear answer on the available vehicle and quoted terms rather than making an uncertain promise.",
            ]),
        ],
        "form_title": "Reserve Southlake Limo Service", "form_btn": "Request a Southlake Quote",
        "service_opts": ["DFW Airport Transfer", "Love Field Transfer", "Executive / Corporate", "Wedding / Formal Event", "Town Square / Dinner", "Prom / Graduation", "Hourly Chauffeur"],
        "vehicle_opts": ["Executive Sedan", "Luxury SUV", "Stretch Limousine", "Executive Sprinter", "Party Bus"],
        "pickup_ph": "Southlake Town Square, home, office, hotel, or venue", "city_val": "Southlake TX",
        "why_title": "The Southlake Standard for Chauffeured Travel", "why": STD_WHY,
        "faq_title": "Southlake Limo Service FAQ",
        "faqs": [
            ("Do you offer Southlake black car service to DFW Airport?", "Yes. Transfers are available 24/7 with flight monitoring for arrivals and planned pickup times for departures from Southlake."),
            ("Can I hire a chauffeur by the hour in Southlake?", "Yes. Hourly service keeps the same chauffeur and vehicle available for meetings, dinners, shopping or any multi-stop itinerary."),
            ("Which vehicle should a Southlake family choose for airport travel?", "A luxury SUV is often best for a family and luggage; an executive Sprinter is better for a larger party or substantial baggage. We recommend the vehicle after reviewing passenger and bag counts."),
            ("Do you provide Southlake wedding and prom limos?", "Yes. Stretch limousines, SUVs, Sprinters and party buses are available for weddings, prom, homecoming, graduation and other formal occasions."),
            ("Is DFW or Love Field better for a Southlake airport transfer?", "Both airports are served. DFW is generally the closer option through the SH 114 corridor, while Love Field requires additional cross-metro travel time. Your airline, terminal and flight schedule let us set the right pickup plan rather than relying on a generic estimate."),
            ("Can a Southlake corporate itinerary include several cities?", "Yes. Hourly chauffeur service can cover a planned day through Southlake, Westlake, Las Colinas, Dallas, Grapevine or other DFW stops. Send the addresses, appointment times and passenger schedule so the vehicle and chauffeur can be reserved for the complete itinerary."),
        ],
        "related": rel(dallas_related, "/limo-service-southlake-tx/") + [("/limo-service-grapevine-tx/", "Grapevine Limo Service"), ("/limo-service-lewisville-tx/", "Lewisville Limo Service"), ("/limo-service-fort-worth-tx/", "Fort Worth Limo Service")],
    })

    return pages
