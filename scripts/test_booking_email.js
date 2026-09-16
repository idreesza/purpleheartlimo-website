'use strict';

const assert = require('node:assert/strict');
const test = require('node:test');
const { buildTemplateParams, sendBookingEmail } = require('../js/booking-email.js');

const trip = {
  name: 'Jordan Zaatreh',
  phone: '512-555-0100',
  email: 'rider@example.com',
  service: 'hourly',
  pickup: 'Austin-Bergstrom International Airport',
  dropoff: '(Hourly — see stops)',
  date: '2026-07-12',
  time: '8:30 PM',
  vehicle: 'Executive Sprinter',
  flight: 'AA123',
  notes: '=== BOOKING REQUEST ===\nPASSENGERS: 7\nSTOPS: Downtown → Hotel\nEND DATE: 2026-07-13\nEND TIME: 12:30 AM\nQUOTE: $480\nSPECIAL REQUESTS: Child seat',
  passengers: '7',
  stops: 'Downtown → Hotel',
  endDate: '2026-07-13',
  endTime: '12:30 AM',
  quote: '$480',
  specialRequests: 'Child seat',
  source: 'Booking Page'
};

test('builds one complete EmailJS payload for both recipients', () => {
  const payload = buildTemplateParams(trip);

  assert.equal(payload.to_email, 'j.zaatreh@gmail.com,idrees.csst@gmail.com');
  for (const field of ['from_name', 'phone', 'email', 'service', 'pickup', 'dropoff',
    'date', 'time', 'vehicle', 'flight', 'notes', 'source', 'passengers', 'stops',
    'end_date', 'end_time', 'quote', 'special_requests']) {
    assert.ok(Object.prototype.hasOwnProperty.call(payload, field), `missing ${field}`);
  }
  assert.match(payload.notes, /PASSENGERS: 7/);
  assert.match(payload.notes, /END TIME: 12:30 AM/);
  assert.equal(payload.special_requests, 'Child seat');
});

test('sends the payload once and accepts only HTTP 200', async () => {
  const payload = buildTemplateParams(trip);
  const calls = [];
  const client = {
    send: async (...args) => {
      calls.push(args);
      return { status: 200, text: 'OK' };
    }
  };

  const result = await sendBookingEmail(payload, { emailjs: client });

  assert.equal(result.status, 200);
  assert.equal(calls.length, 1);
  assert.equal(calls[0][2], payload);
});

test('rejects a failed EmailJS response without another send', async () => {
  let calls = 0;
  const client = {
    send: async () => {
      calls += 1;
      return { status: 500 };
    }
  };

  await assert.rejects(sendBookingEmail(buildTemplateParams(trip), { emailjs: client }));
  assert.equal(calls, 1);
});

test('keeps an optional email field safe when omitted', () => {
  const payload = buildTemplateParams({ ...trip, email: '' });
  assert.equal(payload.email, '—');
  assert.equal(payload.to_email, 'j.zaatreh@gmail.com,idrees.csst@gmail.com');
});