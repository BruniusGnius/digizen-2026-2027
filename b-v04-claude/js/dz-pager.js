/* Digizen · prueba 3: una estación por gesto (pedido del usuario y de su jefe, 2026-09-30).
   Lo que resuelve: con el scroll normal, un gesto se saltaba varias estaciones y el lector no sabía que había texto antes.
   - Cada gesto (rueda, trackpad, dedo o teclado) mueve exactamente una estación, siempre con el mismo movimiento;
     la inercia del gesto se ignora. Cuenta un gesto nuevo cuando el anterior terminó (pausa) o cuando se vuelve a empujar.
   - Las estaciones llegan compuestas: sin animaciones internas.
   - Escenas con video o zoom (desktop): una parada al inicio (primer cuadro) y otra al final; el gesto entre las dos corre la escena.
   - Tarjetas apiladas en el teléfono (08.5m, 11.3m, 11.3bm): cada gesto sube una tarjeta sobre la anterior (pedido del usuario).
   - Otras estaciones más altas que la pantalla: se llega anclado a su inicio, adentro el scroll es fluido y se detiene en su
     final; el gesto siguiente ancla en la estación que sigue.
   - Del FAQ hacia abajo, scroll libre; al volver a subir se detiene en el FAQ y de ahí sigue por estaciones.
   Los saltos del menú, el riel, el logo y los botones también pasan por aquí (DZ.scrollToY). */
