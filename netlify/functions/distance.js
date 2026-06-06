/* Purple Heart Limo — Distance / Drive-Time Proxy (Google Routes API)
   Keeps the API key server-side. Required env var: GOOGLE_MAPS_API_KEY
   Usage: GET /.netlify/functions/distance?origin=ADDR&destination=ADDR
          (also reachable at /api/distance via netlify.toml redirect)
   Returns: { meters, miles, seconds, minutes }
*/

const https = require('https');

function postJson(urlObj, payload, extraHeaders) {
  return new Promise((resolve, reject) => {
    const body = Buffer.from(JSON.stringify(payload));
    const req = https.request(
      {
        hostname: urlObj.hostname,
        path: urlObj.pathname,
        method: 'POST',
        headers: Object.assign(
          {
            'Content-Type': 'application/json',
            'Content-Length': body.length,
          },
          extraHeaders || {}
        ),
      },
      (res) => {
        let data = '';
        res.on('data', (c) => (data += c));
        res.on('end', () => resolve({ status: res.statusCode, body: data }));
      }
    );
    req.on('error', reject);
    req.setTimeout(12000, () => req.destroy(new Error('upstream_timeout')));
    req.write(body);
    req.end();
  });
}

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Content-Type': 'application/json',
    'Cache-Control': 'no-store',
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'GET') {
    return { statusCode: 405, headers, body: JSON.stringify({ error: 'method_not_allowed' }) };
  }

  const params = event.queryStringParameters || {};
  const origin = params.origin || '';
  const destination = params.destination || '';
  const gkey = process.env.GOOGLE_MAPS_API_KEY || '';

  if (!origin || !destination || !gkey) {
    return {
      statusCode: 400,
      headers,
      body: JSON.stringify({ error: 'missing params or key' }),
    };
  }

  try {
    const url = new URL('https://routes.googleapis.com/directions/v2:computeRoutes');
    const resp = await postJson(
      url,
      {
        origin: { address: origin },
        destination: { address: destination },
        travelMode: 'DRIVE',
        routingPreference: 'TRAFFIC_AWARE',
        units: 'IMPERIAL',
      },
      {
        'X-Goog-Api-Key': gkey,
        'X-Goog-FieldMask': 'routes.distanceMeters,routes.duration',
      }
    );

    if (resp.status < 200 || resp.status >= 300) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'HTTP ' + resp.status, message: resp.body.slice(0, 400) }),
      };
    }

    const data = JSON.parse(resp.body || '{}');
    const routes = data.routes || [];
    if (!routes.length) {
      return { statusCode: 400, headers, body: JSON.stringify({ error: 'no_route' }) };
    }

    const rt = routes[0];
    const meters = rt.distanceMeters || 0;
    let dur = String(rt.duration || '0s');
    if (dur.endsWith('s')) dur = dur.slice(0, -1);
    let seconds = 0;
    try {
      seconds = Math.round(parseFloat(dur));
    } catch (e) {
      seconds = 0;
    }
    if (!isFinite(seconds)) seconds = 0;

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        meters: meters,
        miles: Math.round((meters / 1609.34) * 10) / 10,
        seconds: seconds,
        minutes: Math.round(seconds / 60),
      }),
    };
  } catch (e) {
    return { statusCode: 500, headers, body: JSON.stringify({ error: String(e) }) };
  }
};
