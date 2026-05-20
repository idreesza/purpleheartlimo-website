#!/usr/bin/env python3
"""Generate Spanish (/es/) versions of key Purple Heart Limo pages.

- Walks visible text nodes (skips script/style)
- Applies a brand-specific EN->ES dictionary (longest-match first)
- Rewrites <html lang="en">, <title>, meta description, schema description
- Adds hreflang link tags to BOTH the EN original and the new ES page
- Rewrites canonical to ES URL
- Preserves all HTML structure, scripts, schemas, form names/IDs
"""
from __future__ import annotations
import re, json, shutil
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment

ROOT = Path(__file__).resolve().parent.parent
ES = ROOT / "es"

# ---- Per-page metadata overrides (title + meta description) -----------
PAGE_META = {
    "fleet.html": {
        "title": "Nuestra Flota | Purple Heart Limo | Sedanes, Limusinas y Party Buses TX",
        "desc": "Explora la flota de lujo de Purple Heart Limo — sedanes ejecutivos, limusinas, SUVs, sprinters y party buses en Austin, DFW y Houston.",
        "og_title": "Nuestra Flota | Purple Heart Limo | 9 Vehículos de Lujo · TX",
        "og_desc": "Sedanes ejecutivos, limusinas, SUVs, sprinters y party buses. Asegurados y con chofer profesional en Austin, DFW y Houston.",
    },
    "booking.html": {
        "title": "Reservar un Viaje | Purple Heart Limo | Austin · DFW · Houston",
        "desc": "Reserva tu limusina de lujo — cotización instantánea para aeropuerto, bodas y viajes corporativos en Austin, Dallas-Fort Worth y Houston.",
        "og_title": "Reservar Limusina de Lujo | Purple Heart Limo | Austin · DFW · Houston",
        "og_desc": "Cotización al instante con tarifa plana para aeropuerto, boda, corporativo y por hora. Sin precios inflados.",
    },
    "contact.html": {
        "title": "Contáctanos | Purple Heart Limo — Servicio de Limusina TX",
        "desc": "Contacta a Purple Heart Limo — servicio de limusina de lujo con dueño tejano en Austin, Dallas-Fort Worth y Houston.",
        "og_title": "Contacta a Purple Heart Limo | Servicio de Limusina TX",
        "og_desc": "Reservaciones 24/7 en Austin, DFW y Houston. Llama al (833) 740-0700.",
    },
    "limo-service-austin-tx/index.html": {
        "title": "Servicio de Limusina Austin TX | Purple Heart Limo | Lujo con Dueño Tejano",
        "desc": "Purple Heart Limo — el servicio premier de limusina y auto de lujo de Austin TX con dueño tejano. Aeropuerto, bodas, corporativo, graduación. Tarifas planas.",
    },
    "limo-service-dallas-tx/index.html": {
        "title": "Servicio de Limusina Dallas TX | Purple Heart Limo | Auto de Lujo DFW",
        "desc": "Purple Heart Limo — servicio de limusina y auto de lujo en Dallas-Fort Worth TX. Transporte DFW, bodas, corporativo, día de juego Cowboys.",
    },
    "limo-service-houston-tx/index.html": {
        "title": "Servicio de Limusina Houston TX | Purple Heart Limo | IAH HOU Auto de Lujo",
        "desc": "Purple Heart Limo — servicio de limusina y auto de lujo en Houston TX. Aeropuertos IAH y Hobby, bodas, corporativo, Galveston. Tarifas planas.",
    },
}

