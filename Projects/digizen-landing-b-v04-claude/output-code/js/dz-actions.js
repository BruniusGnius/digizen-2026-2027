/* Digizen · acciones de los botones (03-build-plan.md §4.6).
   - «Conversar con ADA primero» abre el diálogo con los datos de la propuesta A
     (nombre, canal Correo / WhatsApp, correo o número). Como en A, todavía no se envía
     a ningún servicio: se emite `digizen:ada-request` para conectarlo después (pendiente).
   - «Inscribir a mi hijo ↗» emite `digizen:checkout`, como en A (destino del pago pendiente).
   - Botones con destino pendiente (data-pending) no hacen nada todavía. */
(function () {
  'use strict';
  var dlg = document.getElementById('ada-dialog');

  // ---------- respuesta inmediata en pointerdown (apple-design §1) ----------
  document.addEventListener('pointerdown', function (e) {
    var b = e.target.closest('.btn'); if (!b) return;
    b.classList.add('is-pressed');
    var up = function () { b.classList.remove('is-pressed'); window.removeEventListener('pointerup', up); window.removeEventListener('pointercancel', up); };
    window.addEventListener('pointerup', up); window.addEventListener('pointercancel', up);
  });

  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-action], [data-pending]'); if (!b) return;
    var act = b.getAttribute('data-action');
    if (act === 'ada' && dlg) { openAda(b); return; }
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

  function openAda(from) {
    opener = from;
    if (typeof dlg.showModal === 'function') dlg.showModal(); else dlg.setAttribute('open', '');
    var first = dlg.querySelector('input'); if (first) first.focus();
  }
  dlg.addEventListener('close', function () { if (opener && opener.focus) opener.focus(); });
  dlg.querySelector('[data-close]').addEventListener('click', function () { dlg.close(); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); }); /* clic en el fondo */
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
