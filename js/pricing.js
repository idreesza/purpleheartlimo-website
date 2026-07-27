/* Purple Heart Limo — shared ride-class pricing (homepage widget + booking page).
   Flat rate covers the first 20 miles; each extra mile (rounded UP) is $2.
   If the estimated drive time exceeds 40 minutes, pricing switches to a
   2-hour minimum at the class hourly rate (hours = max(2, ceil(minutes/60))).
   Hourly rates reuse the existing booking-page hourly rates.
   NOTE FOR OWNER: pax/bag capacities marked estimated:true are placeholders
   from the spec defaults — confirm real capacities.
   NOTE: fleet.html, rates.html and es/fleet.html render their visible price
   labels from this table via /js/price-sync.js — edit rates HERE only.
   IMPORTANT: after ANY rate change here, run `python3 scripts/sync_seo_prices.py`
   to regenerate the SEO-only prices search engines read from the raw HTML
   (JSON-LD offers, FAQ answer text, meta description, no-JS span fallbacks). */
window.PHL_CLASSES = [
  { id: 'luxury-suv',     name: 'Luxury SUV',     flat: 190, hourly: 179, pax: 6, bags: 5,
    vehicle: 'Cadillac Escalade',
    photos: { exterior: 'images/ext-escalade.webp',
              interior: 'images/int-escalade.webp',
              trunk:    'images/trunk-escalade.webp' } },
  { id: 'business-suv',   name: 'Business SUV',   flat: 150, hourly: 149, pax: 6, bags: 5,
    vehicle: 'GMC Yukon Denali',
    photos: { exterior: 'images/ext-yukon.webp',
              interior: 'images/int-yukon.webp',
              trunk:    'images/trunk-yukon.webp' } },
  { id: 'luxury-sedan',   name: 'Luxury Sedan',   flat: 190, hourly: 229, pax: 3, bags: 2,
    vehicle: 'Mercedes S-Class',
    photos: { exterior: 'images/ext-sclass.webp',
              interior: 'images/int-sclass.webp',
              trunk:    'images/trunk-sclass.webp' } },
  { id: 'business-sedan', name: 'Business Sedan', flat: 120, hourly: 119, pax: 3, bags: 2,
    vehicle: 'Cadillac CTS',
    photos: { exterior: 'images/ext-cts.webp',
              interior: 'images/int-cts.webp',
              trunk:    'images/trunk-cts.webp' } }
];


/* Photo sets for larger vehicles (quoted "from" rates, no live pricing). */
window.PHL_GALLERY = {
  'Sprinter Van':  { exterior: 'images/ext-sprinter.webp',     interior: 'images/int-sprinter.webp',     trunk: 'images/trunk-sprinter.webp' },
  'Sprinter Jet':  { exterior: 'images/ext-jetsprinter.webp',  interior: 'images/int-jetsprinter.webp',  trunk: 'images/trunk-jetsprinter.webp' },
  'Stretch Sedan': { exterior: 'images/ext-stretchsedan.webp', interior: 'images/int-stretchsedan.webp', trunk: 'images/trunk-stretchsedan.webp' },
  'Stretch SUV':   { exterior: 'images/ext-stretchsuv.webp',   interior: 'images/int-stretchsuv.webp',   trunk: 'images/trunk-stretchsuv.webp' },
  'Party Bus':     { exterior: 'images/ext-partybus.webp',     interior: 'images/int-partybus.webp',     trunk: 'images/trunk-partybus.webp' },
  'Coach Bus':     { exterior: 'images/ext-coachbus.webp',     interior: 'images/int-coachbus.webp',     trunk: 'images/trunk-coachbus.webp' }
};

window.PHL_INCLUDED_MILES = 20;
window.PHL_PER_MILE = 2;
window.PHL_LONG_TRIP_MINUTES = 40;

window.phlGetClass = function (name) {
  return window.PHL_CLASSES.find(function (c) { return c.name === name || c.id === name; }) || null;
};

/* Returns {total, breakdown, hourlyApplied} or null when the class has no live pricing. */
window.phlComputeFare = function (cls, miles, minutes) {
  if (!cls) return null;
  if (minutes > window.PHL_LONG_TRIP_MINUTES) {
    var hours = Math.max(2, Math.ceil(minutes / 60));
    return {
      total: cls.hourly * hours,
      breakdown: hours + ' hr × $' + cls.hourly + '/hr (trips over 40 min use a 2-hour minimum)',
      hourlyApplied: true
    };
  }
  var extra = Math.max(0, Math.ceil(miles - window.PHL_INCLUDED_MILES));
  var total = cls.flat + extra * window.PHL_PER_MILE;
  return {
    total: total,
    breakdown: extra > 0
      ? '$' + cls.flat + ' first 20 mi + ' + extra + ' mi × $' + window.PHL_PER_MILE
      : 'Flat rate (up to 20 mi)',
    hourlyApplied: false
  };
};

/* ===== Hub positioning =====
   Vehicles operate out of Austin, Dallas–Fort Worth, and Houston hubs.
   Within PHL_HUB_FREE_MILES driving miles of the anchor hub, positioning is
   absorbed into the normal rate. Beyond that, the class hourly rate is
   charged for the round-trip hub drive time, on top of the normal fare. */
window.PHL_HUB_FREE_MILES = 60;

window.phlFetchPositioning = (function () {
  var cache = {};
  return async function (pickup, dropoff) {
    var k = JSON.stringify([pickup || '', dropoff || '']);
    if (cache[k]) return cache[k];
    var url = '/api/positioning?pickup=' + encodeURIComponent(pickup || '') +
              '&dropoff=' + encodeURIComponent(dropoff || '');
    var r = await fetch(url);
    var d = {};
    try { d = await r.json(); } catch (e) {}
    if (!r.ok || d.error) throw new Error(d.error || 'positioning unavailable');
    cache[k] = d;
    return d;
  };
})();

/* Returns {surcharge, hub, miles, minutes, hours} — surcharge is 0 when the
   trip is within the free radius of its anchor hub. */
window.phlComputePositioning = function (cls, pos) {
  if (!cls || !pos) return null;
  if (pos.miles <= window.PHL_HUB_FREE_MILES) {
    return { surcharge: 0, hub: pos.hub, miles: pos.miles, minutes: pos.minutes, hours: 0 };
  }
  var hours = (2 * pos.minutes) / 60; // round trip hub → location → hub
  var surcharge = Math.ceil(cls.hourly * hours);
  return { surcharge: surcharge, hub: pos.hub, miles: pos.miles, minutes: pos.minutes, hours: Math.round(hours * 10) / 10 };
};

window.phlFetchDistance = (function () {
  var cache = {};
  return async function (origin, destination) {
    var k = origin + '|' + destination;
    if (cache[k]) return cache[k];
    var r = await fetch('/api/distance?origin=' + encodeURIComponent(origin) + '&destination=' + encodeURIComponent(destination));
    var d = {};
    try { d = await r.json(); } catch (e) {}
    if (!r.ok || d.error) throw new Error(d.error || 'distance unavailable');
    cache[k] = d;
    return d;
  };
})();