# ---- Comprehensive EN -> ES dictionary, ordered longest-first ---------
# (We sort by length descending at runtime so multi-word phrases match before single words.)
DICT = {
    # Navigation & buttons
    "Book a Ride": "Reservar un Viaje",
    "Book Now": "Reservar Ahora",
    "Book Online Now": "Reservar en Línea Ahora",
    "Book Your Ride": "Reservar tu Viaje",
    "Book Your Next Trip in Minutes": "Reserva tu Próximo Viaje en Minutos",
    "Book This Vehicle": "Reservar Este Vehículo",
    "Book Austin Limo Service": "Reservar Servicio de Limusina Austin",
    "Book Dallas Limo Service": "Reservar Servicio de Limusina Dallas",
    "Book Houston Limo Service": "Reservar Servicio de Limusina Houston",
    "Book Dallas Limo": "Reservar Limo Dallas",
    "Book Houston Limo": "Reservar Limo Houston",
    "Request Austin Limo Booking": "Solicitar Reserva de Limo Austin",
    "Request Dallas Limo Booking": "Solicitar Reserva de Limo Dallas",
    "Request Houston Limo Booking": "Solicitar Reserva de Limo Houston",
    "Send Message": "Enviar Mensaje",
    "Send a Message": "Envíanos un Mensaje",
    "Sending…": "Enviando…",
    "Sending...": "Enviando...",
    "Home": "Inicio",
    "Services": "Servicios",
    "Our Fleet": "Nuestra Flota",
    "Fleet": "Flota",
    "Rates": "Tarifas",
    "Pricing": "Precios",
    "Blog": "Blog",
    "Contact": "Contacto",
    "About Us": "Acerca de",
    "About": "Acerca de",
    "Book": "Reservar",
    "More": "Más",
    "Locations": "Ubicaciones",
    "Flight Tracker": "Rastreador de Vuelos",
    "Airport Transfer": "Traslado al Aeropuerto",
    "Wedding Limo": "Limusina para Boda",
    "Corporate Travel": "Viajes Corporativos",
    "Prom & Graduation": "Graduación y Prom",
    "Prom & Events": "Prom y Eventos",
    "Night Out & Party": "Noche y Fiesta",
    "Night Out / Event": "Noche / Evento",
    "Hourly Service": "Servicio por Hora",
    "Hourly Charter": "Charter por Hora",
    "Hours of Operation": "Horario de Atención",

    # Hero & headers
    "Get In Touch": "Contáctanos",
    "Contact Purple Heart Limo": "Contacta a Purple Heart Limo",
    "Speak with our reservation team 24/7. We're here to make every ride seamless across Austin, DFW & Houston.": "Habla con nuestro equipo de reservaciones 24/7. Estamos aquí para hacer cada viaje impecable en Austin, DFW y Houston.",
    "Reach Us Directly": "Contáctanos Directamente",
    "We're here": "Estamos aquí",
    "around the clock": "las 24 horas",
    "Tell us how we can": "Cuéntanos cómo podemos",
    "help": "ayudar",
    "Ready to Ride": "Listo para Viajar",
    "Ready to Book?": "¿Listo para Reservar?",
    "Choose Your Ride": "Elige tu Viaje",
    "Select any vehicle from the fleet above or call us to match you with the perfect option for your occasion.": "Selecciona cualquier vehículo de la flota o llámanos para encontrar la opción perfecta para tu ocasión.",
    "Skip the form — book your ride instantly online with transparent flat-rate pricing.": "Sáltate el formulario — reserva en línea al instante con tarifas planas transparentes.",
    "Our Vehicles": "Nuestros Vehículos",
    "The Purple Heart": "La",
    "Every vehicle meticulously maintained, professionally detailed, and ready to deliver the luxury experience you deserve.": "Cada vehículo meticulosamente mantenido, profesionalmente detallado y listo para entregar la experiencia de lujo que mereces.",
    "Good to Know": "Bueno Saber",
    "Fleet Policies & Standards": "Políticas y Estándares de la Flota",
    "Fleet Policies &amp; Standards": "Políticas y Estándares de la Flota",
    "The Purple Heart Limo standard isn't a marketing line — it's the same discipline applied to every vehicle, every ride.": "El estándar Purple Heart Limo no es un eslogan — es la misma disciplina aplicada a cada vehículo y cada viaje.",

    # Contact cards
    "Call or Text": "Llamar o Enviar Mensaje",
    "Available 24 hours a day, 7 days a week.": "Disponible 24 horas al día, 7 días a la semana.",
    "Email": "Correo Electrónico",
    "We typically respond within 1 hour during business hours.": "Normalmente respondemos en 1 hora durante horas de oficina.",
    "Message us on WhatsApp": "Envíanos un mensaje por WhatsApp",
    "Fast, convenient messaging from anywhere.": "Mensajería rápida y conveniente desde cualquier lugar.",
    "Service Areas": "Áreas de Servicio",
    "See full coverage map →": "Ver mapa completo de cobertura →",
    "Reservations": "Reservaciones",
    "Customer Support": "Atención al Cliente",
    "Office": "Oficina",
    "Mon–Fri, 8am–8pm CT": "Lun–Vie, 8am–8pm CT",

    # Form fields
    "Your Name *": "Tu Nombre *",
    "Your Name": "Tu Nombre",
    "Email Address *": "Correo Electrónico *",
    "Email Address": "Correo Electrónico",
    "Phone Number *": "Número de Teléfono *",
    "Phone Number": "Número de Teléfono",
    "Phone *": "Teléfono *",
    "Phone": "Teléfono",
    "Email *": "Correo *",
    "First Name *": "Nombre *",
    "First Name": "Nombre",
    "Last Name *": "Apellido *",
    "Last Name": "Apellido",
    "Subject": "Asunto",
    "Message *": "Mensaje *",
    "Message": "Mensaje",
    "How can we help you?": "¿Cómo podemos ayudarte?",
    "General Inquiry": "Consulta General",
    "Booking Question": "Pregunta sobre Reserva",
    "Quote Request": "Solicitar Cotización",
    "Corporate Account": "Cuenta Corporativa",
    "Wedding/Event": "Boda / Evento",
    "Wedding Transportation": "Transporte para Boda",
    "Weddings": "Bodas",
    "Wedding": "Boda",
    "Corporate / Executive": "Corporativo / Ejecutivo",
    "Corporate": "Corporativo",
    "Feedback": "Comentarios",
    "Service Type *": "Tipo de Servicio *",
    "Service Type": "Tipo de Servicio",
    "Vehicle *": "Vehículo *",
    "Vehicle": "Vehículo",
    "Select service...": "Seleccionar servicio...",
    "Select vehicle...": "Seleccionar vehículo...",
    "Pickup Date *": "Fecha de Recogida *",
    "Pickup Time *": "Hora de Recogida *",
    "Pickup Address *": "Dirección de Recogida *",
    "Dropoff Address *": "Dirección de Destino *",
    "Drop-off Location": "Destino",
    "Pickup Location": "Lugar de Recogida",
    "Pickup Date": "Fecha de Recogida",
    "Pickup Time": "Hora de Recogida",
    "Pickup Address": "Dirección de Recogida",
    "Dropoff Address": "Dirección de Destino",
    "Destination address": "Dirección de destino",
    "Additional Notes": "Notas Adicionales",
    "Number of passengers, stops, special requests...": "Número de pasajeros, paradas, solicitudes especiales...",

    # Vehicle types (form options + fleet titles)
    "Executive Sedan": "Sedán Ejecutivo",
    "Luxury Sedan": "Sedán de Lujo",
    "Executive SUV": "SUV Ejecutivo",
    "Luxury SUV": "SUV de Lujo",
    "Stretch Limousine": "Limusina Stretch",
    "Stretched SUV": "SUV Stretch",
    "Executive Sprinter": "Sprinter Ejecutivo",
    "Party Bus": "Party Bus",
    "Sprinter Jet": "Sprinter Jet",
    "Luxury Party Bus": "Party Bus de Lujo",

    # Service strip / city services
    "AUS Airport Transfer": "Traslado Aeropuerto AUS",
    "DFW Airport Transfer": "Traslado Aeropuerto DFW",
    "IAH Airport Transfer": "Traslado Aeropuerto IAH",
    "Hobby Airport Transfer": "Traslado Aeropuerto Hobby",
    "Love Field Airport Transfer": "Traslado Aeropuerto Love Field",
    "Galveston Transfer": "Traslado a Galveston",
    "Cowboys Game Day": "Día de Juego Cowboys",
    "SXSW / ACL / F1": "SXSW / ACL / F1",
    "Other": "Otro",
    "AUS Airport": "Aeropuerto AUS",
    "DFW Airport": "Aeropuerto DFW",
    "IAH Airport": "Aeropuerto IAH",
    "Hobby Airport": "Aeropuerto Hobby",
    "Love Field": "Love Field",
    "Galveston": "Galveston",
    "SXSW & ACL": "SXSW y ACL",
    "F1 at COTA": "F1 en COTA",
    "Uptown / Deep Ellum": "Uptown / Deep Ellum",
    "Events & Night Out": "Eventos y Noche",

    # Service card descriptions
    "Flight-monitored, flat rate, meet & greet at terminal": "Vuelo monitoreado, tarifa plana, recepción en la terminal",
    "Hill Country venues, city ceremonies, full-day packages": "Lugares en Hill Country, ceremonias en la ciudad, paquetes de día completo",
    "Executive travel, client pickups, corporate accounts": "Viajes ejecutivos, recogida de clientes, cuentas corporativas",
    "Safe, professional, multi-stop prom night packages": "Paquetes de prom seguros, profesionales y con múltiples paradas",
    "Event transport with no surge pricing, pre-booked flat rates": "Transporte de eventos sin precios inflados, tarifas planas pre-reservadas",
    "Dedicated COTA transport, group Sprinter packages": "Transporte dedicado a COTA, paquetes de Sprinter en grupo",
    "All terminals covered, flight monitored, meet & greet": "Todas las terminales cubiertas, vuelo monitoreado, recepción",
    "AT&T Stadium transport, pregame parking-free luxury": "Transporte al AT&T Stadium, lujo sin estacionamiento previo al juego",
    "Uptown Dallas, Legacy area, corporate campuses": "Uptown Dallas, área Legacy, campus corporativos",
    "DFW venue coverage, full-day packages available": "Cobertura de lugares DFW, paquetes de día completo disponibles",
    "Safe, stylish group nights out in Dallas": "Noches en grupo seguras y elegantes en Dallas",
    "Southwest & American, same flat-rate service": "Southwest y American, mismo servicio de tarifa plana",
    "Bush Intercontinental, all terminals, flight monitored": "Bush Intercontinental, todas las terminales, vuelo monitoreado",
    "William P. Hobby, flat rate, meet & greet service": "William P. Hobby, tarifa plana, recepción incluida",
    "Energy Corridor, Medical Center, Downtown Houston": "Energy Corridor, Medical Center, Downtown Houston",
    "Houston venues, The Woodlands, Sugar Land packages": "Lugares de Houston, The Woodlands, paquetes de Sugar Land",
    "Houston → Galveston flat-rate transfers and day trips": "Traslados con tarifa plana Houston → Galveston y excursiones de un día",
    "Midtown, Montrose, River Oaks — stylish group transport": "Midtown, Montrose, River Oaks — transporte grupal con estilo",

    # Why us cards (austin/dallas/houston/contact common)
    "Why Purple Heart": "Por Qué Purple Heart",
    "Austin's Texan-Owned Choice": "La Opción de Dueño Tejano en Austin",
    "Dallas-Fort Worth's Trusted Choice": "La Opción de Confianza en Dallas-Fort Worth",
    "Houston's Texan-Owned Choice": "La Opción de Dueño Tejano en Houston",
    "Texan-Owned": "Dueño Tejano",
    "Founded and operated by a U.S. military veteran. Mission discipline applied to every booking, every driver, every ride.": "Fundada y operada por un veterano militar de EE.UU. Disciplina de misión aplicada a cada reserva, cada chofer y cada viaje.",
    "U.S. military veteran operated. The same standards that kept people safe in service are applied to every ride in DFW.": "Operada por un veterano militar de EE.UU. Los mismos estándares que mantuvieron a la gente segura en servicio se aplican a cada viaje en DFW.",
    "U.S. military veteran operated. Discipline, punctuality, and professionalism on every Houston ride.": "Operada por un veterano militar de EE.UU. Disciplina, puntualidad y profesionalismo en cada viaje de Houston.",
    "Flat Rates": "Tarifas Planas",
    "No surge pricing. No surprise fees. The price at booking is the price you pay — regardless of event crowds or time of night.": "Sin precios inflados. Sin cargos sorpresa. El precio al reservar es el que pagas — sin importar la multitud del evento o la hora.",
    "No surge pricing during Cowboys games, concerts, or rush hour. One price, quoted upfront, never changes.": "Sin precios inflados durante juegos de los Cowboys, conciertos u hora pico. Un precio cotizado por adelantado que nunca cambia.",
    "No surge pricing in Houston traffic or during Rodeo season. Your quoted rate is your final rate.": "Sin precios inflados en el tráfico de Houston o durante la temporada de Rodeo. Tu tarifa cotizada es la final.",
    "Flight Monitoring": "Monitoreo de Vuelos",
    "DFW Flight Monitoring": "Monitoreo de Vuelos DFW",
    "IAH & HOU Monitoring": "Monitoreo IAH y HOU",
    "Airport pickups automatically adjust to real-time flight status. Your driver knows before you land.": "Las recogidas en el aeropuerto se ajustan automáticamente al estado del vuelo en tiempo real. Tu chofer lo sabe antes de que aterrices.",
    "Automatic adjustment to your real flight arrival. Your driver is waiting before you reach baggage claim.": "Ajuste automático a la llegada real de tu vuelo. Tu chofer está esperando antes de que llegues a la entrega de equipaje.",
    "Both Houston airports covered with real-time flight monitoring. Drivers adjust automatically.": "Ambos aeropuertos de Houston cubiertos con monitoreo de vuelos en tiempo real. Los choferes se ajustan automáticamente.",
    "Punctuality": "Puntualidad",
    "Drivers arrive 10+ minutes early. Proactive communication if anything changes. Late is not our standard.": "Los choferes llegan 10+ minutos antes. Comunicación proactiva si algo cambia. Llegar tarde no es nuestro estándar.",
    "Full Metroplex Coverage": "Cobertura Completa del Metroplex",
    "Full Metro Coverage": "Cobertura Completa del Metro",
    "Dallas, Fort Worth, Plano, Frisco, Irving, Arlington, and all surrounding cities — one company, seamlessly.": "Dallas, Fort Worth, Plano, Frisco, Irving, Arlington y todas las ciudades aledañas — una sola empresa, sin interrupciones.",
    "Houston, The Woodlands, Sugar Land, Katy, Pearland, Galveston — all seamlessly covered.": "Houston, The Woodlands, Sugar Land, Katy, Pearland, Galveston — todo cubierto sin interrupciones.",

    # City hero copy
    "Austin's most reliable luxury black car service — flat rates, professional chauffeurs, and zero surge pricing. Airport transfers, weddings, corporate travel, prom, and more. Available 24/7 across Austin and the entire metro area.": "El servicio de auto negro de lujo más confiable de Austin — tarifas planas, choferes profesionales y cero precios inflados. Traslados al aeropuerto, bodas, viajes corporativos, prom y más. Disponible 24/7 en todo Austin y el área metropolitana.",
    "DFW's reliable luxury black car service — flat rates, zero surge pricing, professional chauffeurs. DFW & Love Field airport transfers, Cowboys game day, corporate travel, weddings, and more across the entire Metroplex.": "El servicio confiable de auto negro de lujo de DFW — tarifas planas, cero precios inflados, choferes profesionales. Traslados a DFW y Love Field, día de juego Cowboys, viajes corporativos, bodas y más en todo el Metroplex.",
    "Houston's trusted luxury black car service — flat rates, professional chauffeurs, zero surge pricing. IAH & Hobby airport transfers, corporate travel, weddings, Galveston runs, and more across the entire Houston metro area.": "El servicio de auto negro de lujo de confianza de Houston — tarifas planas, choferes profesionales, cero precios inflados. Traslados a IAH y Hobby, viajes corporativos, bodas, viajes a Galveston y más en toda el área metropolitana de Houston.",
    "From AUS airport runs to Hill Country weddings to SXSW event transport — we've got Austin covered.": "De los traslados al aeropuerto AUS a bodas en Hill Country y transporte para SXSW — cubrimos todo Austin.",
    "From DFW terminal pickups to AT&T Stadium game day transport — we cover the entire Metroplex.": "De recogidas en terminales DFW al transporte al AT&T Stadium en día de juego — cubrimos todo el Metroplex.",
    "From IAH & Hobby airport pickups to Medical Center corporate travel to Galveston excursions — we cover all of Houston.": "De recogidas en IAH y Hobby a viajes corporativos al Medical Center y excursiones a Galveston — cubrimos todo Houston.",

    # Booking copy on city pages
    "Fill out the form — we'll confirm your booking and send details to info@purpleheartlimo.com": "Completa el formulario — confirmaremos tu reserva y enviaremos los detalles a info@purpleheartlimo.com",
    "Submit your request — we confirm via email and text to info@purpleheartlimo.com": "Envía tu solicitud — confirmamos por correo y mensaje a info@purpleheartlimo.com",
    "or call us directly": "o llámanos directamente",
    "Available 24/7": "Disponible 24/7",
    "Austin Services": "Servicios en Austin",
    "Dallas Services": "Servicios en Dallas",
    "Houston Services": "Servicios en Houston",
    "Every Ride You Need in Austin": "Cada Viaje que Necesitas en Austin",
    "Every Ride You Need in DFW": "Cada Viaje que Necesitas en DFW",
    "Every Ride You Need in Houston": "Cada Viaje que Necesitas en Houston",

    # Status messages
    "✓ Thank you! Your message has been sent. We'll get back to you shortly.": "✓ ¡Gracias! Tu mensaje ha sido enviado. Te responderemos pronto.",
    "Sorry, something went wrong. Please call us directly at (833) 740-0700.": "Lo sentimos, algo salió mal. Llámanos directamente al (833) 740-0700.",
    "✓ Booking request received! We'll confirm within 30 minutes. Check your email and phone.": "✓ ¡Solicitud de reserva recibida! Confirmaremos en 30 minutos. Revisa tu correo y teléfono.",
    "✓ Booking request received! We'll confirm within 30 minutes.": "✓ ¡Solicitud de reserva recibida! Confirmaremos en 30 minutos.",
    "Something went wrong. Please call us directly at (833) 740-0700.": "Algo salió mal. Llámanos directamente al (833) 740-0700.",
    "Something went wrong. Please call us at (833) 740-0700.": "Algo salió mal. Llámanos al (833) 740-0700.",

    # Footer
    "Texas Areas": "Áreas en Texas",
    "Company": "Empresa",
    "Legal": "Legal",
    "Privacy Policy": "Política de Privacidad",
    "Terms of Service": "Términos de Servicio",
    "Cancellation Policy": "Política de Cancelación",
    "Privacy": "Privacidad",
    "Terms": "Términos",
    "Cancellation": "Cancelación",
    "All rights reserved.": "Todos los derechos reservados.",
    "Texan-owned & operated in Texas.": "Con dueño tejano y operada en Texas.",
    "Texan-owned luxury limousine & black car service in Austin, Dallas-Fort Worth & Houston, Texas. No surge pricing. Flat rates. Professional chauffeurs.": "Servicio de limusina y auto negro de lujo con dueño tejano en Austin, Dallas-Fort Worth y Houston, Texas. Sin precios inflados. Tarifas planas. Choferes profesionales.",

    # Fleet specific
    "Vehicle 01 of 09": "Vehículo 01 de 09",
    "Vehicle 02 of 09 · Premium": "Vehículo 02 de 09 · Premium",
    "Vehicle 03 of 09": "Vehículo 03 de 09",
    "Vehicle 04 of 09": "Vehículo 04 de 09",
    "Vehicle 05 of 09 · Most Popular": "Vehículo 05 de 09 · Más Popular",
    "Vehicle 06 of 09": "Vehículo 06 de 09",
    "Vehicle 07 of 09": "Vehículo 07 de 09",
    "Vehicle 08 of 09": "Vehículo 08 de 09",
    "Vehicle 09 of 09 · Premium": "Vehículo 09 de 09 · Premium",
    "Up to 3 Passengers · 2 Bags": "Hasta 3 Pasajeros · 2 Maletas",
    "Up to 2 Passengers · 2 Bags": "Hasta 2 Pasajeros · 2 Maletas",
    "Up to 6 Passengers · 6 Bags": "Hasta 6 Pasajeros · 6 Maletas",
    "Up to 8 Passengers": "Hasta 8 Pasajeros",
    "Up to 10 Passengers · 6 Bags": "Hasta 10 Pasajeros · 6 Maletas",
    "Up to 10 Passengers": "Hasta 10 Pasajeros",
    "Up to 12 Passengers · 10 Bags": "Hasta 12 Pasajeros · 10 Maletas",
    "Up to 24 Passengers · 8 Bags": "Hasta 24 Pasajeros · 8 Maletas",
    "Up to 24 Passengers": "Hasta 24 Pasajeros",
    "Up to 14 Passengers · 10 Bags": "Hasta 14 Pasajeros · 10 Maletas",
    "12 Passengers · 10 Bags": "12 Pasajeros · 10 Maletas",
    "14 Passengers": "14 Pasajeros",
    "6 Passengers · 6 Bags": "6 Pasajeros · 6 Maletas",
    "Call Us": "Llámanos",
    "Sedan": "Sedán",
    "SUV": "SUV",
    "Limousine": "Limusina",
    "Sprinter": "Sprinter",
    "Jet": "Jet",
    # Fleet vehicle descriptions
    "Cadillac CTS — the definitive choice for solo business travel, executive airport transfers, and point-to-point rides where a professional first impression matters. Sleek, silent, and impeccably clean every time.": "Cadillac CTS — la elección definitiva para viajes de negocios individuales, traslados ejecutivos al aeropuerto y viajes punto a punto donde importa una primera impresión profesional. Elegante, silencioso e impecablemente limpio cada vez.",
    "Mercedes-Benz S-Class — iconic elegance, Burmester sound, massaging seats, ambient lighting and a privacy partition. The definition of effortless premium business class.": "Mercedes-Benz Clase S — elegancia icónica, sonido Burmester, asientos con masaje, iluminación ambiental y mampara de privacidad. La definición de clase ejecutiva premium sin esfuerzo.",
    "GMC Yukon Denali — commanding presence, spacious 3-row seating, panoramic views, and premium sound. Ideal for small groups, family airport runs, and corporate transfers with luggage.": "GMC Yukon Denali — presencia imponente, espaciosos asientos de 3 filas, vistas panorámicas y sonido premium. Ideal para grupos pequeños, viajes familiares al aeropuerto y traslados corporativos con equipaje.",
    "Cadillac Escalade Platinum — premium captain seats, rear entertainment, ambient lighting and a commanding profile. The pinnacle of full-size luxury SUV travel for VIP groups.": "Cadillac Escalade Platinum — asientos capitán premium, entretenimiento trasero, iluminación ambiental y un perfil imponente. El máximo del viaje en SUV de lujo full-size para grupos VIP.",
    "Lincoln Town Car Stretch — the classic icon of luxury transportation. Perfect for weddings, proms, milestone birthdays and any occasion that calls for an unforgettable grand arrival.": "Lincoln Town Car Stretch — el icono clásico del transporte de lujo. Perfecto para bodas, prom, cumpleaños importantes y cualquier ocasión que requiera una llegada inolvidable.",
    "Lincoln Navigator Stretch — large luxury groups in stretched luxury. Premium bar, LED lighting, full audio system. Bachelor / bachelorette ready and a statement arrival for any event.": "Lincoln Navigator Stretch — grupos grandes en lujo stretch. Bar premium, iluminación LED, sistema de audio completo. Listo para despedidas de soltero/a y una llegada de impacto para cualquier evento.",
    "Mercedes Sprinter — the workhorse of group luxury travel. Tall interior, easy boarding, USB charging and Wi-Fi available. Ideal for corporate roadshows, airport groups, and Hill Country tours.": "Mercedes Sprinter — el caballo de batalla del viaje de lujo grupal. Interior alto, fácil abordaje, carga USB y Wi-Fi disponibles. Ideal para roadshows corporativos, grupos al aeropuerto y tours por Hill Country.",
    "Ford Transit Party Bus — the ultimate group experience on wheels. Premium sound, LED lighting, and a full bar setup. Concerts, birthdays, nights out — BYOB welcome and cooler space included.": "Ford Transit Party Bus — la experiencia grupal definitiva sobre ruedas. Sonido premium, iluminación LED y barra completa. Conciertos, cumpleaños, noches — bienvenido a traer tus bebidas (BYOB) y espacio para hielera incluido.",
    "Mercedes Jet-Class — first-class jet interior on the road. Reclining captain chairs, TVs, conference table, Wi-Fi and power. The top-tier solution for corporate & VIP transit.": "Mercedes Jet-Class — interior de jet de primera clase en la carretera. Sillas capitán reclinables, TVs, mesa de conferencia, Wi-Fi y energía. La solución de mayor nivel para tránsito corporativo y VIP.",
    "From $119.": "Desde $119.",
    "From $229.": "Desde $229.",
    "From $149.": "Desde $149.",
    "From $179.": "Desde $179.",
    "From $169.": "Desde $169.",
    "From $279.": "Desde $279.",
    "From $159.": "Desde $159.",
    "From $225.": "Desde $225.",
    "From $190.": "Desde $190.",
    # Chips / features
    "Leather Interior": "Interior de Cuero",
    "Climate Control": "Control de Clima",
    "Bottled Water": "Agua Embotellada",
    "Suit & Tie Chauffeur": "Chofer con Traje",
    "Suit &amp; Tie Chauffeur": "Chofer con Traje",
    "Wi-Fi": "Wi-Fi",
    "Phone Chargers": "Cargadores de Teléfono",
    "Top-Tier Mercedes Comfort": "Comodidad Mercedes de Alto Nivel",
    "Privacy Partition": "Mampara de Privacidad",
    "Rear Climate": "Clima Trasero",
    "Premium Leather": "Cuero Premium",
    "Ambient Lighting": "Iluminación Ambiental",
    "VIP / Executive Ready": "Listo para VIP / Ejecutivo",
    "3-Row Seating": "Asientos de 3 Filas",
    "Tinted Windows": "Ventanas Polarizadas",
    "Family-Friendly": "Familiar",
    "Airport-Ready": "Listo para Aeropuerto",
    "Escalade Platinum Trim": "Escalade Platinum Trim",
    "Captain Seats": "Asientos Capitán",
    "Rear Entertainment": "Entretenimiento Trasero",
    "VIP Group Transport": "Transporte VIP de Grupo",
    "Premium Sound": "Sonido Premium",
    "Wet Bar": "Barra",
    "Mood Lighting": "Iluminación Ambiental",
    "Weddings & Proms": "Bodas y Prom",
    "Weddings &amp; Proms": "Bodas y Prom",
    "Photos Welcome": "Bienvenidas las Fotos",
    "Premium Bar": "Barra Premium",
    "LED Lighting": "Iluminación LED",
    "Full Audio": "Audio Completo",
    "Bachelor / Bachelorette": "Despedida de Soltero/a",
    "Statement Arrival": "Llegada de Impacto",
    "Tall Interior": "Interior Alto",
    "Easy Boarding": "Fácil Abordaje",
    "USB Charging": "Carga USB",
    "Wi-Fi Available": "Wi-Fi Disponible",
    "Corporate Roadshows": "Roadshows Corporativos",
    "Bar Setup": "Barra Instalada",
    "BYOB · Cooler Space": "BYOB · Espacio para Hielera",
    "Party-Ready": "Listo para Fiesta",
    "First-Class Jet Interior": "Interior de Jet Primera Clase",
    "Reclining Captain Chairs": "Sillas Capitán Reclinables",
    "TVs · Conference Table": "TVs · Mesa de Conferencia",
    "Wi-Fi & Power": "Wi-Fi y Energía",
    "Wi-Fi &amp; Power": "Wi-Fi y Energía",
    "Top-Tier VIP": "VIP de Alto Nivel",
    # Fleet policies
    "Cleanliness Standard": "Estándar de Limpieza",
    "Every vehicle is professionally detailed and white-glove inspected before each trip. You will never step into a vehicle that doesn't meet our standard — because we don't allow that to happen.": "Cada vehículo es profesionalmente detallado e inspeccionado con guante blanco antes de cada viaje. Nunca entrarás a un vehículo que no cumpla nuestro estándar — porque no permitimos que eso suceda.",
    "Maintenance Schedule": "Programa de Mantenimiento",
    "All vehicles follow strict preventative maintenance schedules and are inspected by certified mechanics regularly. Mechanical reliability is not optional when clients depend on you.": "Todos los vehículos siguen estrictos programas de mantenimiento preventivo y son inspeccionados regularmente por mecánicos certificados. La fiabilidad mecánica no es opcional cuando los clientes dependen de ti.",
    "Non-Smoking Policy": "Política Libre de Humo",
    "All Purple Heart Limo vehicles are strictly non-smoking. Every client steps into a fresh, clean environment — no exceptions, no matter who rode before them.": "Todos los vehículos Purple Heart Limo son estrictamente libres de humo. Cada cliente entra a un ambiente fresco y limpio — sin excepciones, sin importar quién viajó antes.",
    "Complimentary Amenities": "Amenidades de Cortesía",
    "Every vehicle is stocked with complimentary bottled water. Select vehicles include additional amenities — ask at booking for specific vehicle setups.": "Cada vehículo está equipado con agua embotellada de cortesía. Vehículos selectos incluyen amenidades adicionales — pregunta al reservar por configuraciones específicas.",
    "Insurance & Licensing": "Seguro y Licencias",
    "Insurance &amp; Licensing": "Seguro y Licencias",
    "All vehicles are commercially licensed, properly insured, and compliant with state and federal transportation regulations. You ride protected.": "Todos los vehículos están licenciados comercialmente, adecuadamente asegurados y cumplen con regulaciones estatales y federales de transporte. Viajas protegido.",
    "Professional Chauffeurs": "Choferes Profesionales",
    "Every driver is background-checked, licensed, and trained. Uniformed, professional, and discreet — your chauffeur understands that this is your ride, not theirs.": "Cada chofer pasa verificación de antecedentes, está licenciado y capacitado. Uniformado, profesional y discreto — tu chofer entiende que este es tu viaje, no el suyo.",

    # Stats
    "Average Rating": "Calificación Promedio",
    "Austin Reviews": "Reseñas de Austin",
    "Available": "Disponible",
    "Surge Fees": "Cargos Inflados",
    "Airport Covered": "Aeropuerto Cubierto",
    "& HOU Covered": "y HOU Cubiertos",

    # Booking.html specifics
    "Chat on WhatsApp": "Chatear en WhatsApp",
    "Call": "Llamar",
    # Common short
    "Texan Owned · Est. 2020": "Dueño Tejano · Fundada 2020",
    "Texan Owned · TX": "Dueño Tejano · TX",
    "Texan-Owned · Austin, TX": "Dueño Tejano · Austin, TX",
    "Texan-Owned · Dallas-Fort Worth, TX": "Dueño Tejano · Dallas-Fort Worth, TX",
    "Texan-Owned · Houston, TX": "Dueño Tejano · Houston, TX",
    "Limo Service": "Servicio de Limusina",
    "Texan-owned luxury limo service in Austin TX": "Servicio de limusina de lujo con dueño tejano en Austin TX",
    "Texan-owned luxury limo service in Dallas-Fort Worth TX": "Servicio de limusina de lujo con dueño tejano en Dallas-Fort Worth TX",
    "Texan-owned luxury limo service in Dallas TX": "Servicio de limusina de lujo con dueño tejano en Dallas TX",
    "Texan-owned luxury limo service in Houston TX": "Servicio de limusina de lujo con dueño tejano en Houston TX",
    "Contact Purple Heart Limo, Texan-owned luxury limousine service in Austin, DFW & Houston.": "Contacta a Purple Heart Limo, servicio de limusina de lujo con dueño tejano en Austin, DFW y Houston.",
    "Our Vehicles": "Nuestros Vehículos",
    "Dallas-Fort Worth, TX": "Dallas-Fort Worth, TX",
    "Limo Service Austin, TX": "Servicio de Limusina Austin, TX",
    "Limo Service Dallas-Fort Worth, TX": "Servicio de Limusina Dallas-Fort Worth, TX",
    "Limo Service Houston, TX": "Servicio de Limusina Houston, TX",
    "AUS": "AUS",
    "DFW": "DFW",
    "IAH": "IAH",
    "Austin, TX": "Austin, TX",
    "Houston, TX": "Houston, TX",
    "Dallas-Fort Worth": "Dallas-Fort Worth",
}

