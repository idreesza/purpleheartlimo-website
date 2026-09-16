'use strict';

const assert = require('node:assert/strict');
const test = require('node:test');
const fs = require('node:fs');
const {
  serializeModalData,
  buildBookingPayload,
  createSubmissionGuard
} = require('../js/booking-modal-editor-core.js');
const {
  toggleExpanded,
  nextVehicleIndex,
  vehiclePresentation,
  selectedScrollTarget
} = require('../js/booking-vehicle-state.js');

test('both booking pages retain localized hourly editor fields', () => {
  const english = fs.readFileSync('booking.html', 'utf8');
  const spanish = fs.readFileSync('es/booking.html', 'utf8');
  for (const html of [english, spanish]) {
    assert.match(html, /id="mdlEditEndDate"/);
    assert.match(html, /id="mdlEditEndTime"/);
    assert.match(html, /id="mdlEditStops"/);
  }
  assert.match(spanish, /Obtener una cotización/);
});

test('vehicle state helper toggles once and advances a mobile swipe', () => {
  const selected = { selectedId: 'business-suv', expanded: false };
  const expanded = toggleExpanded(selected);
  assert.equal(expanded.expanded, true);
  assert.equal(toggleExpanded(expanded).expanded, false);

  const vehicleIds = ['sedan', 'business-suv', 'luxury-sedan'];
  assert.equal(vehicleIds[nextVehicleIndex(1, vehicleIds.length, 1)], 'luxury-sedan');
  assert.equal(vehicleIds[nextVehicleIndex(1, vehicleIds.length, -1)], 'sedan');
  assert.equal(vehicleIds[nextVehicleIndex(2, vehicleIds.length, 1)], 'sedan');
});

test('collapsed vehicle states keep the selected slide full and neighbours thumbnail-sized', () => {
  const pages = [
    fs.readFileSync('booking.html', 'utf8'),
    fs.readFileSync('es/booking.html', 'utf8')
  ];
  for (const html of pages) {
    assert.match(html, /vehicle-reveal\.is-collapsed \.veh-slide\.is-selected/);
    assert.match(html, /vehicle-reveal\.is-collapsed \.veh-slide\.is-thumbnail/);
    assert.match(html, /data-vehicle-id="\$\{v\.id\}"/);
    assert.match(html, /vehiclePresentation\(VEHICLES,selVeh,expanded\)/);
    assert.match(html, /const toggle=toggleNode\.cloneNode\(true\)/);
    assert.match(html, /expanded=window\.PHLVehicleState\.toggleExpanded/);
    assert.match(html, /touchend/);
    assert.match(html, /if\(selVeh&&!expanded\)/);
    assert.match(html, /chooseVehicle\(VEHICLES\[next\]\.id\)/);
    assert.match(html, /const syncVehicleLayout=\(\)=>/);
    assert.match(html, /new ResizeObserver\(syncVehicleLayout\)/);
    assert.match(html, /grid\.querySelector\('\.veh-slide\.is-selected'\)/);
    assert.match(html, /selectedScrollTarget\(slideLeft,trackLeft\)/);
    assert.match(html, /function jumpTo\(left\)[\s\S]*?viewport\.scrollLeft=Math\.max\(0,left\)/);
    assert.match(html, /jumpTo\(target\)/);
    assert.doesNotMatch(html, /has-selection/);
    assert.doesNotMatch(html, /index\s*\*\s*(?:slide|width)/i);
  }

  const modalStyles = fs.readFileSync('css/booking-modal-editor.css', 'utf8');
  assert.match(modalStyles, /\.vehicle-reveal\.is-collapsed \.veh-slide\.is-selected[\s\S]*?flex: 0 0 100%/);
  assert.match(modalStyles, /\.vehicle-reveal\.is-collapsed \.veh-slide\.is-selected[\s\S]*?width: 100%/);
  assert.match(modalStyles, /\.vehicle-reveal\.is-collapsed \.veh-slide\.is-thumbnail[\s\S]*?flex: 0 0 25%/);
  assert.match(modalStyles, /@media \(max-width: 767px\)[\s\S]*?\.vehicle-reveal\.is-collapsed \.veh-carousel[\s\S]*?padding: 0/);
  assert.doesNotMatch(modalStyles, /\.has-selection[\s\S]*!important/);
  assert.doesNotMatch(modalStyles, /\.veh-slide[\s\S]*?flex: 0 0 100% !important/);

  const ids = ['sedan', 'business-suv', 'luxury-sedan'];
  const collapsed = vehiclePresentation(ids, 'business-suv', false);
  assert.equal(collapsed.mode, 'collapsed');
  assert.deepEqual(collapsed.cards.map(card => [card.id, card.selected, card.size]), [
    ['sedan', false, 'thumbnail'],
    ['business-suv', true, 'full'],
    ['luxury-sedan', false, 'thumbnail']
  ]);
  const expanded = vehiclePresentation(ids, 'business-suv', true);
  assert.equal(expanded.mode, 'expanded');
  assert.ok(expanded.cards.every(card => card.size === 'full'));
  const switched = vehiclePresentation(ids, 'luxury-sedan', false);
  assert.equal(switched.selectedIndex, 2);
  assert.equal(switched.cards[2].selected, true);
  assert.equal(switched.cards[1].size, 'thumbnail');
  assert.equal(selectedScrollTarget(240, 80), 160);
  assert.equal(selectedScrollTarget(20, 80), 0);
});

