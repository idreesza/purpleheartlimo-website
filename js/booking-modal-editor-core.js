/* Pure booking modal serialization helpers.
 *
 * The browser editor and the Node tests both use these functions so the
 * payload sent after an edit is built from one explicit snapshot.  Keeping
 * this layer DOM-free also makes it difficult for a stale page value to leak
 * into the final EmailJS request.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.PHLBookingModalCore = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  function value(value) {
    return value === undefined || value === null ? '' : String(value).trim();
  }

  function serializeModalData(state) {
    state = state || {};
    var firstName = value(state.firstName);
    var lastName = value(state.lastName);
    var stops = Array.isArray(state.stops)
      ? state.stops.map(value).filter(Boolean)
      : (value(state.stops) ? [value(state.stops)] : []);

    return {
      firstName: firstName,
      lastName: lastName,
      name: [firstName, lastName].filter(Boolean).join(' '),
      phone: value(state.phone),
      email: value(state.email),
      service: value(state.service),
      vehicle: value(state.vehicle),
      vehicleId: value(state.vehicleId),
      passengers: value(state.passengers),
      pickup: value(state.pickup),
      dropoff: value(state.dropoff),
      stops: stops,
      date: value(state.date),
      time: value(state.time),
      hour: value(state.hour),
      minute: value(state.minute),
      ampm: value(state.ampm),
      endDate: value(state.endDate),
      endTime: value(state.endTime),
      flight: value(state.flight),
      specialRequests: value(state.specialRequests),
      quote: value(state.quote),
      estimate: state.estimate || null,
      website: value(state.website)
    };
  }

  function quoteText(data, copy) {
    copy = copy || {};
    if (data.estimate && data.estimate.available &&
        Number.isFinite(Number(data.estimate.total))) {
      var miles = Number(data.estimate.totalMiles);
      var minutes = Number(data.estimate.totalMinutes);
      var detail = [];
      if (Number.isFinite(miles)) detail.push(miles.toFixed(1) + ' mi');
      if (Number.isFinite(minutes)) detail.push(minutes + ' min');
      return '$' + data.estimate.total + (detail.length ? ' (' + detail.join(' · ') + ')' : '');
    }
    return copy.contactQuote || 'Contact us for a quote';
  }

  function summaryFor(data, copy) {
    copy = copy || {};
    var dropoff = data.dropoff || (data.service === 'hourly'
      ? (copy.hourlyDropoff || '(Hourly — see stops)')
      : '—');
    var stops = data.stops.length ? data.stops.join(' → ') : '—';
    var quote = quoteText(data, copy);
    return [
      '=== BOOKING REQUEST ===',
      'FIRST NAME: ' + (data.firstName || '—'),
      'LAST NAME: ' + (data.lastName || '—'),
      'NAME: ' + (data.name || '—'),
      'PHONE: ' + (data.phone || '—'),
      'EMAIL: ' + (data.email || '—'),
      '',
      'SERVICE: ' + (data.service || '—'),
      'VEHICLE: ' + (data.vehicle || '—'),
      'PASSENGERS: ' + (data.passengers || '—'),
      '',
      'PICKUP: ' + (data.pickup || '—'),
      'DROPOFF: ' + dropoff,
      'STOPS: ' + stops,
      '',
      'DATE: ' + (data.date || '—'),
      'TIME: ' + ([data.hour, data.minute].filter(Boolean).join(':') || data.time || '—') +
        (data.ampm ? ' ' + data.ampm : ''),
      'END DATE: ' + (data.endDate || '—'),
      'END TIME: ' + (data.endTime || '—'),
      'FLIGHT: ' + (data.flight || '—'),
      '',
      'QUOTE: ' + quote,
      'SPECIAL REQUESTS: ' + (data.specialRequests || '—')
    ].join('\n');
  }

  function buildBookingPayload(state, copy) {
    var data = serializeModalData(state);
    var summary = summaryFor(data, copy);
    return {
      data: data,
      summary: summary,
      email: {
        firstName: data.firstName,
        lastName: data.lastName,
        name: data.name,
        phone: data.phone,
        email: data.email,
        service: data.service,
        vehicleId: data.vehicleId,
        vehicle: data.vehicle,
        passengers: data.passengers,
        pickup: data.pickup,
        dropoff: data.dropoff || (data.service === 'hourly'
          ? ((copy && copy.hourlyDropoff) || '(Hourly — see stops)') : ''),
        stops: data.stops.join(' → '),
        date: data.date,
        time: data.time || ([data.hour, data.minute].filter(Boolean).join(':') +
          (data.ampm ? ' ' + data.ampm : '')),
        endDate: data.endDate,
        endTime: data.endTime,
        flight: data.flight,
        quote: quoteText(data, copy),
        specialRequests: data.specialRequests,
        notes: summary,
        source: 'Booking Page'
      }
    };
  }

  function createSubmissionGuard(state) {
    state = state || {};
    return function run(task) {
      if (state.promise) return state.promise;
      var pending = Promise.resolve().then(task);
      state.promise = pending.finally(function () {
        state.promise = null;
      });
      return state.promise;
    };
  }

  return {
    serializeModalData: serializeModalData,
    summaryFor: summaryFor,
    buildBookingPayload: buildBookingPayload,
    createSubmissionGuard: createSubmissionGuard
  };
}));