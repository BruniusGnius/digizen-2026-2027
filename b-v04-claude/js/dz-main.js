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
    /* prueba 3: sin scroll animado (flujo normal); solo los videos con scrub siguen fijados mientras corren, en desktop */
    if (DZ.cfg.flow && DZ.hasGsap && !DZ.reduce) {
      document.body.classList.add('flow-video');
      gsap.registerPlugin(ScrollTrigger);
      if (window.ScrollToPlugin) gsap.registerPlugin(ScrollToPlugin);
      var hero = DZ.STOPS.filter(function (x) { return x.s.kind === 'hero'; })[0];
      if (hero && DZ.heroIntro) DZ.heroIntro(hero.el).restart();   /* la entrada del Hero es de tiempo, no de scroll */
      gsap.matchMedia().add('(min-width: 860px)', function () {
        DZ.isD = true;
        DZ.STOPS.forEach(function (x) {
          if (x.flow || !DZ.visible(x.s)) return;
          var fig = x.el.querySelector('[data-seq]'); if (!fig) return;
          if (fig.getAttribute('data-play') === 'time') { DZ.buildSeq(x.el, null, 0, x.s.E); return; }
          var tl = gsap.timeline({ defaults: { ease: 'none' }, scrollTrigger: { trigger: x.el, pin: true, start: 'top top',
            end: function () { return '+=' + (x.s.E * window.innerHeight); }, scrub: 0.4, invalidateOnRefresh: true } });
          tl.to({}, { duration: x.s.E }, 0);
          DZ.buildSeq(x.el, tl, 0, x.s.E);
        });
        ScrollTrigger.refresh();
      });
      ScrollTrigger.addEventListener('refresh', function () { DZ.computeFlowPositions(); });
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