test('ride cards map From/Desde prices through canonical class data', () => {
  const english = fs.readFileSync('booking.html', 'utf8');
  const spanish = fs.readFileSync('es/booking.html', 'utf8');
  for (const html of [english, spanish]) {
    assert.match(html, /function getPrice\(v\)[\s\S]*?window\.phlGetClass/);
    assert.match(html, /vehiclePriceMarkup\(v\)/);
    assert.match(html, /\$\{vehiclePriceMarkup\(v\)\}/);
  }
  assert.match(english, /const label=spanish\?'Desde':'From'/);
  assert.match(spanish, /veh-price">Desde \$\$\{price\}/);
  assert.match(english, /est-label">💰 Final Price/);
  assert.match(spanish, /est-label">💰 Precio final/);
});

test('serializes edited modal fields instead of the original page snapshot', () => {
  const data = serializeModalData({
    firstName: 'Ada',
    lastName: 'Lovelace',
    phone: '512-555-0199',
    email: 'ada@example.com',
    service: 'oneway',
    vehicleId: 'luxsedan',
    vehicle: 'Luxury Sedan',
    passengers: '2',
    pickup: 'New pickup address',
    dropoff: 'New destination',
    stops: ['Edited stop'],
    date: '2026-08-18',
    hour: '9',
    minute: '30',
    ampm: 'PM',
    specialRequests: 'Updated request'
  });

  assert.equal(data.name, 'Ada Lovelace');
  assert.equal(data.pickup, 'New pickup address');
  assert.deepEqual(data.stops, ['Edited stop']);
  assert.equal(data.vehicleId, 'luxsedan');
});

test('builds an EmailJS-ready payload containing every edited request detail', () => {
  const payload = buildBookingPayload({
    firstName: 'Ada',
    lastName: 'Lovelace',
    phone: '512-555-0199',
    email: '',
    service: 'hourly',
    vehicleId: 'sprinter',
    vehicle: 'Executive Sprinter',
    passengers: '7',
    pickup: 'Airport',
    dropoff: '',
    stops: ['Downtown', 'Hotel'],
    date: '2026-08-18',
    hour: '9',
    minute: '30',
    ampm: 'PM',
    endDate: '2026-08-19',
    endTime: '01:30',
    flight: 'AA123',
    specialRequests: 'Child seat',
    estimate: { available: false }
  }, { contactQuote: 'Contact us for a quote' });

  assert.equal(payload.email.name, 'Ada Lovelace');
  assert.equal(payload.email.firstName, 'Ada');
  assert.equal(payload.email.lastName, 'Lovelace');
  assert.equal(payload.email.vehicleId, 'sprinter');
  assert.equal(payload.email.pickup, 'Airport');
  assert.equal(payload.email.dropoff, '(Hourly — see stops)');
  assert.equal(payload.email.time, '9:30 PM');
  assert.equal(payload.email.endDate, '2026-08-19');
  assert.equal(payload.email.endTime, '01:30');
  assert.match(payload.email.notes, /PICKUP: Airport/);
  assert.match(payload.email.notes, /STOPS: Downtown → Hotel/);
  assert.match(payload.email.notes, /SPECIAL REQUESTS: Child seat/);
});

test('submission guard serializes concurrent handlers into one send', async () => {
  const shared = {};
  const guard = createSubmissionGuard(shared);
  let sends = 0;
  let release;
  const pending = new Promise(resolve => { release = resolve; });
  const first = guard(async () => {
    sends += 1;
    await pending;
    return 'sent';
  });
  const second = guard(async () => {
    sends += 1;
    return 'duplicate';
  });

  assert.strictEqual(first, second);
  release();
  assert.equal(await first, 'sent');
  assert.equal(sends, 1);
  assert.equal(shared.promise, null);
});

test('submission guard unlocks after an error so a retry can succeed', async () => {
  const guard = createSubmissionGuard({});
  let attempts = 0;
  await assert.rejects(
    guard(async () => {
      attempts += 1;
      throw new Error('temporary failure');
    }),
    /temporary failure/
  );

  assert.equal(await guard(async () => {
    attempts += 1;
    return 'sent';
  }), 'sent');
  assert.equal(attempts, 2);
});