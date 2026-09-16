/* Editable booking review flow shared by booking.html and es/booking.html. */
(function (root) {
  'use strict';

  var page = root.__PHLBookingPage;
  var core = root.PHLBookingModalCore;
  var modal = document.getElementById('confirmModal');
  if (!page || !core || !modal) return;

  var spanish = (document.documentElement.lang || '').toLowerCase().indexOf('es') === 0;
  var copy = spanish ? {
    service: { airport: '✈ Traslado al aeropuerto', oneway: '📍 Punto a punto', hourly: '⏱ Por hora' },
    selected: 'seleccionado',
    contactQuote: 'Contáctanos para obtener una cotización.',
    finalPrice: 'Precio final',
    quoteGeneric: 'Nuestro representante confirmará el precio final contigo.',
    checking: 'Comprobando disponibilidad…',
    invalid: 'Corrige los datos obligatorios antes de enviar tu solicitud.',
    missingTrip: 'Completa la recogida, el destino, la fecha y la hora.',
    missingHourly: 'Selecciona la fecha y hora de fin del servicio por hora.',
    invalidWindow: 'La hora de fin debe ser posterior a la hora de inicio.',
    sending: 'Enviando…',
    confirm: 'Obtener una cotización',
    cancel: 'Cancelar',
    requestError: 'No pudimos aceptar la solicitud. Tus datos siguen aquí. Inténtalo de nuevo o llama al (833) 740-0700.',
    hourlyDropoff: '(Por hora — ver paradas)',
    addStop: '+ Añadir parada',
    stopPlaceholder: 'Parada (opcional)',
    noStops: 'No hay paradas añadidas.'
  } : {
    service: { airport: '✈ Airport Transfer', oneway: '📍 Point to Point', hourly: '⏱ Hourly' },
    selected: 'selected',
    contactQuote: 'Contact us for a quote',
    finalPrice: 'Final price',
    quoteGeneric: 'Our representative will confirm the final price with you.',
    checking: 'Checking availability…',
    invalid: 'Please correct the required details before submitting your request.',
    missingTrip: 'Please complete pickup, drop-off, date, and time.',
    missingHourly: 'Select an hourly service end date and time.',
    invalidWindow: 'End time must be later than the start time.',
    sending: 'Sending…',
    confirm: 'Get a Quote',
    cancel: 'Cancel',
    requestError: 'We could not accept the request. Your details are still here. Please try again or call (833) 740-0700.',
    hourlyDropoff: '(Hourly — see stops)',
    addStop: '+ Add stop',
    stopPlaceholder: 'Stop (optional)',
    noStops: 'No stops added.'
  };

  var ids = [
    'mdlEditService', 'mdlEditVehicle', 'mdlEditPickup', 'mdlEditDropoff',
    'mdlEditDate', 'mdlEditHour', 'mdlEditMinute', 'mdlEditAmpm',
    'mdlEditEndDate', 'mdlEditEndTime', 'mdlEditFirstName', 'mdlEditLastName',
    'mdlEditPhone', 'mdlEditEmail', 'mdlEditPassengers', 'mdlEditFlight',
    'mdlEditRequests'
  ];
  var fields = {};
  ids.forEach(function (id) { fields[id] = document.getElementById(id); });
  var modalForm = document.getElementById('bookingModalForm');
  var modalError = document.getElementById('modalSubmitError');
  var confirmButton = document.getElementById('mdlConfirm');
  var cancelButton = document.getElementById('mdlCancel');
  var stopsContainer = document.getElementById('mdlEditStops');
  var addStopButton = document.getElementById('mdlEditAddStop');
  var previousFocus = null;
  var editRevision = 0;
  var estimateTimer = null;
  var sendInFlight = false;
  var stopSequence = 0;
  var sendState = root.__PHLBookingSendState;
  if (!sendState || typeof sendState !== 'object') {
    sendState = { promise: null };
    root.__PHLBookingSendState = sendState;
  }
  var sendGuard = core.createSubmissionGuard(sendState);

  function value(field) {
    return field && field.value !== undefined ? String(field.value).trim() : '';
  }

  function pageField(id) {
    return document.getElementById(id);
  }

  function setValue(id, next) {
    if (fields[id]) fields[id].value = next === undefined || next === null ? '' : String(next);
  }

  function selectedVehicle() {
    return page.vehicles.find(function (vehicle) {
      return vehicle.id === page.selectedVehicle;
    }) || null;
  }

  function serviceLabel(service) {
    return copy.service[service] || service || '—';
  }

  function serviceFromPage() {
    return page.service || 'airport';
  }

  function pageStops() {
    if (typeof root.getStops === 'function') return root.getStops();
    return Array.prototype.map.call(
      document.querySelectorAll('#stopsList .stop-row input'),
      function (input) { return value(input); }
    ).filter(Boolean);
  }

  function pageEstimate() {
    return page.estimate || null;
  }

  function copyAddressCoordinates(source, destination) {
    if (!source || !destination) return;
    ['lat', 'lon', 'placeId'].forEach(function (key) {
      if (source.dataset && source.dataset[key]) destination.dataset[key] = source.dataset[key];
      else if (destination.dataset) delete destination.dataset[key];
    });
  }

  function setPageAddress(pageId, modalId) {
    var destination = pageField(pageId);
    var source = fields[modalId];
    if (!destination || !source) return;
    destination.value = value(source);
    copyAddressCoordinates(source, destination);
  }

  function setPageDate() {
    var input = pageField('dateInput');
    if (input) input.value = value(fields.mdlEditDate);
    var label = document.getElementById('dateCddLabel');
    if (label) {
      var parts = value(fields.mdlEditDate).split('-');
      label.textContent = parts.length === 3 ? parts[1] + '/' + parts[2] + '/' + parts[0] : 'mm/dd/yyyy';
      label.classList.toggle('cdate-placeholder', parts.length !== 3);
    }
    var dateRoot = document.getElementById('dateCdd');
    if (dateRoot) dateRoot.dataset.value = value(fields.mdlEditDate);
  }

  function setPageTime() {
    var values = [
      ['timeHour', fields.mdlEditHour],
      ['timeMin', fields.mdlEditMinute],
      ['timeAmpm', fields.mdlEditAmpm]
    ];
    values.forEach(function (pair) {
      var target = pageField(pair[0]);
      if (target && pair[1]) target.value = value(pair[1]);
    });
    [['hourCddLabel', fields.mdlEditHour], ['minCddLabel', fields.mdlEditMinute],
      ['ampmCddLabel', fields.mdlEditAmpm]].forEach(function (pair) {
      var label = document.getElementById(pair[0]);
      if (label && pair[1]) {
        label.textContent = value(pair[1]) || '--';
        label.classList.toggle('cdd-placeholder', !value(pair[1]));
      }
    });
  }

  function syncStopsToPage() {
    var values = Array.prototype.map.call(
      stopsContainer ? stopsContainer.querySelectorAll('input[data-stop-value]') : [],
      function (input) { return value(input); }
    ).filter(Boolean);
    if (typeof root.clearStops === 'function') root.clearStops();
    if (typeof root.addStop !== 'function') return;
    values.forEach(function (stop) {
      root.addStop();
      var pageInputs = document.querySelectorAll('#stopsList .stop-row input');
      var last = pageInputs[pageInputs.length - 1];
      if (last) last.value = stop;
    });
  }

  function setHourlyPageFields() {
    var hourly = serviceFromPage() === 'hourly';
    var dateField = document.getElementById('hourEndDateSf');
    var timeField = document.getElementById('hourEndTimeSf');
    if (dateField) dateField.hidden = !hourly;
    if (timeField) timeField.hidden = !hourly;
    var endDate = pageField('hourEndDate');
    var endTime = pageField('hourEndTime');
    if (endDate) {
      endDate.value = value(fields.mdlEditEndDate);
      endDate.min = value(fields.mdlEditDate);
    }
    if (endTime) endTime.value = value(fields.mdlEditEndTime);
  }

  function paintPageService() {
    var service = serviceFromPage();
    document.querySelectorAll('.svc-tab').forEach(function (tab) {
      tab.classList.toggle('active', tab.dataset.svc === service);
    });
    var dropoff = document.getElementById('dropoffSf');
    if (dropoff) dropoff.style.display = service === 'hourly' ? 'none' : '';
    var stops = document.getElementById('stopsWrap');
    if (stops) stops.classList.toggle('show', service !== 'airport');
    var flight = document.getElementById('flightRow');
    if (flight) flight.classList.toggle('show', service === 'airport');
    var priceMode = document.getElementById('priceModeLabel');
    if (priceMode) priceMode.textContent = serviceLabel(service);
    document.querySelector('.search-row')?.classList.toggle('is-hourly', service === 'hourly');
    setHourlyPageFields();
    if (fields.mdlEditDropoff) {
      fields.mdlEditDropoff.disabled = service === 'hourly';
      fields.mdlEditDropoff.required = service !== 'hourly';
    }
    var hourlyWindow = document.getElementById('mdlEditHourlyWindow');
    if (hourlyWindow) hourlyWindow.hidden = service !== 'hourly';
    if (fields.mdlEditEndDate) fields.mdlEditEndDate.required = service === 'hourly';
    if (fields.mdlEditEndTime) fields.mdlEditEndTime.required = service === 'hourly';
  }

  function setPageContactAndExtras() {
    var pairs = [
      ['fname', fields.mdlEditFirstName], ['lname', fields.mdlEditLastName],
      ['fphone', fields.mdlEditPhone], ['femail', fields.mdlEditEmail],
      ['flightInput', fields.mdlEditFlight], ['fmessage', fields.mdlEditRequests],
      ['fpax', fields.mdlEditPassengers]
    ];
    pairs.forEach(function (pair) {
      var target = pageField(pair[0]);
      if (target && pair[1]) target.value = value(pair[1]);
    });
  }

  function syncModalToPage() {
    page.service = value(fields.mdlEditService) || 'airport';
    page.selectedVehicle = value(fields.mdlEditVehicle) || page.selectedVehicle;
    setPageAddress('pickupInput', 'mdlEditPickup');
    setPageAddress('dropoffInput', 'mdlEditDropoff');
    setPageDate();
    setPageTime();
    setPageContactAndExtras();
    setHourlyPageFields();
    syncStopsToPage();
    paintPageService();
    var vehicle = selectedVehicle();
    var selectedText = document.getElementById('selVehicleText');
    if (selectedText && vehicle) selectedText.textContent = vehicle.name + ' ' + copy.selected;
    if (typeof root.renderVehicles === 'function') root.renderVehicles();
  }

  function stateFromModal() {
    var vehicle = selectedVehicle();
    var service = value(fields.mdlEditService);
    var hour = value(fields.mdlEditHour);
    var minute = value(fields.mdlEditMinute);
    var ampm = value(fields.mdlEditAmpm);
    return {
      firstName: value(fields.mdlEditFirstName),
      lastName: value(fields.mdlEditLastName),
      phone: value(fields.mdlEditPhone),
      email: value(fields.mdlEditEmail),
      service: service,
      vehicleId: value(fields.mdlEditVehicle),
      vehicle: vehicle ? vehicle.name : '',
      passengers: value(fields.mdlEditPassengers),
      pickup: value(fields.mdlEditPickup),
      dropoff: value(fields.mdlEditDropoff),
      stops: Array.prototype.map.call(
        stopsContainer ? stopsContainer.querySelectorAll('input[data-stop-value]') : [],
        function (input) { return value(input); }
      ).filter(Boolean),
      date: value(fields.mdlEditDate),
      hour: hour,
      minute: minute,
      ampm: ampm,
      time: hour && minute ? hour + ':' + minute + (ampm ? ' ' + ampm : '') : '',
      endDate: service === 'hourly' ? value(fields.mdlEditEndDate) : '',
      endTime: service === 'hourly' ? value(fields.mdlEditEndTime) : '',
      flight: value(fields.mdlEditFlight),
      specialRequests: value(fields.mdlEditRequests),
      estimate: pageEstimate(),
      website: value(pageField('bk-website'))
    };
  }

  function paintEstimate(estimate) {
    estimate = estimate || pageEstimate();
    var price = document.getElementById('mdlPrice');
    var sub = document.getElementById('mdlPriceSub');
    if (!price || !sub) return;
    if (estimate && estimate.available && Number.isFinite(Number(estimate.total))) {
      price.textContent = '$' + estimate.total;
      sub.textContent = estimate.breakdown || copy.finalPrice;
    } else {
      price.textContent = copy.contactQuote;
      sub.textContent = copy.quoteGeneric;
    }
  }

  function clearModalError() {
    if (modalError) {
      modalError.classList.remove('show');
      modalError.textContent = '';
    }
  }

  function clearPageError() {
    var pageAlert = document.getElementById('alertError');
    if (pageAlert) {
      pageAlert.classList.remove('show');
      pageAlert.textContent = '';
    }
  }

  function clearAllErrors() {
    clearModalError();
    clearPageError();
  }

  function showModalError(message, field) {
    if (modalError) {
      modalError.textContent = message;
      modalError.classList.add('show');
    }
    if (field && typeof field.focus === 'function') field.focus();
  }

  function scheduleEstimate() {
    editRevision++;
    clearTimeout(estimateTimer);
    estimateTimer = setTimeout(function () {
      var revision = editRevision;
      syncModalToPage();
      if (typeof root.updateEstimate !== 'function') return;
      Promise.resolve(root.updateEstimate()).then(function (estimate) {
        if (revision === editRevision && modal.classList.contains('show')) paintEstimate(estimate);
      });
    }, 240);
  }

  function parseDate(valueText) {
    var parts = String(valueText || '').split('-').map(Number);
    return parts.length === 3 && parts.every(Number.isFinite)
      ? new Date(parts[0], parts[1] - 1, parts[2]) : null;
  }

  function endWindowValid() {
    var startDate = parseDate(value(fields.mdlEditDate));
    var startHour = Number(value(fields.mdlEditHour));
    var startMinute = Number(value(fields.mdlEditMinute));
    var startAmpm = value(fields.mdlEditAmpm);
    var endDate = parseDate(value(fields.mdlEditEndDate));
    var endParts = value(fields.mdlEditEndTime).split(':').map(Number);
    if (!startDate || !Number.isFinite(startHour) || !Number.isFinite(startMinute) ||
        !endDate || endParts.length !== 2 || !endParts.every(Number.isFinite)) return false;
    var startHour24 = (startHour % 12) + (startAmpm === 'PM' ? 12 : 0);
    var start = new Date(startDate.getFullYear(), startDate.getMonth(), startDate.getDate(),
      startHour24, startMinute);
    var end = new Date(endDate.getFullYear(), endDate.getMonth(), endDate.getDate(),
      endParts[0], endParts[1]);
    return end > start;
  }

  function validateModal() {
    var service = value(fields.mdlEditService);
    var required = [
      [fields.mdlEditVehicle, service ? '' : copy.missingTrip],
      [fields.mdlEditPickup, copy.missingTrip],
      [fields.mdlEditDate, copy.missingTrip],
      [fields.mdlEditHour, copy.missingTrip],
      [fields.mdlEditMinute, copy.missingTrip],
      [fields.mdlEditFirstName, copy.invalid],
      [fields.mdlEditLastName, copy.invalid],
      [fields.mdlEditPhone, copy.invalid]
    ];
    if (service !== 'hourly') required.push([fields.mdlEditDropoff, copy.missingTrip]);
    for (var i = 0; i < required.length; i++) {
      if (!value(required[i][0])) {
        showModalError(required[i][1], required[i][0]);
        return false;
      }
    }
    if (service === 'hourly' &&
        (!value(fields.mdlEditEndDate) || !value(fields.mdlEditEndTime))) {
      showModalError(copy.missingHourly, fields.mdlEditEndDate);
      return false;
    }
    if (service === 'hourly' && !endWindowValid()) {
      showModalError(copy.invalidWindow, fields.mdlEditEndTime);
      return false;
    }
    if (modalForm && !modalForm.checkValidity()) {
      modalForm.reportValidity();
      showModalError(copy.invalid, modalForm.querySelector(':invalid'));
      return false;
    }
    return true;
  }

  function refreshEstimateAndWait() {
    clearTimeout(estimateTimer);
    syncModalToPage();
    if (typeof root.updateEstimate !== 'function') return Promise.resolve(pageEstimate());
    var attempt = 0;
    function run() {
      var revision = editRevision;
      return Promise.resolve(root.updateEstimate()).then(function (estimate) {
        if (revision !== editRevision && attempt++ < 4) return run();
        if (revision === editRevision) paintEstimate(estimate);
        return revision === editRevision ? (estimate || pageEstimate()) : pageEstimate();
      });
    }
    return run();
  }

  function populateOptions() {
    var vehicleSelect = fields.mdlEditVehicle;
    if (vehicleSelect) {
      vehicleSelect.innerHTML = page.vehicles.map(function (vehicle) {
        var option = document.createElement('option');
        option.value = vehicle.id;
        option.textContent = vehicle.name;
        return option.outerHTML;
      }).join('');
    }
    var hourSelect = fields.mdlEditHour;
    if (hourSelect) hourSelect.innerHTML = [''].concat(
      ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    ).map(function (hour) {
      return '<option value="' + hour + '">' + (hour || '--') + '</option>';
    }).join('');
    var minuteSelect = fields.mdlEditMinute;
    if (minuteSelect) minuteSelect.innerHTML = [''].concat(['00', '15', '30', '45']).map(function (minute) {
      return '<option value="' + minute + '">' + (minute || '--') + '</option>';
    }).join('');
    var ampmSelect = fields.mdlEditAmpm;
    if (ampmSelect) ampmSelect.innerHTML = ['AM', 'PM'].map(function (part) {
      return '<option value="' + part + '">' + part + '</option>';
    }).join('');
    var paxSelect = fields.mdlEditPassengers;
    if (paxSelect) paxSelect.innerHTML = [''].concat(
      ['1', '2', '3', '4', '5', '6', '7–10', '11–14', '15–24', '25+']
    ).map(function (pax) {
      return '<option value="' + pax + '">' + (pax || (spanish ? 'Seleccionar…' : 'Select…')) + '</option>';
    }).join('');
  }

  function renderStops() {
    if (!stopsContainer) return;
    var stops = pageStops();
    stopsContainer.innerHTML = '';
    if (!stops.length) {
      var empty = document.createElement('p');
      empty.className = 'booking-editor-help';
      empty.textContent = copy.noStops;
      stopsContainer.appendChild(empty);
      return;
    }
    stops.forEach(function (stop) { addStopRow(stop); });
  }

  function addStopRow(initialValue) {
    if (!stopsContainer) return;
    stopSequence++;
    var row = document.createElement('div');
    row.className = 'booking-editor-stop';
    var input = document.createElement('input');
    input.type = 'text';
    input.autocomplete = 'off';
    input.placeholder = copy.stopPlaceholder;
    input.value = initialValue || '';
    input.dataset.stopValue = 'true';
    input.id = 'mdlEditStop' + stopSequence;
    var remove = document.createElement('button');
    remove.type = 'button';
    remove.className = 'booking-editor-stop-remove';
    remove.setAttribute('aria-label', spanish ? 'Eliminar parada' : 'Remove stop');
    remove.textContent = '×';
    remove.addEventListener('click', function () {
      row.remove();
      if (!stopsContainer.querySelector('input[data-stop-value]')) renderStops();
      syncStopsToPage();
      scheduleEstimate();
    });
    input.addEventListener('input', scheduleEstimate);
    row.appendChild(input);
    row.appendChild(remove);
    stopsContainer.appendChild(row);
    if (typeof root.initAddressAutocomplete === 'function') {
      root.initAddressAutocomplete(input, { restrict: true, pickupId: 'mdlEditPickup' });
    }
  }

  function populateFromPage() {
    if (fields.mdlEditDate) {
      var now = new Date();
      fields.mdlEditDate.min = now.getFullYear() + '-' +
        String(now.getMonth() + 1).padStart(2, '0') + '-' +
        String(now.getDate()).padStart(2, '0');
    }
    setValue('mdlEditService', serviceFromPage());
    setValue('mdlEditVehicle', page.selectedVehicle || '');
    setValue('mdlEditPickup', value(pageField('pickupInput')));
    setValue('mdlEditDropoff', value(pageField('dropoffInput')));
    setValue('mdlEditDate', value(pageField('dateInput')));
    setValue('mdlEditHour', value(pageField('timeHour')));
    setValue('mdlEditMinute', value(pageField('timeMin')));
    setValue('mdlEditAmpm', value(pageField('timeAmpm')) || 'AM');
    setValue('mdlEditEndDate', value(pageField('hourEndDate')));
    setValue('mdlEditEndTime', value(pageField('hourEndTime')));
    setValue('mdlEditFirstName', value(pageField('fname')));
    setValue('mdlEditLastName', value(pageField('lname')));
    setValue('mdlEditPhone', value(pageField('fphone')));
    setValue('mdlEditEmail', value(pageField('femail')));
    setValue('mdlEditPassengers', value(pageField('fpax')));
    setValue('mdlEditFlight', value(pageField('flightInput')));
    setValue('mdlEditRequests', value(pageField('fmessage')));
    if (fields.mdlEditPickup) copyAddressCoordinates(pageField('pickupInput'), fields.mdlEditPickup);
    if (fields.mdlEditDropoff) copyAddressCoordinates(pageField('dropoffInput'), fields.mdlEditDropoff);
    renderStops();
    paintPageService();
    paintEstimate(pageEstimate());
  }

  function setErrorOnPage(message) {
    var pageAlert = document.getElementById('alertError');
    if (pageAlert) {
      pageAlert.textContent = message;
      pageAlert.classList.add('show');
    }
  }

  function restoreFormDisabled(disabled) {
    ids.forEach(function (id) {
      if (fields[id]) fields[id].disabled = disabled || (id === 'mdlEditDropoff' && serviceFromPage() === 'hourly');
    });
    if (addStopButton) addStopButton.disabled = disabled;
    if (stopsContainer) stopsContainer.querySelectorAll('button,input').forEach(function (element) {
      element.disabled = disabled;
    });
  }

  function serializePayload() {
    var state = stateFromModal();
    var payload = core.buildBookingPayload(state, copy);
    var template = root.PHLBookingEmail.buildTemplateParams(payload.email);
    return { state: state, payload: payload, template: template };
  }

  function modalFocusables() {
    return Array.prototype.filter.call(
      modal.querySelectorAll('button, input, select, textarea, [tabindex]:not([tabindex="-1"])'),
      function (element) { return !element.disabled && element.offsetParent !== null; }
    );
  }

  function openEditor() {
    clearAllErrors();
    populateFromPage();
    previousFocus = document.activeElement;
    modal.classList.add('show');
    document.body.classList.add('booking-modal-open');
    modal.setAttribute('aria-hidden', 'false');
    var focusables = modalFocusables();
    if (focusables[0]) focusables[0].focus();
    refreshEstimateAndWait();
  }

  function closeEditor(force) {
    if ((sendInFlight || sendState.promise) && !force) return;
    modal.classList.remove('show');
    document.body.classList.remove('booking-modal-open');
    modal.setAttribute('aria-hidden', 'true');
    clearAllErrors();
    if (previousFocus && typeof previousFocus.focus === 'function') previousFocus.focus();
  }

  function bindField(field, handler) {
    if (!field) return;
    field.addEventListener('input', handler);
    field.addEventListener('change', handler);
  }

  function onServiceChange() {
    page.service = value(fields.mdlEditService) || 'airport';
    if (page.service === 'airport' && typeof root.clearStops === 'function') root.clearStops();
    if (page.service !== 'airport' && fields.mdlEditFlight) {
      fields.mdlEditFlight.value = '';
      var flight = pageField('flightInput');
      if (flight) flight.value = '';
    }
    paintPageService();
    renderStops();
    syncModalToPage();
    scheduleEstimate();
  }

  function onVehicleChange() {
    page.selectedVehicle = value(fields.mdlEditVehicle);
    syncModalToPage();
    scheduleEstimate();
  }

  function onRegularFieldChange() {
    syncModalToPage();
    scheduleEstimate();
  }

  populateOptions();
  paintPageService();
  if (fields.mdlEditPickup && typeof root.initAddressAutocomplete === 'function') {
    root.initAddressAutocomplete(fields.mdlEditPickup, { restrict: true });
  }
  if (fields.mdlEditDropoff && typeof root.initAddressAutocomplete === 'function') {
    root.initAddressAutocomplete(fields.mdlEditDropoff, { restrict: true, pickupId: 'mdlEditPickup' });
  }
  bindField(fields.mdlEditService, onServiceChange);
  bindField(fields.mdlEditVehicle, onVehicleChange);
  [
    fields.mdlEditPickup, fields.mdlEditDropoff, fields.mdlEditDate,
    fields.mdlEditHour, fields.mdlEditMinute, fields.mdlEditAmpm,
    fields.mdlEditEndDate, fields.mdlEditEndTime, fields.mdlEditFirstName,
    fields.mdlEditLastName, fields.mdlEditPhone, fields.mdlEditEmail,
    fields.mdlEditPassengers, fields.mdlEditFlight, fields.mdlEditRequests
  ].forEach(function (field) { bindField(field, onRegularFieldChange); });
  if (addStopButton) addStopButton.addEventListener('click', function () {
    var empty = stopsContainer && stopsContainer.querySelector('.booking-editor-help');
    if (empty) empty.remove();
    addStopRow('');
    var inputs = stopsContainer.querySelectorAll('input[data-stop-value]');
    if (inputs.length) inputs[inputs.length - 1].focus();
  });
  if (cancelButton) cancelButton.textContent = copy.cancel;
  if (confirmButton) {
    confirmButton.textContent = copy.confirm;
    confirmButton.addEventListener('click', function () { root.confirmAndSend(); });
  }
  if (cancelButton) cancelButton.addEventListener('click', closeEditor);
  modal.addEventListener('click', function (event) {
    if (sendInFlight || sendState.promise) {
      event.preventDefault();
      event.stopImmediatePropagation();
    }
  }, true);
  modal.addEventListener('click', function (event) {
    if (event.target === modal) closeEditor();
  });
  document.addEventListener('keydown', function (event) {
    if (!modal.classList.contains('show')) return;
    if (event.key === 'Escape') {
      event.preventDefault();
      closeEditor();
      return;
    }
    if (event.key !== 'Tab') return;
    var focusables = modalFocusables();
    if (!focusables.length) return;
    var first = focusables[0];
    var last = focusables[focusables.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  root.openEstimateModal = openEditor;
  var pageSubmitButton = document.getElementById('submitBtn');
  if (pageSubmitButton) pageSubmitButton.onclick = openEditor;
  root.closeModal = closeEditor;
  root.confirmAndSend = function () {
    if (sendInFlight || sendState.promise) return sendState.promise || Promise.resolve();
    sendInFlight = true;
    if (confirmButton) {
      confirmButton.disabled = true;
      confirmButton.textContent = copy.sending;
    }
    clearAllErrors();
    return sendGuard(async function () {
      try {
        syncModalToPage();
        if (!validateModal()) return;
        if (value(pageField('bk-website'))) {
          showModalError(copy.requestError);
          return;
        }
        restoreFormDisabled(true);
        await refreshEstimateAndWait();
        if (!validateModal()) throw new Error('validation');
        var serialized = serializePayload();
        await root.PHLBookingEmail.sendBookingEmail(serialized.template);
        clearAllErrors();
        if (typeof root.gtag === 'function') {
          root.gtag('event', 'quote_request_submit', { form_location: 'booking_page', service_type: serialized.state.service });
          root.gtag('event', 'qualify_lead', { form_location: 'booking_page', service_type: serialized.state.service, vehicle: serialized.state.vehicle });
        }
        closeEditor(true);
        var success = document.getElementById('alertSuccess');
        if (success) {
          var estimate = serialized.state.estimate;
          success.innerHTML = estimate && estimate.available && Number.isFinite(Number(estimate.total))
            ? (spanish ? '✅ <strong>¡Solicitud recibida!</strong> Cotización estimada: <strong>$' + estimate.total + '</strong>.' :
              '✅ <strong>Request received!</strong> Estimated fare: <strong>$' + estimate.total + '</strong>.')
            : (spanish ? '✅ <strong>¡Solicitud recibida!</strong> Nuestro representante te llamará pronto para confirmar tu reserva.' :
              '✅ <strong>Request received!</strong> Our representative will call you shortly to confirm your reservation.');
          success.classList.add('show');
        }
        var moovs = document.getElementById('moovsLink');
        if (moovs) moovs.style.display = 'block';
      } catch (error) {
        if (error && error.message === 'validation') return;
        showModalError(copy.requestError);
        setErrorOnPage(copy.requestError);
      } finally {
        sendInFlight = false;
        restoreFormDisabled(false);
        if (confirmButton) {
          confirmButton.disabled = false;
          confirmButton.textContent = copy.confirm;
        }
      }
    });
  };
}(window));