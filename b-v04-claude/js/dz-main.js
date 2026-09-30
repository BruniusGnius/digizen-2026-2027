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
    /* prueba 3: sin scroll animado para el texto (flujo normal); las escenas (imágenes y videos con scrub) conservan su animación,
       fijadas mientras corre, en desktop y móvil. La entrada del Hero va por tiempo. */
    if (DZ.cfg.flow && DZ.hasGsap && !DZ.reduce) {
      document.body.classList.add('flow-video');
      gsap.registerPlugin(ScrollTrigger);
      if (window.ScrollToPlugin) gsap.registerPlugin(ScrollToPlugin);
      /* anclas por pantalla (pedido del usuario): al soltar el scroll, avanza a la siguiente pantalla en la dirección del gesto
         (inicio de cada composición; en las escenas fijadas, su inicio y su final). Dentro de una escena fijada el scroll es libre
         para que el scrub siga al dedo, y en una composición más alta que la pantalla también, para no saltarse su parte de abajo.
         Desde el FAQ hacia abajo, scroll libre. */
      var snapPts = [], snapFree = [], snapStop = Infinity, snapMax = 1;
      var buildSnap = function () {
        snapMax = Math.max(1, ScrollTrigger.maxScroll(window)); snapStop = Infinity; var pts = [], free = [], vh = window.innerHeight;
        DZ.STOPS.forEach(function (x) {
          var top = x.el.getBoundingClientRect().top + window.scrollY, h = x.el.offsetHeight;
          if (x.flow) { snapStop = Math.min(snapStop, top); pts.push(top); return; }
          if (!DZ.visible(x.s) || !h) return;
          if (x._st) { pts.push(x._st.start, x._st.end); free.push([x._st.start, x._st.end]); }
          else if (h > vh + 40) { pts.push(top, top + h - vh); free.push([top, top + h - vh]); }
          else pts.push(top);
        });
        snapPts = pts.filter(function (p) { return p >= 0 && p <= snapMax; }).sort(function (a, b) { return a - b; });
        snapFree = free;
      };
      /* dirección del último gesto, leída del scroll real; los ajustes internos de ScrollTrigger al recalcular no cuentan */
      var snapDir = 1, dirY = window.scrollY, dirHold = false;
      ScrollTrigger.addEventListener('refreshInit', function () { dirHold = true; });
      ScrollTrigger.addEventListener('refresh', function () { dirHold = false; dirY = window.scrollY; });
      window.addEventListener('scroll', function () {
        var y = window.scrollY; if (dirHold || y === dirY) return; snapDir = y > dirY ? 1 : -1; dirY = y;
      }, { passive: true });
      ScrollTrigger.addEventListener('refresh', buildSnap);
      ScrollTrigger.create({ start: 0, end: 'max', snap: {
        snapTo: function (p) {
          var y = p * snapMax, i; if (y >= snapStop - 4 || !snapPts.length) return p;
          for (i = 0; i < snapFree.length; i++) if (y > snapFree[i][0] + 2 && y < snapFree[i][1] - 2) return p;
          if (snapDir >= 0) { for (i = 0; i < snapPts.length; i++) if (snapPts[i] >= y - 2) return snapPts[i] / snapMax; return p; }
          for (i = snapPts.length - 1; i >= 0; i--) if (snapPts[i] <= y + 2) return snapPts[i] / snapMax;
          return p;
        }, duration: { min: 0.25, max: 0.6 }, delay: 0.12, ease: 'power1.inOut' } });
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { ScrollTrigger.refresh(); });
      window.addEventListener('load', function () { ScrollTrigger.refresh(); });
      var hero = DZ.STOPS.filter(function (x) { return x.s.kind === 'hero'; })[0];
      if (hero && DZ.heroIntro) DZ.heroIntro(hero.el).restart();   /* la entrada del Hero es de tiempo, no de scroll */
      gsap.matchMedia().add({ isD: '(min-width: 860px)', isM: '(max-width: 859px)' }, function (ctx) {
        DZ.isD = !!ctx.conditions.isD;
        DZ.STOPS.forEach(function (x) {
          if (x.flow || !DZ.visible(x.s)) return;
          var fig = x.el.querySelector('[data-seq]');
          if (fig && fig.getAttribute('data-play') === 'time') { DZ.buildSeq(x.el, null, 0, x.s.E); return; }  /* saludo de ADA: por tiempo */
          if (x.s.kind !== 'seal' && x.s.kind !== 'seq') return;   /* solo las escenas conservan su animación con scroll */
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
