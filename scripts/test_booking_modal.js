'use strict';

const assert = require('node:assert/strict');
const test = require('node:test');
const fs = require('node:fs');
const {
  serializeModalData,
  buildBookingPayload,
  createSubmissionGuard
} = require('../js/booking-modal-editor-core.js');

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