# Phrases that appear inside HTML attributes (placeholder, alt, aria-label, etc.)
ATTR_DICT = {
    "Open navigation menu": "Abrir menú de navegación",
    "John": "Juan",
    "Smith": "García",
    "you@email.com": "tu@correo.com",
    "Destination address": "Dirección de destino",
    "Number of passengers, stops, special requests...": "Número de pasajeros, paradas, solicitudes especiales...",
    "123 Main St, Austin TX or AUS Airport": "Calle Principal 123, Austin TX o Aeropuerto AUS",
    "123 Main St, Dallas TX or DFW Airport Terminal": "Calle Principal 123, Dallas TX o Terminal DFW",
    "123 Main St, Houston TX or IAH Airport Terminal": "Calle Principal 123, Houston TX o Terminal IAH",
    "How can we help you?": "¿Cómo podemos ayudarte?",
    "Purple Heart Limo Logo": "Logo de Purple Heart Limo",
    "Purple Heart Limo": "Purple Heart Limo",
    "WhatsApp": "WhatsApp",
    "Chat on WhatsApp": "Chatear en WhatsApp",
    "Send us a text": "Envíanos un mensaje",
    "Cadillac CTS Executive Sedan — Purple Heart Limo": "Sedán Ejecutivo Cadillac CTS — Purple Heart Limo",
    "Mercedes-Benz S-Class Luxury Sedan — Purple Heart Limo": "Sedán de Lujo Mercedes-Benz Clase S — Purple Heart Limo",
    "GMC Yukon Denali Executive SUV — Purple Heart Limo": "SUV Ejecutivo GMC Yukon Denali — Purple Heart Limo",
    "Cadillac Escalade Luxury SUV — Purple Heart Limo": "SUV de Lujo Cadillac Escalade — Purple Heart Limo",
    "Lincoln Town Car Stretch Limousine — Purple Heart Limo": "Limusina Stretch Lincoln Town Car — Purple Heart Limo",
    "Lincoln Navigator Stretched SUV — Purple Heart Limo": "SUV Stretch Lincoln Navigator — Purple Heart Limo",
    "Mercedes Executive Sprinter Van — Purple Heart Limo": "Sprinter Ejecutivo Mercedes — Purple Heart Limo",
    "Ford Transit Luxury Party Bus — Purple Heart Limo": "Party Bus de Lujo Ford Transit — Purple Heart Limo",
    "Mercedes Sprinter Jet-Class — Purple Heart Limo": "Sprinter Jet-Class Mercedes — Purple Heart Limo",
}

