/* ============================================================
   Above & Beyond Janitorial — site app.js
   Quote modal (4-step), form submission, animations, a11y.
   ============================================================ */

/* ---- CONFIG ---- */
/* Recipient: abovejanitorial@hotmail.com
   Replace FORMSPREE_ID with the form ID from formspree.io.
   Form ID looks like "xqalbpoz" — endpoint becomes
   https://formspree.io/f/xqalbpoz. See SETUP.md. */
const FORMSPREE_ID = 'REPLACE_WITH_FORMSPREE_ID';
const FORM_ENDPOINT = `https://formspree.io/f/${FORMSPREE_ID}`;

/* ---- STATE ---- */
const STATE = { step: 0, facility: null, size: null, frequency: null, contact: { name: '', email: '', phone: '', notes: '' } };
const FACILITIES = [
  { id: 'office', label: 'Corporate office' }, { id: 'medical', label: 'Medical / dental' },
  { id: 'bank', label: 'Bank / financial' }, { id: 'retail', label: 'Retail storefront' },
  { id: 'church', label: 'Church' }, { id: 'gov', label: 'Government' }, { id: 'other', label: 'Something else' }
];
const SIZES = [
  { id: 'sm', label: 'Under 2,000 sq ft' }, { id: 'md', label: '2,000 – 8,000 sq ft' },
  { id: 'lg', label: '8,000 – 20,000 sq ft' }, { id: 'xl', label: '20,000+ sq ft' }
];
const FREQS = [
  { id: 'daily', label: '5+ times a week' }, { id: '3x', label: '2–4 times a week' },
  { id: '1x', label: 'Once a week' }, { id: 'monthly', label: 'Monthly or one-time' }
];

let lastFocusBeforeModal = null;

const FOCUSABLE_SEL = 'button:not([disabled]), input:not([disabled]), textarea:not([disabled]), select:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])';

function getModalFocusables() {
  const modal = document.getElementById('quote-modal-inner');
  return modal ? [...modal.querySelectorAll(FOCUSABLE_SEL)].filter(el => el.offsetParent !== null) : [];
}

function modalKeydown(e) {
  if (e.key === 'Escape') {
    e.preventDefault();
    closeQuote();
    return;
  }
  if (e.key !== 'Tab') return;
  const focusables = getModalFocusables();
  if (!focusables.length) return;
  const first = focusables[0];
  const last = focusables[focusables.length - 1];
  if (e.shiftKey && document.activeElement === first) {
    e.preventDefault();
    last.focus();
  } else if (!e.shiftKey && document.activeElement === last) {
    e.preventDefault();
    first.focus();
  }
}

function openQuote() {
  lastFocusBeforeModal = document.activeElement;
  STATE.step = 0;
  document.getElementById('quote-modal').classList.add('open');
  document.body.style.overflow = 'hidden';
  document.addEventListener('keydown', modalKeydown);
  render();
}
function openQuoteFromCard() {
  lastFocusBeforeModal = document.activeElement;
  const f = document.getElementById('hf-facility');
  const s = document.getElementById('hf-size');
  const fr = document.getElementById('hf-freq');
  const c = document.getElementById('hf-contact');
  if (f) STATE.facility = (FACILITIES.find(x => f.value.toLowerCase().startsWith(x.label.toLowerCase().slice(0,5))) || FACILITIES[0]).id;
  if (s) STATE.size = (SIZES.find(x => x.label === s.value) || SIZES[1]).id;
  if (fr) STATE.frequency = (FREQS.find(x => x.label === fr.value) || FREQS[1]).id;
  const cv = (c && c.value) || '';
  if (cv.includes('@')) STATE.contact.email = cv; else STATE.contact.phone = cv;
  STATE.step = 3;
  document.getElementById('quote-modal').classList.add('open');
  document.body.style.overflow = 'hidden';
  document.addEventListener('keydown', modalKeydown);
  render();
}
function closeQuote() {
  document.getElementById('quote-modal').classList.remove('open');
  document.body.style.overflow = '';
  document.removeEventListener('keydown', modalKeydown);
  if (lastFocusBeforeModal && typeof lastFocusBeforeModal.focus === 'function') {
    lastFocusBeforeModal.focus();
  }
}
function next() { STATE.step++; render(); }
function back() { STATE.step--; render(); }
function pickOption(field, value) { STATE[field] = value; setTimeout(next, 180); render(); }

