(function () {
  'use strict';

  function event(name, params) {
    if (typeof window.gtag !== 'function') return false;
    window.gtag('event', name, params || {});
    return true;
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
    var link = e.target.closest && e.target.closest('a[href]');
    if (!link) return;
    var href = link.getAttribute('href') || '';
    var parent = link.closest('nav,header,footer,aside,main');
    var context = {
      link_text: (link.textContent || link.getAttribute('aria-label') || '').trim().slice(0, 80),
      link_location: parent ? parent.tagName.toLowerCase() : 'body',
      page_path: window.location.pathname
    };
    if (href.toLowerCase().indexOf('tel:') === 0) event('phone_call_click', context);
    if (href.toLowerCase().indexOf('mailto:') === 0) event('email_click', context);
  });
})();