# Build sorted phrase list (longest first to avoid partial matches)
SORTED_PHRASES = sorted(DICT.items(), key=lambda kv: (-len(kv[0]), kv[0]))
SORTED_ATTRS = sorted(ATTR_DICT.items(), key=lambda kv: (-len(kv[0]), kv[0]))


def translate_string(s: str, table) -> str:
    if not s or not s.strip():
        return s
    # Pass 1: full-string match
    stripped = s.strip()
    for en, es in table:
        if stripped == en:
            return s.replace(en, es, 1)
    # Pass 2: substring replace using placeholders so already-translated text
    # is not re-scanned (prevents e.g. "Contact" matching inside "Contacta").
    out = s
    placeholders = {}
    for i, (en, es) in enumerate(table):
        if en and en in out:
            ph = f"\x00PH{i}\x00"
            placeholders[ph] = es
            out = out.replace(en, ph)
    for ph, es in placeholders.items():
        out = out.replace(ph, es)
    return out


def translate_text_nodes(soup: BeautifulSoup):
    SKIP = {"script", "style", "noscript", "title"}
    for el in soup.find_all(string=True):
        if isinstance(el, Comment):
            continue
        parent = el.parent
        if not parent or parent.name in SKIP:
            continue
        new = translate_string(str(el), SORTED_PHRASES)
        if new != str(el):
            el.replace_with(NavigableString(new))


