/* Purple Heart Limo — shared ride-class pricing (homepage widget + booking page).
   Flat rate covers the first 20 miles; each extra mile (rounded UP) is $2.
   If the estimated drive time exceeds 40 minutes, pricing switches to a
   2-hour minimum at the class hourly rate (hours = max(2, ceil(minutes/60))).
   Hourly rates reuse the existing booking-page hourly rates.
   NOTE FOR OWNER: pax/bag capacities marked estimated:true are placeholders
   from the spec defaults — confirm real capacities. Photos with photoPlaceholder
   flags are stock stand-ins — swap `interior`/`trunk` URLs with real photos. */
window.PHL_CLASSES = [
  { id: 'luxury-suv',     name: 'Luxury SUV',     flat: 190, hourly: 179, pax: 6, bags: 5,
    vehicle: 'Cadillac Escalade',
    photos: { exterior: 'images/luxsuv-escalade.webp',
              interior: 'https://images.unsplash.com/photo-1563720223185-11003d516935?w=640&q=70&auto=format',
              trunk:    'https://images.unsplash.com/photo-1606016159991-dfe4f2746ad5?w=640&q=70&auto=format' },
    photoPlaceholder: { interior: true, trunk: true } },
  { id: 'business-suv',   name: 'Business SUV',   flat: 150, hourly: 149, pax: 6, bags: 5,
    vehicle: 'GMC Yukon Denali',
    photos: { exterior: 'images/suv-yukon.webp',
              interior: 'https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?w=640&q=70&auto=format',
              trunk:    'https://images.unsplash.com/photo-1502877338535-766e1452684a?w=640&q=70&auto=format' },
    photoPlaceholder: { interior: true, trunk: true } },
  { id: 'luxury-sedan',   name: 'Luxury Sedan',   flat: 190, hourly: 229, pax: 3, bags: 2,
    vehicle: 'Mercedes S-Class',
    photos: { exterior: 'images/sclass.webp',
              interior: 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=640&q=70&auto=format',
              trunk:    'https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=640&q=70&auto=format' },
    photoPlaceholder: { interior: true, trunk: true } },
  { id: 'business-sedan', name: 'Business Sedan', flat: 120, hourly: 119, pax: 3, bags: 2,
    vehicle: 'Cadillac CTS',
    photos: { exterior: 'images/sedan-cadillac.webp',
              interior: 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=640&q=70&auto=format',
              trunk:    'https://images.unsplash.com/photo-1489824904134-891ab64532f1?w=640&q=70&auto=format' },
    photoPlaceholder: { interior: true, trunk: true } }
];

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