(function () {
  'use strict';
  var DZ = window.DZ;

  DZ.pager = function () {
    var pages = [], zones = [], freeFrom = Infinity, busy = false, dragging = false, curKey = null, skipY = null;
    var blocked = function () { return document.documentElement.classList.contains('menu-open') || !!document.querySelector('dialog[open]'); };
    var done = function () { busy = false; };
    var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };

    function nearest(y) {
      var best = null; pages.forEach(function (p) { if (!best || Math.abs(p.y - y) < Math.abs(best.y - y)) best = p; });
      return best;
    }
    function jump(y) { skipY = y; window.scrollTo(0, y); }
    /* tramo fluido (estación más alta que la pantalla) que contiene y */
    function zoneAt(y) { for (var i = 0; i < zones.length; i++) if (y >= zones[i].top - 2 && y <= zones[i].end + 2) return zones[i]; return null; }
    /* dentro del tramo fluido, este gesto se desplaza libre (no ancla): todo menos salir por sus bordes */
    function inside(z, y, dir) { return z && !((dir > 0 && y >= z.end - 2) || (dir < 0 && y <= z.top + 2)); }

    /* las paradas del recorrido, en px; se recalculan con cada refresh (fuentes, carga, cambio de tamaño) */
    function measure() {
      var vh = window.innerHeight, sy = window.scrollY, max = ScrollTrigger.maxScroll(window), list = [], zs = [];
      freeFrom = Infinity;
      DZ.STOPS.forEach(function (x) {
        if (freeFrom !== Infinity) return;
        var top = Math.round(x.el.getBoundingClientRect().top + sy);
        if (x.flow) { freeFrom = Math.min(top, max); list.push({ y: freeFrom, key: x.id }); return; }  /* si el FAQ y el pie caben en una pantalla, la última parada es el final de la página */
        if (!DZ.visible(x.s) || !x.el.offsetHeight) return;
        if (x._st && x._steps) {   /* tarjetas apiladas (teléfono): una parada por tarjeta */
          var len = x._st.end - x._st.start;
          for (var k = 0; k <= x._steps; k++) list.push({ y: Math.round(x._st.start + len * k / x._steps), key: x.id + (k ? '·' + k : '') });
          return;
        }
        if (x._st) {   /* escena fijada: inicio (primer cuadro) y final (la escena ya corrió) */
          list.push({ y: Math.round(x._st.start), key: x.id });
          list.push({ y: Math.round(x._st.end), key: x.id + '·fin', scene: true });
          return;
        }
        var h = x.el.offsetHeight;
        if (h > vh + 8) {   /* más alta que la pantalla: se ancla al inicio y al final; entre los dos, fluido */
          var end = Math.round(top + h - vh);
          list.push({ y: top, key: x.id }); list.push({ y: end, key: x.id + '·fin' });
          zs.push({ top: top, end: end });
          return;
        }
        list.push({ y: top, key: x.id });
      });
      pages = list.filter(function (p, i) { return p.y <= max + 1 && (i === 0 || p.y - list[i - 1].y > 3); });
      zones = zs;
      var y = window.scrollY;
      if (busy || dragging || y > freeFrom + 2 || zoneAt(y)) return;
      var p = null; pages.forEach(function (q) { if (q.key === curKey) p = q; });
      p = p || nearest(y);
      if (p) { curKey = p.key; if (Math.abs(p.y - y) > 1) jump(p.y); }  /* sigue en la misma estación */
    }

    function go(i, far) {
      var p = pages[i]; if (!p) return;
      var y0 = window.scrollY, dist = Math.abs(p.y - y0), vh = window.innerHeight;
      curKey = p.key;
      if (dist < 2) return;
      var from = function (q) { return q && Math.abs(q.y - y0) < 4; };
      var scene = !far && ((p.scene && from(pages[i - 1])) || (pages[i + 1] && pages[i + 1].scene && from(pages[i + 1])));
      busy = true;
      gsap.to(window, { scrollTo: { y: p.y, autoKill: false }, overwrite: true,
        duration: scene ? 1.6 : Math.min(1.1, 0.6 + 0.05 * dist / vh),   /* una estación ≈ 0.65 s; la escena, 1.6 s */
        ease: scene ? 'power1.inOut' : 'power2.inOut', onComplete: done });
    }

    function step(dir) {
      if (busy || !pages.length) return;
      var y = window.scrollY, i;
      if (dir > 0) { for (i = 0; i < pages.length; i++) if (pages[i].y > y + 3) return go(i); }
      else { for (i = pages.length - 1; i >= 0; i--) if (pages[i].y < y - 3) return go(i); }
    }

    /* ¿este gesto va por estaciones? (en el FAQ o más abajo, bajar es libre) */
    function paging(dir) { var y = window.scrollY; return !(y > freeFrom + 2 || (y >= freeFrom - 2 && dir > 0)); }

    // ---------- rueda y trackpad ----------
    var wLast = 0, wAcc = 0, wDone = false, hist = [];
    var avg = function (a) { var s = 0; a.forEach(function (v) { s += v; }); return a.length ? s / a.length : 0; };
    window.addEventListener('wheel', function (e) {
      if (blocked() || e.ctrlKey) return;   /* ctrl + rueda = zoom del navegador */
      var d = e.deltaY * (e.deltaMode === 1 ? 33 : (e.deltaMode === 2 ? window.innerHeight : 1));
      if (Math.abs(e.deltaX) > Math.abs(d)) return;
      var y = window.scrollY, now = performance.now(), same = now - wLast <= 200;
      if (y > freeFrom + 2) {   /* zona libre; si el gesto la cruzaría hacia arriba, se detiene en el FAQ */
        if (d < 0 && y + d < freeFrom) { e.preventDefault(); jump(freeFrom); wDone = true; wLast = now; }
        return;
      }
      if (y >= freeFrom - 2 && d > 0 && !(wDone && same)) return;
      var z = zoneAt(y);
      if (inside(z, y, d > 0 ? 1 : -1)) {   /* tramo fluido: se desplaza libre y se detiene en su borde */
        if (busy || (wDone && same)) { e.preventDefault(); wLast = now; return; }   /* la inercia del gesto que llegó aquí no desplaza */
        if (!same) { wAcc = 0; wDone = false; hist = []; }
        wLast = now;
        if (y + d > z.end || y + d < z.top) { e.preventDefault(); jump(d > 0 ? z.end : z.top); wDone = true; }
        return;
      }
      e.preventDefault();
      if (!same) { wAcc = 0; wDone = false; hist = []; }   /* pausa = gesto nuevo */
      wLast = now; hist.push(Math.abs(d)); if (hist.length > 24) hist.shift();
      if (wDone) {   /* este gesto ya movió una estación: solo cuenta un empujón nuevo, y no mientras se mueve */
        if (busy || hist.length < 10 || Math.abs(d) < 15 || avg(hist.slice(-3)) < avg(hist.slice(-10, -3)) * 1.8) return;
        wAcc = 0; wDone = false; hist = hist.slice(-3);
      }
      wAcc += d;
      if (!busy && Math.abs(wAcc) >= 24) { wDone = true; step(wAcc > 0 ? 1 : -1); }
    }, { passive: false });

    // ---------- dedo ----------
    /* por estaciones: un deslizamiento = una estación. En un tramo fluido el desplazamiento lo hace la página
       (sigue al dedo 1:1 y, al soltar, se desliza con su impulso), siempre dentro del tramo: no se sale por inercia. */
    var ty = null, tMode = null, tDone = false, tS0 = 0, tZone = null, samples = [], glide = null;
    document.addEventListener('touchstart', function (e) {
      if (glide) { glide.kill(); glide = null; busy = false; }   /* tocar detiene el deslizamiento */
      ty = e.touches.length === 1 ? e.touches[0].clientY : null; tMode = null; tDone = false;
      tS0 = window.scrollY; samples = ty == null ? [] : [[performance.now(), ty]];
    }, { passive: true });
    document.addEventListener('touchmove', function (e) {
      if (ty == null || blocked()) return;
      var cy = e.touches[0].clientY, dy = ty - cy;   /* > 0: el dedo sube = avanzar */
      if (tMode === null) {   /* se decide en el primer movimiento */
        var y = window.scrollY, dir = dy < 0 ? -1 : 1, z = zoneAt(y);
        if (!busy && inside(z, y, dir)) { tMode = 'drag'; tZone = z; }
        else tMode = paging(dir) ? 'page' : 'native';
      }
      if (tMode === 'native') return;
      if (e.cancelable) e.preventDefault();
      if (tMode === 'drag') {
        dragging = true; window.scrollTo(0, clamp(tS0 + dy, tZone.top, tZone.end));
        samples.push([performance.now(), cy]); if (samples.length > 6) samples.shift();
        return;
      }
      if (!tDone && !busy && Math.abs(dy) > 28) { tDone = true; step(dy > 0 ? 1 : -1); }
    }, { passive: false });
    document.addEventListener('touchend', function () {
      if (tMode === 'drag') {
        dragging = false;
        var a = samples[0], b = samples[samples.length - 1], dt = b[0] - a[0];
        var v = (dt > 0 && performance.now() - b[0] < 80) ? (a[1] - b[1]) / dt : 0;   /* px/ms; > 0 = hacia abajo */
        var y = window.scrollY, target = clamp(y + v * 400, tZone.top, tZone.end);
        if (Math.abs(target - y) > 2) {
          busy = true;
          glide = gsap.to(window, { scrollTo: { y: target, autoKill: false }, overwrite: true, ease: 'power3.out',
            duration: Math.min(0.9, 0.3 + Math.abs(v) * 0.25), onComplete: function () { busy = false; glide = null; var q = nearest(window.scrollY); if (q) curKey = q.key; } });
        }
      }
      ty = null; tMode = null;
    }, { passive: true });

    // ---------- teclado ----------
    document.addEventListener('keydown', function (e) {
      if (e.defaultPrevented || e.altKey || e.ctrlKey || e.metaKey || blocked()) return;
      var t = e.target, tag = t && t.tagName, k = e.key, dir = 0;
      if (t && (t.isContentEditable || tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT')) return;
      if (k === ' ' && (tag === 'BUTTON' || tag === 'A' || tag === 'SUMMARY')) return;   /* espacio sobre un botón = tocarlo */
      if (k === 'ArrowDown' || k === 'PageDown' || (k === ' ' && !e.shiftKey)) dir = 1;
      else if (k === 'ArrowUp' || k === 'PageUp' || (k === ' ' && e.shiftKey)) dir = -1;
      else if (k === 'Home') { e.preventDefault(); go(0, true); return; }
      if (!dir || !paging(dir) || inside(zoneAt(window.scrollY), window.scrollY, dir)) return;   /* en un tramo fluido, las teclas desplazan normal */
      e.preventDefault();
      if (!e.repeat) step(dir);
    });

    // ---------- scroll que no viene de un gesto (barra, foco, buscar en la página, teclas en un tramo fluido) ----------
    var lastY = window.scrollY, alignT = null;
    function align() {
      var y = window.scrollY;
      if (busy || dragging || y > freeFrom + 2 || zoneAt(y)) return;
      var p = nearest(y); if (!p) return;
      if (Math.abs(p.y - y) > 2) go(pages.indexOf(p)); else curKey = p.key;
    }
    window.addEventListener('scroll', function () {
      var y = window.scrollY;
      if (skipY !== null && Math.abs(y - skipY) < 2) { skipY = null; lastY = y; return; }
      if (!busy && !dragging) {
        var z = zoneAt(lastY);
        if (lastY > freeFrom + 2 && y < freeFrom - 2) jump(freeFrom);                         /* subía desde el FAQ: se detiene ahí */
        else if (z && (y > z.end + 2 || y < z.top - 2)) jump(y > z.end ? z.end : z.top);    /* salía de un tramo fluido: se detiene en su borde */
        else if (y <= freeFrom + 2) { clearTimeout(alignT); alignT = setTimeout(align, 180); }
      }
      lastY = window.scrollY;
    }, { passive: true });

    /* menú, riel, logo y botones: a la estación que empieza en y (o, del FAQ hacia abajo, directo) */
    DZ.scrollToY = function (y) {
      if (y > freeFrom + 2) { busy = true; gsap.to(window, { scrollTo: { y: y, autoKill: false }, overwrite: true, duration: 0.9, ease: 'power2.inOut', onComplete: done }); return; }
      var best = 0; pages.forEach(function (p, i) { if (p.y <= y + 4) best = i; });
      go(best, true);
    };
    DZ.pagerState = function () { return { pages: pages, zones: zones, freeFrom: freeFrom, busy: busy, curKey: curKey }; };  /* para revisar */

    ScrollTrigger.addEventListener('refresh', measure);
    measure();
  };
})();