def translate_attrs(soup: BeautifulSoup):
    targets = ("placeholder", "alt", "aria-label", "title")
    for el in soup.find_all(True):
        for attr in targets:
            if attr in el.attrs and isinstance(el.attrs[attr], str):
                el.attrs[attr] = translate_string(el.attrs[attr], SORTED_ATTRS)
                el.attrs[attr] = translate_string(el.attrs[attr], SORTED_PHRASES)


def make_es_url(en_url: str) -> str:
    """https://purpleheartlimo.com/foo.html -> https://purpleheartlimo.com/es/foo.html"""
    if en_url.startswith("https://purpleheartlimo.com/"):
        path = en_url[len("https://purpleheartlimo.com/"):]
        return f"https://purpleheartlimo.com/es/{path}"
    return en_url


def update_schema_descriptions(soup: BeautifulSoup):
    """Translate `description` and add `inLanguage` to JSON-LD blocks."""
    for s in soup.find_all("script", {"type": "application/ld+json"}):
        if not s.string:
            continue
        try:
            data = json.loads(s.string)
        except Exception:
            continue

        def walk(obj):
            if isinstance(obj, dict):
                if "description" in obj and isinstance(obj["description"], str):
                    obj["description"] = translate_string(obj["description"], SORTED_PHRASES)
                obj["inLanguage"] = "es"
                if "url" in obj and isinstance(obj["url"], str):
                    obj["url"] = make_es_url(obj["url"])
                if "item" in obj and isinstance(obj["item"], str):
                    obj["item"] = make_es_url(obj["item"])
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for v in obj:
                    walk(v)
        walk(data)
        s.string.replace_with(json.dumps(data, ensure_ascii=False))


