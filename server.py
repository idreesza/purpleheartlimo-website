import os
import json
import datetime
import email.utils
import gzip
import io
import html
import math
import posixpath
import re
import threading
import time
import tomllib
import urllib.request
import urllib.parse
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

# Production caching on any real deployment: Render sets RENDER=true;
# PRODUCTION=1 works on any host; REPLIT_DEPLOYMENT kept for the old host.
IS_PROD = bool(os.environ.get('PRODUCTION') or os.environ.get('RENDER')
               or os.environ.get('REPLIT_DEPLOYMENT'))

# The static site was originally deployed with a Netlify function at this
# path.  Autoscale runs this Python server instead, so keep the browser
# contract while routing the notification through the same SendGrid account.
CONTACT_PATHS = frozenset(('/.netlify/functions/contact', '/api/contact'))
CONTACT_MAX_BYTES = 64 * 1024
CONTACT_BUSINESS_EMAIL = 'info@purpleheartlimo.com'
CONTACT_FROM_EMAIL = 'noreply@purpleheartlimo.com'
CONTACT_BUSINESS_NAME = 'Purple Heart Limo'
CONTACT_OWNER_PHONE = '2544355877'
CONTACT_SMS_GATEWAYS = (
    f'{CONTACT_OWNER_PHONE}@txt.att.net',
    f'{CONTACT_OWNER_PHONE}@vtext.com',
    f'{CONTACT_OWNER_PHONE}@tmomail.net',
    f'{CONTACT_OWNER_PHONE}@messaging.sprintpcs.com',
)

# Hourly estimates are intentionally gated on a real Google driving-distance
# result.  These are server-only values: the hourly endpoint returns only an
# availability flag, and the static-file guard below prevents this source from
# being downloaded by a browser.
HOURLY_HUBS = (
    ('austin', '3100 Esperanza Crossing, Austin, TX 78758'),
    ('dallas', '777 S Central Expy, Richardson, TX 75080'),
    ('houston', '15200 Memorial Dr, Houston, TX 77079'),
)
HOURLY_HUB_PATH = '/api/hourly-hub'
HOURLY_HUB_CACHE_MAX_ENTRIES = 256
HOURLY_HUB_CACHE_TTL_SECONDS = 300
HOURLY_HUB_FAILURE_TTL_SECONDS = 15
HOURLY_HUB_MAX_PICKUP_LENGTH = 500
HOURLY_HUB_CACHE_MISS = object()


class _BoundedTTLCache:
    """Small thread-safe TTL cache used for hourly hub checks.

    Successful selections live longer than failures.  Keeping failures for a
    short period avoids a thundering herd while allowing a temporarily
    unavailable provider to recover quickly.  Values are internal hub IDs (or
    ``None`` for a failed check), never API response details.
    """

    def __init__(self, max_entries, success_ttl, failure_ttl, clock=None):
        self.max_entries = max(1, int(max_entries))
        self.success_ttl = max(0, float(success_ttl))
        self.failure_ttl = max(0, float(failure_ttl))
        self._clock = clock or time.monotonic
        self._entries = OrderedDict()
        self._lock = threading.RLock()

    def get(self, key, default=HOURLY_HUB_CACHE_MISS):
        with self._lock:
            entry = self._entries.get(key)
            if entry is None:
                return default
            expires, value = entry
            if expires <= self._clock():
                self._entries.pop(key, None)
                return default
            self._entries.move_to_end(key)
            return value

    def set(self, key, value):
        ttl = self.success_ttl if value is not None else self.failure_ttl
        with self._lock:
            self._entries[key] = (self._clock() + ttl, value)
            self._entries.move_to_end(key)
            while len(self._entries) > self.max_entries:
                self._entries.popitem(last=False)

    def clear(self):
        with self._lock:
            self._entries.clear()

    def __len__(self):
        with self._lock:
            return len(self._entries)


def _normalize_hourly_request(pickup, lat=None, lon=None):
    """Validate and normalize the public hourly-hub query.

    Address whitespace/case and equivalent decimal coordinate spellings map
    to one cache key.  Coordinates are optional, but must be supplied as a
    complete finite latitude/longitude pair when present.
    """
    if not isinstance(pickup, str):
        raise ValueError('pickup is required')
    address = re.sub(r'\s+', ' ', pickup).strip()
    if not address:
        raise ValueError('pickup is required')
    if len(address) > HOURLY_HUB_MAX_PICKUP_LENGTH:
        raise ValueError('pickup is too long')

    supplied_coordinates = lat is not None or lon is not None
    coordinates = None
    if supplied_coordinates:
        if lat in (None, '') or lon in (None, ''):
            raise ValueError('lat and lon must be supplied together')
        try:
            latitude = float(lat)
            longitude = float(lon)
        except (TypeError, ValueError):
            raise ValueError('invalid coordinates') from None
        if (
            not math.isfinite(latitude)
            or not math.isfinite(longitude)
            or not -90 <= latitude <= 90
            or not -180 <= longitude <= 180
        ):
            raise ValueError('invalid coordinates')
        # Eight decimal places preserve sub-meter-level address precision
        # while making 30, 30.0, and 30.00000000 one cache coordinate.
        latitude = 0.0 if latitude == 0 else latitude
        longitude = 0.0 if longitude == 0 else longitude
        coordinates = (latitude, longitude)

    normalized_coordinates = (
        None
        if coordinates is None
        else tuple(f'{value:.8f}' for value in coordinates)
    )
    key = (address.casefold(), normalized_coordinates)
    return address, coordinates, key


