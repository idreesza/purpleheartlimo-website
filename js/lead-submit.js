/* Purple Heart Limo — send contact/booking-request forms by email.
 *
 * Drop-in replacement for fetch('/.netlify/functions/contact', {...}) used by
 * the contact page and the city/service landing pages. It sends the same JSON
 * payload through EmailJS (js/booking-email.js — the path the booking page
 * already uses) and resolves with a fetch-like response:
 *   { ok, status, json() -> { success, message } | { error } }
 * so each page's existing success/error handling keeps working unchanged.
 *
 * Requires js/booking-email.js to be loaded on the page.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory(typeof globalThis !== 'undefined' ? globalThis : {});
  } else {
    root.PHLLeadFetch = factory(root);
  }
}(typeof self !== 'undefined' ? self : this, function (root) {
  'use strict';

  var HONEYPOTS = ['website', 'bk-website', 'company', 'fax'];

  function isSpanish() {
    var doc = root.document && root.document.documentElement;
    return !!doc && /^es/i.test(doc.getAttribute('lang') || '');
  }

  function thanks() {
    return isSpanish()
      ? '¡Gracias! Le llamaremos o enviaremos un mensaje en 5 minutos con su tarifa exacta.'
      : "Thank you! We'll call or text you within 5 minutes with your exact rate.";
  }

  function response(ok, body) {
    return {
      ok: ok,
      status: ok ? 200 : 502,
      json: function () { return Promise.resolve(body); }
    };
  }

  function pageSource() {
    var loc = root.location || {};
    var title = (root.document && root.document.title) || '';
    return 'Website form: ' + (title ? title + ' ' : '') + '(' + (loc.pathname || '') + ')';
  }

  function toBookingData(payload) {
    var notes = [];
    if (payload.message) notes.push(String(payload.message));
    if (payload.notes) notes.push(String(payload.notes));
    if (payload.city) notes.push('City: ' + payload.city);
    if (payload.subject) notes.push('Subject: ' + payload.subject);
    var data = {};
    for (var key in payload) {
      if (Object.prototype.hasOwnProperty.call(payload, key)) data[key] = payload[key];
    }
    data.notes = notes.join('\n');
    data.flight = payload.flight || payload.flightNumber || '';
    data.source = payload.source || pageSource();
    return data;
  }

  return function PHLLeadFetch(_url, init) {
    var payload = {};
    try {
      payload = JSON.parse((init && init.body) || '{}') || {};
    } catch (_) {
      payload = {};
    }
    // Same quiet bot handling the server used: pretend success, send nothing.
    for (var i = 0; i < HONEYPOTS.length; i++) {
      if (payload[HONEYPOTS[i]]) return Promise.resolve(response(true, { success: true, message: thanks() }));
    }
    if (!payload.name || !String(payload.name).trim()) {
      return Promise.resolve(response(false, { error: 'Missing required field: name' }));
    }
    var mailer = root.PHLBookingEmail;
    if (!mailer || typeof mailer.sendBookingEmail !== 'function') {
      return Promise.resolve(response(false, { error: 'Email service is unavailable.' }));
    }
    var params = mailer.buildTemplateParams(toBookingData(payload));
    return Promise.resolve()
      .then(function () { return mailer.sendBookingEmail(params); })
      .then(function () { return response(true, { success: true, message: thanks() }); },
            function () { return response(false, { error: 'Email service is unavailable.' }); });
  };
}));