def add_hreflang(soup: BeautifulSoup, en_url: str, es_url: str):
    """Add hreflang alternate link tags in <head>."""
    head = soup.head
    if not head:
        return
    # Remove existing hreflang to avoid duplicates
    for link in head.find_all("link", rel="alternate", hreflang=True):
        link.decompose()
    for hreflang, href in (("en", en_url), ("es", es_url), ("x-default", en_url)):
        tag = soup.new_tag("link", rel="alternate", hreflang=hreflang, href=href)
        head.append(tag)


def add_language_link_to_nav(soup: BeautifulSoup, en_path: str):
    """Add an 'English' switcher to ES pages — handles both nav layouts."""
    en_href = "/" + en_path
    # 1) Mobile menu (booking/fleet/contact)
    mm = soup.find(id="mobile-menu")
    if mm:
        btn_html = (
            f'<a href="{en_href}" '
            'style="display:flex;align-items:center;justify-content:center;gap:8px;width:100%;'
            'padding:12px;margin-bottom:12px;background:#2D0045;color:#fff;border:none;'
            'border-radius:8px;font-size:0.9rem;font-weight:700;letter-spacing:0.08em;text-decoration:none;">'
            '🌐 English</a>'
        )
        mm.insert(0, BeautifulSoup(btn_html, "html.parser"))

    # 2) nav-links UL (city pages use this for the mobile drawer + desktop)
    nl = soup.find("ul", id="navLinks") or soup.find("ul", class_="nav-links")
    if nl:
        li_html = (
            f'<li><a href="{en_href}" '
            'style="color:#C9A84C;font-weight:700;letter-spacing:0.08em;">🌐 English</a></li>'
        )
        new_li = BeautifulSoup(li_html, "html.parser")
        nl.insert(0, new_li)

    # 3) Desktop nav-cta pill (all pages have this)
    cta = soup.find("div", class_="nav-cta")
    if cta and not soup.find(id="lang-toggle"):
        nav_el = soup.find("nav")
        is_light = bool(nav_el and "navbar" in (nav_el.get("class") or []))
        border = "rgba(0,0,0,0.15)" if is_light else "rgba(255,255,255,0.25)"
        color = "#2D0045" if is_light else "#C9A84C"
        pill_html = (
            f'<a href="{en_href}" id="lang-toggle" '
            f'style="background:none;border:1.5px solid {border};'
            'border-radius:20px;padding:5px 12px;font-size:0.72rem;font-weight:700;'
            f'letter-spacing:0.08em;color:{color};display:inline-flex;align-items:center;'
            'gap:5px;text-decoration:none;">🌐 EN</a>'
        )
        cta.insert(0, BeautifulSoup(pill_html, "html.parser"))


