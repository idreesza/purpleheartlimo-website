/* Shared EmailJS sender for the booking pages.
 * The browser SDK is loaded only when a booking is submitted so the booking
 * shell does not add another third-party request during normal page loading.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory(typeof globalThis !== 'undefined' ? globalThis : {});
  } else {
    root.PHLBookingEmail = factory(root);
  }
}(typeof self !== 'undefined' ? self : this, function (root) {
  'use strict';

  const SDK_URL = 'https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js';
  const PUBLIC_KEY = 'coK69SSFSbc1x8dc6';
  const SERVICE_ID = 'service_53lh00r';
  const TEMPLATE_ID = 'template_xwek3ac';
  const RECIPIENTS = 'j.zaatreh@gmail.com,idrees.csst@gmail.com';
  let sdkPromise = null;
  let initialized = false;

  function valueOrDash(value) {
    if (Array.isArray(value)) value = value.join(' → ');
    if (value === undefined || value === null || String(value).trim() === '') return '—';
    return String(value);
  }

  function buildTemplateParams(data) {
    data = data || {};
    return {
      // The EmailJS template must use To Email={{to_email}} in its dashboard
      // settings; the browser request supplies both explicit recipients.
      to_email: RECIPIENTS,
      from_name: valueOrDash(data.name),
      phone: valueOrDash(data.phone),
      email: valueOrDash(data.email),
      service: valueOrDash(data.service),
      pickup: valueOrDash(data.pickup),
      dropoff: valueOrDash(data.dropoff),
      date: valueOrDash(data.date),
      time: valueOrDash(data.time),
      vehicle: valueOrDash(data.vehicle),
      flight: valueOrDash(data.flight),
      notes: valueOrDash(data.notes || data.summary),
      source: valueOrDash(data.source || 'Booking Page'),

      // Keep the same details available as individual template variables as
      // well as in the complete notes summary.
      passengers: valueOrDash(data.passengers),
      stops: valueOrDash(data.stops),
      end_date: valueOrDash(data.endDate !== undefined ? data.endDate : data.end_date),
      end_time: valueOrDash(data.endTime !== undefined ? data.endTime : data.end_time),
      quote: valueOrDash(data.quote),
      special_requests: valueOrDash(
        data.specialRequests !== undefined ? data.specialRequests : data.special_requests
      )
    };
  }

  function findLoadedSdk() {
    return root && root.emailjs && typeof root.emailjs.send === 'function'
      ? root.emailjs
      : null;
  }

  function initialize(sdk) {
    if (!initialized) {
      sdk.init({ publicKey: PUBLIC_KEY });
      initialized = true;
    }
    return sdk;
  }

  function loadSdk() {
    const loaded = findLoadedSdk();
    if (loaded) return Promise.resolve(initialize(loaded));
    if (sdkPromise) return sdkPromise;
    if (!root || !root.document) {
      return Promise.reject(new Error('Email service is unavailable.'));
    }

    sdkPromise = new Promise(function (resolve, reject) {
      const document = root.document;
      const existing = document.querySelector('script[data-phl-emailjs],script[src*="@emailjs/browser"]');
      const script = existing || document.createElement('script');
      let settled = false;

      function fail() {
        sdkPromise = null;
        if (!settled) {
          settled = true;
          reject(new Error('Email service is unavailable.'));
        }
      }

      function finish() {
        if (settled) return;
        const sdk = findLoadedSdk();
        if (!sdk) {
          fail();
          return;
        }
        settled = true;
        try {
          resolve(initialize(sdk));
        } catch (_) {
          sdkPromise = null;
          reject(new Error('Email service is unavailable.'));
        }
      }

      script.addEventListener('load', finish, { once: true });
      script.addEventListener('error', function () {
        fail();
      }, { once: true });
      if (!existing) {
        script.src = SDK_URL;
        script.async = true;
        script.dataset.phlEmailjs = 'true';
        document.head.appendChild(script);
      } else {
        // A script already in the document may have loaded before listeners
        // were attached, so check once more on the next task.
        root.setTimeout(finish, 0);
      }
    });
    return sdkPromise;
  }

  function sendBookingEmail(templateParams, options) {
    options = options || {};
    const sdkPromiseForRequest = options.emailjs
      ? Promise.resolve(options.emailjs)
      : loadSdk();
    return sdkPromiseForRequest.then(function (sdk) {
      if (!sdk || typeof sdk.send !== 'function') {
        throw new Error('Email service is unavailable.');
      }
      if (!options.emailjs) initialize(sdk);
      return Promise.resolve(sdk.send(SERVICE_ID, TEMPLATE_ID, templateParams)).then(function (response) {
        if (!response || Number(response.status) !== 200) {
          throw new Error('Email service did not accept the request.');
        }
        return response;
      });
    });
  }

  return {
    buildTemplateParams: buildTemplateParams,
    sendBookingEmail: sendBookingEmail
  };
}));