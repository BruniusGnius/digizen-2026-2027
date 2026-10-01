/* Digizen · acciones de los botones (03-build-plan.md §4.6).
   - «Conversar con ADA primero» abre el diálogo con los datos de la propuesta A
     (nombre, canal Correo / WhatsApp, correo o número). Como en A, todavía no se envía
     a ningún servicio: se emite `digizen:ada-request` para conectarlo después (pendiente).
   - «Inscribir a mi hijo ↗» emite `digizen:checkout`, como en A (destino del pago pendiente).
     En el menú, ese botón lleva a las tarjetas de precio para elegir la forma de pago (pedido del usuario, 2026-09-30).
   - Botones con destino pendiente (data-pending) no hacen nada todavía. */
(function () {
  'use strict';
  var DZ = window.DZ;
  var dlg = document.getElementById('ada-dialog');

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
    if (act === 'pricing') { DZ.goTo(DZ.isD ? '11.4' : '11.5m'); return; }   /* menú: a las tarjetas de precio (desktop 11.4, móvil 11.5m) */
    if (act === 'checkout') { /* como en A: el plan viaja en el evento (contado / diferido); sin plan = CTA general */
      window.dispatchEvent(new CustomEvent('digizen:checkout', { detail: { plan: b.getAttribute('data-plan') || null } })); return; }
    if (b.hasAttribute('data-pending')) { e.preventDefault(); if (window.console) console.info('[digizen] destino pendiente:', b.getAttribute('data-pending')); }
  });

  if (!dlg) return;
  var form = dlg.querySelector('form'), contact = dlg.querySelector('[name=contact]');
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
  form.addEventListener('submit', function (e) {
    e.preventDefault(); /* como en A: sin envío todavía (destino pendiente) */
    if (!form.reportValidity()) return;
    window.dispatchEvent(new CustomEvent('digizen:ada-request', { detail: {
      name: form.elements.name.value.trim(),
      channel: dlg.getAttribute('data-channel-active') || 'correo',
      contact: contact.value.trim()
    } }));
  });
  setChannel('correo');
})();
