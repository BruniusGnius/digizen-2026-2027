/* Digizen · acciones de los botones (03-build-plan.md §4.6).
   - «Conversar con ADA primero» abre el diálogo; el envío a la API lo gestiona
     digizen-ab.js sin emitir datos personales en eventos del navegador.
   - «Inscribir a mi hijo ↗» emite `digizen:checkout`, como en A (destino del pago pendiente).
     En el menú y al final (12.4), ese botón lleva a las tarjetas de precio para elegir la forma de pago (decisión del usuario, 2026-09-30).
   - Botones con destino pendiente (data-pending) no hacen nada todavía. */
(function () {
  'use strict';
  var DZ = window.DZ;
  var dlg = document.getElementById('ada-dialog');
  var checkoutDlg = document.getElementById('checkout-dialog');
  var checkoutPlan = null;
  var COOKIE_KEY = 'digizen_cookie_preferences_v1';

  // ---------- respuesta inmediata en pointerdown (apple-design §1, A2) ----------
  var PRESSABLE = '.btn, .lnk, .channel button, .faq summary, .menu-item, .rail-item, .menu-btn, .close';
  document.addEventListener('touchstart', function () {}, { passive: true }); /* iOS: activa :active al primer toque */
  document.addEventListener('pointerdown', function (e) {
    var b = e.target.closest(PRESSABLE); if (!b) return;
    b.classList.add('is-pressed');
    var up = function () { b.classList.remove('is-pressed'); window.removeEventListener('pointerup', up); window.removeEventListener('pointercancel', up); };
    window.addEventListener('pointerup', up); window.addEventListener('pointercancel', up);
  });

  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-action], [data-pending]'); if (!b) return;
    var act = b.getAttribute('data-action');
    if (b.closest('#menu') && DZ.closeMenu) DZ.closeMenu(true);
    if (act === 'ada' && dlg) { openAda(b); return; }
    if (act === 'pricing') { DZ.goTo(DZ.isD ? '11.4' : '11.5m'); return; }   /* menú y 12.4: a las tarjetas de precio (desktop 11.4, móvil 11.5m) */
    if (act === 'checkout') {
      checkoutPlan = b.getAttribute('data-plan') || null;
      if (checkoutDlg) { checkoutDlg.showModal(); }
      return;
    }
    if (b.hasAttribute('data-pending')) { e.preventDefault(); if (window.console) console.info('[digizen] destino pendiente:', b.getAttribute('data-pending')); }
  });

  if (!dlg) return;
  var contact = dlg.querySelector('[name=contact]');
  var labelTxt = dlg.querySelector('[data-contact-label]');
  var chans = dlg.querySelectorAll('[data-channel]'), opener = null;
  var CH = {
    correo:   { label: 'Correo electrónico', type: 'email', auto: 'email', ph: 'tu@correo.com' },
    whatsapp: { label: 'Número de WhatsApp', type: 'tel',   auto: 'tel',   ph: '+52 55 0000 0000' }
  };
  function setChannel(c) {
    Array.prototype.forEach.call(chans, function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-channel') === c)); });
    var d = CH[c]; labelTxt.textContent = d.label;
    contact.type = d.type; contact.autocomplete = d.auto; contact.placeholder = d.ph;
    dlg.setAttribute('data-channel-active', c);
  }
  Array.prototype.forEach.call(chans, function (b) { b.addEventListener('click', function () { setChannel(b.getAttribute('data-channel')); }); });

  // ---------- A3: el diálogo emerge desde su botón y vuelve hacia él (apple-design §7), con resorte interrumpible ----------
  var sp = null, closing = false;
  function draw(p) {
    dlg.style.opacity = Math.max(0, Math.min(1, p));
    if (!DZ.reduce) dlg.style.transform = 'scale(' + (0.9 + 0.1 * p) + ')'; /* movimiento reducido: solo fundido */
  }
  function originFromOpener() {
    var r = dlg.getBoundingClientRect(), o = opener && opener.getBoundingClientRect ? opener.getBoundingClientRect() : null;
    var ox = o ? o.left + o.width / 2 - r.left : r.width / 2, oy = o ? o.top + o.height / 2 - r.top : r.height / 2;
    dlg.style.transformOrigin = ox + 'px ' + oy + 'px';
  }
  function animate(to, done) {
    if (sp && sp.running()) { sp.to(to); sp._done = done; return; }
    var from = to ? 0 : 1;
    sp = DZ.spring({ from: from, to: to, response: 0.36, eps: 0.002, onUpdate: draw,
      onRest: function () { var d = sp && sp._done; sp = null; if (d) d(); } });
    sp._done = done;
  }
  function openAda(from) {
    opener = from; closing = false;
    if (!dlg.open) {
      if (typeof dlg.showModal === 'function') dlg.showModal(); else dlg.setAttribute('open', '');
      originFromOpener(); draw(0);   /* el origen se mide sin escala */
    }
    animate(1, function () { dlg.style.transform = ''; });
    var first = dlg.querySelector('input'); if (first) first.focus({ preventScroll: true });
  }
  function closeAda() {
    if (!dlg.open || closing) return; closing = true;
    originFromOpener();
    animate(0, function () { closing = false; dlg.close(); dlg.style.opacity = ''; dlg.style.transform = ''; });
  }
  dlg.addEventListener('cancel', function (e) { e.preventDefault(); closeAda(); }); /* Esc */
  dlg.addEventListener('close', function () { if (opener && opener.focus) opener.focus({ preventScroll: true }); });
  dlg.querySelector('[data-close]').addEventListener('click', closeAda);
  dlg.addEventListener('click', function (e) { if (e.target === dlg) closeAda(); }); /* clic en el fondo */
  // El envío del formulario lo gestiona digizen-ab.js; no emitir PII en eventos del navegador.
  setChannel('correo');

  if (checkoutDlg) {
    var checkoutForm = checkoutDlg.querySelector('[data-checkout-consent]');
    var closeCheckout = function () { checkoutDlg.close(); };
    checkoutDlg.querySelector('[data-checkout-close]').addEventListener('click', closeCheckout);
    checkoutDlg.addEventListener('click', function (e) { if (e.target === checkoutDlg) closeCheckout(); });
    checkoutForm.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!checkoutForm.checkValidity()) { checkoutForm.reportValidity(); return; }
      window.dispatchEvent(new CustomEvent('digizen:checkout', { detail: { plan: checkoutPlan } }));
      closeCheckout();
    });
  }

  function saveCookies(v) {
    try { localStorage.setItem(COOKIE_KEY, JSON.stringify(v)); } catch (_) {}
    window.dispatchEvent(new CustomEvent('digizen:cookie-preferences', { detail: { action: 'accepted', categories: v } }));
    var banner = document.getElementById('cookie-banner'); if (banner) banner.remove();
    var settings = document.getElementById('cookie-settings'); if (settings && settings.open) settings.close();
  }
  function openCookieSettings() {
    var settings = document.getElementById('cookie-settings'); if (!settings) return;
    var saved = {}; try { saved = JSON.parse(localStorage.getItem(COOKIE_KEY) || '{}'); } catch (_) {}
    settings.querySelector('[name=performance]').checked = !!saved.performance;
    settings.querySelector('[name=marketing]').checked = !!saved.marketing;
    settings.showModal();
  }
  function installCookieControls() {
    document.querySelectorAll('[data-cookie-settings]').forEach(function (b) { b.addEventListener('click', openCookieSettings); });
    var settings = document.getElementById('cookie-settings');
    if (settings) {
      settings.querySelector('[data-cookie-close]').addEventListener('click', function () { settings.close(); });
      settings.querySelector('[data-cookie-reset]').addEventListener('click', function () { var prior = {}; try { prior = JSON.parse(localStorage.getItem(COOKIE_KEY) || '{}'); localStorage.removeItem(COOKIE_KEY); } catch (_) {} if (typeof prior.performance === 'boolean' && typeof prior.marketing === 'boolean') window.dispatchEvent(new CustomEvent('digizen:cookie-preferences', { detail: { action: 'revoked', categories: prior } })); window.location.reload(); });
      settings.querySelector('form').addEventListener('submit', function (e) { e.preventDefault(); saveCookies({ performance: settings.querySelector('[name=performance]').checked, marketing: settings.querySelector('[name=marketing]').checked }); });
    }
    try { if (localStorage.getItem(COOKIE_KEY)) return; } catch (_) {}
    var banner = document.createElement('section'); banner.id = 'cookie-banner'; banner.className = 'cookie-banner'; banner.setAttribute('role', 'region');
    banner.innerHTML = "<h2 id='cookie-title'>Tus preferencias de cookies</h2><p>Usamos cookies necesarias para que el sitio funcione. Puedes decidir si permites medición y marketing. Consulta la <a class='lnk' href='https://digizen.gnius.club/politica-de-cookies-digizen.html' target='_blank' rel='noopener'>política de cookies</a>.</p><div class='cookie-actions'><button type='button' class='btn alt' data-cookie-reject>Rechazar opcionales</button><button type='button' class='btn alt' data-cookie-config>Configurar</button><button type='button' class='btn' data-cookie-accept>Aceptar todas</button></div>";
    document.body.appendChild(banner);
    banner.querySelector('[data-cookie-reject]').addEventListener('click', function () { saveCookies({ performance: false, marketing: false }); });
    banner.querySelector('[data-cookie-accept]').addEventListener('click', function () { saveCookies({ performance: true, marketing: true }); });
    banner.querySelector('[data-cookie-config]').addEventListener('click', openCookieSettings);
  }
  var cookieDialog = document.createElement('dialog');
  cookieDialog.id = 'cookie-settings'; cookieDialog.className = 'ada-dialog legal-dialog'; cookieDialog.setAttribute('aria-labelledby', 'cookie-settings-title');
  cookieDialog.innerHTML = "<form class='legal-form'><div class='dlg-head'><h2 id='cookie-settings-title' class='pf w7 t-head bw'>Configura tus preferencias</h2><button type='button' class='close' data-cookie-close aria-label='Cerrar'>×</button></div><p class='in w5 t-small note'>Elige qué tipos de cookies opcionales permites.</p><label class='consent cookie-choice'><input type='checkbox' checked disabled><strong>Necesarias</strong><span>Siempre activas para seguridad y guardar tu elección.</span></label><label class='consent cookie-choice'><input name='performance' type='checkbox'><strong>Rendimiento y medición</strong><span>Analítica y pruebas de mejora del sitio.</span></label><label class='consent cookie-choice'><input name='marketing' type='checkbox'><strong>Marketing</strong><span>Publicidad y audiencias personalizadas.</span></label><button type='submit' class='btn alt'>Guardar preferencias</button><button type='button' class='legal-link' data-cookie-reset>Restablecer elección</button></form>";
  document.body.appendChild(cookieDialog);
  installCookieControls();
})();
