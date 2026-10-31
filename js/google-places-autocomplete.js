/* Purple Heart Limo — Places API (New) address autocomplete.
 *
 * The Maps JavaScript API and its restricted browser key are loaded only
 * after an address field receives focus.  The key is intentionally public:
 * Google Cloud must restrict it to this site's referrers and to the Maps
 * JavaScript/Places APIs.  No server-side Maps key is requested here.
 */
(function () {
  'use strict';

  var KEY_ENDPOINT = '/api/google-maps-browser-key';
  var TX_OK_BOUNDS = {
    west: -106.65,
    north: 37.05,
    east: -93.50,
    south: 25.80
  };
  // Keep the loader promise on window as well as in this closure. This
  // prevents duplicate Maps API tags if a page shell or hot reload evaluates
  // this shared file more than once.
  var loaderState = window.__PHL_GOOGLE_PLACES_LOADER__;
  if (!loaderState) {
    loaderState = { promise: null };
    window.__PHL_GOOGLE_PLACES_LOADER__ = loaderState;
  }
  var instances = window.__PHL_GOOGLE_PLACES_INSTANCES__;
  if (!instances) {
    instances = new WeakMap();
    window.__PHL_GOOGLE_PLACES_INSTANCES__ = instances;
  }
  var styleAdded = !!document.querySelector('style[data-phl-google-places]');

  function isSpanish() {
    var html = document.documentElement;
    return html && (html.getAttribute('lang') || '').toLowerCase().indexOf('es') === 0;
  }

  function message(key) {
    var es = isSpanish();
    var copy = {
      loading: es ? 'Cargando sugerencias de direcciones de Google…' : 'Loading Google address suggestions…',
      ready: '',
      unavailable: es
        ? 'La búsqueda de direcciones de Google no está disponible. Puede ingresar la dirección manualmente.'
        : 'Google address search is unavailable. You can enter the address manually.',
      noResults: es
        ? 'No se encontraron sugerencias de Google. Puede ingresar la dirección manualmente.'
        : 'No Google address suggestions found. You can enter the address manually.',
      details: es
        ? 'Google no pudo cargar los detalles de esta dirección. Puede ingresarla manualmente.'
        : 'Google could not load this address details. You can enter it manually.'
    };
    return copy[key] || '';
  }

  function addStyles() {
    if (!styleAdded && document.querySelector('style[data-phl-google-places]')) {
      styleAdded = true;
    }
    if (styleAdded) return;
    styleAdded = true;
    var style = document.createElement('style');
    style.setAttribute('data-phl-google-places', '');
    style.textContent =
      '.phl-place-list{box-sizing:border-box;position:fixed;z-index:2147483600;' +
      'display:none;margin:0;padding:0;list-style:none;background:#fff;' +
      'border:1px solid rgba(45,0,69,.18);border-radius:0 0 10px 10px;' +
      'max-height:280px;overflow-y:auto;box-shadow:0 12px 32px rgba(0,0,0,.24);' +
      'font-family:Inter,Arial,sans-serif;color:#222}' +
      '.phl-place-list.phl-place-list-dark{background:#1a1a2e;' +
      'border-color:rgba(255,255,255,.18);box-shadow:0 12px 32px rgba(0,0,0,.5)}' +
      '.phl-place-item{display:block;width:100%;box-sizing:border-box;padding:10px 14px;' +
      'border:0;border-bottom:1px solid rgba(45,0,69,.07);background:transparent;' +
      'color:#333;text-align:left;cursor:pointer;font:inherit;line-height:1.4}' +
      '.phl-place-list.phl-place-list-dark .phl-place-item{color:rgba(255,255,255,.92);' +
      'border-bottom-color:rgba(255,255,255,.08)}' +
      '.phl-place-item:last-of-type{border-bottom:0}' +
      '.phl-place-item:hover,.phl-place-item.phl-place-active,' +
      '.phl-place-list.phl-place-list-dark .phl-place-item:hover,' +
      '.phl-place-list.phl-place-list-dark .phl-place-item.phl-place-active{' +
      'background:rgba(201,168,76,.18);color:#8a6d1f}' +
      '.phl-place-list.phl-place-list-dark .phl-place-item:hover,' +
      '.phl-place-list.phl-place-list-dark .phl-place-item.phl-place-active{color:#fff}' +
      '.phl-place-main{display:block;font-size:.84rem;font-weight:600}' +
      '.phl-place-sub{display:block;margin-top:2px;font-size:.73rem;color:#6a6a6a}' +
      '.phl-place-list.phl-place-list-dark .phl-place-sub{color:rgba(255,255,255,.65)}' +
      '.phl-place-attribution{padding:6px 10px 7px;text-align:right;color:#6a6a6a;' +
      'font-size:10px;line-height:1.2;background:#fff}' +
      '.phl-place-attribution img{display:inline-block;width:120px;height:14px;' +
      'max-width:100%;object-fit:contain;vertical-align:middle}' +
      '.phl-place-list.phl-place-list-dark .phl-place-attribution{color:#6a6a6a;background:#fff}' +
      '.phl-place-status{display:none;margin-top:4px;font-size:.72rem;line-height:1.35;color:#6a6a6a}' +
      '.phl-place-status.phl-place-status-visible{display:block}' +
      '.phl-place-status.phl-place-status-error{color:#b42318}';
    document.head.appendChild(style);
  }

  function asText(value) {
    if (value === null || value === undefined) return '';
    return typeof value.toString === 'function' ? value.toString() : String(value);
  }

  function resolveElement(value) {
    if (!value) return null;
    if (typeof value === 'string') return document.getElementById(value);
    return value.nodeType ? value : null;
  }

  function setStatus(instance, text, error) {
    var status = instance.status;
    if (!status) return;
    status.textContent = text || '';
    status.classList.toggle('phl-place-status-visible', !!text);
    status.classList.toggle('phl-place-status-error', !!error);
    if (text) status.setAttribute('role', 'status');
  }

  function hideList(instance) {
    instance.list.style.display = 'none';
    instance.input.setAttribute('aria-expanded', 'false');
    instance.input.removeAttribute('aria-activedescendant');
    instance.activeIndex = -1;
  }

  function positionList(instance) {
    if (instance.list.style.display === 'none') return;
    var rect = instance.input.getBoundingClientRect();
    instance.list.style.top = rect.bottom + 'px';
    instance.list.style.left = rect.left + 'px';
    instance.list.style.width = rect.width + 'px';
  }

  function hasImportLibrary() {
    return window.google && window.google.maps &&
      typeof window.google.maps.importLibrary === 'function';
  }

  function findExistingMapsScript() {
    var scripts = document.getElementsByTagName('script');
    for (var i = 0; i < scripts.length; i++) {
      var src = scripts[i].getAttribute('src') || '';
      if (src.indexOf('/maps/api/js') !== -1 &&
          (src.indexOf('maps.google') !== -1 || src.indexOf('googleapis.com') !== -1)) {
        return scripts[i];
      }
    }
    return null;
  }

  function waitForExistingMapsScript(script) {
    return new Promise(function (resolve, reject) {
      if (hasImportLibrary()) {
        resolve();
        return;
      }
      var settled = false;
      function finish(callback, value) {
        if (settled) return;
        settled = true;
        script.removeEventListener('load', onLoad);
        script.removeEventListener('error', onError);
        callback(value);
      }
      function onLoad() {
        if (hasImportLibrary()) finish(resolve);
        else finish(reject, new Error('Google Maps library unavailable'));
      }
      function onError() {
        finish(reject, new Error('Google Maps JavaScript API failed to load'));
      }
      script.addEventListener('load', onLoad, { once: true });
      script.addEventListener('error', onError, { once: true });
      // A completed script will not emit load again for listeners added here.
      if (script.readyState === 'complete') onLoad();
    });
  }

  function installAuthFailureMonitor() {
    var previous = window.gm_authFailure;
    var rejectFailure;
    var failure = new Promise(function (resolve, reject) {
      rejectFailure = reject;
    });
    var handler = function () {
      if (typeof previous === 'function') {
        try { previous.apply(window, arguments); } catch (ignored) {}
      }
      rejectFailure(new Error('Google Maps authentication failed'));
    };
    window.gm_authFailure = handler;
    return {
      failure: failure,
      restore: function () {
        if (window.gm_authFailure === handler) window.gm_authFailure = previous;
      }
    };
  }

  function importPlacesLibrary() {
    if (!hasImportLibrary()) {
      return Promise.reject(new Error('Google Maps library unavailable'));
    }
    var monitor = installAuthFailureMonitor();
    return Promise.race([
      window.google.maps.importLibrary('places'),
      monitor.failure
    ]).finally(monitor.restore);
  }

  function installDynamicImportLoader(browserKey) {
    if (hasImportLibrary()) return;
    var google = window.google || (window.google = {});
    var maps = google.maps || (google.maps = {});
    if (typeof maps.importLibrary === 'function') return;

    var requested = new Set();
    var bootstrapPromise = null;
    var startBootstrap = function () {
      if (bootstrapPromise) return bootstrapPromise;
      bootstrapPromise = new Promise(function (resolve, reject) {
        var script = document.createElement('script');
        var query = 'key=' + encodeURIComponent(browserKey) +
          '&v=weekly&loading=async&libraries=' + encodeURIComponent(Array.from(requested).join(',')) +
          '&callback=google.maps.__ib__';
        script.src = 'https://maps.googleapis.com/maps/api/js?' + query;
        script.async = true;
        script.defer = true;
        script.dataset.phlGooglePlaces = 'true';
        maps.__ib__ = resolve;
        script.onerror = function () {
          reject(new Error('Google Maps JavaScript API failed to load'));
        };
        document.head.appendChild(script);
      });
      return bootstrapPromise;
    };
    var loader = function (libraryName) {
      requested.add(libraryName);
      return startBootstrap().then(function () {
        if (maps.importLibrary === loader) {
          throw new Error('Google Maps importLibrary unavailable');
        }
        return maps.importLibrary(libraryName);
      });
    };
    // Publish the bootstrap function before inserting the async script, as
    // Google's official dynamic-import loader does.
    maps.importLibrary = loader;
  }

  async function loadPlaces() {
    if (loaderState.promise) return loaderState.promise;
    var attempt = (async function () {
      // Reuse an already-loaded Maps loader instead of appending another
      // script. This also safely rejects an existing loader's auth/library
      // failure rather than silently falling back to a second provider.
      if (hasImportLibrary()) return importPlacesLibrary();
      var existingScript = findExistingMapsScript();
      if (existingScript) {
        var existingMonitor = installAuthFailureMonitor();
        try {
          await Promise.race([
            waitForExistingMapsScript(existingScript),
            existingMonitor.failure
          ]);
        } finally {
          existingMonitor.restore();
        }
        if (!hasImportLibrary()) throw new Error('Google Maps library unavailable');
        return importPlacesLibrary();
      }

      var response = await fetch(KEY_ENDPOINT, {
        cache: 'no-store',
        credentials: 'same-origin'
      });
      if (!response.ok) throw new Error('Google Maps browser key unavailable');
      var config = await response.json();
      var browserKey = typeof config.key === 'string' ? config.key.trim() : '';
      if (!browserKey) throw new Error('Google Maps browser key unavailable');

      var monitor = installAuthFailureMonitor();
      try {
        // Use Google's Dynamic Library Import bootstrap rather than a direct
        // API tag plus importLibrary. The bootstrap is the supported loader
        // that coalesces libraries and protects a page from duplicate loads.
        installDynamicImportLoader(browserKey);
        return await Promise.race([
          window.google.maps.importLibrary('places'),
          monitor.failure
        ]);
      } finally {
        monitor.restore();
      }
    }());

    // Allow a later focus to retry after a temporary network failure, without
    // ever printing or retaining the key in an error message.
    loaderState.promise = attempt.catch(function (error) {
      loaderState.promise = null;
      throw error;
    });
    return loaderState.promise;
  }

  function clearCoordinates(instance) {
    delete instance.input.dataset.lat;
    delete instance.input.dataset.lon;
    delete instance.input.dataset.placeId;
    instance.selectedValue = '';
  }

  function requestFor(instance, inputValue, places) {
    var request = {
      input: inputValue,
      sessionToken: instance.sessionToken,
      includedRegionCodes: ['us'],
      language: isSpanish() ? 'es' : 'en',
      region: 'us'
    };
    if (instance.options.restrict) {
      request.locationRestriction = TX_OK_BOUNDS;
    } else {
      request.locationBias = TX_OK_BOUNDS;
    }
    var pickup = resolveElement(instance.options.pickupId);
    if (pickup && pickup.dataset.lat && pickup.dataset.lon) {
      var lat = Number(pickup.dataset.lat);
      var lng = Number(pickup.dataset.lon);
      if (Number.isFinite(lat) && Number.isFinite(lng)) {
        request.origin = { lat: lat, lng: lng };
      }
    }
    return request;
  }

  function showPredictions(instance, predictions) {
    var list = instance.list;
    list.innerHTML = '';
    if (!predictions.length) {
      hideList(instance);
      setStatus(instance, message('noResults'), true);
      return;
    }
    predictions.forEach(function (prediction, index) {
      var item = document.createElement('li');
      item.className = 'phl-place-item';
      item.id = instance.input.id + '-google-place-' + index;
      item.setAttribute('role', 'option');
      item.setAttribute('aria-selected', 'false');
      item.dataset.index = String(index);

      var main = document.createElement('span');
      main.className = 'phl-place-main';
      main.textContent = asText(prediction.text);
      item.appendChild(main);
      if (prediction.secondaryText) {
        var secondary = document.createElement('span');
        secondary.className = 'phl-place-sub';
        secondary.textContent = asText(prediction.secondaryText);
        item.appendChild(secondary);
      }
      list.appendChild(item);
    });

    var attribution = document.createElement('li');
    attribution.className = 'phl-place-attribution';
    attribution.setAttribute('role', 'presentation');
    attribution.setAttribute('aria-hidden', 'true');
    var logo = document.createElement('img');
    logo.src = 'https://maps-docs-team.web.app/samples/place-autocomplete-data-simple/dist/powered_by_google_on_white.png';
    logo.alt = 'Powered by Google';
    logo.width = 120;
    logo.height = 14;
    logo.decoding = 'async';
    attribution.appendChild(logo);
    list.appendChild(attribution);
    list.style.display = 'block';
    positionList(instance);
    instance.input.setAttribute('aria-expanded', 'true');
    setStatus(instance, '', false);
  }

  async function search(instance, inputValue, sequence) {
    var places;
    try {
      places = await loadPlaces();
      if (sequence !== instance.sequence) return;
      var api = places.AutocompleteSuggestion;
      if (!api || typeof api.fetchAutocompleteSuggestions !== 'function') {
        throw new Error('Google Places autocomplete unavailable');
      }
      if (!instance.sessionToken) instance.sessionToken = new places.AutocompleteSessionToken();
      var result = await api.fetchAutocompleteSuggestions(
        requestFor(instance, inputValue, places)
      );
      if (sequence !== instance.sequence) return;
      var suggestions = (result && result.suggestions) || [];
      instance.predictions = suggestions.map(function (suggestion) {
        return suggestion && suggestion.placePrediction;
      }).filter(Boolean);
      showPredictions(instance, instance.predictions);
    } catch (error) {
      if (sequence !== instance.sequence) return;
      hideList(instance);
      instance.sessionToken = null;
      setStatus(instance, message('unavailable'), true);
    }
  }

  async function selectPrediction(instance, index) {
    var prediction = instance.predictions[index];
    if (!prediction) return;
    instance.sequence++;
    hideList(instance);
    var fallbackText = asText(prediction.text);
    instance.input.value = fallbackText;
    setStatus(instance, message('loading'), false);
    try {
      var place = prediction.toPlace();
      await place.fetchFields({ fields: ['formattedAddress', 'location', 'displayName'] });
      var location = place.location;
      var lat = location && typeof location.lat === 'function' ? location.lat() : location && location.lat;
      var lng = location && typeof location.lng === 'function' ? location.lng() : location && location.lng;
      var formatted = asText(place.formattedAddress) || fallbackText;
      instance.input.value = formatted;
      if (Number.isFinite(Number(lat)) && Number.isFinite(Number(lng))) {
        instance.input.dataset.lat = String(lat);
        instance.input.dataset.lon = String(lng);
      }
      var placeId = place.id || prediction.placeId;
      if (placeId) instance.input.dataset.placeId = String(placeId);
      instance.selectedValue = instance.input.value;
      instance.sessionToken = null;
      setStatus(instance, '', false);
      instance.suppressNextInput = true;
      instance.input.dispatchEvent(new Event('input', { bubbles: true }));
      instance.input.dispatchEvent(new Event('change', { bubbles: true }));
    } catch (error) {
      // Keep the selected prediction in the field so manual entry remains
      // possible, while clearly identifying that Google details were not used.
      instance.sessionToken = null;
      clearCoordinates(instance);
      setStatus(instance, message('details'), true);
      instance.suppressNextInput = true;
      instance.input.dispatchEvent(new Event('input', { bubbles: true }));
      instance.input.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }

  function showLoading(instance) {
    setStatus(instance, message('loading'), false);
  }

  function createInstance(input, options) {
    addStyles();
    options = options || {};
    var dropdown = resolveElement(options.dropdown);
    var list = dropdown || document.getElementById(input.id + '-google-places') || document.createElement('ul');
    var dark = input.id === 'pickup-input' || input.id === 'dropoff-input' ||
      input.id.indexOf('stop-input-') === 0;
    list.classList.add('phl-place-list');
    list.classList.toggle('phl-place-list-dark', dark);
    list.setAttribute('role', 'listbox');
    list.setAttribute('aria-label', input.getAttribute('aria-label') ||
      (input.labels && input.labels[0] && input.labels[0].textContent.trim()) ||
      input.getAttribute('placeholder') || input.id);
    // Existing booking CSS targets .ac-list/.stop-ac and is intentionally
    // kept for layout compatibility. Inline geometry/style here prevents
    // those legacy rules from defeating the fixed, body-level list.
    Object.assign(list.style, {
      position: 'fixed',
      zIndex: '2147483600',
      margin: '0',
      padding: '0',
      listStyle: 'none',
      right: 'auto',
      maxHeight: '280px',
      overflowY: 'auto',
      boxSizing: 'border-box',
      borderRadius: '0 0 10px 10px',
      boxShadow: '0 12px 32px rgba(0,0,0,.24)',
      background: dark ? '#1a1a2e' : '#fff',
      border: dark ? '1px solid rgba(255,255,255,.18)' : '1px solid rgba(45,0,69,.18)'
    });
    list.style.display = 'none';
    // Fixed positioning prevents an ancestor's backdrop-filter or overflow
    // from clipping the list. Existing booking dropdown nodes stay in their
    // rows so clearing dynamic stops removes them normally; newly-created
    // lists are attached to <body>.
    if (!dropdown && list.parentNode !== document.body) document.body.appendChild(list);

    var status = document.getElementById(input.id + '-place-status');
    if (!status) {
      status = document.createElement('div');
      status.id = input.id + '-place-status';
      status.className = 'phl-place-status';
      status.setAttribute('aria-live', 'polite');
      if (input.parentNode) input.parentNode.appendChild(status);
    }

    var instance = {
      input: input,
      list: list,
      status: status,
      options: options,
      sessionToken: null,
      sequence: 0,
      timer: null,
      activeIndex: -1,
      predictions: [],
      selectedValue: '',
      suppressNextInput: false
    };
    instances.set(input, instance);
    input.setAttribute('role', 'combobox');
    input.setAttribute('aria-autocomplete', 'list');
    input.setAttribute('aria-controls', list.id || (input.id + '-google-places'));
    if (!list.id) list.id = input.id + '-google-places';
    input.setAttribute('aria-expanded', 'false');
    if (!input.labels || !input.labels.length) {
      if (!input.hasAttribute('aria-label') && !input.hasAttribute('aria-labelledby')) {
        input.setAttribute('aria-label', input.getAttribute('placeholder') || input.id);
      }
    }
    var descriptions = (input.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean);
    if (descriptions.indexOf(status.id) < 0) descriptions.push(status.id);
    input.setAttribute('aria-describedby', descriptions.join(' '));

    input.addEventListener('focus', function () {
      showLoading(instance);
      loadPlaces().then(function () {
        if (!input.value.trim()) setStatus(instance, message('ready'), false);
      }).catch(function () {
        hideList(instance);
        setStatus(instance, message('unavailable'), true);
      });
    });

    input.addEventListener('input', function () {
      // Selecting a prediction dispatches an input event for the page's
      // pricing listeners. Do not treat that programmatic notification as
      // freshly typed text, or it immediately reopens the suggestion search.
      if (instance.suppressNextInput) {
        instance.suppressNextInput = false;
        clearTimeout(instance.timer);
        instance.sequence++;
        instance.activeIndex = -1;
        instance.predictions = [];
        hideList(instance);
        return;
      }
      var value = input.value.trim();
      if (instance.selectedValue && value !== instance.selectedValue) clearCoordinates(instance);
      clearTimeout(instance.timer);
      instance.sequence++;
      instance.activeIndex = -1;
      instance.predictions = [];
      hideList(instance);
      if (value.length < 3) {
        if (value) showLoading(instance);
        else setStatus(instance, message('ready'), false);
        return;
      }
      showLoading(instance);
      var sequence = instance.sequence;
      instance.timer = setTimeout(function () {
        search(instance, value, sequence);
      }, 300);
    });

    input.addEventListener('keydown', function (event) {
      if (instance.list.style.display === 'none' || !instance.predictions.length) return;
      if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
        event.preventDefault();
        var delta = event.key === 'ArrowDown' ? 1 : -1;
        instance.activeIndex = instance.activeIndex < 0
          ? (delta > 0 ? 0 : instance.predictions.length - 1)
          : (instance.activeIndex + delta + instance.predictions.length) % instance.predictions.length;
        Array.prototype.forEach.call(
          instance.list.querySelectorAll('.phl-place-item'),
          function (item, index) {
            var active = index === instance.activeIndex;
            item.classList.toggle('phl-place-active', active);
            item.setAttribute('aria-selected', active ? 'true' : 'false');
          }
        );
        var active = instance.list.querySelector('.phl-place-active');
        if (active) input.setAttribute('aria-activedescendant', active.id);
      } else if (event.key === 'Enter' && instance.activeIndex >= 0) {
        event.preventDefault();
        selectPrediction(instance, instance.activeIndex);
      } else if (event.key === 'Escape') {
        hideList(instance);
      }
    });

    list.addEventListener('mousedown', function (event) {
      var item = event.target.closest('.phl-place-item');
      if (!item) return;
      event.preventDefault();
      selectPrediction(instance, Number(item.dataset.index));
    });

    input.addEventListener('blur', function () {
      setTimeout(function () {
        hideList(instance);
        if (document.activeElement !== input) instance.sessionToken = null;
      }, 180);
    });

    document.addEventListener('mousedown', function (event) {
      if (event.target !== input && !list.contains(event.target)) hideList(instance);
    });
    window.addEventListener('scroll', function () { positionList(instance); }, true);
    window.addEventListener('resize', function () { positionList(instance); });
    return instance;
  }

  window.initGooglePlacesAutocomplete = function (inputOrId, options) {
    var input = resolveElement(inputOrId);
    if (!input) return null;
    if (instances.has(input)) return instances.get(input);
    return createInstance(input, options);
  };
  // Shared name for forms that do not need to know the provider details.
  window.initAddressAutocomplete = window.initGooglePlacesAutocomplete;
}());