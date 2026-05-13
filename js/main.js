/* Purple Heart Limo — Main JavaScript */

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initScrollAnimations();
  initContactForm();
  initScrollTop();
});

/* ---- Navigation ---- */
function initNavigation() {
  const header      = document.getElementById('header');
  const menuToggle  = document.getElementById('menuToggle');
  const navLinks    = document.getElementById('navLinks');

  window.addEventListener('scroll', () => {
    header.classList.toggle('scrolled', window.scrollY > 60);
  }, { passive: true });

  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
      const open = menuToggle.classList.toggle('active');
      navLinks.classList.toggle('open', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });

    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', closeMenu);
    });

    document.addEventListener('click', e => {
      if (!header.contains(e.target)) closeMenu();
    });
  }

  function closeMenu() {
    menuToggle && menuToggle.classList.remove('active');
    navLinks  && navLinks.classList.remove('open');
    document.body.style.overflow = '';
  }

  // Highlight active nav link
  const page = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === page || (page === '' && href === 'index.html')) {
      a.classList.add('active');
    }
  });
}

/* ---- Scroll-in Animations ---- */
function initScrollAnimations() {
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll(
    '.service-card, .fleet-card, .feature-item, .testimonial-card, .area-tag, .contact-item, .anim'
  ).forEach((el, i) => {
    el.classList.add('anim');
    el.style.transitionDelay = `${Math.min(i % 4, 3) * 80}ms`;
    io.observe(el);
  });
}

/* ---- Scroll-to-top ---- */
function initScrollTop() {
  const btn = document.getElementById('scrollTop');
  if (!btn) return;
  window.addEventListener('scroll', () => {
    btn.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });
  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

/* ---- Contact Form ---- */
function initContactForm() {
  const form = document.getElementById('contactForm');
  if (!form) return;

  const alertSuccess = document.getElementById('alertSuccess');
  const alertError   = document.getElementById('alertError');
  const submitBtn    = form.querySelector('button[type="submit"]');

  form.addEventListener('submit', async e => {
    e.preventDefault();

    const name    = form.querySelector('[name="name"]')?.value.trim();
    const phone   = form.querySelector('[name="phone"]')?.value.trim();
    const email   = form.querySelector('[name="email"]')?.value.trim();
    const service = form.querySelector('[name="service"]')?.value.trim();
    const date    = form.querySelector('[name="date"]')?.value.trim();

    if (!name || !phone) {
      showAlert(alertError, 'Please enter your full name and phone number.');
      return;
    }
    if (!service) {
      showAlert(alertError, 'Please select a service type.');
      return;
    }
    if (!date) {
      showAlert(alertError, 'Please select your event date.');
      return;
    }
    if (email && !validEmail(email)) {
      showAlert(alertError, 'Please enter a valid email address.');
      return;
    }

    const origText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '⏳ Sending…';
    hideAlerts();

    // Collect all fields including new ones
    const payload = {};
    new FormData(form).forEach((v, k) => { if (v) payload[k] = v; });

    try {
      const res  = await fetch('/.netlify/functions/contact', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(payload),
      });
      const data = await res.json();

      if (res.ok && data.success) {
        showAlert(alertSuccess, data.message || "✅ Request received! We'll call or text you within 5 minutes.");
        form.reset();
        document.getElementById('cf-flight-row').style.display = 'none';
      } else {
        showAlert(alertError, data.error || 'Something went wrong. Please call (833) 740-0700.');
      }
    } catch {
      showAlert(alertError, 'Network error. Please call (833) 740-0700.');
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = origText;
    }
  });

  function showAlert(el, msg) {
    if (!el) return;
    hideAlerts();
    el.textContent = msg;
    el.classList.add('show');
    el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function hideAlerts() {
    [alertSuccess, alertError].forEach(a => a && a.classList.remove('show'));
  }
}

function validEmail(v) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
}

/* ---- Toggle Flight Fields (contact.html) ---- */
function toggleFlightFields(serviceValue) {
  const row = document.getElementById('cf-flight-row');
  if (row) row.style.display = serviceValue === 'Airport Transfer' ? 'block' : 'none';
}
