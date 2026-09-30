/* Digizen · menú de hamburguesa (pedido del usuario, 2026-09-29: en todos los dispositivos).
   El panel entra desde la derecha, del lado del botón, y sale por el mismo lado (apple-design §7).
   Respuesta inmediata al tocar; transición interrumpible (si se vuelve a tocar a medio camino, revierte
   desde donde está). Foco atrapado dentro del panel; Esc, la X o tocar fuera lo cierran y el foco
   vuelve al botón. No cambia el scroll: los saltos usan las mismas posiciones del recorrido. */
(function () {
  'use strict';
  var DZ = window.DZ;
  var btn = document.querySelector('.menu-btn'), menu = document.getElementById('menu');
  if (!btn || !menu) return;
  var panel = menu.querySelector('.menu-panel'), backdrop = menu.querySelector('.menu-backdrop');
  var items = Array.prototype.slice.call(menu.querySelectorAll('.menu-item[data-tramo]'));
  var hideTimer = null, open = false;

  function focusables() {
    return Array.prototype.slice.call(panel.querySelectorAll('button, a[href], input, [tabindex]:not([tabindex="-1"])'))
      .filter(function (el) { return !el.disabled && el.offsetParent !== null; });
  }
  function markCurrent() {
    var cur = DZ.currentTramo ? DZ.currentTramo() : 0;
    items.forEach(function (it) {
      if (+it.getAttribute('data-tramo') === cur) it.setAttribute('aria-current', 'step'); else it.removeAttribute('aria-current');
    });
  }
  function openMenu() {
    if (open) return; open = true;
    clearTimeout(hideTimer);
    markCurrent();
    menu.hidden = false;
    void menu.offsetWidth;                     /* arranca la transición desde el estado cerrado */
    menu.classList.add('is-open');
    btn.setAttribute('aria-expanded', 'true');
    btn.setAttribute('aria-label', 'Cerrar menú');
    document.documentElement.classList.add('menu-open');
    var f = focusables()[0]; if (f) f.focus({ preventScroll: true });
  }
  function closeMenu(silent) {
    if (!open) return; open = false;
    menu.classList.remove('is-open');
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-label', 'Abrir menú');
    document.documentElement.classList.remove('menu-open');
    clearTimeout(hideTimer);
    hideTimer = setTimeout(function () { if (!open) menu.hidden = true; }, 360);
    if (!silent) btn.focus({ preventScroll: true });
  }
  DZ.closeMenu = closeMenu;

  btn.addEventListener('click', function () { if (open) closeMenu(); else openMenu(); });
  backdrop.addEventListener('click', function () { closeMenu(); });
  /* el fondo no se mueve mientras el menú está abierto (la lista sí puede desplazarse si no cabe) */
  ['wheel', 'touchmove'].forEach(function (ev) {
    backdrop.addEventListener(ev, function (e) { e.preventDefault(); }, { passive: false });
  });
  document.addEventListener('keydown', function (e) {
    if (!open) return;
    if (e.key === 'Escape') { e.preventDefault(); closeMenu(); return; }
    if (e.key === 'Tab') { /* foco atrapado: el botón de cerrar + el contenido del panel */
      var list = [btn].concat(focusables()), i = list.indexOf(document.activeElement);
      if (e.shiftKey && i <= 0) { e.preventDefault(); list[list.length - 1].focus(); }
      else if (!e.shiftKey && i === list.length - 1) { e.preventDefault(); list[0].focus(); }
    }
  });

  /* tramos: se cierra el menú y se viaja al inicio del tramo; FAQ: a su sección */
  items.forEach(function (it) {
    it.addEventListener('click', function () {
      var y = DZ.tramoStart ? DZ.tramoStart(+it.getAttribute('data-tramo')) : null;
      closeMenu(true);
      if (y != null) DZ.scrollToY(y + 1);
    });
  });
  var faq = menu.querySelector('[data-menu-goto]');
  if (faq) faq.addEventListener('click', function () { closeMenu(true); DZ.goTo(faq.getAttribute('data-menu-goto')); });
})();
