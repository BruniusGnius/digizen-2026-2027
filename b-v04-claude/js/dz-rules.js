/* Digizen · página «Las reglas de ADA» (03-build-plan-reglas.md).
   La página se abre desde la landing en una pestaña nueva, para no romper la narrativa: la landing se queda en su
   pestaña, en la estación donde estaba (decisión del usuario, 2026-10-02). Aquí solo hay tres comportamientos:
   - «Volver a Digizen» sale por donde se entró: cierra esta pestaña. Si no vino de la landing, o el navegador no
     deja cerrarla, va a la landing en la estación del botón «Conocer las reglas de ADA».
   - Los enlaces a una sección de la landing (inscripción, menú) la mueven en SU pestaña y cierran ésta; si no hay
     landing abierta, navegan aquí mismo.
   - El índice (lista completa, desktop) lleva a cada tarjeta; el desplazamiento es el del navegador, que se
     interrumpe en cuanto el lector hace scroll. No cambia la dirección de la página.
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

  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var idx = e.target.closest('.rg-full a[href^="#regla-"]');
    if (idx) {   /* índice → tarjeta */
      var t = document.getElementById(idx.getAttribute('href').slice(1)); if (!t) return;
      e.preventDefault();
      t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      t.setAttribute('tabindex', '-1'); t.focus({ preventScroll: true });
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
