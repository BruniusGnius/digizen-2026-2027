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
    /* prueba 2: en pantallas solo táctiles, el scroll del dedo lo maneja GSAP y la inercia de cada deslizamiento se acorta,
       para que un gesto normal avance más o menos una parada. Desktop y pantallas mixtas no cambian. */
    if (DZ.cfg.touchMomentum && ScrollTrigger.isTouch === 1) {
      ScrollTrigger.config({ ignoreMobileResize: true });
      ScrollTrigger.normalizeScroll({ type: 'touch', allowNestedScroll: true, lockAxis: false,
        momentum: function (self) { return Math.min(0.8, Math.abs(self.velocityY) / 3000); } });
    }
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
    /* prueba 3 (pedido del usuario y de su jefe, 2026-09-30): una estación por gesto (dz-pager.js). Las estaciones llegan
       compuestas, sin animaciones internas ni la entrada del Hero. En desktop, las escenas con efecto (zoom o video con scrub)
       conservan su animación, fijadas; en teléfono y tablet todas las imágenes son estaciones ancladas, sin animación.
       El saludo de ADA sigue corriendo por tiempo al llegar (solo desktop). */
    if (DZ.cfg.flow && DZ.hasGsap && !DZ.reduce) {
      document.body.classList.add('flow-video');
      gsap.registerPlugin(ScrollTrigger);
      if (window.ScrollToPlugin) gsap.registerPlugin(ScrollToPlugin);
      var paged = !!(DZ.cfg.pager && DZ.pager);
      var hero = DZ.STOPS.filter(function (x) { return x.s.kind === 'hero'; })[0];
      if (paged) {
        document.body.classList.add('paged'); document.documentElement.classList.add('dz-paged');
        DZ.STOPS.forEach(function (x) { if (!x.flow) x.el.classList.add('inview'); });
        window.addEventListener('load', function () { if (DZ.afterHero) DZ.afterHero(); });   /* el Hero ya está compuesto: se adelanta la precarga */
      } else if (hero && DZ.heroIntro) DZ.heroIntro(hero.el).restart();   /* la entrada del Hero es de tiempo, no de scroll */
      gsap.matchMedia().add({ isD: '(min-width: 860px)', isM: '(max-width: 859px)', isS: '(max-width: 599px)' }, function (ctx) {
        DZ.isD = !!ctx.conditions.isD;
        DZ.STOPS.forEach(function (x) {
          x._st = null; x._steps = 0;
          if (x.flow || !DZ.visible(x.s)) return;
          var fig = x.el.querySelector('[data-seq]');
          if (fig && fig.getAttribute('data-play') === 'time') { DZ.buildSeq(x.el, null, 0, x.s.E); return; }  /* saludo de ADA: por tiempo */
          /* teléfono: las tarjetas apiladas (08.5m, 11.3m, 11.3bm) como en la versión animada; cada gesto sube una tarjeta
             sobre la anterior y, con la última en su lugar, el siguiente pasa de estación (pedido del usuario) */
          var cards = x.el.querySelectorAll('.entries.deck > .card');
          if (paged && ctx.conditions.isS && x.s.kind === 'deck' && cards.length > 1) {
            var n = cards.length - 1;
            var dt = gsap.timeline({ defaults: { ease: 'none' }, scrollTrigger: { trigger: x.el, pin: true, start: 'top top',
              end: function () { return '+=' + (n * 0.6 * DZ.unit()); }, scrub: 0.4, invalidateOnRefresh: true } });
            dt.to({}, { duration: n }, 0);
            for (var q = 1; q <= n; q++) {
              dt.fromTo(cards[q], { opacity: 0, y: function () { return window.innerHeight * 0.6; } },
                { opacity: 1, y: 0, duration: 0.8, ease: 'power2.out', immediateRender: true }, q - 1 + 0.1);
            }
            x._st = dt.scrollTrigger; x._steps = n;
            return;
          }
          if (x.s.kind !== 'seal' && x.s.kind !== 'seq') return;   /* solo las escenas conservan su animación con scroll */
          if (!DZ.isD) return;   /* teléfono y tablet: todas las imágenes son estaciones ancladas, sin animación (pedido del usuario) */
          /* desktop: una escena sin efecto visible (zoom 1 o casi, o video que no se descarga) es una estación normal: una sola
             parada, sin fijarla, para que no pida un gesto de más sin que pase nada (pedido del usuario) */
          var zf = x.el.querySelector('[data-zoom]'), z = zf ? parseFloat(zf.getAttribute('data-zoom')) : 1.06;
          if (fig ? DZ.lite : Math.abs(z - 1) < 0.1) return;
          x.el.classList.add('inview');
          var tl = gsap.timeline({ defaults: { ease: 'none' }, scrollTrigger: { trigger: x.el, pin: true, start: 'top top',
            end: function () { return '+=' + (x.s.E * DZ.unit()); }, scrub: 0.4, invalidateOnRefresh: true } });
          tl.to({}, { duration: x.s.E }, 0);
          x._st = tl.scrollTrigger;
          if (fig) DZ.buildSeq(x.el, tl, 0, x.s.E); else DZ.sealZoom(x.el, tl, 0, x.s.E);
        });
        ScrollTrigger.refresh();
      });
      ScrollTrigger.addEventListener('refresh', function () { DZ.computeFlowPositions(); });
      if (paged) DZ.pager();
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { ScrollTrigger.refresh(); });
      window.addEventListener('load', function () { ScrollTrigger.refresh(); });
    }
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
