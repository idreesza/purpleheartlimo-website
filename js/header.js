/* Unified header — safe language toggle shared across pages.
   Navigates to a Spanish twin when one exists (ES_PAGES); otherwise
   just flips the EN/ES label without errors. Dropdown open/close is
   handled by js/nav-dropdown.js; the mobile menu by each page's
   toggleMenu(). */
(function () {
  var ES_PAGES = ['/fleet.html', '/booking.html', '/contact.html', '/limo-service-austin-tx/', '/limo-service-dallas-tx/', '/limo-service-houston-tx/'];

  function _altUrlForLang(targetLang) {
    var path = window.location.pathname;
    if (path.endsWith('/index.html')) path = path.slice(0, -'index.html'.length);
    var isEs = path.startsWith('/es/');
    var bare = isEs ? path.slice(3) : path;
    var matches = ES_PAGES.some(function (p) { return bare === p || bare === p + 'index.html'; });
    if (!matches) return null;
    if (targetLang === 'es' && !isEs) return '/es' + bare + window.location.search + window.location.hash;
    if (targetLang === 'en' && isEs) return bare + window.location.search + window.location.hash;
    return null;
  }

  window.toggleLang = function () {
    var html = document.documentElement;
    var current = html.getAttribute('data-lang') || 'en';
    var next = current === 'en' ? 'es' : 'en';
    try { localStorage.setItem('phl_lang', next); } catch (e) {}
    var alt = _altUrlForLang(next);
    if (alt) { window.location.href = alt; return; }
    html.setAttribute('data-lang', next);
    var lbl = document.getElementById('lang-label');
    if (lbl) lbl.textContent = next.toUpperCase();
  };
})();
