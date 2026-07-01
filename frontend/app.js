/* ================================================================
   BPJS Care Assistant — app.js
   Landing page + Floating Chat Popup logic
   ================================================================ */

'use strict';

// ── Config ──────────────────────────────────────────────────────
const API_BASE   = window.location.origin;
const API_CHAT   = `${API_BASE}/api/chat`;
const API_HEALTH = `${API_BASE}/api/health`;

// ── State ────────────────────────────────────────────────────────
let isLoading     = false;
let popupOpen     = false;
let firstMessage  = true;

// ── DOM ──────────────────────────────────────────────────────────
const navbar         = document.getElementById('navbar');
const navHamburger   = document.getElementById('navHamburger');
const mobileMenu     = document.getElementById('mobileMenu');
const navCta         = document.getElementById('navCta');
const heroCta        = document.getElementById('heroCta');
const mobileCta      = document.getElementById('mobileCta');

const fabBtn         = document.getElementById('fabBtn');
const chatPopup      = document.getElementById('chatPopup');
const popupBody      = document.getElementById('popupBody');
const popupWelcome   = document.getElementById('popupWelcome');
const popupChips     = document.getElementById('popupChips');
const popupInput     = document.getElementById('popupInput');
const popupSendBtn   = document.getElementById('popupSendBtn');
const popupCloseBtn  = document.getElementById('popupCloseBtn');
const popupClearBtn  = document.getElementById('popupClearBtn');
const popupStatusDot = document.getElementById('popupStatusDot');
const popupStatusText= document.getElementById('popupStatusText');

// ── Navbar scroll effect ─────────────────────────────────────────
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 20);
}, { passive: true });

// ── Mobile hamburger ─────────────────────────────────────────────
navHamburger.addEventListener('click', () => {
  mobileMenu.classList.toggle('open');
});
// Close mobile menu on link click
mobileMenu.querySelectorAll('.mobile-nav-link').forEach(link => {
  link.addEventListener('click', () => mobileMenu.classList.remove('open'));
});

// ── Open/close chat popup ────────────────────────────────────────
function openPopup() {
  popupOpen = true;
  chatPopup.classList.add('open');
  chatPopup.setAttribute('aria-hidden', 'false');
  fabBtn.classList.add('open');
  // Focus input after transition
  setTimeout(() => popupInput.focus(), 350);
}

function closePopup() {
  popupOpen = false;
  chatPopup.classList.remove('open');
  chatPopup.setAttribute('aria-hidden', 'true');
  fabBtn.classList.remove('open');
}

function togglePopup() {
  if (popupOpen) closePopup();
  else openPopup();
}

fabBtn.addEventListener('click', togglePopup);
popupCloseBtn.addEventListener('click', closePopup);
navCta.addEventListener('click', openPopup);
if (heroCta) heroCta.addEventListener('click', openPopup);
if (mobileCta) mobileCta.addEventListener('click', () => {
  mobileMenu.classList.remove('open');
  openPopup();
});

// Close popup on Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && popupOpen) closePopup();
});

// ── Health check ─────────────────────────────────────────────────
async function checkHealth() {
  setStatus('loading', 'Memuat sistem...');
  try {
    const res = await fetch(API_HEALTH, { signal: AbortSignal.timeout(10000) });
    if (!res.ok) throw new Error();
    const data = await res.json();
    if (data.rag_ready) {
      setStatus('online', 'Siap menjawab');
    } else {
      setStatus('loading', 'Memuat model...');
      setTimeout(checkHealth, 5000);
    }
  } catch {
    setStatus('error', 'Tidak terhubung');
    setTimeout(checkHealth, 8000);
  }
}

function setStatus(state, text) {
  popupStatusDot.className = `popup-status-dot ${state}`;
  popupStatusText.textContent = text;
}

// ── Quick chips ──────────────────────────────────────────────────
popupChips.querySelectorAll('.popup-chip').forEach(chip => {
  chip.addEventListener('click', () => {
    popupInput.value = chip.dataset.q;
    popupInput.dispatchEvent(new Event('input'));
    sendMessage();
  });
});

