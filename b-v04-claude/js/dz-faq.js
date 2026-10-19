/* Digizen · FAQ (A1): la respuesta abre y cierra con resorte crítico y se puede interrumpir
   (si se toca a medio camino, revierte desde donde está). El indicador gira con el estado,
   no con el atributo `open`, para que su respuesta sea inmediata al tocar.
   Movimiento reducido: sin animar la altura (se degrada a mostrar/ocultar). */
(function () {
  'use strict';
  var DZ = window.DZ;
  var items = document.querySelectorAll('.faq details'); if (!items.length) return;

  function refreshPositions() { if (DZ.mode === 'full') DZ.computePositions(); else DZ.computeFlowPositions(); }

  DZ.each(items, function (d) {
    var sum = d.querySelector('summary'), body = d.querySelector('summary ~ *');
    if (!sum || !body) return;
    var isOpen = d.open, sp = null;
    d.classList.toggle('is-open', isOpen);
    sum.addEventListener('click', function (e) {
      e.preventDefault();
      isOpen = !isOpen;
      d.classList.toggle('is-open', isOpen);          /* respuesta inmediata del indicador */
      if (isOpen) d.open = true;
      if (DZ.reduce) { if (!isOpen) d.open = false; refreshPositions(); return; }
      var full = body.scrollHeight;
      body.style.overflow = 'hidden';
      var draw = function (h) { body.style.height = Math.max(0, h) + 'px'; body.style.opacity = full ? Math.min(1, Math.max(0, h / full)) : 1; };
      var rest = function () {
        if (!isOpen) d.open = false;
        body.style.height = ''; body.style.opacity = ''; body.style.overflow = ''; sp = null;
        refreshPositions();
      };
      if (sp && sp.running()) sp.to(isOpen ? full : 0);
      else sp = DZ.spring({ from: isOpen ? 0 : full, to: isOpen ? full : 0, response: 0.42, eps: 0.5, onUpdate: draw, onRest: rest });
    });
  });
})();
