/* Digizen · motor de pines.
   Es buildPin del wireframe aprobado, sin cambios de lógica ni de tiempos:
   entradas, puentes, pasos, mazo, diálogo, sellos, salidas, etiquetas de snap y scrub 0.4. */
(function () {
  'use strict';
  var DZ = window.DZ;

  DZ.buildPin = function (sec, vis, pin) {
    var total = vis.reduce(function (a, x) { return a + x.s.E; }, 0);
    var night = sec.querySelector('.night');
    vis.forEach(function (x) { gsap.set(x.el, { opacity: 0 }); });
    gsap.set(night, { opacity: 0 });
    var tl = gsap.timeline({ defaults: { ease: 'none' }, scrollTrigger: {
      id: pin.id, trigger: sec, pin: true, start: 'top top',
      end: function () { return '+=' + (total * window.innerHeight); },
      scrub: 0.4, invalidateOnRefresh: true,
      snap: { snapTo: 'labels', duration: { min: 0.2, max: 0.5 }, delay: 0.08, ease: 'power1.inOut' }
    } });
    tl.to({}, { duration: total }, 0);
    var labels = [], t = 0;
    vis.forEach(function (x, i) {
      var s = x.s, el = x.el, span = s.E, first = i === 0, last = i === vis.length - 1;
      var c = el.querySelector(':scope > .c') || el;
      var prevN = i > 0 && vis[i - 1].s.night, nextN = !last && vis[i + 1].s.night;
      var dIn = span * (s.kind === 'golpe' ? 0.10 : 0.15);
      if (first) { gsap.set(el, { opacity: 1 }); if (s.night) gsap.set(night, { opacity: 1 }); }
      else {
        tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: dIn }, t);
        if (s.kind === 'read' || s.kind === 'cta' || s.kind === 'dialog' || s.kind === 'deck') tl.fromTo(c, { y: 24 }, { y: 0, duration: dIn, ease: 'power2.out' }, t);
        if (s.kind === 'lead' || s.kind === 'two' || s.kind === 'reveal') { var ld = el.querySelector('[data-beat=lead]') || c; tl.fromTo(ld, { x: -16 }, { x: 0, duration: dIn, ease: 'power2.out' }, t); }
        if (s.night && !prevN) tl.to(night, { opacity: 1, duration: span * 0.10 }, t);
      }
      var holdStart = t + (first ? 0 : dIn), holdEnd = t + span * 0.85, lt;
      if (s.kind === 'two') {
        var cl = el.querySelector('[data-beat=close]');
        gsap.set(cl, { opacity: 0 });
        tl.to(cl, { opacity: 1, duration: span * 0.10 }, t + span * 0.30);
        var la = first ? t : t + span * 0.20;
        tl.addLabel(s.id + '·a', la); labels.push([s.id + ' (puente)', la, x]);
        holdStart = t + span * 0.40;
      }
      if (el.querySelector('[data-seq]')) DZ.buildSeq(el, tl, t, span);
      if (s.kind === 'reveal') { /* revelación en tiempos: puente → se desvanece → paso 1 → paso 2 */
        var rl = el.querySelector('[data-beat=lead]'), steps = el.querySelectorAll('[data-step]');
        if (rl) { /* con puente (01.3) */
          DZ.each(steps, function (st) { gsap.set(st, { opacity: 0 }); });
          var la1 = first ? t : t + span * 0.18;
          tl.addLabel(s.id + '·a', la1); labels.push([s.id + ' (puente)', la1, x]);
          tl.to(rl, { opacity: 0, duration: span * 0.08 }, t + span * 0.26);
          if (steps[0]) { tl.to(steps[0], { opacity: 1, duration: span * 0.05 }, t + span * 0.36); tl.addLabel(s.id + '·b', t + span * 0.46); labels.push([s.id + ' (paso 1)', t + span * 0.46, x]); }
          if (steps[1]) { tl.to(steps[1], { opacity: 1, duration: span * 0.05 }, t + span * 0.54); }
          holdStart = t + span * 0.60;
        } else { /* golpe en dos alturas sin puente (05.4) */
          var lb = first ? t : t + span * 0.2, lastAt = 0;
          tl.addLabel(s.id + '·a', lb); labels.push([s.id + ' (paso 1)', lb, x]);
          var b0 = steps.length > 3 ? 0.30 : 0.36, gp = steps.length > 3 ? 0.14 : 0.18;
          for (var k = 1; k < steps.length; k++) {
            var at = t + span * (b0 + (k - 1) * gp); lastAt = at;
            gsap.set(steps[k], { opacity: 0 }); tl.to(steps[k], { opacity: 1, duration: span * 0.05 }, at);
            var ar = steps[k].querySelector('.evo-arrow'); /* la flecha se dibuja */
            if (ar) tl.fromTo(ar, DZ.isD ? { scaleX: 0 } : { scaleY: 0 }, DZ.isD ? { scaleX: 1, duration: span * 0.08, transformOrigin: 'left center' } : { scaleY: 1, duration: span * 0.08, transformOrigin: 'center top' }, at);
            if (k < steps.length - 1) { tl.addLabel(s.id + '·p' + (k + 1), at + span * 0.08); labels.push([s.id + ' (paso ' + (k + 1) + ')', at + span * 0.08, x]); }
          }
          holdStart = lastAt ? lastAt + span * 0.09 : t + span * 0.45;
        }
      }
      if (s.kind === 'deck') { /* móvil < 600: cada tarjeta sube y se apila sobre la anterior; tablet: aparece debajo */
        var cards = el.querySelectorAll('.entries.deck > .card'), small = window.matchMedia('(max-width:599px)');
        var ld0 = first ? t : t + span * 0.18, lastD = 0;
        tl.addLabel(s.id + '·1', ld0); labels.push([s.id + ' · tarjeta 1', ld0, x]);
        for (var q = 1; q < cards.length; q++) {
          var atd = t + span * (0.30 + (q - 1) * 0.24); lastD = atd;
          tl.fromTo(cards[q], { opacity: 0, y: function () { return small.matches ? window.innerHeight * 0.6 : 24; } },
            { opacity: 1, y: 0, duration: span * 0.14, ease: 'power2.out', immediateRender: true }, atd);
          if (q < cards.length - 1) { tl.addLabel(s.id + '·' + (q + 1), atd + span * 0.16); labels.push([s.id + ' · tarjeta ' + (q + 1), atd + span * 0.16, x]); }
        }
        holdStart = lastD ? lastD + span * 0.16 : holdStart;
      }
      if (s.kind === 'dialog') {
        var msgs = el.querySelectorAll('.msg-row'); if (!msgs.length) msgs = el.querySelectorAll('.msg'); /* el avatar entra con su burbuja */
        DZ.each(msgs, function (m, k) {
          var at = t + span * (0.12 + k * 0.18);
          tl.fromTo(m, { opacity: 0, x: (m.classList.contains('hijo') ? 16 : -16) }, { opacity: 1, x: 0, duration: span * 0.08, ease: 'power2.out' }, at);
          tl.addLabel(s.id + '·' + (k + 1), at + span * 0.09); labels.push([s.id + ' · mensaje ' + (k + 1), at + span * 0.09, x]);
        });
      }
      if (s.kind === 'seal') { /* zoom con scroll; data-zoom = escala inicial (por defecto 1.06) */
        var img = el.querySelector('img'), fig = el.querySelector('[data-zoom]');
        var z = fig ? parseFloat(fig.getAttribute('data-zoom')) : 1.06;
        var zin = fig && fig.getAttribute('data-zoom-dir') === 'in';
        if (img) {
          /* en móvil/tablet con vertical, el punto del zoom puede ser otro (data-origin-m): mismo objeto, otra posición en la imagen */
          var org = fig && ((!DZ.isD && img.hasAttribute('data-v') && fig.getAttribute('data-origin-m')) || fig.getAttribute('data-origin'));
          if (org) gsap.set(img, { transformOrigin: org });
          tl.fromTo(img, { scale: (zin ? 1 : z) }, { scale: (zin ? z : 1), duration: span * 0.7, ease: (z > 1.2 ? (zin ? 'power1.in' : 'power1.out') : 'none') }, t);
        }
      }
      DZ.each(el.querySelectorAll('[data-at=exit]'), function (m) { gsap.set(m, { opacity: 0 }); tl.to(m, { opacity: 1, duration: span * 0.08 }, t + span * 0.78); });
      if (s.kind !== 'dialog') {
        lt = (s.kind === 'seal' || s.kind === 'seq') ? t + span * 0.78 : ((first && s.kind !== 'two' && s.kind !== 'reveal' && s.kind !== 'deck') ? t : (holdStart + holdEnd) / 2);
        tl.addLabel(s.id, lt); labels.push([s.id, lt, x]);
      }
      if (!last) {
        var outAt = t + span * (s.kind === 'golpe' ? 0.92 : 0.85), outD = span * (s.kind === 'golpe' ? 0.08 : 0.15);
        tl.to(el, { opacity: 0, duration: outD }, outAt);
        if (s.night && !nextN) tl.to(night, { opacity: 0, duration: span * 0.15 }, t + span * 0.85);
      }
      t += span;
    });
    tl.addLabel('fin', total);
    sec._wf = { total: total, labels: labels, vis: vis };
  };
})();
