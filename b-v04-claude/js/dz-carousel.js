/* Digizen · carrusel horizontal (cap. 02). Es buildH del wireframe, sin cambios:
   cada panel llega y se estaciona el 70 % de su E, y solo después se desplaza (30 %).
   Snap a la mitad de cada estacionamiento, sin inercia. */
(function () {
  'use strict';
  var DZ = window.DZ;

  DZ.buildH = function (sec, vis, pin) {
    var track = sec.querySelector('.track'), n = vis.length;
    track.style.setProperty('--n', n);
    vis.forEach(function (x) { gsap.set(x.el, { opacity: 1 }); });
    var total = vis.reduce(function (a, x) { return a + x.s.E; }, 0);
    var tl = gsap.timeline({ defaults: { ease: 'none' }, scrollTrigger: {
      id: pin.id, trigger: sec, pin: true, start: 'top top',
      end: function () { return '+=' + (total * DZ.unit()); },
      scrub: 0.4, invalidateOnRefresh: true,
      onToggle: function (self) { sec.classList.toggle('is-pinned', self.isActive); }, /* B7: will-change solo mientras está activo */
      snap: { snapTo: 'labels', duration: { min: 0.3, max: 0.6 }, delay: 0.15, ease: 'power1.inOut', inertia: false }
    } });
    tl.to({}, { duration: total }, 0);
    var labels = [], t = 0;
    vis.forEach(function (x, i) {
      var last = i === n - 1, hold = last ? x.s.E : x.s.E * 0.7, move = x.s.E - hold;
      var lt = t + hold / 2;
      tl.addLabel(x.s.id, lt); labels.push([x.s.id, lt, x]);
      if (!last) {
        tl.to(track, { x: function () { return -(i + 1) * window.innerWidth; }, duration: move, ease: 'power2.inOut' }, t + hold);
      }
      t += x.s.E;
    });
    tl.addLabel('fin', total);
    sec._wf = { total: total, labels: labels, vis: vis };
  };
})();
