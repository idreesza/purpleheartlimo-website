/* Purple Heart Limo — Flight Lookup Proxy (AviationStack)
   Keeps the API key server-side. Required env var: AVIATIONSTACK_API_KEY
   Usage: GET /.netlify/functions/flights?flight=AA1234
   Returns: { data: [ ...flight objects ] }  (same shape the page expects)
*/

const https = require('https');

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin':  '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Content-Type': 'application/json',
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }
  if (event.httpMethod !== 'GET') {
    return { statusCode: 405, headers, body: JSON.stringify({ error: 'Method not allowed', data: [] }) };
  }

  // Light anti-abuse: block hotlinking from foreign origins (deters casual quota theft).
  // A missing Referer is allowed so privacy-stripped legit visitors still work.
  const ref = (event.headers && (event.headers.referer || event.headers.Referer)) || '';
  if (ref) {
    try {
      const host = new URL(ref).hostname;
      const ok = /(^|\.)purpleheartlimo\.com$/.test(host) ||
                 /\.netlify\.app$/.test(host) ||
                 host === 'localhost' || host === '127.0.0.1';
      if (!ok) {
        return { statusCode: 403, headers, body: JSON.stringify({ error: 'Forbidden', data: [] }) };
      }
    } catch (_) { /* unparseable referer — allow through */ }
  }

  const flight = ((event.queryStringParameters && event.queryStringParameters.flight) || '')
    .trim().toUpperCase();

  if (!flight || !/^[A-Z0-9]{2,8}$/.test(flight)) {
    return { statusCode: 400, headers, body: JSON.stringify({ error: 'Invalid flight number', data: [] }) };
  }

  const key = process.env.AVIATIONSTACK_API_KEY;
  if (!key) {
    // No key configured — return empty so the page falls back to airline deep links
    return { statusCode: 200, headers, body: JSON.stringify({ data: [] }) };
  }

  try {
    const result = await lookupFlight(key, flight);
    return { statusCode: 200, headers, body: JSON.stringify({ data: result.data || [] }) };
  } catch (err) {
    console.error('AviationStack error:', err.message || err);
    // Soft-fail: empty data lets the page show airline deep links instead of erroring
    return { statusCode: 200, headers, body: JSON.stringify({ data: [], error: 'lookup_failed' }) };
  }
};

function lookupFlight(key, flight) {
  return new Promise((resolve, reject) => {
    const path = `/v1/flights?access_key=${encodeURIComponent(key)}` +
                 `&flight_iata=${encodeURIComponent(flight)}&limit=1`;

    const req = https.request(
      { hostname: 'api.aviationstack.com', path, method: 'GET' },
      (res) => {
        const chunks = [];
        res.on('data', (c) => chunks.push(c));
        res.on('end', () => {
          try { resolve(JSON.parse(Buffer.concat(chunks).toString() || '{}')); }
          catch (e) { reject(e); }
        });
      }
    );
    req.on('error', reject);
    req.setTimeout(10000, () => req.destroy(new Error('timeout')));
    req.end();
  });
}