// ── Input handlers ───────────────────────────────────────────────
popupInput.addEventListener('input', () => {
  const val = popupInput.value.trim();
  popupSendBtn.disabled = val.length === 0 || isLoading;
  popupInput.style.height = 'auto';
  popupInput.style.height = Math.min(popupInput.scrollHeight, 80) + 'px';
});

popupInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    if (!popupSendBtn.disabled) sendMessage();
  }
});

popupSendBtn.addEventListener('click', sendMessage);

// ── Clear chat ───────────────────────────────────────────────────
popupClearBtn.addEventListener('click', () => {
  popupBody.querySelectorAll('.popup-msg, .popup-error').forEach(el => el.remove());
  popupWelcome.style.display = '';
  popupWelcome.style.opacity = '1';
  popupChips.classList.remove('hidden');
  firstMessage = true;
  popupInput.value = '';
  popupInput.style.height = 'auto';
  popupSendBtn.disabled = true;
});

// ── Send message ─────────────────────────────────────────────────
async function sendMessage() {
  const text = popupInput.value.trim();
  if (!text || isLoading) return;

  // Hide welcome on first message
  if (firstMessage) {
    popupWelcome.style.transition = 'opacity 250ms ease';
    popupWelcome.style.opacity = '0';
    setTimeout(() => { popupWelcome.style.display = 'none'; }, 250);
    popupChips.classList.add('hidden');
    firstMessage = false;
  }

  popupInput.value = '';
  popupInput.style.height = 'auto';
  popupSendBtn.disabled = true;
  isLoading = true;

  appendMsg('user', text);
  const typingEl = appendTyping();
  scrollBottom();

  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);

    const res = await fetch(API_CHAT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text }),
      signal: controller.signal,
    });
    clearTimeout(timeout);
    typingEl.remove();

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      appendError(err.detail ?? `Error ${res.status}`);
    } else {
      const data = await res.json();
      appendMsg('bot', data.answer);
    }
  } catch (err) {
    typingEl.remove();
    if (err.name === 'AbortError') {
      appendError('Timeout — coba lagi.');
    } else {
      appendError('Tidak bisa terhubung ke server.');
    }
  } finally {
    isLoading = false;
    popupSendBtn.disabled = popupInput.value.trim().length === 0;
    scrollBottom();
  }
}

// ── DOM helpers ──────────────────────────────────────────────────
function appendMsg(role, text) {
  const timeStr = new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' });
  const el = document.createElement('div');
  el.className = `popup-msg ${role}`;
  el.innerHTML = `
    <div class="popup-bubble">${escHtml(text)}</div>
    <div class="popup-msg-time">${timeStr}</div>
  `;
  popupBody.appendChild(el);
  return el;
}

function appendTyping() {
  const el = document.createElement('div');
  el.className = 'popup-typing';
  el.innerHTML = '<span></span><span></span><span></span>';
  popupBody.appendChild(el);
  scrollBottom();
  return el;
}

function appendError(msg) {
  const el = document.createElement('div');
  el.className = 'popup-error';
  el.textContent = msg;
  popupBody.appendChild(el);
}

function scrollBottom() {
  requestAnimationFrame(() => {
    popupBody.scrollTop = popupBody.scrollHeight;
  });
}

function escHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/\n/g, '<br>');
}

// ── Smooth scroll for anchor links ───────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', (e) => {
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ── Intersection observer for scroll animations ───────────────────
const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -60px 0px' };
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

// Observe cards for fade-in animation
document.querySelectorAll('.about-card, .feature-item, .flow-step, .team-card').forEach((el, i) => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(24px)';
  el.style.transition = `opacity 500ms ease ${i * 60}ms, transform 500ms cubic-bezier(0.4, 0, 0.2, 1) ${i * 60}ms`;
  el.classList.add('animate-on-scroll');
  observer.observe(el);
});

// Add visible class handling
const styleTag = document.createElement('style');
styleTag.textContent = `.animate-on-scroll.visible { opacity: 1 !important; transform: translateY(0) !important; }`;
document.head.appendChild(styleTag);

// ── Init ─────────────────────────────────────────────────────────
(function init() {
  checkHealth();
})();
