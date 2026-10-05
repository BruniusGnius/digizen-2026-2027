/* Digizen · resorte con amortiguación crítica (apple-design §3–§5).
   Sin rebote; el tiempo de asentamiento sale de `response`, no de una duración fija.
   Interrumpible: .to(nuevoDestino) parte del valor y la velocidad actuales (sin saltos),
   y acepta una velocidad inicial para continuar un gesto que se suelta (traspaso de velocidad). */
(function () {
  'use strict';
  var DZ = window.DZ;

  DZ.spring = function (o) {
    var w = 2 * Math.PI / (o.response || 0.4);   /* frecuencia natural */
    var eps = o.eps || 0.001;                     /* umbral de reposo, en las unidades del valor */
    var x0, v0, target, t0, raf = null;
    function state(t) {                           /* solución analítica del resorte crítico */
      var d = x0 - target, e = Math.exp(-w * t);
      return [target + (d + (v0 + w * d) * t) * e, (v0 - (v0 + w * d) * w * t) * e];
    }
    function tick(now) {
      var s = state((now - t0) / 1000);
      if (Math.abs(s[0] - target) < eps && Math.abs(s[1]) < eps * 10) {
        raf = null; o.onUpdate(target); if (o.onRest) o.onRest(); return;
      }
      o.onUpdate(s[0]); raf = requestAnimationFrame(tick);
    }
    function start(from, vel, to) {
      x0 = from; v0 = vel || 0; target = to; t0 = performance.now();
      if (!raf) raf = requestAnimationFrame(tick);
    }
    var api = {
      value: function () { return t0 == null ? [o.from, 0] : state((performance.now() - t0) / 1000); },
      to: function (to, vel) { var s = api.value(); start(s[0], vel != null ? vel : s[1], to); return api; },
      stop: function () { if (raf) cancelAnimationFrame(raf); raf = null; },
      running: function () { return !!raf; }
    };
    start(o.from, o.velocity, o.to);
    return api;
  };
})();