def _google_hourly_distances(pickup, coordinates):
    """Return the two Google driving distances, or ``None`` on any failure.

    This uses the server-side Distance Matrix REST endpoint only.  In
    particular, it never reads the referrer-restricted browser key and never
    falls back to OSRM for an hourly availability decision.
    """
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY', '').strip()
    if not api_key:
        return None

    origin = (
        f'{coordinates[0]},{coordinates[1]}'
        if coordinates is not None
        else pickup
    )
    destinations = '|'.join(address for _, address in HOURLY_HUBS)
    params = urllib.parse.urlencode({
        'origins': origin,
        'destinations': destinations,
        'mode': 'driving',
        'units': 'imperial',
        'key': api_key,
    })
    request = urllib.request.Request(
        'https://maps.googleapis.com/maps/api/distancematrix/json?' + params,
        headers={
            'Accept': 'application/json',
            'User-Agent': 'PurpleHeartLimo/1.0 (purpleheartlimo.com)',
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            status = getattr(response, 'status', None)
            if status is None:
                getcode = getattr(response, 'getcode', None)
                status = getcode() if getcode else None
            if status is not None and not 200 <= status < 300:
                return None
            raw = response.read()
            if isinstance(raw, bytes):
                raw = raw.decode('utf-8')
            payload = json.loads(raw)
    except Exception:
        # Deliberately keep provider errors and credentials out of both the
        # response and logs.  The caller turns this into contact-us behavior.
        return None

    if not isinstance(payload, dict) or payload.get('status') != 'OK':
        return None
    rows = payload.get('rows')
    if not isinstance(rows, list) or not rows:
        return None
    elements = rows[0].get('elements') if isinstance(rows[0], dict) else None
    if not isinstance(elements, list) or len(elements) < len(HOURLY_HUBS):
        return None

    distances = []
    for element in elements[:len(HOURLY_HUBS)]:
        if not isinstance(element, dict) or element.get('status') != 'OK':
            return None
        distance = element.get('distance')
        value = distance.get('value') if isinstance(distance, dict) else None
        if isinstance(value, bool):
            return None
        try:
            value = float(value)
        except (TypeError, ValueError):
            return None
        if not math.isfinite(value) or value < 0:
            return None
        distances.append(value)
    return distances


def _select_hourly_hub(pickup, coordinates):
    """Select the nearest configured hub internally, without exposing it."""
    distances = _google_hourly_distances(pickup, coordinates)
    if (
        not isinstance(distances, (list, tuple))
        or len(distances) < len(HOURLY_HUBS)
    ):
        return None
    nearest_index = min(range(len(distances)), key=distances.__getitem__)
    return HOURLY_HUBS[nearest_index][0]


def _contact_text(value, limit=4000):
    """Normalize untrusted contact fields without ever exposing credentials."""
    if value is None:
        return ''
    if not isinstance(value, (str, int, float)):
        return ''
    return str(value).strip()[:limit]


def _contact_header(value, limit=180):
    """Keep user values safe when interpolated into mail headers."""
    return re.sub(r'[\r\n]+', ' ', _contact_text(value, limit)).strip()


def _contact_result(body, status=200):
    return {'body': body, 'status': status}


def _sendgrid_email(*, to, from_email, from_name, reply_to=None, subject='',
                    text='', html_body='', api_key=None, opener=None):
    """Send one message through SendGrid using only the configured API key.

    ``opener`` is injectable so route tests can use a controlled transport and
    never send a real message.  Production uses urllib's HTTPS opener.
    """
    key = api_key or os.environ.get('SENDGRID_API_KEY', '').strip()
    if not key:
        raise RuntimeError('SENDGRID_API_KEY is missing')

    payload = json.dumps({
        'personalizations': [{'to': [{'email': to}]}],
        'from': {'email': from_email, 'name': from_name or CONTACT_BUSINESS_NAME},
        **({'reply_to': {'email': reply_to}} if reply_to else {}),
        'subject': _contact_header(subject),
        'content': [
            {'type': 'text/plain', 'value': text},
            {'type': 'text/html', 'value': html_body},
        ],
    }).encode('utf-8')
    request = urllib.request.Request(
        'https://api.sendgrid.com/v3/mail/send',
        data=payload,
        method='POST',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {key}',
            'Content-Length': str(len(payload)),
        },
    )
    transport = opener or urllib.request.urlopen
    with transport(request, timeout=12) as response:
        status = getattr(response, 'status', None)
        if status is None:
            status = response.getcode()
        response.read()
    if not 200 <= status < 300:
        raise RuntimeError(f'SendGrid returned HTTP {status}')


def _contact_messages(data):
    """Build the notification, SMS, and customer acknowledgement payloads."""
    name = _contact_text(data.get('name'), 200)
    email = _contact_text(data.get('email'), 320)
    phone = _contact_text(data.get('phone'), 80)
    service = _contact_text(data.get('service'), 160)
    date = _contact_text(data.get('date'), 80)
    time = _contact_text(data.get('time'), 80)
    vehicle = _contact_text(data.get('vehicle'), 160)
    passengers = _contact_text(data.get('passengers'), 80)
    pickup = _contact_text(data.get('pickup'), 500)
    dropoff = _contact_text(data.get('dropoff'), 500)
    flight_number = _contact_text(data.get('flightNumber'), 80)
    airline = _contact_text(data.get('airline'), 100)
    message = _contact_text(data.get('message'), 8000)
    service_or_general = service or 'General'
    submitted = datetime.datetime.now(
        datetime.timezone.utc
    ).astimezone(datetime.timezone(datetime.timedelta(hours=-5))).strftime(
        '%m/%d/%Y, %I:%M:%S %p'
    )

    esc = lambda value: html.escape(str(value), quote=True)
    rows = ''.join(
        f'<div class="field"><div class="label">{label}</div>'
        f'<div class="value">{esc(value)}</div></div>'
        for label, value in (
            ('Name', name),
            ('Phone', phone or 'Not provided'),
            ('Email', email or 'Not provided'),
            ('Service', service_or_general),
            ('Vehicle', vehicle or 'Not specified'),
            ('Passengers', passengers or 'Not specified'),
            ('Date', date or 'Not specified'),
            ('Pickup Time', time or 'Not specified'),
            ('Pickup', pickup or 'Not specified'),
            ('Drop-off', dropoff or 'Not specified'),
            ('Flight No.', flight_number or 'Not provided'),
            ('Airline', airline or 'Not provided'),
        )
    )
    html_body = f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
body{{font-family:Arial,sans-serif;background:#f4f1f8;margin:0;padding:0;}}
.wrapper{{max-width:620px;margin:0 auto;padding:2rem;}}
.header{{background:linear-gradient(135deg,#2D0045,#5b0080);padding:2rem;border-radius:12px 12px 0 0;text-align:center;}}
.header h1{{color:#fff;margin:0;font-size:1.4rem;}}
.header p{{color:rgba(255,255,255,.7);margin:.5rem 0 0;font-size:.88rem;}}
.body{{background:#fff;padding:2rem;border:1px solid rgba(45,0,69,.12);}}
.field{{margin-bottom:.85rem;padding-bottom:.85rem;border-bottom:1px solid #f0ebf8;}}
.label{{font-size:.72rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#C9A84C;margin-bottom:3px;}}
.value{{font-size:.95rem;color:#1a0028;}}
.msg-box{{background:#f8f4ff;border-left:4px solid #2D0045;border-radius:0 8px 8px 0;padding:1rem;color:#333;font-size:.9rem;line-height:1.7;white-space:pre-wrap;margin-top:1rem;}}
.footer{{background:#2D0045;padding:1.25rem 2rem;border-radius:0 0 12px 12px;text-align:center;font-size:.78rem;color:rgba(255,255,255,.55);}}
</style></head><body><div class="wrapper">
<div class="header"><h1>📋 New Booking Inquiry</h1>
<p>Submitted {esc(submitted)} CT via purpleheartlimo.com</p></div>
<div class="body">{rows}
{f'<div class="label" style="margin-top:1rem;">Additional Notes</div><div class="msg-box">{esc(message)}</div>' if message else ''}
</div><div class="footer">Purple Heart Limo &bull; (833) 740-0700 &bull; info@purpleheartlimo.com &bull; Veteran-Owned TX</div>
</div></body></html>'''
    plain_text = '\n'.join(filter(
        lambda line: line != '',
        (
            f'New Booking Inquiry — {CONTACT_BUSINESS_NAME}',
            '=' * 45,
            f'Name:       {name}',
            f'Phone:      {phone or "Not provided"}',
            f'Email:      {email or "Not provided"}',
            f'Service:    {service or "Not specified"}',
            f'Vehicle:    {vehicle or "Not specified"}',
            f'Passengers: {passengers or "Not specified"}',
            f'Date:       {date or "Not specified"}',
            f'Time:       {time or "Not specified"}',
            f'Pickup:     {pickup or "Not specified"}',
            f'Drop-off:   {dropoff or "Not specified"}',
            f'Flight No.: {flight_number or "Not provided"}',
            f'Airline:    {airline or "Not provided"}',
            f'\nNotes:\n{message}' if message else '',
            '',
            '=' * 45,
            f'Submitted: {submitted} CT',
        )
    ))
    sms_text = '\n'.join(filter(
        None,
        (
            '📋 NEW RIDE REQUEST',
            f'From: {name} | {phone or "no phone"}',
            f'Service: {service_or_general}',
            f'Vehicle: {vehicle}' if vehicle else '',
            f'Pickup: {pickup or "not given"}',
            f'Drop-off: {dropoff}' if dropoff else '',
            f'Date: {date} @ {time}' if date else '',
            f'Flight: {flight_number}' + (f' ({airline})' if airline else '') if flight_number else '',
            f'Reply: {phone or email or "see email"}',
            '— PurpleHeartLimo.com',
        )
    ))
    customer_text = (
        f'Hi {name},\n\nThank you! We received your {service_or_general} request '
        'and will call or text you within 5 minutes with your exact flat rate.\n\n'
        'Need us now? Call (833) 740-0700\n\nPurple Heart Limo\ninfo@purpleheartlimo.com'
    )
    customer_html = (
        f'<p>We received your <strong>{esc(service_or_general)}</strong> request '
        'and will call or text you within <strong>5 minutes</strong> with your exact flat rate.</p>'
    )
    return {
        'business': {
            'to': os.environ.get('NOTIFY_EMAIL', CONTACT_BUSINESS_EMAIL).strip() or CONTACT_BUSINESS_EMAIL,
            'from_email': CONTACT_FROM_EMAIL,
            'from_name': f'{CONTACT_BUSINESS_NAME} Website',
            'reply_to': email or None,
            'subject': f'📋 New Ride Request: {service_or_general} — {name}',
            'text': plain_text,
            'html_body': html_body,
        },
        'sms': {
            'from_email': CONTACT_FROM_EMAIL,
            'from_name': CONTACT_BUSINESS_NAME,
            'subject': f'New Ride: {name}',
            'text': sms_text,
            'html_body': f'<pre style="font-family:monospace;font-size:13px;">{esc(sms_text)}</pre>',
        },
        'customer': {
            'to': email,
            'from_email': CONTACT_FROM_EMAIL,
            'from_name': CONTACT_BUSINESS_NAME,
            'subject': f'We Got Your Request — {CONTACT_BUSINESS_NAME}',
            'text': customer_text,
            'html_body': customer_html,
        },
    }


def _process_contact(data, send_email=None, api_key=None):
    """Validate and deliver one contact request.

    ``send_email`` is intentionally injectable for deterministic tests.  No
    success response is returned unless the primary business notification was
    accepted by the transport.
    """
    if not isinstance(data, dict):
        return _contact_result({'error': 'Invalid request body'}, 400)
    # Preserve the existing forms' quiet honeypot behavior: discard bots
    # without sending a message, but do not reveal the spam check to them.
    if any(_contact_text(data.get(field)) for field in ('website', 'bk-website', 'company', 'fax')):
        return _contact_result({
            'success': True,
            'message': "Thank you! We'll call or text you within 5 minutes with your exact rate.",
        })
    name = _contact_text(data.get('name'), 200)
    email = _contact_text(data.get('email'), 320)
    if not name:
        return _contact_result({'error': 'Missing required field: name'}, 400)
    if email and not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email):
        return _contact_result({'error': 'Invalid email address'}, 400)

    key = api_key if api_key is not None else os.environ.get('SENDGRID_API_KEY', '').strip()
    if not key:
        return _contact_result({
            'error': 'Booking service is not configured: SENDGRID_API_KEY is missing.',
        }, 503)

    messages = _contact_messages(data)
    sender = send_email or _sendgrid_email
    try:
        sender(api_key=key, **messages['business'])
        # SMS gateway failures must not turn a confirmed business notification
        # into a customer-facing failure.
        def send_sms(gateway):
            try:
                sender(api_key=key, to=gateway, **messages['sms'])
            except Exception:
                return False
            return True
        with ThreadPoolExecutor(max_workers=len(CONTACT_SMS_GATEWAYS)) as pool:
            list(pool.map(send_sms, CONTACT_SMS_GATEWAYS))
        if email:
            sender(api_key=key, **messages['customer'])
    except Exception:
        # Deliberately omit provider details and credentials from logs/body.
        return _contact_result({
            'error': 'Failed to send. Please call (833) 740-0700.',
        }, 502)
    return _contact_result({
        'success': True,
        'message': "Thank you! We'll call or text you within 5 minutes with your exact rate.",
    })

def _load_redirects():
    """Load path-based redirect rules from netlify.toml (single source of
    truth for legacy-slug 301s). Host-based rules (www) are handled in code;
    status-200 rewrites are covered by the extensionless handler or native
    /api endpoints; the /* -> /404.html catch-all is handled as a custom
    error page."""
    exact, prefixes = {}, []
    try:
        with open(os.path.join(os.path.dirname(__file__), 'netlify.toml'), 'rb') as f:
            rules = tomllib.load(f).get('redirects', [])
    except Exception as e:
        print('WARNING: could not load netlify.toml redirects:', e)
        return exact, prefixes
    for r in rules:
        frm, to, status = r.get('from', ''), r.get('to', ''), int(r.get('status', 301))
        if frm.startswith('http') or status not in (301, 410) or frm == '/*':
            continue
        # Query-gated rules must not become unconditional path redirects.
        # The retired blog pagination parameters are handled explicitly below.
        if r.get('query'):
            continue
        if frm.endswith('/*'):
            prefixes.append((frm[:-1], to, status))  # keep trailing slash on prefix
        else:
            exact.setdefault(frm, (to, status))
    return exact, prefixes

REDIRECTS_EXACT, REDIRECT_PREFIXES = _load_redirects()


def _redirect_destination(request_target):
    """Resolve configured aliases without emitting intermediate redirects.

    Only explicit legacy mappings are followed; unknown blog slugs are never
    guessed into folder URLs. Preserve unrelated query parameters, but retire
    the old blog search/pagination aliases on both /blog and /blog/.
    """
    parsed = urllib.parse.urlsplit(request_target)
    path, query = parsed.path, parsed.query
    if path in ('/blog', '/blog/'):
        pairs = urllib.parse.parse_qsl(query, keep_blank_values=True)
        if any(key in ('q', 'p') for key, _ in pairs):
            query = urllib.parse.urlencode([
                (key, value) for key, value in pairs if key not in ('q', 'p')
            ])
            path = '/blog/'

    seen = set()
    while path not in seen:
        seen.add(path)
        hit = REDIRECTS_EXACT.get(path)
        if hit is None and path != '/':
            hit = REDIRECTS_EXACT.get(path.rstrip('/'))
        if hit is None:
            for prefix, to, status in REDIRECT_PREFIXES:
                if path.startswith(prefix):
                    hit = (to, status)
                    break
        if hit is None:
            break
        to, status = hit
        if status == 410:
            return to, status
        if to == path:
            break
        if to in seen:
            # Bad future configuration must not create a browser redirect loop.
            return None
        path = to

    destination = path + ('?' + query if query else '')
    return (destination, 301) if destination != request_target else None


_CANONICAL_RE = re.compile(
    r'<link\b[^>]*\brel\s*=\s*["\']canonical["\'][^>]*>', re.I)
_HREF_RE = re.compile(r'\bhref\s*=\s*["\']([^"\']+)["\']', re.I)
_canonical_cache = {}


def _page_file_for(root, url_path):
    """Map a request path to the HTML file the static handler would serve
    (including the alias forms that duplicate a canonical URL), or None."""
    try:
        rel = posixpath.normpath('/' + urllib.parse.unquote(url_path).lstrip('/'))
    except (TypeError, ValueError):
        return None
    if rel.startswith('/..'):
        return None
    base = os.path.join(root, rel.lstrip('/'))
    candidates = []
    if url_path.endswith('/'):
        candidates = [os.path.join(base, 'index.html'), base.rstrip('/\\') + '.html']
    elif url_path.endswith('.html'):
        candidates = [base]
    elif not os.path.splitext(rel)[1]:
        candidates = [base + '.html', os.path.join(base, 'index.html')]
    for candidate in candidates:
        if os.path.isfile(candidate):
            return os.path.realpath(candidate)
    return None


def _canonical_path(html_file):
    """Path component of the page's own <link rel="canonical">, cached by mtime."""
    try:
        mtime = os.path.getmtime(html_file)
    except OSError:
        return None
    cached = _canonical_cache.get(html_file)
    if cached and cached[0] == mtime:
        return cached[1]
    path = None
    try:
        with open(html_file, encoding='utf-8', errors='replace') as f:
            head = f.read(65536)
        tag = _CANONICAL_RE.search(head)
        href = _HREF_RE.search(tag.group(0)) if tag else None
        if href:
            parsed = urllib.parse.urlsplit(href.group(1))
            if parsed.netloc in ('', 'purpleheartlimo.com') and parsed.path.startswith('/'):
                path = parsed.path
    except OSError:
        path = None
    _canonical_cache[html_file] = (mtime, path)
    return path


def _canonical_redirect_target(root, request_target):
    """Return the canonical URL when ``request_target`` is a duplicate address
    of the same page (/x/index.html, /post vs /post.html, /post/ vs /post),
    else None. Only redirects when the canonical resolves to the very same
    file, so pages that canonicalise elsewhere are never redirected here."""
    parsed = urllib.parse.urlsplit(request_target)
    path = parsed.path
    if not path or path.startswith('/api/'):
        return None
    html_file = _page_file_for(root, path)
    if not html_file:
        return None
    canonical = _canonical_path(html_file)
    if not canonical or canonical == path:
        return None
    if _page_file_for(root, canonical) != html_file:
        return None
    return canonical + ('?' + parsed.query if parsed.query else '')


class Handler(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        content_type = super().guess_type(path)
        return content_type + '; charset=utf-8' if content_type == 'text/html' else content_type

    def translate_path(self, path):
        source = super().translate_path(path)
        # The build is an internal serving layer, never a separate public site.
        if os.path.isdir(source):
            candidate = os.path.join(source, 'index.html')
            if os.path.isfile(candidate) and urllib.parse.urlsplit(path).path.endswith('/'):
                source = candidate
        relative = os.path.relpath(source, self.directory)
        compiled = os.path.join(self.directory, 'compiled-static', relative)
        if (not relative.startswith(('..', 'compiled-static'))
                and os.path.isfile(source) and os.path.isfile(compiled)
                and os.path.getmtime(compiled) >= os.path.getmtime(source)):
            return compiled
        return source

    _gzip_cache = {}
    _compressible_extensions = ('.html', '.css', '.js', '.json', '.xml', '.txt', '.svg')
    _hourly_hub_cache = _BoundedTTLCache(
        HOURLY_HUB_CACHE_MAX_ENTRIES,
        HOURLY_HUB_CACHE_TTL_SECONDS,
        HOURLY_HUB_FAILURE_TTL_SECONDS,
    )

    def _encoding_quality(self, requested_encoding):
        """Return the client's quality preference for a content encoding."""
        explicit_quality = None
        wildcard_quality = None
        header = self.headers.get('Accept-Encoding')
        if not header:
            return 1.0 if requested_encoding == 'identity' else 0.0
        for value in header.split(','):
            parts = [part.strip() for part in value.split(';')]
            encoding = parts[0].lower()
            if encoding not in (requested_encoding, '*'):
                continue
            quality = 1.0
            for parameter in parts[1:]:
                if parameter.lower().startswith('q='):
                    try:
                        quality = float(parameter[2:])
                    except ValueError:
                        quality = 0.0
            if encoding == requested_encoding:
                explicit_quality = quality
            else:
                wildcard_quality = quality
        if explicit_quality is not None:
            return explicit_quality
        if wildcard_quality is not None:
            return wildcard_quality
        return 1.0 if requested_encoding == 'identity' else 0.0

    def send_head(self):
        """Serve compressible static files with negotiated gzip encoding."""
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            if not urllib.parse.urlsplit(self.path).path.endswith('/'):
                return super().send_head()
            for filename in ('index.html', 'index.htm'):
                candidate = os.path.join(path, filename)
                if os.path.isfile(candidate):
                    path = candidate
                    break

        compressible = (
            os.path.isfile(path)
            and path.lower().endswith(self._compressible_extensions)
        )
        self._vary_accept_encoding = compressible
        if not compressible:
            return super().send_head()
        if self._encoding_quality('gzip') <= 0:
            if self._encoding_quality('identity') <= 0:
                self.send_response(406)
                self.send_header('Content-Length', '0')
                self.end_headers()
                return None
            return super().send_head()

        try:
            stat = os.stat(path)
            if ('If-Modified-Since' in self.headers
                    and 'If-None-Match' not in self.headers):
                try:
                    modified_since = email.utils.parsedate_to_datetime(
                        self.headers['If-Modified-Since']
                    )
                except (TypeError, IndexError, OverflowError, ValueError):
                    modified_since = None
                if modified_since is not None:
                    if modified_since.tzinfo is None:
                        modified_since = modified_since.replace(
                            tzinfo=datetime.timezone.utc
                        )
                    last_modified = datetime.datetime.fromtimestamp(
                        stat.st_mtime, datetime.timezone.utc
                    ).replace(microsecond=0)
                    if last_modified <= modified_since:
                        self.send_response(304)
                        self.end_headers()
                        return None

            signature = (stat.st_mtime_ns, stat.st_size)
            cached = self._gzip_cache.get(path)
            if cached and cached[0] == signature:
                body = cached[1]
            else:
                with open(path, 'rb') as source:
                    body = gzip.compress(source.read(), compresslevel=6, mtime=0)
                self._gzip_cache[path] = (signature, body)

            self.send_response(200)
            self.send_header('Content-Type', self.guess_type(path))
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Last-Modified', self.date_time_string(stat.st_mtime))
            self.end_headers()
            return io.BytesIO(body)
        except OSError:
            return super().send_head()

    def _www_redirect(self):
        """Collapse the www host and any configured path alias in one hop."""
        host = (self.headers.get('Host') or '').split(':')[0].strip().lower()
        if host == 'www.purpleheartlimo.com':
            hit = _redirect_destination(self.path)
            # Retired/Gone URLs must remain Gone, not redirect to /404.html.
            if hit and hit[1] == 410:
                return False
            target = hit[0] if hit else self.path
            self.send_response(301)
            self.send_header('Location', 'https://purpleheartlimo.com' + target)
            self.send_header('Cache-Control', 'max-age=3600')
            SimpleHTTPRequestHandler.end_headers(self)
            return True
        return False

    def send_error(self, code, message=None, explain=None):
        # Custom branded 404 page (parity with the old static deployment's
        # /* -> /404.html rule).
        if code == 404 and os.path.isfile('404.html'):
            try:
                with open('404.html', 'rb') as f:
                    body = f.read()
                self.send_response(404)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                SimpleHTTPRequestHandler.end_headers(self)
                if self.command != 'HEAD':
                    self._write_body(body)
                return
            except Exception:
                pass
        return SimpleHTTPRequestHandler.send_error(self, code, message, explain)

    def do_HEAD(self):
        # HEAD must mirror GET exactly (same status + headers, no body), so
        # it goes through the same routing; body writes are gated on
        # self.command inside the handlers.
        if urllib.parse.urlsplit(self.path).path in CONTACT_PATHS:
            self._json({'error': 'Method not allowed'}, 405,
                       extra_headers=self._contact_headers())
            return
        return self._route()

    def do_OPTIONS(self):
        path = urllib.parse.urlsplit(self.path).path
        if path in CONTACT_PATHS:
            self.send_response(204)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return
        self.send_error(405, 'Method not allowed')

    def do_POST(self):
        path = urllib.parse.urlsplit(self.path).path
        if path not in CONTACT_PATHS:
            self.send_error(404, 'Not found')
            return
        content_length = self.headers.get('Content-Length')
        try:
            length = int(content_length) if content_length is not None else 0
        except ValueError:
            self._json({'error': 'Invalid Content-Length'}, 400,
                       extra_headers=self._contact_headers())
            return
        if length < 0 or length > CONTACT_MAX_BYTES:
            self._json({'error': 'Request body is too large'}, 413,
                       extra_headers=self._contact_headers())
            return
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode('utf-8') or '{}')
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._json({'error': 'Invalid request body'}, 400,
                       extra_headers=self._contact_headers())
            return
        result = _process_contact(payload)
        self._json(result['body'], result['status'],
                   extra_headers=self._contact_headers())

    @staticmethod
    def _contact_headers():
        return {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
        }

    def _legacy_redirect(self):
        """Legacy-slug 301s/410s ported from netlify.toml (the static
        deployment's rewrites don't apply once a server handles requests)."""
        hit = _redirect_destination(self.path)
        if hit is None:
            return False
        to, status = hit
        if status == 410:
            self.send_response(410)
            SimpleHTTPRequestHandler.end_headers(self)
            return True
        self.send_response(301)
        self.send_header('Location', to)
        self.send_header('Cache-Control', 'max-age=3600')
        SimpleHTTPRequestHandler.end_headers(self)
        return True

    def _canonical_redirect(self):
        """One-hop 301 from duplicate URL forms to the page's canonical URL,
        so duplicates stop returning 200 and splitting link equity."""
        root = getattr(self, 'directory', None) or os.getcwd()
        target = _canonical_redirect_target(root, self.path)
        if not target:
            return False
        self.send_response(301)
        self.send_header('Location', target)
        self.send_header('Cache-Control', 'max-age=3600')
        SimpleHTTPRequestHandler.end_headers(self)
        return True

    def do_GET(self):
        if urllib.parse.urlsplit(self.path).path in CONTACT_PATHS:
            self._json({'error': 'Method not allowed'}, 405,
                       extra_headers=self._contact_headers())
            return
        return self._route()

    def _route(self):
        """Shared routing for GET and HEAD."""
        self._vary_accept_encoding = False
        request_path = urllib.parse.urlsplit(self.path).path
        if self._private_static_path(request_path):
            self.send_error(404, 'Not found')
            return
        if self._www_redirect():
            return
        if self._legacy_redirect():
            return
        if self._canonical_redirect():
            return
        if self.path == '/config.js':
            key = os.environ.get('AVIATIONSTACK_API_KEY', '')
            ejs_pub  = os.environ.get('EMAILJS_PUBLIC_KEY', '')
            ejs_svc  = os.environ.get('EMAILJS_SERVICE_ID', '')
            ejs_tpl  = os.environ.get('EMAILJS_TEMPLATE_ID', '')
            js = (f'window.AVIATION_KEY = "{key}";'
                  f'window.EJS_PUBLIC_KEY = "{ejs_pub}";'
                  f'window.EJS_SERVICE_ID = "{ejs_svc}";'
                  f'window.EJS_TEMPLATE_ID = "{ejs_tpl}";')
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(js.encode())))
            self.end_headers()
            if self.command != 'HEAD':
                self._write_body(js.encode())
            return

        if self.path == '/api/google-maps-browser-key':
            # This is deliberately the only endpoint that exposes the
            # restricted browser key.  Keep the server-side Routes API key
            # out of this response and do not include the key in diagnostics.
            browser_key = os.environ.get('GOOGLE_MAPS_BROWSER_API_KEY', '').strip()
            if not browser_key:
                return self._json({'error': 'Google Maps address search unavailable'}, 503)
            return self._json({'key': browser_key})

        if request_path == HOURLY_HUB_PATH:
            return self._hourly_hub_route()

        if self.path.startswith('/api/positioning'):
            # Hub positioning: pick the anchor hub for a trip and return the
            # real driving distance/time from that hub to the far end.
            try:
                qs = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(qs)
                pickup = params.get('pickup', [''])[0]
                dropoff = params.get('dropoff', [''])[0]
                if not pickup:
                    return self._json({'error': 'missing pickup'}, 400)
                result = self._hub_positioning(pickup, dropoff)
                if result is None:
                    return self._json({'error': 'no_route'}, 400)
                return self._json(result)
            except Exception as e:
                return self._json({'error': str(e)}, 500)

        if self.path.startswith('/api/distance'):
            try:
                qs = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(qs)
                origin = params.get('origin', [''])[0]
                destination = params.get('destination', [''])[0]
                if not (origin and destination):
                    return self._json({'error': 'missing params'}, 400)
                def query_point(lat_name, lon_name):
                    try:
                        lat = float(params.get(lat_name, [''])[0])
                        lon = float(params.get(lon_name, [''])[0])
                    except (TypeError, ValueError):
                        return None
                    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                        return None
                    return (lat, lon)
                origin_point = query_point('originLat', 'originLon')
                destination_point = query_point('destinationLat', 'destinationLon')
                result = self._google_route(origin, destination, origin_point, destination_point)
                if result is None:
                    # Google Routes API unavailable (not enabled on the
                    # project yet) — fall back to free OpenStreetMap routing.
                    result = self._osrm_route(
                        origin, destination, origin_point, destination_point
                    )
                if result is None:
                    return self._json({'error': 'no_route'}, 400)
                return self._json(result)
            except Exception as e:
                return self._json({'error': str(e)}, 500)

        # Netlify-style pretty URLs: serve /blog/foo from /blog/foo.html
        # so the dev preview matches production (extensionless canonicals).
        clean = urllib.parse.urlparse(self.path).path
        if clean and not clean.endswith('/'):
            fs_path = clean.lstrip('/')
            if not os.path.isfile(fs_path) and os.path.isfile(fs_path + '.html'):
                self.path = clean + '.html'

        if self.command == 'HEAD':
            return super().do_HEAD()
        return super().do_GET()

    @staticmethod
    def _private_static_path(path):
        """Keep Python/config/source files out of the static document root.

        The workspace is also the deployment public directory.  Restrict only
        source/document paths that are not browser assets, rather than denying
        the whole attached-assets tree and breaking images used by the site.
        """
        try:
            decoded = urllib.parse.unquote(path)
            normalized = posixpath.normpath('/' + decoded.lstrip('/'))
        except (TypeError, ValueError):
            return True
        lower = normalized.lower()
        if (
            lower == '/server.py'
            or lower.endswith('/server.py')
            or lower.endswith(('.py', '.pyc', '.pyo'))
            or lower == '/.replit'
            or lower == '/netlify.toml'
            or lower.startswith('/.git/')
            or lower == '/.git'
            or lower == '/scripts'
            or lower.startswith('/scripts/')
            or lower.startswith('/compiled-static/')
            or lower.startswith('/node_modules/')
            or lower.startswith('/generated-artifacts/')
        ):
            return True
        # Briefs and other source documents under attached_assets can contain
        # backend-only configuration. Image/video/archive assets remain public.
        if lower.startswith('/attached_assets/'):
            extension = os.path.splitext(lower)[1]
            if extension in (
                '.txt', '.md', '.json', '.toml', '.yaml', '.yml', '.csv',
                '.py', '.js', '.ts', '.css', '.html',
            ):
                return True
        return False

    def _hourly_hub_route(self):
        """Handle the intentionally minimal hourly availability contract."""
        params = urllib.parse.parse_qs(
            urllib.parse.urlsplit(self.path).query,
            keep_blank_values=True,
        )
        pickup = params.get('pickup', [None])[0]
        lat = params.get('lat', [None])[0]
        lon = params.get('lon', [None])[0]
        try:
            address, coordinates, cache_key = _normalize_hourly_request(
                pickup, lat, lon
            )
        except ValueError as error:
            # Validation details are safe; no provider response or address
            # data is echoed back to the browser.
            return self._json({'error': str(error)}, 400)

        selected = self._hourly_hub_cache.get(cache_key)
        if selected is HOURLY_HUB_CACHE_MISS:
            try:
                selected = _select_hourly_hub(address, coordinates)
            except Exception:
                # Provider failures must produce contact-us behavior, never a
                # guessed/default hourly price and never a diagnostic leak.
                selected = None
            self._hourly_hub_cache.set(cache_key, selected)
        return self._json({'available': selected is not None})

    def end_headers(self):
        path = urllib.parse.urlparse(self.path).path.lower()
        if getattr(self, '_vary_accept_encoding', False):
            self.send_header('Vary', 'Accept-Encoding')
        # Baseline security headers. CSP starts report-only so third-party
        # tags (GTM, Google Maps, EmailJS, Moovs) can't break before a
        # tested enforcing policy is written.
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('Permissions-Policy',
                         'camera=(), microphone=(), payment=(), usb=(), geolocation=(self)')
        self.send_header('Content-Security-Policy-Report-Only',
                         "default-src 'self' https: data: blob: 'unsafe-inline' 'unsafe-eval'; "
                         "frame-ancestors 'self'; object-src 'none'; base-uri 'self'")
        if IS_PROD:
            # Production: cache static assets, always revalidate HTML.
            if path.endswith(('.css', '.js', '.webp', '.png', '.jpg', '.jpeg', '.svg', '.ico', '.woff', '.woff2', '.mp4')):
                versioned = bool(urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query).get('v'))
                self.send_header('Cache-Control', 'public, max-age=31536000, immutable' if versioned else 'public, max-age=0, must-revalidate')
            else:
                self.send_header('Cache-Control', 'public, max-age=0, must-revalidate')
        else:
            # Dev preview: never cache, so edits show up on refresh.
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        SimpleHTTPRequestHandler.end_headers(self)

    @staticmethod
    def _route_point(address, coordinates):
        if coordinates:
            lat, lon = coordinates
            return {
                'location': {
                    'latLng': {
                        'latitude': lat,
                        'longitude': lon,
                    }
                }
            }
        return {'address': address}

    def _google_route(self, origin, destination, origin_coordinates=None,
                      destination_coordinates=None):
        gkey = os.environ.get('GOOGLE_MAPS_API_KEY', '')
        if not gkey:
            return None
        try:
            url = 'https://routes.googleapis.com/directions/v2:computeRoutes'
            body = json.dumps({
                'origin': self._route_point(origin, origin_coordinates),
                'destination': self._route_point(destination, destination_coordinates),
                'travelMode': 'DRIVE',
                'routingPreference': 'TRAFFIC_AWARE',
                'units': 'IMPERIAL',
            }).encode()
            req = urllib.request.Request(url, data=body, method='POST', headers={
                'Content-Type': 'application/json',
                'X-Goog-Api-Key': gkey,
                'X-Goog-FieldMask': 'routes.distanceMeters,routes.duration',
            })
            with urllib.request.urlopen(req, timeout=12) as r:
                data = json.loads(r.read().decode())
            routes = data.get('routes') or []
            if not routes:
                return None
            rt = routes[0]
            meters = rt.get('distanceMeters', 0)
            dur = str(rt.get('duration', '0s'))
            ds = dur[:-1] if dur.endswith('s') else dur
            try:
                seconds = int(round(float(ds)))
            except Exception:
                seconds = 0
            return {
                'meters': meters,
                'miles': round(meters / 1609.34, 1),
                'seconds': seconds,
                'minutes': round(seconds / 60),
                'source': 'google',
            }
        except Exception:
            return None

    # Operating hubs: every vehicle starts and ends its day at one of these.
    HUBS = [
        ('Austin',            -97.7431, 30.2672),
        ('Dallas\u2013Fort Worth', -96.7970, 32.7767),
        ('Houston',           None, None),
    ]
    HUB_FREE_MILES = 60
    _geo_cache = {}

    @staticmethod
    def _haversine_miles(a, b):
        import math
        lon1, lat1, lon2, lat2 = map(math.radians, (float(a[0]), float(a[1]), float(b[0]), float(b[1])))
        h = (math.sin((lat2 - lat1) / 2) ** 2 +
             math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
        return 3958.8 * 2 * math.asin(math.sqrt(h))

    def _hub_positioning(self, pickup, dropoff):
        p = self._geocode(pickup)
        if not p:
            return None
        d = None
        if dropoff:
            d = self._geocode(dropoff)
            if not d:
                # A drop-off was given but couldn't be located — fail loudly
                # rather than quietly pricing from the pickup alone.
                return None
        # Anchor hub: the hub nearest to either end of the trip. A trip that
        # touches a hub metro naturally selects that hub; a remote trip gets
        # whichever hub is closest overall.
        best = None
        for name, lon, lat in self.HUBS:
            if name == 'Houston':
                # Resolve the private operating base, never a city-center guess.
                address = dict(HOURLY_HUBS)['houston']
                try:
                    point = self._geocode(address)
                except Exception:
                    return None
                if not point:
                    return None
                lon, lat = point
            hp = self._haversine_miles((lon, lat), p)
            hd = self._haversine_miles((lon, lat), d) if d else hp
            score = min(hp, hd)
            if best is None or score < best[0]:
                best = (score, name, (lon, lat), hp, hd)
        _, hub_name, hub_pt, hp, hd = best
        # Far end of the trip relative to the anchor hub
        far_pt = d if (d and hd > hp) else p
        route = self._route_coords(hub_pt, far_pt)
        if route is None:
            return None
        route['hub'] = hub_name
        route['free_miles'] = self.HUB_FREE_MILES
        return route

    def _route_coords(self, a, b):
        try:
            url = (f'https://router.project-osrm.org/route/v1/driving/'
                   f'{a[0]},{a[1]};{b[0]},{b[1]}?overview=false')
            req = urllib.request.Request(url, headers={
                'User-Agent': 'PurpleHeartLimo/1.0 (purpleheartlimo.com)',
            })
            with urllib.request.urlopen(req, timeout=12) as r:
                data = json.loads(r.read().decode())
            routes = data.get('routes') or []
            if not routes:
                return None
            meters = routes[0].get('distance', 0)
            seconds = int(round(routes[0].get('duration', 0)))
            return {
                'meters': int(meters),
                'miles': round(meters / 1609.34, 1),
                'seconds': seconds,
                'minutes': round(seconds / 60),
                'source': 'osrm',
            }
        except Exception:
            return None

    def _geocode(self, q):
        cached = Handler._geo_cache.get(q)
        if cached is not None:
            return cached
        url = ('https://nominatim.openstreetmap.org/search?format=json&limit=1'
               '&countrycodes=us&q=' + urllib.parse.quote(q))
        req = urllib.request.Request(url, headers={
            'User-Agent': 'PurpleHeartLimo/1.0 (purpleheartlimo.com)',
            'Accept-Language': 'en',
        })
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
        if not data:
            return None
        result = (data[0]['lon'], data[0]['lat'])
        Handler._geo_cache[q] = result
        return result

    def _osrm_route(self, origin, destination, origin_coordinates=None,
                    destination_coordinates=None):
        try:
            # Query coordinates arrive as (latitude, longitude), while
            # Nominatim and OSRM use (longitude, latitude).
            a = (
                (origin_coordinates[1], origin_coordinates[0])
                if origin_coordinates else self._geocode(origin)
            )
            b = (
                (destination_coordinates[1], destination_coordinates[0])
                if destination_coordinates else self._geocode(destination)
            )
            if not a or not b:
                return None
            url = (f'https://router.project-osrm.org/route/v1/driving/'
                   f'{a[0]},{a[1]};{b[0]},{b[1]}?overview=false')
            req = urllib.request.Request(url, headers={
                'User-Agent': 'PurpleHeartLimo/1.0 (purpleheartlimo.com)',
            })
            with urllib.request.urlopen(req, timeout=12) as r:
                data = json.loads(r.read().decode())
            routes = data.get('routes') or []
            if not routes:
                return None
            meters = routes[0].get('distance', 0)
            seconds = int(round(routes[0].get('duration', 0)))
            return {
                'meters': int(meters),
                'miles': round(meters / 1609.34, 1),
                'seconds': seconds,
                'minutes': round(seconds / 60),
                'source': 'osrm',
            }
        except Exception:
            return None

    def _json(self, obj, status=200, extra_headers=None):
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Access-Control-Allow-Origin', '*')
        for name, value in (extra_headers or {}).items():
            if name.lower() == 'access-control-allow-origin':
                continue
            self.send_header(name, value)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if self.command != 'HEAD':
            self._write_body(body)

    def _write_body(self, data):
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass  # client disconnected mid-response; not an error worth a traceback

    def log_message(self, format, *args):
        print(format % args)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    server = ThreadingHTTPServer(('0.0.0.0', port), Handler)
    print(f'Serving on port {port} ({"production" if IS_PROD else "dev"}; '
          f'{len(REDIRECTS_EXACT)} exact + {len(REDIRECT_PREFIXES)} prefix redirects loaded)')
    server.serve_forever()
