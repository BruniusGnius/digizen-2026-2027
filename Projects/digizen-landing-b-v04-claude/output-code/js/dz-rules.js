/* Digizen · página «Las reglas de ADA» (03-build-plan-reglas.md).
   La página se abre desde la landing en una pestaña nueva, para no romper la narrativa: la landing se queda en su
   pestaña, en la estación donde estaba (decisión del usuario, 2026-10-02). Aquí solo hay tres comportamientos:
   - «Volver a Digizen» sale por donde se entró: cierra esta pestaña. Si no vino de la landing, o el navegador no
     deja cerrarla, va a la landing en la estación del botón «Conocer las reglas de ADA».
   - Los enlaces a una sección de la landing (inscripción, menú) la mueven en SU pestaña y cierran ésta; si no hay
     landing abierta, navegan aquí mismo.
   - El índice (lista completa, desktop) lleva a la estación de cada tarjeta. No cambia la dirección de la página.
   La página se recorre por estaciones con el motor de la landing (dz-pager.js): una estación por gesto.
   La respuesta al tocar, el menú y el formulario son los de la landing (dz-actions.js, dz-menu.js). */
(function () {
  'use strict';
  var reduce = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);

  /* la landing que abrió esta pestaña, si sigue abierta (mismo sitio) */
  function landing() {
    try { var o = window.opener; return (o && !o.closed && o.location.origin === window.location.origin) ? o : null; }
    catch (err) { return null; }
  }
  /* cerrar esta pestaña; si el navegador no lo permite, navegar aquí */
  function leave(href) {
    window.close();
    setTimeout(function () { if (!window.closed) window.location.href = href; }, 180);
  }

  /* logo: versión clara (con sombra) sobre la lámina oscura, como sobre las bisagras de la landing; solo desde 860 px,
     donde el panel oscuro queda detrás del logo (abajo de eso la imagen va arriba y es clara). El botón de menú se queda
     oscuro: en esa lámina siempre cae sobre la parte clara de la imagen */
  var DZh = window.DZ, brand = document.querySelector('.brand');
  if (DZh && DZh.hooks && brand) DZh.hooks.frame.push(function (y, hit) {
    var dark = !!(hit && hit.night) && window.innerWidth >= 860;
    brand.classList.toggle('on-light', !dark); brand.classList.toggle('on-image', dark);
  });

  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var idx = e.target.closest('[data-rule-link]');
    if (idx) {   /* índice → la estación de esa tarjeta (la variante visible en este ancho) */
      var n = idx.getAttribute('data-rule-link'), t = null;
      Array.prototype.forEach.call(document.querySelectorAll('[data-rule="' + n + '"]'), function (c) { if (!t && c.offsetParent !== null) t = c; });
      if (!t) return;
      e.preventDefault();
      var st = t.closest('.stop'), DZ = window.DZ;
      if (!(st && DZ && DZ.goTo && DZ.goTo(st.getAttribute('data-id')))) t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      t.setAttribute('tabindex', '-1'); t.focus({ preventScroll: true });
      return;
    }
    if (e.target.closest('[data-rules=top]')) {   /* «Reglas de ADA» en el menú de esta página: al inicio */
      e.preventDefault();
      if (window.DZ && window.DZ.scrollToY) window.DZ.scrollToY(0); else window.scrollTo(0, 0);
      return;
    }
    var back = e.target.closest('[data-rules=back]');
    if (back) {   /* «Volver a Digizen» */
      var o = landing(), href = back.getAttribute('href');
      if (!o) return;                 /* sin landing abierta: el enlace navega normal a la estación */
      e.preventDefault();
      try { o.focus(); } catch (err) {}
      leave(href);
      return;
    }
    var price = e.target.closest('[data-action=pricing]');
    var a = price ? null : e.target.closest('a[href^="./#"]');
    if (!price && !a) return;
    var hash = price ? 'precio' : a.getAttribute('href').slice(3), url = './#' + hash, op = landing();
    e.preventDefault();
    if (!op) { window.location.href = url; return; }
    try {
      if (op.location.hash === '#' + hash) op.dispatchEvent(new HashChangeEvent('hashchange')); else op.location.hash = hash;
      op.focus();
    } catch (err) { window.location.href = url; return; }
    leave(url);
  });
})();
