/* Digizen · logo flotante (pedido del usuario, 2026-09-29).
   Fijo arriba a la izquierda, siempre del mismo tamaño (sin animación de escala: esa era la del menú de la
   propuesta A y se descartó). Mientras el Hero está debajo manda el logo grande del Hero; el flotante aparece
   con un fundido cuando el Hero termina de salir. Sobre una bisagra oscura usa la versión para fondo oscuro;
   sobre el fondo claro, la versión clara. No cambia el scroll ni las paradas. */
(function () {
  'use strict';
  var DZ = window.DZ;
  var brand = document.querySelector('.brand'); if (!brand) return;
  var heroEnd = 0;

  DZ.hooks.positions.push(function () {
    heroEnd = 0;
    DZ.POS.forEach(function (p) {
      if (p.pin && p.pin.type === 'hero' && p.kind !== 'label' && p.kind !== 'transit') heroEnd = Math.max(heroEnd, p.to);
    });
  });
  DZ.hooks.frame.push(function (y, hit) {
    /* el Hero deja de estar debajo del logo cuando su escenario termina de salir por arriba */
    var clear = DZ.mode === 'full' ? heroEnd + window.innerHeight - 60 : heroEnd - 60;
    /* sobre una escena (sello o secuencia) va la versión dark, como sobre una bisagra oscura (pedido del usuario) */
    var onImage = !!(hit && (hit.kind === 'seal' || hit.kind === 'seq'));
    brand.classList.toggle('is-on', y >= clear);
    brand.classList.toggle('on-image', onImage);
    brand.classList.toggle('on-light', y >= clear && !(hit && hit.night) && !onImage);
  });
  brand.addEventListener('click', function (e) { e.preventDefault(); DZ.scrollToY(0); });
})();
