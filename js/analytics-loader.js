/* Keep the inline gtag queue; load its transport after load/first interaction. */
(function () {
  'use strict';
  var loaded = false;
  function load() {
    if (loaded) return;
    loaded = true;
    ['pointerdown', 'keydown', 'touchstart'].forEach(function (name) {
      window.removeEventListener(name, load, true);
    });
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=G-Y469VZMYZT';
    document.head.appendChild(script);
  }
  ['pointerdown', 'keydown', 'touchstart'].forEach(function (name) {
    window.addEventListener(name, load, { capture: true, passive: true, once: true });
  });
  function afterLoad() {
    if (window.requestIdleCallback) window.requestIdleCallback(load, { timeout: 2000 });
    else setTimeout(load, 0);
  }
  if (document.readyState === 'complete') afterLoad();
  else window.addEventListener('load', afterLoad, { once: true });
})();
