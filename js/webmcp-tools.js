/*
 * Optional WebMCP enhancement. Reviewed against upstream README and
 * declarative-api-explainer.md fetched for this implementation.
 *
 * The current spec uses document.modelContext. Some experimental Chromium
 * builds expose navigator.modelContext instead; feature-detect both.
 * The declarative prepare_limo_quote form deliberately has a DIFFERENT name
 * from the imperative request_limo_quote tool and has no toolautosubmit.
 * Neither path invokes a lead, payment, confirmation, or submission handler.
 */
(function () {
  'use strict';
  var context = ('modelContext' in document && document.modelContext) ||
    ('modelContext' in navigator && navigator.modelContext);
  if (!context || typeof context.registerTool !== 'function') return;

  function byId(id) { return document.getElementById(id); }
  function text(id) { var node = byId(id); return node ? node.textContent.trim() : ''; }
  function result(value) {
    return { content: [{ type: 'text', text: JSON.stringify(value) }] };
  }
  function fail(errors) {
    return result({ status: 'invalid_input', errors: errors, submitted: false });
  }
  function notify(node) {
    node.dispatchEvent(new Event('input', { bubbles: true }));
    node.dispatchEvent(new Event('change', { bubbles: true }));
  }
  function fill(id, value) {
    var node = byId(id);
    if (!node) return;
    node.value = String(value);
    if (node.getAttribute('role') === 'combobox') {
      delete node.dataset.lat;
      delete node.dataset.lon;
      delete node.dataset.placeId;
    }
    notify(node);
  }
  function delay(ms) { return new Promise(function (resolve) { setTimeout(resolve, ms); }); }
  function bounded(promise, ms) {
    return new Promise(function (resolve, reject) {
      var timer = setTimeout(function () { reject(new Error('estimate_timeout')); }, ms);
      Promise.resolve(promise).then(function (value) {
        clearTimeout(timer); resolve(value);
      }, function (error) {
        clearTimeout(timer); reject(error);
      });
    });
  }
  function localDate(date) {
    return date.getFullYear() + '-' + String(date.getMonth() + 1).padStart(2, '0') +
      '-' + String(date.getDate()).padStart(2, '0');
  }

  function initialize() {
    var home = !!byId('booking-widget');
    var page = window.__PHLBookingPage;
    if (!home && (!page || !byId('bookingDetailsForm'))) return;
    var form = byId(home ? 'booking-widget' : 'bookingDetailsForm');
    // The form remains review-only even in a declarative implementation.
    // Prevent implicit Enter submission as well as an agent's requestSubmit().
    form.addEventListener('submit', function (event) { event.preventDefault(); });

    var vehicleOptions = home
      ? Array.prototype.map.call(document.querySelectorAll('#csel-vehicle .csel-opt'), function (node) {
        var match = (node.getAttribute('onclick') || '').match(/'vehicle-input'\s*,\s*'([^']+)'/);
        return match ? { value: match[1], name: node.textContent.trim() } : null;
      }).filter(Boolean)
      : page.vehicles.map(function (vehicle) {
        return { value: vehicle.id, name: vehicle.name, capacity: vehicle.pax };
      });
    if (!vehicleOptions.length) return;
    var vehicleValues = vehicleOptions.map(function (vehicle) { return vehicle.value; });
    var homePax = home && typeof PAX_OPTIONS !== 'undefined' ? PAX_OPTIONS : null;
    var maximum = homePax
      ? Math.max.apply(null, Object.keys(homePax).reduce(function (all, vehicle) {
        return all.concat(homePax[vehicle].map(function (option) { return Number(option[1]); }));
      }, []))
      : Math.max.apply(null, vehicleOptions.map(function (vehicle) { return vehicle.capacity; }));
    var minutes = home
      ? Array.prototype.map.call(document.querySelectorAll('#csel-min .csel-opt'), function (node) {
        var match = (node.getAttribute('onclick') || '').match(/'time-min'\s*,\s*'([^']+)'/);
        return match && match[1];
      }).filter(Boolean)
      : Array.prototype.map.call(document.querySelectorAll('#minCdd .cdd-opt'), function (node) {
        return node.dataset.v;
      });
    var properties = {
      pickup: { type: 'string', minLength: 1, description: 'Pickup street address, airport or hotel.' },
      dropoff: { type: 'string', minLength: 1, description: 'Destination street address, airport or hotel.' },
      date: { type: 'string', format: 'date', pattern: '^\\d{4}-\\d{2}-\\d{2}$',
        description: 'Future pickup date, YYYY-MM-DD, in the service location local time.' },
      time: { type: 'string', pattern: '^(?:[01]\\d|2[0-3]):(?:' + minutes.join('|') + ')$',
        description: 'Pickup time in local 24-hour HH:MM. Supported minutes: ' + minutes.join(', ') + '.' },
      passengers: { type: 'integer', minimum: 1, maximum: maximum,
        description: 'Number of passengers; must fit the selected vehicle and its available passenger options.' },
      vehicle: { type: 'string', enum: vehicleValues,
        description: 'Exact vehicle option: ' + vehicleOptions.map(function (v) {
          return v.value === v.name ? v.value : v.value + ' (' + v.name + ')';
        }).join('; ') + '.' },
      phone: { type: 'string', pattern: '^\\+?[0-9() .-]+$', minLength: 10, maxLength: 32,
        description: 'Customer phone number with 10 to 15 digits; optional leading + and formatting punctuation.' },
      email: { type: 'string', format: 'email', description: 'Optional valid customer email address.' },
      flight: { type: 'string', description: 'Optional airline flight number.' },
      service: { type: 'string', enum: ['airport', 'oneway', 'hourly'],
        description: 'Optional service type; uses the currently selected tab when omitted.' }
    };
    properties[home ? 'notes' : 'message'] = {
      type: 'string', description: 'Optional special requests for the chauffeur.'
    };
    if (home) properties.name = { type: 'string', minLength: 1, description: 'Customer full name.' };
    else {
      properties.first_name = { type: 'string', minLength: 1, description: 'Customer first name.' };
      properties.last_name = { type: 'string', minLength: 1, description: 'Customer last name.' };
      properties.end_date = { type: 'string', format: 'date', pattern: '^\\d{4}-\\d{2}-\\d{2}$',
        description: 'Required for hourly charter: end date in YYYY-MM-DD.' };
      properties.end_time = { type: 'string', pattern: '^(?:[01]\\d|2[0-3]):[0-5]\\d$',
        description: 'Required for hourly charter: end time in local 24-hour HH:MM.' };
    }
    var required = ['pickup', 'dropoff', 'date', 'time', 'passengers', 'vehicle', 'phone']
      .concat(home ? ['name'] : ['first_name', 'last_name']);
    var schema = { type: 'object', properties: properties, required: required, additionalProperties: false };
    var busy = false;

    function validDate(value) {
      if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
      var parsed = new Date(value + 'T12:00:00');
      return !isNaN(parsed.getTime()) && localDate(parsed) === value;
    }
    function validate(input) {
      var errors = [];
      if (!input || typeof input !== 'object' || Array.isArray(input)) return ['Provide a JSON object.'];
      Object.keys(input).forEach(function (key) {
        if (!Object.prototype.hasOwnProperty.call(properties, key)) errors.push('Unknown field: ' + key + '.');
      });
      required.forEach(function (key) {
        if (key === 'passengers') return;
        if (typeof input[key] !== 'string' || !input[key].trim()) errors.push(key + ' is required and must be a nonempty string.');
      });
      var vehicle = vehicleOptions.find(function (option) { return option.value === input.vehicle; });
      if (!vehicle) errors.push('vehicle must be one of: ' + vehicleValues.join(', ') + '.');
      if (!Number.isInteger(input.passengers) || input.passengers < 1 || input.passengers > maximum) {
        errors.push('passengers must be an integer between 1 and ' + maximum + '.');
      } else if (vehicle) {
        if (homePax && (!homePax[input.vehicle] || !homePax[input.vehicle].some(function (option) {
          return Number(option[1]) === input.passengers;
        }))) errors.push('Passenger count is not an available option for ' + input.vehicle + '.');
        if (!home && input.passengers > vehicle.capacity) errors.push('Passenger count exceeds this vehicle capacity (' + vehicle.capacity + ').');
      }
      if (!validDate(input.date)) errors.push('date must be a real calendar date in YYYY-MM-DD.');
      if (typeof input.time !== 'string' || !new RegExp(properties.time.pattern).test(input.time)) {
        errors.push('time must be HH:MM (24-hour) using minutes: ' + minutes.join(', ') + '.');
      } else if (validDate(input.date) && new Date(input.date + 'T' + input.time) <= new Date()) {
        errors.push('Pickup date and time must be in the future.');
      }
      if (typeof input.phone !== 'string' || !/^\+?[0-9() .-]+$/.test(input.phone) ||
          input.phone.length > 32 || input.phone.replace(/\D/g, '').length < 10 ||
          input.phone.replace(/\D/g, '').length > 15) {
        errors.push('phone must contain 10 to 15 digits with an optional leading +.');
      }
      if (input.email !== undefined && (typeof input.email !== 'string' || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.email))) {
        errors.push('email must be a valid email address, or omit it.');
      }
      ['flight', home ? 'notes' : 'message'].forEach(function (key) {
        if (input[key] !== undefined && typeof input[key] !== 'string') errors.push(key + ' must be a string.');
      });
      if (input.service !== undefined && properties.service.enum.indexOf(input.service) < 0) {
        errors.push('service must be airport, oneway or hourly.');
      }
      var service = input.service || (home ? (typeof getActiveTab === 'function' ? getActiveTab() : 'airport') : page.service);
      if (!home && service === 'hourly') {
        if (!validDate(input.end_date) || typeof input.end_time !== 'string' ||
            !/^(?:[01]\d|2[0-3]):[0-5]\d$/.test(input.end_time)) {
          errors.push('Hourly charter requires end_date (YYYY-MM-DD) and end_time (HH:MM).');
        } else if (new Date(input.end_date + 'T' + input.end_time) <= new Date(input.date + 'T' + input.time)) {
          errors.push('Hourly charter end must be after pickup.');
        }
      } else if (!home) {
        if (input.end_date !== undefined && !validDate(input.end_date)) errors.push('end_date must be YYYY-MM-DD.');
        if (input.end_time !== undefined && !/^(?:[01]\d|2[0-3]):[0-5]\d$/.test(input.end_time)) errors.push('end_time must be HH:MM.');
      }
      return errors;
    }

    function homePick(wrap, id, value, label) {
      if (typeof cselPick === 'function') cselPick(wrap, id, String(value), label);
      else fill(id, value);
      var node = byId(id);
      if (node) notify(node);
    }
    function bookingPick(rootId, inputId, value) {
      fill(inputId, value);
      var root = byId(rootId);
      if (!root) return;
      root.dataset.value = String(value);
      var label = root.querySelector('span');
      if (label) {
        label.textContent = String(value);
        label.classList.remove('cdd-placeholder');
      }
      root.querySelectorAll('.cdd-opt').forEach(function (option) {
        option.classList.toggle('sel', option.dataset.v === String(value));
      });
    }
    function fingerprint() {
      var ids = home ? ['pickup-input', 'dropoff-input', 'date-input', 'time-hour', 'time-min', 'time-ampm', 'vehicle-input', 'pax-input']
        : ['pickupInput', 'dropoffInput', 'dateInput', 'timeHour', 'timeMin', 'timeAmpm', 'hourEndDate', 'hourEndTime', 'fpax'];
      return JSON.stringify(ids.map(function (id) { return byId(id) && byId(id).value; })) +
        (home ? window._quoteTab : page.selectedVehicle + ':' + page.service) +
        JSON.stringify(Array.prototype.map.call(document.querySelectorAll(home
          ? '#extra-stops-container input' : '#stopsList input'), function (node) { return node.value; }));
    }
    async function refresh() {
      if (home) {
        if (typeof _phlDebounce !== 'undefined') { clearTimeout(_phlDebounce); _phlDebounce = null; }
        if (typeof refreshLivePricing !== 'function') throw new Error('estimate_unavailable');
        await refreshLivePricing();
        // An existing widget event may supersede the request while it runs.
        var current = window._phlPricePromise;
        for (var i = 0; current && i < 3; i++) {
          await current;
          if (current === window._phlPricePromise) return;
          current = window._phlPricePromise;
        }
        throw new Error('estimate_changed');
      } else {
        if (typeof _estDebounce !== 'undefined') { clearTimeout(_estDebounce); _estDebounce = null; }
        if (typeof updateEstimate !== 'function') throw new Error('estimate_unavailable');
        // Cancel stale estimates using the page's own request-generation guard.
        if (typeof _estimateVersion !== 'undefined') _estimateVersion++;
        await updateEstimate();
      }
    }
    async function execute(input) {
      var errors = validate(input);
      if (errors.length) return fail(errors);
      if (busy) return result({ status: 'busy', message: 'A quote is already being prepared. Try again after it finishes.', submitted: false });
      busy = true;
      try {
        var service = input.service || (home ? getActiveTab() : page.service);
        var tab = home ? (service === 'oneway' ? 'pointtopoint' : service) : service;
        var tabs = document.querySelectorAll(home ? '.trip-tab' : '#svcTabs .svc-tab');
        var target = Array.prototype.find.call(tabs, function (button) {
          return home ? (button.getAttribute('onclick') || '').indexOf("'" + tab + "'") >= 0
            : button.dataset.svc === tab;
        });
        if (target) {
          if (home && typeof setTab === 'function') setTab(target, tab);
          else target.click(); // service tab only; never a quote/submit button
        }
        await delay(60); // existing tab handlers schedule resets/estimates
        fill(home ? 'pickup-input' : 'pickupInput', input.pickup.trim());
        fill(home ? 'dropoff-input' : 'dropoffInput', input.dropoff.trim());
        var dateParts = input.date.split('-');
        fill(home ? 'date-input' : 'dateInput', home
          ? dateParts[1] + '/' + dateParts[2] + '/' + dateParts[0] : input.date);
        var hour = Number(input.time.slice(0, 2));
        var hour12 = String(hour % 12 || 12);
        var minute = input.time.slice(3);
        var ampm = hour >= 12 ? 'PM' : 'AM';
        if (home) {
          homePick('csel-hour', 'time-hour', hour12);
          homePick('csel-min', 'time-min', minute);
          homePick('csel-ampm', 'time-ampm', ampm);
          homePick('csel-vehicle', 'vehicle-input', input.vehicle);
          if (typeof onVehicleChange === 'function') onVehicleChange(input.vehicle);
          var paxOption = homePax && homePax[input.vehicle].find(function (option) {
            return Number(option[1]) === input.passengers;
          });
          homePick('csel-pax', 'pax-input', input.passengers, paxOption ? paxOption[0] : undefined);
          if (typeof checkCapacity === 'function') checkCapacity();
          fill('quote-name', input.name.trim());
          fill('quote-phone', input.phone.trim());
          if (input.email !== undefined) fill('quote-email', input.email.trim());
          if (input.flight !== undefined) fill('flight-input', input.flight.trim());
          if (input.notes !== undefined) fill('quote-notes', input.notes);
          form.classList.add('expanded');
        } else {
          var dateRoot = byId('dateCdd');
          if (dateRoot) dateRoot.dataset.value = input.date;
          var dateLabel = byId('dateCddLabel');
          if (dateLabel) {
            dateLabel.textContent = dateParts[1] + '/' + dateParts[2] + '/' + dateParts[0];
            dateLabel.classList.remove('cdate-placeholder');
          }
          bookingPick('hourCdd', 'timeHour', hour12);
          bookingPick('minCdd', 'timeMin', minute);
          bookingPick('ampmCdd', 'timeAmpm', ampm);
          if (input.end_date !== undefined) fill('hourEndDate', input.end_date);
          if (input.end_time !== undefined) fill('hourEndTime', input.end_time);
          var vehicleStage = byId('vehicleSection');
          if (vehicleStage) {
            vehicleStage.hidden = false;
            vehicleStage.setAttribute('aria-hidden', 'false');
            vehicleStage.classList.add('is-ready');
          }
          // Existing public selection handler updates the real carousel/details.
          if (typeof window.selectVehicle !== 'function') throw new Error('vehicle_selection_unavailable');
          window.selectVehicle(input.vehicle);
          var pax = String(input.passengers);
          if (input.passengers >= 7 && input.passengers <= 10) pax = '7–10';
          else if (input.passengers >= 11 && input.passengers <= 14) pax = '11–14';
          else if (input.passengers >= 15 && input.passengers <= 24) pax = '15–24';
          bookingPick('paxCdd', 'fpax', pax);
          fill('fname', input.first_name.trim());
          fill('lname', input.last_name.trim());
          fill('fphone', input.phone.trim());
          if (input.email !== undefined) fill('femail', input.email.trim());
          if (input.flight !== undefined) fill('flightInput', input.flight.trim());
          if (input.message !== undefined) fill('fmessage', input.message);
        }
        var snapshot = fingerprint();
        await bounded(refresh(), 15000);
        if (snapshot !== fingerprint()) {
          return result({ status: 'form_changed', message: 'Trip details changed while calculating; request a new estimate.', submitted: false });
        }
        var price = text(home ? 'price-value' : 'estPrice');
        var fare = home ? window._phlLastFare : page.estimate;
        return result({
          status: fare && fare.available !== false ? 'estimate_ready' : 'estimate_requires_confirmation',
          displayed_price: price,
          details: text(home ? 'price-note' : 'estMeta'),
          estimate: fare || null,
          currency: 'USD',
          submitted: false,
          requires_user_confirmation: true,
          message: 'Details filled. The user must review and click the existing booking button to send the request.'
        });
      } catch (error) {
        return result({
          status: 'estimate_unavailable',
          submitted: false, requires_user_confirmation: true,
          message: 'Details remain in the form. A current estimate could not be confirmed; review the widget or try again.'
        });
      } finally {
        busy = false;
      }
    }
    // Registration may be rejected by Permissions Policy or an experimental
    // implementation. Do not produce an unhandled rejection or console error.
    try {
      Promise.resolve(context.registerTool({
        name: 'request_limo_quote',
        description: 'Prepare a Purple Heart Limo trip quote using the live booking widget and return its current displayed estimate. Fills trip and contact details for review; the user must click the existing booking button to send a request. This tool never sends a lead, books or charges.',
        inputSchema: schema,
        execute: execute
      })).catch(function () {});
    } catch (error) { /* unsupported/blocked experimental implementation */ }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, { once: true });
  else initialize();
}());
