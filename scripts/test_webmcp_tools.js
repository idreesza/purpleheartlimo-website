'use strict';
const assert = require('node:assert/strict');
const test = require('node:test');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('js/webmcp-tools.js', 'utf8');

function fixture(filename = 'index.html', api = 'document') {
  const html = fs.readFileSync(filename, 'utf8');
  const home = filename === 'index.html';
  const elements = new Map();
  const events = [];
  const tools = [];
  const classes = () => ({ add() {}, remove() {}, toggle() {} });
  const node = (id, attrs = {}, content = '') => ({
    id, value: attrs.value || '', dataset: {}, textContent: content,
    classList: classes(), listeners: {},
    getAttribute(key) { return attrs[key] ?? null; },
    setAttribute(key, value) { attrs[key] = value; },
    addEventListener(key, fn) { this.listeners[key] = fn; },
    dispatchEvent(event) { events.push([id, event.type]); },
    querySelector() { return this.label || null; },
    querySelectorAll() { return this.options || []; },
    click() { if (this.service) sandbox.__PHLBookingPage.service = this.service; }
  });
  for (const match of html.matchAll(/<(?:input|div|form|span|textarea)\b([^>]*)>/g)) {
    const attrs = Object.fromEntries([...match[1].matchAll(/([\w-]+)="([^"]*)"/g)].map(m => [m[1], m[2]]));
    if (attrs.id) elements.set(attrs.id, node(attrs.id, attrs));
  }
  const options = id => {
    const start = html.indexOf(`id="${id}"`);
    const stop = html.indexOf('<input', start);
    return [...html.slice(start, stop).matchAll(/<div class="csel-opt[^"]*" onclick="([^"]*)"[^>]*>([^<]*)<\/div>/g)]
      .map((m, i) => node(`${id}-${i}`, { onclick: m[1] }, m[2]));
  };
  const homeVehicles = options('csel-vehicle');
  const homeMinutes = options('csel-min');
  const homePaxSource = html.match(/const PAX_OPTIONS = (\{[\s\S]*?\n\});/);
  const paxOptions = homePaxSource ? vm.runInNewContext('(' + homePaxSource[1] + ')') : null;
  const bookingVehicles = [
    { id: 'suv', name: 'Luxury SUV', pax: 6 },
    { id: 'sedan', name: 'Business Sedan', pax: 3 },
    { id: 'partybus', name: 'Luxury Party Bus', pax: 24 }
  ];
  const minuteOptions = ['00', '15', '30', '45'].map(v => ({ dataset: { v } }));
  for (const id of ['dateCdd', 'hourCdd', 'minCdd', 'ampmCdd', 'paxCdd']) {
    if (elements.has(id)) elements.get(id).label = node(`${id}-label`);
  }
  const doc = {
    readyState: 'complete',
    getElementById: id => elements.get(id) || null,
    querySelectorAll(selector) {
      if (selector === '#csel-vehicle .csel-opt') return homeVehicles;
      if (selector === '#csel-min .csel-opt') return homeMinutes;
      if (selector === '#minCdd .cdd-opt') return minuteOptions;
      if (selector === '.trip-tab') return ['airport', 'pointtopoint', 'hourly'].map(v =>
        node(v, { onclick: `setTab(this,'${v}')` }));
      if (selector === '#svcTabs .svc-tab') return ['airport', 'oneway', 'hourly'].map(v => {
        const n = node(v); n.dataset.svc = v; n.service = v; return n;
      });
      return [];
    }
  };
  const sandbox = {
    document: doc, navigator: {}, Event: class { constructor(type) { this.type = type; } },
    setTimeout, clearTimeout, console: { error() { assert.fail('Unexpected console error'); } },
    PAX_OPTIONS: paxOptions,
    _phlDebounce: null, _estDebounce: null, _estimateVersion: 0,
    __PHLBookingPage: { service: 'airport', selectedVehicle: null, vehicles: bookingVehicles, estimate: null },
    _quoteTab: 'airport', _phlLastFare: null,
    getActiveTab() { return sandbox._quoteTab === 'pointtopoint' ? 'oneway' : sandbox._quoteTab; },
    setTab(_button, value) { sandbox._quoteTab = value; },
    cselPick(_root, id, value) { elements.get(id).value = value; },
    onVehicleChange() { elements.get('pax-input').value = '1'; },
    checkCapacity() {},
    selectVehicle(value) { sandbox.__PHLBookingPage.selectedVehicle = value; },
    async refreshLivePricing() {
      sandbox._phlPricePromise = new Promise(resolve => setTimeout(() => {
        elements.get('price-value').textContent = 'Estimated fare: $213';
        sandbox._phlLastFare = { total: 213, vehicle: elements.get('vehicle-input').value };
        resolve();
      }, 25));
      await sandbox._phlPricePromise;
    },
    async updateEstimate() {
      await new Promise(resolve => setTimeout(resolve, 25));
      elements.get('estPrice').textContent = '$213';
      sandbox.__PHLBookingPage.estimate = { total: 213 };
    },
    submitQuote() { assert.fail('Lead submission forbidden'); },
    confirmAndSend() { assert.fail('Lead submission forbidden'); },
    gtag() { assert.fail('Conversion event forbidden'); },
    fetch() { assert.fail('New network endpoint forbidden'); }
  };
  sandbox.window = sandbox;
  sandbox.__PHLBookingPage = home ? undefined : sandbox.__PHLBookingPage;
  const context = { registerTool(tool) { tools.push(tool); return Promise.resolve(); } };
  if (api === 'document') doc.modelContext = context;
  else if (api === 'navigator') sandbox.navigator.modelContext = context;
  else if (api === 'blocked') doc.modelContext = { registerTool() { return Promise.reject(new Error('NotAllowedError')); } };
  vm.runInNewContext(source, sandbox);
  return { tools, elements, events, sandbox, html };
}
const input = {
  pickup: 'DFW Airport', dropoff: '2401 McKinney Avenue, Dallas',
  date: '2099-05-17', time: '13:30', passengers: 3,
  vehicle: 'Luxury SUV', name: 'Marisol Vega', phone: '+1 (214) 555-0183',
  email: 'marisol@example.com', service: 'airport'
};
const unpack = result => JSON.parse(result.content[0].text);

test('unsupported and permissions-blocked browsers remain quiet', async () => {
  assert.equal(fixture('index.html', 'unsupported').tools.length, 0);
  fixture('index.html', 'blocked');
  await new Promise(resolve => setTimeout(resolve, 5));
});
test('current document API and navigator prototype each register once with valid schema vocabulary', () => {
  for (const api of ['document', 'navigator']) {
    const f = fixture('index.html', api);
    assert.equal(f.tools.length, 1);
    const schema = f.tools[0].inputSchema;
    assert.equal(schema.type, 'object');
    assert.equal(schema.additionalProperties, false);
    assert.equal(new Set(schema.properties.vehicle.enum).size, 10);
    for (const name of schema.required) assert.ok(schema.properties[name]);
    for (const value of Object.values(schema.properties)) {
      assert.ok(['string', 'integer'].includes(value.type));
      assert.ok(value.description);
      if (value.pattern) new RegExp(value.pattern);
    }
    assert.doesNotMatch(f.html, /toolautosubmit/);
    assert.match(f.html, /toolname="prepare_limo_quote"/);
    assert.equal(f.tools[0].name, 'request_limo_quote');
  }
});
test('home tool fills actual fields, converts ISO/24-hour time, emits changes, awaits estimate and never submits', async () => {
  const f = fixture();
  const promise = f.tools[0].execute(input);
  assert.notEqual(f.elements.get('price-value').textContent, 'Estimated fare: $213');
  const output = unpack(await promise);
  assert.equal(output.status, 'estimate_ready');
  assert.equal(output.displayed_price, 'Estimated fare: $213');
  assert.equal(output.estimate.total, 213);
  assert.equal(output.submitted, false);
  assert.equal(output.requires_user_confirmation, true);
  for (const [id, expected] of Object.entries({
    'date-input': '05/17/2099', 'time-hour': '1', 'time-min': '30',
    'time-ampm': 'PM', 'vehicle-input': 'Luxury SUV', 'pax-input': '3',
    'quote-name': 'Marisol Vega', 'quote-phone': input.phone
  })) assert.equal(f.elements.get(id).value, expected, id);
  assert.ok(f.events.some(([id, event]) => id === 'pickup-input' && event === 'input'));
  assert.ok(f.events.some(([id, event]) => id === 'vehicle-input' && event === 'change'));
  let prevented = false;
  f.elements.get('booking-widget').listeners.submit({ preventDefault() { prevented = true; } });
  assert.equal(prevented, true);
});
test('invalid dates, time increments, unknown vehicles, phone, email and capacity reject before mutation', async () => {
  const f = fixture();
  for (const patch of [
    { date: '2020-01-01' }, { date: '2099-02-30' }, { time: '25:00' },
    { time: '13:17' }, { vehicle: 'Escalade' }, { phone: '123' },
    { email: 'not-an-email' }, { passengers: 7 }, { passengers: '3' },
    { name: ' ' }, { unexpected: true }
  ]) {
    const output = unpack(await f.tools[0].execute({ ...input, ...patch }));
    assert.equal(output.status, 'invalid_input', JSON.stringify(patch));
    assert.ok(output.errors.length);
    assert.equal(output.submitted, false);
  }
  assert.equal(f.events.length, 0);
});
test('English and Spanish standalone widgets use their actual IDs, date format, passenger groups and estimate', async () => {
  for (const filename of ['booking.html', 'es/booking.html']) {
    const f = fixture(filename);
    assert.equal(f.tools.length, 1);
    assert.equal(f.tools[0].inputSchema.properties.vehicle.enum.join(','), 'suv,sedan,partybus');
    const args = { ...input, vehicle: 'partybus', passengers: 17, first_name: 'Marisol', last_name: 'Vega' };
    delete args.name;
    const output = unpack(await f.tools[0].execute(args));
    assert.equal(output.status, 'estimate_ready');
    assert.equal(output.submitted, false);
    assert.equal(f.elements.get('dateInput').value, '2099-05-17');
    assert.equal(f.elements.get('timeHour').value, '1');
    assert.equal(f.elements.get('timeAmpm').value, 'PM');
    assert.equal(f.elements.get('fpax').value, '15–24');
    assert.equal(f.sandbox.__PHLBookingPage.selectedVehicle, 'partybus');
    const invalid = unpack(await f.tools[0].execute({ ...args, vehicle: 'sedan', passengers: 4 }));
    assert.equal(invalid.status, 'invalid_input');
    const hourly = unpack(await f.tools[0].execute({ ...args, service: 'hourly' }));
    assert.equal(hourly.status, 'invalid_input');
    const endBeforeStart = unpack(await f.tools[0].execute({
      ...args, service: 'hourly', end_date: args.date, end_time: '12:00'
    }));
    assert.equal(endBeforeStart.status, 'invalid_input');
  }
});
test('registration schemas are serializable JSON documents', () => {
  for (const filename of ['index.html', 'booking.html', 'es/booking.html']) {
    const schema = fixture(filename).tools[0].inputSchema;
    const restored = JSON.parse(JSON.stringify(schema));
    assert.equal(restored.type, 'object');
    if (process.env.PRINT_WEBMCP_SCHEMAS) console.log(JSON.stringify(restored));
  }
});
