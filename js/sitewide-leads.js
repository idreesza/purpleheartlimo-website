/* Shared, privacy-safe lead tracking for Purple Heart Limo. */
(function (window, document) {
  'use strict';

  var GA_ID = 'G-Y469VZMYZT';
  var recentLeadEvents = Object.create(null);

  function dataLayerHasConfig() {
    var layer = window.dataLayer || [];
    for (var i = 0; i < layer.length; i += 1) {
      var entry = layer[i];
      if (entry && entry[0] === 'config' && entry[1] === GA_ID) return true;
    }
    return false;
  }

  function hasGtagScript() {
    var scripts = document.getElementsByTagName('script');
    for (var i = 0; i < scripts.length; i += 1) {
      if ((scripts[i].src || '').indexOf('googletagmanager.com/gtag/js?id=' + GA_ID) !== -1) return true;
    }
    return false;
  }

  function initializeAnalytics() {
    window.dataLayer = window.dataLayer || [];
    if (typeof window.gtag !== 'function') {
      window.gtag = function () { window.dataLayer.push(arguments); };
    }
    if (!dataLayerHasConfig()) window.gtag('js', new Date());
    if (!dataLayerHasConfig()) window.gtag('config', GA_ID);

    if (!hasGtagScript()) {
      var script = document.createElement('script');
      script.async = true;
      script.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
      document.head.appendChild(script);
    }
  }

  /* Only approved, non-identifying categories can be included in analytics. */
  function leadSource(source) {
    var value = typeof source === 'string' ? source.toLowerCase() : '';
    if (value.indexOf('booking') !== -1) return 'booking_form';
    if (value.indexOf('contact') !== -1) return 'contact_form';
    if (value.indexOf('quote') !== -1) return 'quote_form';
    return 'form';
  }

  function trackEvent(name, parameters) {
    if (typeof window.gtag === 'function') window.gtag('event', name, parameters);
  }

  window.PHLTrackLead = function (formOrSource) {
    var source = leadSource(
      typeof formOrSource === 'string'
        ? formOrSource
        : (formOrSource && formOrSource.getAttribute && formOrSource.getAttribute('data-lead-source'))
    );
    var formId = typeof formOrSource === 'object' && formOrSource
      ? (formOrSource.id || formOrSource.getAttribute('name') || '')
      : '';
    var key = source + ':' + formId;
    var now = Date.now();
    if (recentLeadEvents[key] && now - recentLeadEvents[key] < 1500) return false;
    recentLeadEvents[key] = now;
    trackEvent('generate_lead', {
      lead_source: source,
      form_id: formId || undefined,
      page_path: window.location.pathname
    });
    return true;
  };

  initializeAnalytics();

  document.addEventListener('click', function (event) {
    var link = event.target.closest && event.target.closest('a[href]');
    if (!link) return;
    var href = link.getAttribute('href') || '';
    var context = {
      link_text: (link.textContent || link.getAttribute('aria-label') || '').trim().slice(0, 80),
      link_location: link.closest('nav,header,footer,aside,main')?.tagName.toLowerCase() || 'body',
      page_path: window.location.pathname
    };
    if (href.toLowerCase().indexOf('tel:') === 0) trackEvent('phone_call_click', context);
    if (href.toLowerCase().indexOf('mailto:') === 0) trackEvent('email_click', context);
  });
})(window, document);