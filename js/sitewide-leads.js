(function () {
  'use strict';
  if (window.__PHLSitewideLeadsLoaded) return;
  window.__PHLSitewideLeadsLoaded = true;

  function event(name, params) {
    if (typeof window.gtag !== 'function') return false;
    try {
      window.gtag('event', name, params || {});
      return true;
    } catch (_) {
      // Analytics must never interrupt a call, email, or booking.
      return false;
    }
  }

  var recent = Object.create(null);
  window.PHLTrackLead = function (formOrSource) {
    var isForm = formOrSource && typeof formOrSource === 'object';
    var source = typeof formOrSource === 'string'
      ? formOrSource
      : (isForm && (formOrSource.getAttribute('data-lead-source') ||
        formOrSource.id || formOrSource.getAttribute('name'))) || 'form';
    var formId = isForm ? (formOrSource.id || formOrSource.getAttribute('name') || '') : '';
    var key = source + ':' + formId;
    var now = Date.now();
    if (recent[key] && now - recent[key] < 1500) return false;
    recent[key] = now;
    return event('generate_lead', {
      lead_source: source,
      form_id: formId || undefined,
      page_path: window.location.pathname
    });
  };

  document.addEventListener('click', function (e) {
    var target = e.target && (e.target.nodeType === 3 ? e.target.parentElement : e.target);
    var link = target && target.closest && target.closest('a[href]');
    if (!link) return;
    var href = (link.getAttribute('href') || '').trim();
    var parent = link.closest('nav,header,footer,aside,main');
    var context = {
      link_text: (link.textContent || link.getAttribute('aria-label') || '').trim().slice(0, 80),
       link_location: link.closest('.mobile-bar,.phl-mobile-call-bar,.floating-widgets')
         ? 'floating_button' : (parent ? parent.tagName.toLowerCase() : 'body'),
      page_path: window.location.pathname
    };
    if (href.toLowerCase().indexOf('tel:') === 0) {
      context.transport_type = 'beacon';
      event('phone_call_click', context);
    }
    if (href.toLowerCase().indexOf('mailto:') === 0) event('email_click', context);
  }, { capture: true, passive: true });
})();