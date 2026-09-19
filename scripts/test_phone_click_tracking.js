'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('js/sitewide-leads.js', 'utf8');

function setup(gtag) {
  const calls = [], listeners = [];
  const context = vm.createContext({
    window: { location: { pathname: '/booking.html' },
      gtag: gtag === undefined ? (...args) => calls.push(args) : gtag },
    document: { addEventListener: (type, fn, options) => listeners.push({ type, fn, options }) }
  });
  vm.runInContext(source, context);
  function click(href, location = 'nav', textNode = false) {
    const link = {
      textContent: 'Call',
      getAttribute: name => name === 'href' ? href : null,
      closest: selector => selector.includes('.mobile-bar')
        ? (location === 'floating_button' ? {} : null)
        : (location === 'body' || location === 'floating_button' ? null : { tagName: location.toUpperCase() })
    };
    const target = { closest: () => link };
    const event = {
      target: textNode ? { nodeType: 3, parentElement: target } : target,
      preventDefault() { throw Error('Tracking must not block calls'); }
    };
    listeners.forEach(listener => listener.fn(event));
  }
  return { context, calls, listeners, click };
}

test('one phone event per click, including nested and dynamic phone links', () => {
  const app = setup();
  app.click('tel:+18337400700', 'nav', true);
  app.click(' TEL:+18337400700 ', 'floating_button');
  assert.equal(app.calls.length, 2);
  assert.equal(app.calls[0][1], 'phone_call_click');
  assert.equal(app.calls[0][2].page_path, '/booking.html');
  assert.equal(app.calls[0][2].link_location, 'nav');
  assert.equal(app.calls[1][2].link_location, 'floating_button');
  assert.equal(app.calls[1][2].transport_type, 'beacon');
  assert.equal(app.listeners[0].options.capture, true);
  assert.equal(app.listeners[0].options.passive, true);
});

test('loading the shared script twice does not duplicate events', () => {
  const app = setup();
  vm.runInContext(source, app.context);
  app.click('tel:+18337400700', 'footer');
  assert.equal(app.calls.length, 1);
  assert.equal(app.calls[0][2].link_location, 'footer');
});

test('ordinary links do not count as calls and email tracking remains', () => {
  const app = setup();
  app.click('/booking.html');
  app.click('https://wa.me/18337400700');
  assert.equal(app.calls.length, 0);
  app.click('mailto:example@example.com');
  assert.equal(app.calls[0][1], 'email_click');
});

test('missing or failing analytics never blocks phone navigation', () => {
  assert.doesNotThrow(() => setup(null).click('tel:+18337400700'));
  assert.doesNotThrow(() => setup(() => { throw Error('blocked'); }).click('tel:+18337400700'));
});