/* Purple Heart Limo — renders price labels on display-only pages
   (fleet.html, rates.html, es/fleet.html) from the shared rate table in
   /js/pricing.js (window.PHL_CLASSES). Include pricing.js BEFORE this file.

   Markup contract (static text inside the span is the no-JS fallback):
     <span data-phl-from="business-sedan">119</span>   → min(flat, hourly)
     <span data-phl-flat="business-sedan">120</span>   → flat rate
     <span data-phl-hourly="business-sedan">119</span> → hourly rate

   Changing a flat/hourly rate in js/pricing.js updates these pages
   automatically — no HTML edits needed. */
(function () {
  function cls(id) {
    return (window.PHL_CLASSES || []).find(function (c) { return c.id === id; }) || null;
  }
  function set(attr, pick) {
    document.querySelectorAll('[' + attr + ']').forEach(function (el) {
      var c = cls(el.getAttribute(attr));
      if (c) el.textContent = pick(c);
    });
  }
  function run() {
    set('data-phl-from', function (c) { return Math.min(c.flat, c.hourly); });
    set('data-phl-flat', function (c) { return c.flat; });
    set('data-phl-hourly', function (c) { return c.hourly; });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();
