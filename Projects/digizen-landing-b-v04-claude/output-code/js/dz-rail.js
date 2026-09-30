/* Digizen · menú de recorrido (03-build-plan.md §4.5).
   Va encima del recorrido y no toca el scroll: lee las posiciones que calcula el núcleo.
   Desktop: riel a la derecha con un punto por tramo y una línea que se llena con el avance.
   Móvil y tablet: solo la barra fina de progreso arriba. */
(function () {
  'use strict';
  var DZ = window.DZ;
  var rail = document.querySelector('.rail'), bar = document.querySelector('.progress');
  if (!rail && !bar) return;

  var items = rail ? Array.prototype.slice.call(rail.querySelectorAll('.rail-item')) : [];
  var fill = rail ? rail.querySelector('.rail-fill') : null;
  var starts = {}, heroEnd = 0, lastKey = '', maxY = 1;

  /* todo lo que requiere medir se calcula aquí, una vez por refresh; en cada frame solo se escribe transform */
  function computeStarts() {
    starts = {}; heroEnd = 0; maxY = DZ.maxScroll();
    DZ.POS.forEach(function (p) {
      if (p.kind === 'label' || p.kind === 'transit' || !p.pin) return;
      var n = p.pin.tramo;
      if (p.pin.type === 'hero') heroEnd = Math.max(heroEnd, p.to);
      if (n && (starts[n] == null || p.from < starts[n])) starts[n] = p.from;
    });
    lastKey = '';
  }

  function update(y, hit) {
    var prog = Math.min(1, Math.max(0, y / maxY));
    if (bar) bar.style.transform = 'scaleX(' + prog.toFixed(4) + ')';
    if (!rail) return;
    var on = y >= heroEnd - window.innerHeight * 0.5;
    var cur = 0, probe = y + window.innerHeight * 0.4;
    items.forEach(function (it) { var n = +it.getAttribute('data-tramo'); if (starts[n] != null && starts[n] <= probe) cur = Math.max(cur, n); });
    var night = !!(hit && hit.night);
    var key = on + '|' + cur + '|' + night;
    if (fill) fill.style.transform = 'scaleY(' + prog.toFixed(4) + ')';  /* solo transform: sin recalcular layout (apple-design §11) */
    if (key === lastKey) return; lastKey = key;
    rail.classList.toggle('is-on', on);
    rail.classList.toggle('on-night', night);
    items.forEach(function (it) {
      var n = +it.getAttribute('data-tramo');
      it.classList.toggle('is-past', n < cur);
      if (n === cur) it.setAttribute('aria-current', 'step'); else it.removeAttribute('aria-current');
    });
  }

  items.forEach(function (it) {
    it.addEventListener('click', function () {
      var n = +it.getAttribute('data-tramo');
      if (starts[n] != null) DZ.scrollToY(starts[n] + 1);
    });
  });

  DZ.tramoStart = function (n) { return starts[n] != null ? starts[n] : null; };
  DZ.currentTramo = function () {
    var cur = 0, probe = window.scrollY + window.innerHeight * 0.4;
    Object.keys(starts).forEach(function (n) { if (starts[n] <= probe) cur = Math.max(cur, +n); });
    return cur;
  };
  DZ.hooks.positions.push(computeStarts);
  DZ.hooks.frame.push(update);
})();
