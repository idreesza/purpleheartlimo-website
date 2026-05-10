/* Purple Heart Limo — Contact Form Handler
   Netlify Serverless Function
   Required env vars: SENDGRID_API_KEY
   Optional env vars: NOTIFY_EMAIL (defaults to info@purpleheartlimo.com)
*/

const https = require('https');

const BUSINESS_EMAIL = process.env.NOTIFY_EMAIL || 'info@purpleheartlimo.com';
const FROM_EMAIL     = 'noreply@purpleheartlimo.com';
const BUSINESS_NAME  = 'Purple Heart Limo';

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

  const { name, email, phone, service, date, passengers, pickup, dropoff, message } = body;

  if (!name || !email || !message) {
    return {
      statusCode: 400,
      headers,
      body: JSON.stringify({ error: 'Missing required fields: name, email, message' }),
    };
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return {
      statusCode: 400,
      headers,
      body: JSON.stringify({ error: 'Invalid email address' }),
    };
  }

  const plainText = [
    `New Booking Inquiry — ${BUSINESS_NAME}`,
    '='.repeat(45),
    `Name:       ${name}`,
    `Email:      ${email}`,
    `Phone:      ${phone || 'Not provided'}`,
    `Service:    ${service || 'Not specified'}`,
    `Date:       ${date || 'Not specified'}`,
    `Passengers: ${passengers || 'Not specified'}`,
    `Pickup:     ${pickup || 'Not specified'}`,
    `Drop-off:   ${dropoff || 'Not specified'}`,
    '',
    'Message:',
    message,
    '',
    '='.repeat(45),
    `Submitted: ${new Date().toLocaleString('en-US', { timeZone: 'America/Chicago' })} CT`,
  ].join('\n');

  const htmlBody = `
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><style>
  body { font-family: Arial, sans-serif; background: #0f0f0f; color: #f5f5f5; margin: 0; padding: 0; }
  .wrapper { max-width: 620px; margin: 0 auto; padding: 2rem; }
  .header { background: linear-gradient(135deg, #5b21b6, #7c3aed); padding: 2rem; border-radius: 12px 12px 0 0; text-align: center; }
  .header h1 { color: #fff; margin: 0; font-size: 1.4rem; }
  .header p  { color: rgba(255,255,255,0.7); margin: 0.5rem 0 0; font-size: 0.9rem; }
  .body { background: #1a1a1a; padding: 2rem; border: 1px solid rgba(124,58,237,0.3); }
  .field { margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #2e2e2e; }
  .label { font-size: 0.8rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #d4af37; margin-bottom: 0.25rem; }
  .value { font-size: 1rem; color: #f5f5f5; }
  .message-box { background: #242424; border: 1px solid #2e2e2e; border-radius: 8px; padding: 1rem; color: #9ca3af; font-size: 0.95rem; line-height: 1.7; white-space: pre-wrap; }
  .footer { background: #111; padding: 1.5rem 2rem; border-radius: 0 0 12px 12px; text-align: center; font-size: 0.8rem; color: #6b7280; }
  .cta { display: inline-block; background: linear-gradient(135deg, #d4af37, #c9a227); color: #0f0f0f; padding: 0.75rem 1.75rem; border-radius: 8px; font-weight: 700; text-decoration: none; margin: 1rem 0; }
</style></head>
<body><div class="wrapper">
  <div class="header">
    <h1>&#128222; New Booking Inquiry</h1>
    <p>Someone just submitted a request on purpleheartlimo.com</p>
  </div>
  <div class="body">
    <div class="field"><div class="label">Name</div><div class="value">${escHtml(name)}</div></div>
    <div class="field"><div class="label">Email</div><div class="value"><a href="mailto:${escHtml(email)}" style="color:#d4af37;">${escHtml(email)}</a></div></div>
    <div class="field"><div class="label">Phone</div><div class="value">${escHtml(phone || 'Not provided')}</div></div>
    <div class="field"><div class="label">Service Requested</div><div class="value">${escHtml(service || 'Not specified')}</div></div>
    <div class="field"><div class="label">Event Date</div><div class="value">${escHtml(date || 'Not specified')}</div></div>
    <div class="field"><div class="label">Passengers</div><div class="value">${escHtml(passengers || 'Not specified')}</div></div>
    <div class="field"><div class="label">Pickup Location</div><div class="value">${escHtml(pickup || 'Not specified')}</div></div>
    <div class="field"><div class="label">Drop-off Location</div><div class="value">${escHtml(dropoff || 'Not specified')}</div></div>
    <div class="label" style="margin-bottom:0.5rem;">Message</div>
    <div class="message-box">${escHtml(message)}</div>
    <div style="text-align:center;margin-top:1.5rem;">
      <a href="mailto:${escHtml(email)}?subject=Re: Your Limo Inquiry — Purple Heart Limo" class="cta">Reply to ${escHtml(name)}</a>
    </div>
  </div>
  <div class="footer">
    Purple Heart Limo &bull; Austin, TX &bull; (512) 890-0900<br>
    Submitted: ${new Date().toLocaleString('en-US', { timeZone: 'America/Chicago' })} CT
  </div>
</div></body></html>`;

  try {
    await sendgridEmail({
      to:       BUSINESS_EMAIL,
      from:     FROM_EMAIL,
      fromName: `${BUSINESS_NAME} Website`,
      replyTo:  email,
      subject:  `New Booking Inquiry: ${service || 'General'} — ${name}`,
      text:     plainText,
      html:     htmlBody,
    });

    // Auto-reply to the client
    const autoReplyHtml = `
<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
  body { font-family: Arial, sans-serif; background: #0f0f0f; color: #f5f5f5; }
  .wrapper { max-width: 580px; margin: 0 auto; padding: 2rem; }
  .header { background: linear-gradient(135deg, #5b21b6, #7c3aed); padding: 2rem; border-radius: 12px 12px 0 0; text-align: center; }
  .body { background: #1a1a1a; padding: 2rem; border: 1px solid rgba(124,58,237,0.3); }
  .footer { background: #111; padding: 1.5rem 2rem; border-radius: 0 0 12px 12px; text-align: center; font-size: 0.8rem; color: #6b7280; }
  .cta { display: inline-block; background: linear-gradient(135deg, #d4af37, #c9a227); color: #0f0f0f; padding: 0.875rem 2rem; border-radius: 8px; font-weight: 700; text-decoration: none; }
</style></head>
<body><div class="wrapper">
  <div class="header"><h1 style="color:#fff;margin:0;">Thank You, ${escHtml(name)}!</h1><p style="color:rgba(255,255,255,0.7);margin:0.5rem 0 0;">Purple Heart Limo — Austin, TX</p></div>
  <div class="body">
    <p>We've received your booking inquiry and our team will respond within <strong>1 hour</strong>.</p>
    <p style="color:#9ca3af;">Here's a summary of your request:</p>
    <ul style="color:#9ca3af;line-height:2;">
      <li><strong style="color:#f5f5f5;">Service:</strong> ${escHtml(service || 'Not specified')}</li>
      <li><strong style="color:#f5f5f5;">Date:</strong> ${escHtml(date || 'Not specified')}</li>
      <li><strong style="color:#f5f5f5;">Passengers:</strong> ${escHtml(passengers || 'Not specified')}</li>
    </ul>
    <p style="color:#9ca3af;">Need an immediate response?</p>
    <div style="text-align:center;margin:1.5rem 0;"><a href="tel:+15128900900" class="cta">&#128222; Call (512) 890-0900</a></div>
  </div>
  <div class="footer">Purple Heart Limo &bull; Austin, TX &bull; info@purpleheartlimo.com<br>Veteran-Owned Business &bull; Available 24/7</div>
</div></body></html>`;

    await sendgridEmail({
      to:       email,
      from:     FROM_EMAIL,
      fromName: BUSINESS_NAME,
      subject:  `We Received Your Request — ${BUSINESS_NAME}`,
      text:     `Hi ${name},\n\nThank you for contacting Purple Heart Limo! We've received your inquiry and will respond within 1 hour.\n\nNeed immediate help? Call us: (512) 890-0900\n\nPurple Heart Limo\ninfo@purpleheartlimo.com`,
      html:     autoReplyHtml,
    });
  } catch (err) {
    console.error('SendGrid error:', err.message || err);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Failed to send message. Please call (512) 890-0900.' }),
    };
  }

  return {
    statusCode: 200,
    headers,
    body: JSON.stringify({ success: true, message: "Thank you! We'll contact you within the hour." }),
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
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve();
          } else {
            reject(new Error(`SendGrid ${res.statusCode}: ${Buffer.concat(chunks).toString()}`));
          }
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
