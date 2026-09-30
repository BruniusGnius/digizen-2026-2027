/* Digizen · secuencias de cuadros (scrub de video en canvas) y su precarga.
   El scrub es el del wireframe (buildSeq): mismo tramo, misma dirección, mismo encuadre.
   Lo nuevo es CUÁNDO se descargan los cuadros (03-build-plan.md §5.1):
   - no al abrir la página, sino ~6 encuadres antes de llegar al pin, o en reposo después del Hero;
   - primero 1 de cada 4 cuadros (el scrub ya funciona) y luego los intermedios;
   - como máximo 6 descargas a la vez; mientras falta un cuadro se dibuja el más cercano;
   - con ahorro de datos o conexión lenta no se descargan: queda el cuadro fijo (póster). */
(function () {
  'use strict';
  var DZ = window.DZ;

  // ---------- cargador con cola y concurrencia limitada ----------
  var cache = {}, queue = [], active = 0, MAX = 6;
  function pump() {
    queue.sort(function (a, b) { return a.prio - b.prio; });
    while (active < MAX && queue.length) {
      var job = queue.shift(); active++;
      (function (job) {
        var done = function () { active--; pump(); };
        var ready = function () { job.im._dzReady = true; job.im.dispatchEvent(new Event('dz-ready')); done(); };
        /* B6 (apple-design §11): decodificar antes de dibujar, para que el scrub no dé tirones */
        job.im.addEventListener('load', function () { if (job.im.decode) job.im.decode().then(ready, ready); else ready(); }, { once: true });
        job.im.addEventListener('error', done, { once: true });
        job.im.src = job.url;
      })(job);
    }
  }
  DZ.loader = {
    /* devuelve la imagen (la misma si ya se pidió) y la encola con su prioridad (menor = antes) */
    get: function (url, prio) {
      if (cache[url]) return cache[url];
      var im = new Image(); im.decoding = 'async';
      cache[url] = im; queue.push({ im: im, url: url, prio: prio || 0 }); pump();
      return im;
    },
    /* cuando el lector está a ~6 encuadres del pin (o después del Hero, en reposo), se llama fn una vez */
    near: function (sec, fn) {
      var fired = false, go = function () { if (!fired) { fired = true; fn(); } };
      ScrollTrigger.create({ trigger: sec, start: 'top bottom+=600%', once: true, onEnter: go });
      idleJobs.push(go);
    }
  };
  var idleJobs = [];
  /* el Hero llama a DZ.afterHero al terminar: se adelantan en reposo las secuencias, en orden de aparición */
  DZ.afterHero = function () {
    var run = function () { var fn = idleJobs.shift(); if (!fn) return; fn(); schedule(); };
    var schedule = function () { (window.requestIdleCallback || function (f) { return setTimeout(f, 400); })(run, { timeout: 2000 }); };
    schedule();
  };

  // ---------- dibujo (igual que en el wireframe) ----------
  function drawCover(ctx, im, cw, ch) {
    var ir = im.naturalWidth / im.naturalHeight, cr = cw / ch, w, h, x, y;
    if (ir > cr) { h = ch; w = h * ir; x = (cw - w) / 2; y = 0; } else { w = cw; h = w / ir; x = 0; y = (ch - h) / 2; }
    ctx.drawImage(im, x, y, w, h);
  }
  function drawContain(ctx, im, cw, ch) {
    var s = Math.min(cw / im.naturalWidth, ch / im.naturalHeight), w = im.naturalWidth * s, h = im.naturalHeight * s;
    ctx.drawImage(im, (cw - w) / 2, (ch - h) / 2, w, h);
  }

  /* orden progresivo: cuadro inicial, luego 1 de cada 4, luego el resto */
  function order(n, first) {
    var seen = {}, out = [];
    var add = function (i) { if (i >= 0 && i < n && !seen[i]) { seen[i] = 1; out.push(i); } };
    add(first);
    for (var i = 0; i < n; i += 4) add(i);
    add(n - 1);
    for (var j = 0; j < n; j++) add(j);
    return out;
  }

  DZ.buildSeq = function (el, tl, t, span) {
    var fig = el.querySelector('[data-seq]'); if (!fig) return;
    if (!DZ.isD && fig.getAttribute('data-mobile') === 'still') return; /* móvil/tablet: cuadro fijo, sin descargar la secuencia */
    if (DZ.lite) return;                                                /* ahorro de datos / conexión lenta: cuadro fijo */
    var cv = fig.querySelector('canvas'), ctx = cv.getContext('2d');
    var n = +fig.getAttribute('data-n'), base = fig.getAttribute('data-seq');
    var start = +(fig.getAttribute('data-start') || 1), contain = fig.getAttribute('data-fit') === 'contain'; /* cubre su contenedor (decisión del usuario, 2026-09-29) */
    var dur = parseFloat(fig.getAttribute('data-span') || 0.7);
    var rev = fig.getAttribute('data-reverse') === '1';
    var imgs = new Array(n), state = { f: (rev ? n - 1 : 0) };
    var url = function (k) { return base + '/f' + ('00' + (start + k)).slice(-3) + '.webp'; };
    function ok(im) { return im && im._dzReady && im.naturalWidth; }
    function draw() {
      var i = Math.max(0, Math.min(n - 1, Math.round(state.f)));
      var im = imgs[i];
      if (!ok(im)) { /* el cuadro más cercano ya cargado */
        for (var d = 1; d < n; d++) {
          if (ok(imgs[i - d])) { im = imgs[i - d]; break; }
          if (ok(imgs[i + d])) { im = imgs[i + d]; break; }
        }
      }
      if (!ok(im)) return;
      ctx.clearRect(0, 0, cv.width, cv.height); (contain ? drawContain : drawCover)(ctx, im, cv.width, cv.height);
    }
    function size() {
      var r = Math.min(window.devicePixelRatio || 1, 2);
      cv.width = Math.max(1, Math.round(cv.clientWidth * r)); cv.height = Math.max(1, Math.round(cv.clientHeight * r)); draw();
    }
    var firstIdx = rev ? n - 1 : 0;
    var loadAll = function () {
      order(n, firstIdx).forEach(function (k, rank) {
        var im = DZ.loader.get(url(k), rank < 13 ? 0 : 1);
        imgs[k] = im;
        var onload = function () {
          if (k === firstIdx) { fig.classList.add('ready'); size(); }
          else if (Math.abs(Math.round(state.f) - k) <= 4) draw();
        };
        if (ok(im)) onload(); else im.addEventListener('dz-ready', onload, { once: true });
      });
    };
    DZ.loader.near(el.closest('.pin'), loadAll);
    if (fig._seqSize) window.removeEventListener('resize', fig._seqSize);
    fig._seqSize = size; window.addEventListener('resize', size);
    if (fig.getAttribute('data-play') === 'time') { /* gesto de un solo uso: en tiempo real al entrar, se repite al regresar (no scrub) */
      var fps = +(fig.getAttribute('data-fps') || 24);
      var play = gsap.fromTo(state, { f: 0 }, { f: n - 1, duration: (n - 1) / fps, ease: 'none', paused: true, onUpdate: draw });
      ScrollTrigger.create({ trigger: el.closest('.pin'), start: 'top 60%',
        onEnter: function () { play.restart(); }, onEnterBack: function () { play.restart(); } });
      return;
    }
    tl.fromTo(state, { f: (rev ? n - 1 : 0) }, { f: (rev ? 0 : n - 1), duration: span * dur, ease: 'none', onUpdate: draw }, t);
  };
})();
