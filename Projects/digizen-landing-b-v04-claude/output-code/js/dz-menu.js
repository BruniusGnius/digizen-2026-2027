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

  // ---------- B2: cerrar deslizando con el dedo (apple-design §2, §5, §6) ----------
  /* El panel sigue al dedo 1:1 desde el punto donde se agarró. Hacia la derecha cierra; hacia la izquierda
     (más allá de abierto) ofrece resistencia progresiva. Al soltar, el resorte continúa con la velocidad del
     gesto y el destino sale de proyectar hacia dónde iba, no del punto más cercano. Solo tacto y lápiz. */
  var drag = null, settle = null;
  function place(x, W) {
    panel.style.transform = 'translateX(' + x + 'px)';
    backdrop.style.opacity = String(Math.max(0, Math.min(1, 1 - Math.max(0, x) / W)));
  }
  function rubber(d, W) { return (1 - 1 / (d * 0.55 / W + 1)) * W * 0.25; } /* resistencia creciente, tope suave */
  function release() {
    panel.style.transform = ''; panel.style.transition = ''; backdrop.style.transition = ''; backdrop.style.opacity = '';
  }
  panel.addEventListener('pointerdown', function (e) {
    if (!open || e.pointerType === 'mouse') return;
    if (settle) { settle.stop(); settle = null; }
    var now = performance.now();
    drag = { id: e.pointerId, x0: e.clientX, y0: e.clientY, x: 0, active: false, lastX: e.clientX, lastT: now, v: 0 };
  });
  window.addEventListener('pointermove', function (e) {
    if (!drag || e.pointerId !== drag.id) return;
    var dx = e.clientX - drag.x0, dy = e.clientY - drag.y0;
    if (!drag.active) {
      if (Math.abs(dx) < 8 && Math.abs(dy) < 8) return;
      if (Math.abs(dy) > Math.abs(dx)) { drag = null; return; }   /* gesto vertical: es el scroll de la lista */
      drag.active = true;
      panel.style.transition = 'none'; backdrop.style.transition = 'none';
    }
    var now = performance.now(), W = panel.offsetWidth;
    drag.v = (e.clientX - drag.lastX) / Math.max(1, now - drag.lastT) * 1000;   /* px/s */
    drag.lastX = e.clientX; drag.lastT = now;
    drag.x = dx > 0 ? dx : -rubber(-dx, W);
    place(drag.x, W);
  });
  function end(e) {
    if (!drag || (e && e.pointerId !== drag.id)) return;
    var d = drag; drag = null;
    if (!d.active) return;
    /* un arrastre no es un toque: se anula el clic que viene después */
    var block = function (ev) { ev.stopPropagation(); ev.preventDefault(); };
    window.addEventListener('click', block, true);
    setTimeout(function () { window.removeEventListener('click', block, true); }, 60);
    var W = panel.offsetWidth, projected = d.x + d.v * 0.2;   /* proyección de ~200 ms del gesto */
    var shut = projected > W * 0.5;
    settle = DZ.spring({ from: d.x, to: shut ? W : 0, velocity: d.v, response: 0.34, eps: 0.5,
      onUpdate: function (x) { place(x, W); },
      onRest: function () {
        settle = null;
        if (shut) { closeMenu(); menu.hidden = true; }
        release();
      } });
  }
  window.addEventListener('pointerup', end);
  window.addEventListener('pointercancel', end);
})();