# Hand-translated fleet panel H2s (cleanly handles split em tags)
FLEET_H2_ES = {
    "panel-sedan":     ("Sedán", "Ejecutivo"),
    "panel-luxsedan":  ("Sedán", "de Lujo"),
    "panel-execsuv":   ("SUV", "Ejecutivo"),
    "panel-suv":       ("SUV", "de Lujo"),
    "panel-stretch":   ("Limusina", "Stretch"),
    "panel-stretchsuv":("SUV", "Stretch"),
    "panel-sprinter":  ("Sprinter", "Ejecutivo"),
    "panel-partybus":  ("Party", "Bus"),
    "panel-jet":       ("Sprinter", "Jet"),
}
def fix_fleet_h2s(soup: BeautifulSoup):
    for panel_id, (prefix, italic) in FLEET_H2_ES.items():
        panel = soup.find(id=panel_id)
        if not panel:
            continue
        h2 = panel.find("h2")
        if not h2:
            continue
        h2.clear()
        h2.append(NavigableString(prefix + " "))
        em = soup.new_tag("em")
        em.string = italic
        h2.append(em)


# Runtime JS strings that need translation in ES copies
JS_STRINGS = {
    "Sending...": "Enviando...",
    "Sending…": "Enviando…",
    "✓ Booking request received! We'll confirm within 30 minutes. Check your email and phone.":
        "✓ ¡Solicitud de reserva recibida! Confirmaremos en 30 minutos. Revisa tu correo y teléfono.",
    "✓ Booking request received! We'll confirm within 30 minutes.":
        "✓ ¡Solicitud de reserva recibida! Confirmaremos en 30 minutos.",
    "Something went wrong. Please call us directly at (833) 740-0700.":
        "Algo salió mal. Llámanos directamente al (833) 740-0700.",
    "Something went wrong. Please call us at (833) 740-0700.":
        "Algo salió mal. Llámanos al (833) 740-0700.",
    "Request Austin Limo Booking": "Solicitar Reserva de Limo Austin",
    "Request Dallas Limo Booking": "Solicitar Reserva de Limo Dallas",
    "Request Houston Limo Booking": "Solicitar Reserva de Limo Houston",
    "✓ Thank you! Your message has been sent. We'll get back to you shortly.":
        "✓ ¡Gracias! Tu mensaje ha sido enviado. Te responderemos pronto.",
    "Sorry, something went wrong. Please call us directly at (833) 740-0700.":
        "Lo sentimos, algo salió mal. Llámanos directamente al (833) 740-0700.",
    "Send Message": "Enviar Mensaje",
}
def translate_js_strings(html: str) -> str:
    """Replace runtime JS string literals (quoted) inside the entire HTML."""
    for en, es in JS_STRINGS.items():
        # Match inside both single and double quotes
        html = html.replace("'" + en + "'", "'" + es.replace("'", "\\'") + "'")
        html = html.replace('"' + en + '"', '"' + es.replace('"', '\\"') + '"')
    return html


