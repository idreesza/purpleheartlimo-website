'use strict';

const assert = require('node:assert/strict');
const test = require('node:test');
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..');

function loadWith(root) {
  const factory = require('../js/lead-submit.js');
  delete require.cache[require.resolve('../js/lead-submit.js')];
  // The module returns the function built for globalThis; rebuild for `root`.
  const source = fs.readFileSync(path.join(ROOT, 'js/lead-submit.js'), 'utf8');
  const module = { exports: {} };
  new Function('module', 'globalThis', source)(module, root);
  return module.exports || factory;
}

function fakeMailer(result) {
  const sent = [];
  return {
    sent,
    buildTemplateParams: (data) => ({ built: data }),
    sendBookingEmail: (params) => { sent.push(params); return result; }
  };
}

const body = (o) => ({ method: 'POST', body: JSON.stringify(o) });

test('sends the form payload through EmailJS and reports success', async () => {
  const mailer = fakeMailer(Promise.resolve({ status: 200 }));
  const send = loadWith({ PHLBookingEmail: mailer, location: { pathname: '/limo-service-dallas-tx/' } });
  const res = await send('/.netlify/functions/contact', body({
    name: 'Ana Ruiz', phone: '2145550100', message: 'Airport run', city: 'Dallas', flightNumber: 'AA1'
  }));
  assert.equal(res.ok, true);
  assert.equal((await res.json()).success, true);
  const data = mailer.sent[0].built;
  assert.equal(data.name, 'Ana Ruiz');
  assert.match(data.notes, /Airport run/);
  assert.match(data.notes, /City: Dallas/);
  assert.equal(data.flight, 'AA1');
  assert.match(data.source, /limo-service-dallas-tx/);
});

test('reports failure when EmailJS rejects', async () => {
  const send = loadWith({ PHLBookingEmail: fakeMailer(Promise.reject(new Error('x'))) });
  const res = await send('/x', body({ name: 'A' }));
  assert.equal(res.ok, false);
  assert.ok((await res.json()).error);
});

test('honeypot submissions succeed quietly without sending', async () => {
  const mailer = fakeMailer(Promise.resolve({ status: 200 }));
  const send = loadWith({ PHLBookingEmail: mailer });
  const res = await send('/x', body({ name: 'Bot', website: 'spam.example' }));
  assert.equal(res.ok, true);
  assert.equal(mailer.sent.length, 0);
});

test('missing name or missing mailer is an error, not a false success', async () => {
  const send = loadWith({ PHLBookingEmail: fakeMailer(Promise.resolve({})) });
  assert.equal((await send('/x', body({ phone: '1' }))).ok, false);
  const noMailer = loadWith({});
  assert.equal((await noMailer('/x', body({ name: 'A' }))).ok, false);
});

test('every page posting a lead loads booking-email.js and lead-submit.js', () => {
  const skip = new Set(['exports', 'reports', 'compiled-static', 'dist', 'node_modules', 'attached_assets', '.git']);
  const pages = [];
  (function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (skip.has(entry.name) || entry.name.startsWith('.')) continue;
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (entry.name.endsWith('.html')) pages.push(full);
    }
  })(ROOT);
  const bad = [];
  for (const page of pages) {
    const html = fs.readFileSync(page, 'utf8');
    const rel = path.relative(ROOT, page).split(path.sep).join('/');
    if (html.includes('PHLLeadFetch(') &&
        !(html.includes('src="/js/booking-email.js"') && html.includes('src="/js/lead-submit.js"'))) {
      bad.push(rel + ': missing scripts');
    }
    // Only the booking pages keep the old server call, inside a function
    // that is replaced by their EmailJS confirmAndSend before it can run.
    if (/(?<![\w.])fetch\(\s*['"]\/\.netlify\/functions\/contact/.test(html) &&
        !['booking.html', 'es/booking.html'].includes(rel)) {
      bad.push(rel + ': posts to server contact endpoint (needs SendGrid)');
    }
  }
  assert.deepEqual(bad, []);
});
