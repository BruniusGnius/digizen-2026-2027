/* Digizen · arranque. Igual que el wireframe:
   - modo completo: un ScrollTrigger por pin (Hero autoplay, horizontal, pines), matchMedia en 860 px,
     refresh después de las fuentes y de la carga;
   - modo reducido (movimiento reducido o sin GSAP): flujo normal, cada parada aparece con un fundido corto. */
(function () {
  'use strict';
  var DZ = window.DZ;

  if (DZ.mode === 'full') {
    document.body.classList.add('fullmode');
    gsap.registerPlugin(ScrollTrigger);
    if (window.ScrollToPlugin) gsap.registerPlugin(ScrollToPlugin);
    ScrollTrigger.addEventListener('refresh', DZ.computePositions);
    var mm = gsap.matchMedia();
    mm.add({ isD: '(min-width: 860px)', isM: '(max-width: 859px)' }, function (ctx) {
      DZ.isD = !!ctx.conditions.isD;
      DZ.PINS.forEach(function (pin) {
        if (pin.type === 'flow') return;
        var vis = pin.stops.filter(DZ.visible).map(DZ.rec);
        if (pin.type === 'hero') DZ.buildHero(pin.el, vis, pin);
        else if (pin.type === 'h') DZ.buildH(pin.el, vis, pin);
        else DZ.buildPin(pin.el, vis, pin);
      });
      ScrollTrigger.refresh();
      return function () { DZ.POS = []; };
    });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { ScrollTrigger.refresh(); });
    window.addEventListener('load', function () { ScrollTrigger.refresh(); });
  } else {
    document.body.classList.add('flowmode');
    var io = ('IntersectionObserver' in window) ? new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) e.target.classList.add('inview'); });
    }, { threshold: 0.15 }) : null;
    DZ.STOPS.forEach(function (x) { if (x.flow) return; if (io) io.observe(x.el); else x.el.classList.add('inview'); });
    var refreshFlow = function () { DZ.isD = window.innerWidth >= 860; DZ.computeFlowPositions(); };
    requestAnimationFrame(refreshFlow);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(refreshFlow);
    window.addEventListener('load', refreshFlow);
    window.addEventListener('resize', function () { clearTimeout(window._rf); window._rf = setTimeout(refreshFlow, 200); });
  }
})();