def translate_page(rel_path: str):
    """rel_path is relative to ROOT (e.g. 'fleet.html' or 'limo-service-austin-tx/index.html')."""
    src = ROOT / rel_path
    dst = ES / rel_path
    dst.parent.mkdir(parents=True, exist_ok=True)

    html = src.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "lxml")

    # 1) <html lang="es">
    if soup.html:
        soup.html["lang"] = "es"

    # 2) Title & meta
    meta = PAGE_META.get(rel_path, {})
    if soup.title and meta.get("title"):
        soup.title.string = meta["title"]
    for name in ("description",):
        tag = soup.find("meta", attrs={"name": name})
        if tag and meta.get("desc"):
            tag["content"] = meta["desc"]
    # OG / Twitter
    for prop, key in (("og:title", "og_title"), ("og:description", "og_desc"),
                       ("twitter:title", "og_title"), ("twitter:description", "og_desc")):
        if not meta.get(key):
            continue
        tag = soup.find("meta", attrs={"property": prop}) or soup.find("meta", attrs={"name": prop})
        if tag:
            tag["content"] = meta[key]

    # 3) Canonical -> ES
    canon = soup.find("link", rel="canonical")
    en_canon = None
    if canon and canon.get("href"):
        en_canon = canon["href"]
        canon["href"] = make_es_url(en_canon)

    # 4) og:url -> ES
    ogu = soup.find("meta", attrs={"property": "og:url"})
    if ogu and ogu.get("content"):
        ogu["content"] = make_es_url(ogu["content"])

    # 5) Translate text nodes & attributes
    translate_text_nodes(soup)
    translate_attrs(soup)

    # 6) Schema descriptions
    update_schema_descriptions(soup)

    # 6b) Fleet panel H2s — clean Spanish word order
    if rel_path == "fleet.html":
        fix_fleet_h2s(soup)

    # 7) Add hreflang
    if en_canon:
        add_hreflang(soup, en_canon, make_es_url(en_canon))

    # 8) Add EN switcher link in nav
    add_language_link_to_nav(soup, rel_path)

    # 9) Set body data-lang attribute (so JS can detect)
    if soup.body:
        soup.body["data-lang"] = "es"

    # 10) JS string substitution (script bodies were skipped during DOM walk)
    final_html = translate_js_strings(str(soup))
    dst.write_text(final_html, encoding="utf-8")
    print(f"  ✓ {rel_path} -> es/{rel_path}")


def add_hreflang_to_en(rel_path: str):
    """Add hreflang tags to the EN original so search engines know about ES alternate."""
    src = ROOT / rel_path
    html = src.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "lxml")
    canon = soup.find("link", rel="canonical")
    if not canon or not canon.get("href"):
        return
    en_url = canon["href"]
    es_url = make_es_url(en_url)
    add_hreflang(soup, en_url, es_url)
    src.write_text(str(soup), encoding="utf-8")
    print(f"  ✓ Added hreflang to EN: {rel_path}")


if __name__ == "__main__":
    pages = list(PAGE_META.keys())
    print(f"Translating {len(pages)} pages to /es/ ...")
    ES.mkdir(exist_ok=True)
    for p in pages:
        translate_page(p)
    print("\nAdding hreflang tags to EN originals...")
    # Also add hreflang to homepage (index.html)
    for p in pages + ["index.html"]:
        try:
            add_hreflang_to_en(p)
        except Exception as e:
            print(f"  ! {p}: {e}")
    print("\nDone.")