function render() {
  const m = document.getElementById('quote-modal-inner');
  const s = STATE.step;
  const dots = (n) => `<div class="stepper">${[0,1,2,3].map(i => `<div class="s ${i===n?'active':(i<n?'done':'')}"></div>`).join('')}<span class="cnt">${n+1}/4</span></div>`;
  const close = `<button class="modal-close" aria-label="Close quote form" onclick="closeQuote()"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg></button>`;

  if (s === 0) {
    m.innerHTML = `<div class="modal-head"><h3 id="quote-modal-title">What kind of <span class="accent">facility?</span></h3>${close}</div>${dots(0)}
      <div class="modal-body"><div class="step-lbl">— Step 1 / 4 · Facility type</div>
      <div class="opts" role="list">${FACILITIES.map(f => `<button class="opt ${STATE.facility===f.id?'selected':''}" onclick="pickOption('facility','${f.id}')">${f.label}</button>`).join('')}</div></div>`;
  } else if (s === 1) {
    m.innerHTML = `<div class="modal-head"><h3 id="quote-modal-title">Roughly <span class="accent">how big?</span></h3>${close}</div>${dots(1)}
      <div class="modal-body"><div class="step-lbl">— Step 2 / 4 · Facility size</div>
      <div class="opts opts-single">${SIZES.map(o => `<button class="opt ${STATE.size===o.id?'selected':''}" onclick="pickOption('size','${o.id}')">${o.label}</button>`).join('')}</div></div>
      <div class="modal-foot"><button class="back" onclick="back()">← Back</button><span style="font-size:11px;color:var(--ink-3);font-family:var(--mono)">Ballpark is fine</span></div>`;
  } else if (s === 2) {
    m.innerHTML = `<div class="modal-head"><h3 id="quote-modal-title">How <span class="accent">often?</span></h3>${close}</div>${dots(2)}
      <div class="modal-body"><div class="step-lbl">— Step 3 / 4 · Frequency</div>
      <div class="opts opts-single">${FREQS.map(o => `<button class="opt ${STATE.frequency===o.id?'selected':''}" onclick="pickOption('frequency','${o.id}')">${o.label}</button>`).join('')}</div></div>
      <div class="modal-foot"><button class="back" onclick="back()">← Back</button></div>`;
  } else if (s === 3) {
    m.innerHTML = `<div class="modal-head"><h3 id="quote-modal-title">Send <span class="accent">the quote where?</span></h3>${close}</div>${dots(3)}
      <div class="modal-body"><div class="step-lbl">— Step 4 / 4 · Your details</div>
      <div class="form-row"><label for="qf-name">Your name</label><input id="qf-name" autocomplete="name" value="${escAttr(STATE.contact.name)}" placeholder="Full name"></div>
      <div class="form-row"><label for="qf-email">Email</label><input id="qf-email" type="email" autocomplete="email" value="${escAttr(STATE.contact.email)}" placeholder="you@company.com"></div>
      <div class="form-row"><label for="qf-phone">Phone</label><input id="qf-phone" type="tel" autocomplete="tel" value="${escAttr(STATE.contact.phone)}" placeholder="(208) 555-0123"></div>
      <div class="form-row"><label for="qf-notes">Anything we should know? (optional)</label><textarea id="qf-notes" rows="3" placeholder="Pain points, special access, walkthrough times...">${escHtml(STATE.contact.notes)}</textarea></div>
      <!-- honeypot: bots fill this, humans don't see it -->
      <input type="text" name="_gotcha" id="qf-gotcha" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px;opacity:0;height:0;width:0;">
      <div id="qf-error" class="form-error" role="alert" aria-live="polite"></div>
      </div>
      <div class="modal-foot"><button class="back" onclick="back()">← Back</button><button class="btn btn-primary" id="qf-submit" onclick="submitQuote()">Send →</button></div>`;
  } else {
    m.innerHTML = `<div class="success"><div class="ic"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m5 12 5 5L20 7"/></svg></div>
      <h3 id="quote-modal-title">Quote received.</h3><p>Todd will reach out within one business day — from <strong>(208) 818-3175</strong>.</p>
      <button class="btn btn-ink" onclick="closeQuote()">Close</button></div>`;
  }

  /* Move focus into modal */
  const firstFocusable = m.querySelector('button, input, textarea, select, [tabindex]:not([tabindex="-1"])');
  if (firstFocusable) firstFocusable.focus();
}

