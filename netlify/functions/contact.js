/* Purple Heart Limo — Contact Form Handler
   Netlify Serverless Function
   Required env vars: SENDGRID_API_KEY
   Optional env vars: NOTIFY_EMAIL (defaults to info@purpleheartlimo.com)
*/

const https = require('https');

const BUSINESS_EMAIL = process.env.NOTIFY_EMAIL || 'info@purpleheartlimo.com';
const FROM_EMAIL     = 'noreply@purpleheartlimo.com';
const BUSINESS_NAME  = 'Purple Heart Limo';
const OWNER_PHONE    = '2544355877';
// SMS gateways — all major US carriers; whichever matches delivers, others bounce silently
const SMS_GATEWAYS   = [
  `${OWNER_PHONE}@txt.att.net`,
  `${OWNER_PHONE}@vtext.com`,
  `${OWNER_PHONE}@tmomail.net`,
  `${OWNER_PHONE}@messaging.sprintpcs.com`,
];

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin':  '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json',
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers, body: JSON.stringify({ error: 'Method not allowed' }) };
  }

  let body;
  try {
    body = JSON.parse(event.body || '{}');
  } catch {
    return { statusCode: 400, headers, body: JSON.stringify({ error: 'Invalid request body' }) };
  }

  const {
    name, email, phone, service, date, time,
    vehicle, passengers, pickup, dropoff,
    flightNumber, airline, message
  } = body;

  // Name is always required; email is optional (home form may not have it)
  if (!name) {
    return { statusCode: 400, headers, body: JSON.stringify({ error: 'Missing required field: name' }) };
  }
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return { statusCode: 400, headers, body: JSON.stringify({ error: 'Invalid email address' }) };
  }

  // ── Build SMS short text (160 char friendly) ──────────────────────────────
  const smsLines = [
    `📋 NEW RIDE REQUEST`,
    `From: ${name} | ${phone || 'no phone'}`,
    `Service: ${service || 'General'}`,
    vehicle ? `Vehicle: ${vehicle}` : '',
    `Pickup: ${pickup || 'not given'}`,
    dropoff  ? `Drop-off: ${dropoff}` : '',
    date     ? `Date: ${date}${time ? ' @ ' + time : ''}` : '',
    flightNumber ? `Flight: ${flightNumber}${airline ? ' (' + airline + ')' : ''}` : '',
    `Reply: ${phone || email || 'see email'}`,
    `— PurpleHeartLimo.com`,
  ].filter(Boolean).join('\n');

  // ── Build rich email ──────────────────────────────────────────────────────
  const submitted = new Date().toLocaleString('en-US', { timeZone: 'America/Chicago' });

  const rows = [
    ['Name',         name],
    ['Phone',        phone || 'Not provided'],
    ['Email',        email || 'Not provided'],
    ['Service',      service || 'Not specified'],
    ['Vehicle',      vehicle || 'Not specified'],
    ['Passengers',   passengers || 'Not specified'],
    ['Date',         date || 'Not specified'],
    ['Pickup Time',  time || 'Not specified'],
    ['Pickup',       pickup || 'Not specified'],
    ['Drop-off',     dropoff || 'Not specified'],
    ['Flight No.',   flightNumber || 'Not provided'],
    ['Airline',      airline || 'Not provided'],
  ].map(([label, val]) =>
    `<div class="field"><div class="label">${label}</div><div class="value">${escHtml(val)}</div></div>`
  ).join('');

  const htmlBody = `<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><style>
  body { font-family: Arial, sans-serif; background:#f4f1f8; margin:0; padding:0; }
  .wrapper { max-width:620px; margin:0 auto; padding:2rem; }
  .header { background:linear-gradient(135deg,#2D0045,#5b0080); padding:2rem; border-radius:12px 12px 0 0; text-align:center; }
  .header h1 { color:#fff; margin:0; font-size:1.4rem; }
  .header p  { color:rgba(255,255,255,0.7); margin:0.5rem 0 0; font-size:0.88rem; }
  .body { background:#fff; padding:2rem; border:1px solid rgba(45,0,69,0.12); }
  .field { margin-bottom:0.85rem; padding-bottom:0.85rem; border-bottom:1px solid #f0ebf8; }
  .label { font-size:0.72rem; font-weight:700; letter-spacing:1px; text-transform:uppercase; color:#C9A84C; margin-bottom:3px; }
  .value { font-size:0.95rem; color:#1a0028; }
  .msg-box { background:#f8f4ff; border-left:4px solid #2D0045; border-radius:0 8px 8px 0; padding:1rem; color:#333; font-size:0.9rem; line-height:1.7; white-space:pre-wrap; margin-top:1rem; }
  .cta { display:inline-block; background:linear-gradient(135deg,#C9A84C,#E2C36A); color:#2D0045; padding:0.75rem 1.75rem; border-radius:8px; font-weight:700; text-decoration:none; margin:1rem 0; }
  .footer { background:#2D0045; padding:1.25rem 2rem; border-radius:0 0 12px 12px; text-align:center; font-size:0.78rem; color:rgba(255,255,255,0.55); }
</style></head>
<body><div class="wrapper">
  <div class="header">
    <h1>📋 New Booking Inquiry</h1>
    <p>Submitted ${submitted} CT via purpleheartlimo.com</p>
  </div>
  <div class="body">
    ${rows}
    ${message ? `<div class="label" style="margin-top:1rem;">Additional Notes</div><div class="msg-box">${escHtml(message)}</div>` : ''}
    <div style="text-align:center;margin-top:1.5rem;">
      ${email ? `<a href="mailto:${escHtml(email)}?subject=Re: Your Limo Inquiry — Purple Heart Limo" class="cta">Reply to ${escHtml(name)}</a>` : ''}
      ${phone ? `&nbsp;<a href="tel:+1${phone.replace(/\D/g,'')}" class="cta" style="background:linear-gradient(135deg,#2D0045,#5b0080);color:#fff;">Call ${escHtml(phone)}</a>` : ''}
    </div>
  </div>
  <div class="footer">Purple Heart Limo &bull; (833) 740-0700 &bull; info@purpleheartlimo.com &bull; Veteran-Owned TX</div>
</div></body></html>`;

  const plainText = [
    `New Booking Inquiry — ${BUSINESS_NAME}`,
    '='.repeat(45),
    `Name:       ${name}`,
    `Phone:      ${phone || 'Not provided'}`,
    `Email:      ${email || 'Not provided'}`,
    `Service:    ${service || 'Not specified'}`,
    `Vehicle:    ${vehicle || 'Not specified'}`,
    `Passengers: ${passengers || 'Not specified'}`,
    `Date:       ${date || 'Not specified'}`,
    `Time:       ${time || 'Not specified'}`,
    `Pickup:     ${pickup || 'Not specified'}`,
    `Drop-off:   ${dropoff || 'Not specified'}`,
    `Flight No.: ${flightNumber || 'Not provided'}`,
    `Airline:    ${airline || 'Not provided'}`,
    message ? `\nNotes:\n${message}` : '',
    '',
    '='.repeat(45),
    `Submitted: ${submitted} CT`,
  ].filter(s => s !== undefined).join('\n');

  try {
    // 1 — Notify business email
    await sendgridEmail({
      to:       BUSINESS_EMAIL,
      from:     FROM_EMAIL,
      fromName: `${BUSINESS_NAME} Website`,
      replyTo:  email || undefined,
      subject:  `📋 New Ride Request: ${service || 'General'} — ${name}`,
      text:     plainText,
      html:     htmlBody,
    });

    // 2 — SMS owner via email-to-SMS gateways (fire & forget, errors silently ignored)
    await Promise.allSettled(
      SMS_GATEWAYS.map(to =>
        sendgridEmail({
          to,
          from:     FROM_EMAIL,
          fromName: BUSINESS_NAME,
          subject:  `New Ride: ${name}`,
          text:     smsLines,
          html:     `<pre style="font-family:monospace;font-size:13px;">${escHtml(smsLines)}</pre>`,
        })
      )
    );

    // 3 — Auto-reply to customer (only if we have their email)
    if (email) {
      const autoHtml = `<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
  body{font-family:Arial,sans-serif;background:#f4f1f8;margin:0;padding:0;}
  .w{max-width:560px;margin:0 auto;padding:2rem;}
  .h{background:linear-gradient(135deg,#2D0045,#5b0080);padding:2rem;border-radius:12px 12px 0 0;text-align:center;}
  .b{background:#fff;padding:2rem;border:1px solid rgba(45,0,69,0.12);}
  .f{background:#2D0045;padding:1.25rem 2rem;border-radius:0 0 12px 12px;text-align:center;font-size:0.78rem;color:rgba(255,255,255,0.55);}
  .cta{display:inline-block;background:linear-gradient(135deg,#C9A84C,#E2C36A);color:#2D0045;padding:.75rem 1.75rem;border-radius:8px;font-weight:700;text-decoration:none;}
</style></head>
<body><div class="w">
  <div class="h"><h1 style="color:#fff;margin:0;">Thank You, ${escHtml(name)}!</h1><p style="color:rgba(255,255,255,0.7);margin:.5rem 0 0;">Purple Heart Limo — Veteran-Owned Texas</p></div>
  <div class="b">
    <p style="color:#333;">We received your <strong>${escHtml(service || 'ride')}</strong> request and will call or text you within <strong>5 minutes</strong> with your exact flat rate.</p>
    <ul style="color:#555;line-height:2;">
      ${vehicle ? `<li><strong>Vehicle:</strong> ${escHtml(vehicle)}</li>` : ''}
      ${date    ? `<li><strong>Date:</strong> ${escHtml(date)}${time ? ' at ' + escHtml(time) : ''}</li>` : ''}
      ${pickup  ? `<li><strong>Pickup:</strong> ${escHtml(pickup)}</li>` : ''}
      ${dropoff ? `<li><strong>Drop-off:</strong> ${escHtml(dropoff)}</li>` : ''}
    </ul>
    <p style="color:#555;">Need to reach us now?</p>
    <div style="text-align:center;margin:1.5rem 0;"><a href="tel:+18337400700" class="cta">📞 (833) 740-0700</a></div>
  </div>
  <div class="f">Purple Heart Limo &bull; Austin · DFW · Houston &bull; Veteran-Owned &bull; No Surge Pricing</div>
</div></body></html>`;

      await sendgridEmail({
        to:       email,
        from:     FROM_EMAIL,
        fromName: BUSINESS_NAME,
        subject:  `We Got Your Request — ${BUSINESS_NAME}`,
        text:     `Hi ${name},\n\nThank you! We received your ${service || 'ride'} request and will call or text you within 5 minutes with your exact flat rate.\n\nNeed us now? Call (833) 740-0700\n\nPurple Heart Limo\ninfo@purpleheartlimo.com`,
        html:     autoHtml,
      });
    }
  } catch (err) {
    console.error('SendGrid error:', err.message || err);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Failed to send. Please call (833) 740-0700.' }),
    };
  }

  return {
    statusCode: 200,
    headers,
    body: JSON.stringify({ success: true, message: "Thank you! We'll call or text you within 5 minutes with your exact rate." }),
  };
};

function sendgridEmail({ to, from, fromName, replyTo, subject, text, html }) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({
      personalizations: [{ to: [{ email: to }] }],
      from: { email: from, name: fromName || 'Purple Heart Limo' },
      ...(replyTo ? { reply_to: { email: replyTo } } : {}),
      subject,
      content: [
        { type: 'text/plain', value: text },
        { type: 'text/html',  value: html },
      ],
    });

    const req = https.request(
      {
        hostname: 'api.sendgrid.com',
        path:     '/v3/mail/send',
        method:   'POST',
        headers: {
          'Content-Type':   'application/json',
          'Authorization':  `Bearer ${process.env.SENDGRID_API_KEY}`,
          'Content-Length': Buffer.byteLength(payload),
        },
      },
      (res) => {
        const chunks = [];
        res.on('data', (c) => chunks.push(c));
        res.on('end', () => {
          if (res.statusCode >= 200 && res.statusCode < 300) resolve();
          else reject(new Error(`SendGrid ${res.statusCode}: ${Buffer.concat(chunks).toString()}`));
        });
      }
    );
    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
