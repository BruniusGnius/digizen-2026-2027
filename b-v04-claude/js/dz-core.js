/* Digizen · núcleo del recorrido.
   Estado compartido, lectura del DOM (pines y paradas con data-*), posiciones del recorrido,
   parada activa y saltos (data-goto). La lógica es la del wireframe aprobado; solo cambia
   la fuente de datos: aquí se leen los atributos del HTML en vez de un JSON incrustado.
   Scripts clásicos con `defer` (no módulos ES) para que la página funcione también abierta
   directamente desde el disco. */
(function () {
  'use strict';

  var DZ = window.DZ = {};
  var each = function (list, fn) { Array.prototype.forEach.call(list, fn); };
  DZ.each = each;

  /* Configuración por página (pruebas de scroll, 2026-09-30). Los valores por defecto son los del wireframe aprobado:
     stepFade/closeFade/msgFade = en cuánto de la parada aparece cada línea; minUnit = recorrido mínimo por encuadre (px);
     touchMomentum = limitar la inercia del dedo; flow = sin scroll animado (solo los videos con scrub). */
  DZ.cfg = Object.assign({ stepFade: 0.05, closeFade: 0.10, msgFade: 0.08, minUnit: 0, touchMomentum: false, flow: false }, window.DZ_CFG || {});
  DZ.unit = function () { return Math.max(window.innerHeight, DZ.cfg.minUnit || 0); }; /* 1 E en px */
  DZ.hasGsap = typeof window.gsap !== 'undefined' && typeof window.ScrollTrigger !== 'undefined';
  DZ.reduce = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  /* movimiento reducido (o sin GSAP) → modo reducido del wireframe: flujo normal con fundidos */
  /* B5 (apple-design §10): si el usuario agrandó el texto del navegador, las paradas (un encuadre fijo)
     podrían no caber; entonces la página se lee en el modo de flujo, sin pines. Para el resto, nada cambia. */
  DZ.bigText = (parseFloat(getComputedStyle(document.documentElement).fontSize) || 16) > 17;
  DZ.mode = (DZ.hasGsap && !DZ.reduce && !DZ.bigText && !DZ.cfg.flow) ? 'full' : 'flow';
  DZ.isD = window.innerWidth >= 860;
  /* conexión lenta o ahorro de datos: las secuencias se quedan en su cuadro fijo */
  var cn = navigator.connection || {};
  DZ.lite = !!(cn.saveData || /(^|-)2g|3g/.test(cn.effectiveType || ''));

  DZ.PINS = []; DZ.STOPS = []; DZ.POS = [];
  DZ.hooks = { positions: [], frame: [] };

  // ---------- lectura del DOM ----------
  each(document.querySelectorAll('[data-pin]'), function (sec) {
    var pin = { id: sec.id, type: sec.getAttribute('data-type'), tramo: +(sec.getAttribute('data-tramo') || 0), stops: [], el: sec };
    DZ.PINS.push(pin);
    if (pin.type === 'flow') {
      DZ.STOPS.push({ id: pin.id, el: sec, pin: pin, s: { id: pin.id, kind: 'flow', bp: 'all' }, flow: true });
      return;
    }
    each(sec.querySelectorAll('.stop'), function (el) {
      var s = {
        id: el.getAttribute('data-id'),
        kind: el.getAttribute('data-kind'),
        E: parseFloat(el.getAttribute('data-e')),
        night: el.getAttribute('data-night') === '1',
        bp: el.getAttribute('data-bp') || 'all'
      };
      pin.stops.push(s);
      DZ.STOPS.push({ id: s.id, el: el, pin: pin, s: s });
    });
  });

  DZ.rec = function (s) { for (var i = 0; i < DZ.STOPS.length; i++) { if (DZ.STOPS[i].s === s) return DZ.STOPS[i]; } };
  DZ.visible = function (s) { return !s.bp || s.bp === 'all' || (DZ.isD ? s.bp === 'd' : s.bp === 'm'); };

  // ---------- recorrido: posiciones ----------
  DZ.maxScroll = function () {
    return Math.max(1, (DZ.mode === 'full') ? ScrollTrigger.maxScroll(window) : (document.documentElement.scrollHeight - window.innerHeight));
  };
  function emitPositions() { DZ.hooks.positions.forEach(function (fn) { fn(); }); onScroll(); }

  DZ.computePositions = function () {
    var POS = DZ.POS = [];
    var H = window.innerHeight;
    DZ.PINS.forEach(function (pin) {
      var sec = pin.el;
      if (pin.type === 'flow') {
        var top = sec.getBoundingClientRect().top + window.scrollY;
        var x = DZ.STOPS.filter(function (z) { return z.id === pin.id; })[0];
        POS.push({ kind: 'flow', id: pin.id, from: top, to: top + sec.offsetHeight, x: x, pin: pin });
        POS.push({ kind: 'label', id: pin.id, at: top, x: x, pin: pin });
        return;
      }
      var st = ScrollTrigger.getById(pin.id); if (!st || !sec._wf) return;
      var w = sec._wf, len = st.end - st.start, t = 0;
      if (st.start > 0) POS.push({ kind: 'transit', from: Math.max(0, st.start - H), to: st.start, pin: pin });
      w.vis.forEach(function (x) {
        POS.push({ kind: x.s.kind, night: x.s.night, id: x.s.id, from: st.start + t / w.total * len, to: st.start + (t + x.s.E) / w.total * len, x: x, pin: pin });
        t += x.s.E;
      });
      w.labels.forEach(function (l) { POS.push({ kind: 'label', id: l[0].split(' ')[0], at: st.start + l[1] / w.total * len, x: l[2], pin: pin }); });
    });
    emitPositions();
  };

  DZ.computeFlowPositions = function () {
    var POS = DZ.POS = [];
    DZ.STOPS.forEach(function (x) {
      if (!x.flow && !DZ.visible(x.s)) return;
      var el = x.el; if (!el.offsetHeight) return;
      var top = el.getBoundingClientRect().top + window.scrollY;
      POS.push({ kind: x.flow ? 'flow' : x.s.kind, night: x.s.night, id: x.id, from: top, to: top + el.offsetHeight, x: x, pin: x.pin });
      POS.push({ kind: 'label', id: x.id, at: top, x: x, pin: x.pin });
    });
    emitPositions();
  };

  // ---------- saltos ----------
  DZ.scrollToY = function (y) {
    if (DZ.mode === 'full' && window.ScrollToPlugin) gsap.to(window, { scrollTo: { y: y, autoKill: true }, duration: 0.9, ease: 'power2.inOut' });
    else window.scrollTo({ top: y, behavior: DZ.reduce ? 'auto' : 'smooth' });
  };
  DZ.goTo = function (id) {
    var POS = DZ.POS;
    for (var i = 0; i < POS.length; i++) { if (POS[i].kind === 'label' && POS[i].id === id) { DZ.scrollToY(POS[i].at); return true; } }
    for (var j = 0; j < POS.length; j++) { if (POS[j].id === id && POS[j].from != null) { DZ.scrollToY(POS[j].from); return true; } }
    return false;
  };
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-goto]');
    if (a && DZ.goTo(a.getAttribute('data-goto'))) e.preventDefault();
  });

  // ---------- parada activa (solo ella recibe clics, como en el wireframe) ----------
  var current = null, ticking = false;
  function setActive(hit) {
    var key = !hit ? null : (hit.kind === 'transit' ? 't:' + hit.pin.id : hit.id);
    if (current === key) return; current = key;
    DZ.STOPS.forEach(function (x) { x.el.classList.remove('is-active'); });
    if (hit && hit.x && hit.x.el) hit.x.el.classList.add('is-active');
  }
  function onScroll() {
    if (ticking) return; ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      var y = window.scrollY, probe = y + 1, hit = null, POS = DZ.POS;
      for (var i = 0; i < POS.length; i++) {
        var p = POS[i]; if (p.kind === 'label') continue;
        if (probe >= p.from && probe < p.to) { if (!hit || hit.kind === 'transit') hit = p; }
      }
      setActive(hit);
      DZ.hooks.frame.forEach(function (fn) { fn(y, hit); });
    });
  }
  DZ.onScroll = onScroll;
  window.addEventListener('scroll', onScroll, { passive: true });
})();