function escHtml(s) { return String(s || '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function escAttr(s) { return escHtml(s); }

async function submitQuote() {
  const gotcha = document.getElementById('qf-gotcha');
  if (gotcha && gotcha.value) {
    /* Spam — fake success */
    STATE.step = 4; render(); return;
  }
  STATE.contact.name  = document.getElementById('qf-name').value.trim();
  STATE.contact.email = document.getElementById('qf-email').value.trim();
  STATE.contact.phone = document.getElementById('qf-phone').value.trim();
  STATE.contact.notes = document.getElementById('qf-notes').value.trim();

  const err = document.getElementById('qf-error');
  if (!STATE.contact.name) { err.textContent = 'Please enter your name.'; document.getElementById('qf-name').focus(); return; }
  if (!STATE.contact.email && !STATE.contact.phone) { err.textContent = 'Email or phone — one is required.'; document.getElementById('qf-email').focus(); return; }
  err.textContent = '';

  const facilityLabel  = (FACILITIES.find(x => x.id === STATE.facility) || {}).label || STATE.facility || '—';
  const sizeLabel      = (SIZES.find(x => x.id === STATE.size) || {}).label || STATE.size || '—';
  const frequencyLabel = (FREQS.find(x => x.id === STATE.frequency) || {}).label || STATE.frequency || '—';

  const payload = {
    name: STATE.contact.name,
    email: STATE.contact.email,
    phone: STATE.contact.phone,
    notes: STATE.contact.notes,
    facility: facilityLabel,
    size: sizeLabel,
    frequency: frequencyLabel,
    source_page: window.location.pathname,
    referrer: document.referrer || '(direct)',
    _subject: `[Quote] ${facilityLabel} · ${STATE.contact.name}`,
    _replyto: STATE.contact.email
  };

  const btn = document.getElementById('qf-submit');
  const orig = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = 'Sending…';

  try {
    if (FORMSPREE_ID === 'REPLACE_WITH_FORMSPREE_ID') {
      /* Dev fallback — log and show success so the UI is testable before Formspree is wired. */
      console.warn('[quote] FORMSPREE_ID not set — payload would be:', payload);
    } else {
      const res = await fetch(FORM_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error('Submission failed (' + res.status + ')');
    }
    STATE.step = 4;
    render();
  } catch (e) {
    console.error(e);
    btn.disabled = false;
    btn.innerHTML = orig;
    err.textContent = "Sorry — couldn't send. Please call (208) 818-3175 or email abovejanitorial@hotmail.com.";
  }
}

/* ============ MODAL FOCUS TRAP ============ */
document.addEventListener('keydown', (e) => {
  const modal = document.getElementById('quote-modal');
  const open = modal && modal.classList.contains('open');
  if (!open) return;
  if (e.key === 'Escape') { closeQuote(); return; }
  if (e.key !== 'Tab') return;
  const focusables = modal.querySelectorAll(
    'a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), textarea:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
  );
  if (focusables.length === 0) return;
  const first = focusables[0];
  const last = focusables[focusables.length - 1];
  if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
  else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
});

/* ============ MOBILE NAV TOGGLE ============ */
document.addEventListener('click', (e) => {
  const toggle = e.target.closest('.nav-toggle');
  if (!toggle) return;
  const nav = document.querySelector('.nav');
  if (!nav) return;
  nav.classList.toggle('mobile-open');
  const open = nav.classList.contains('mobile-open');
  toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
});

/* ============ ANIMATIONS ============ */
const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!prefersReduced) {
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.services-grid, .ind-grid, .why-list, .quotes-grid, .proc-grid').forEach(el => {
    el.classList.add('stagger');
    revealObserver.observe(el);
  });
  document.querySelectorAll('.areas-section, .industries-section').forEach(el => revealObserver.observe(el));

  const indObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        indObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });
  document.querySelectorAll('.ind-card').forEach(el => indObserver.observe(el));

  function animateCount(textNode, originalText, duration) {
    const numMatch = originalText.match(/[\d.]+/);
    if (!numMatch) return;
    const targetNum = parseFloat(numMatch[0]);
    const prefix = originalText.substring(0, numMatch.index);
    const suffix = originalText.substring(numMatch.index + numMatch[0].length);
    const decimals = (numMatch[0].split('.')[1] || '').length;
    const start = performance.now();
    function tick(now) {
      const elapsed = now - start;
      const t = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - t, 3);
      const current = (targetNum * eased).toFixed(decimals);
      textNode.textContent = prefix + current + suffix;
      if (t < 1) requestAnimationFrame(tick);
      else textNode.textContent = originalText;
    }
    requestAnimationFrame(tick);
  }
  function findCountTarget(el) {
    const firstText = Array.from(el.childNodes).find(n => n.nodeType === Node.TEXT_NODE && n.textContent.trim());
    return firstText || el;
  }

  setTimeout(() => {
    document.querySelectorAll('.hero-stat .n').forEach((el, i) => {
      setTimeout(() => animateCount(findCountTarget(el), el.textContent, 1100), i * 80);
    });
  }, 700);

  const metricObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = findCountTarget(el);
        animateCount(target, target.textContent, 1300);
        metricObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('.why-metric .big').forEach(el => metricObserver.observe(el));

  const heroEl = document.querySelector('.hero');
  if (heroEl) {
    let pRaf = null;
    window.addEventListener('scroll', () => {
      if (pRaf) return;
      pRaf = requestAnimationFrame(() => {
        const sy = window.scrollY;
        if (sy < 900) heroEl.style.setProperty('--hero-parallax', (sy * 0.35) + 'px');
        pRaf = null;
      });
    }, { passive: true });
  }
}
