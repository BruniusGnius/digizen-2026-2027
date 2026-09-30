/* Digizen · Hero. Es buildHero del wireframe, con los mismos tiempos:
   zoom-out de 3.7 s → pausa 0.6 s → velo 0.5 s → frase 0.5 s → indicador.
   Único cambio (pedido del usuario, 2026-09-29): el logo grande del Hero aparece desde el primer cuadro
   (fundido de 0.6 s al empezar), no al final del zoom, para dar presencia de marca al inicio.
   Al terminar avisa al cargador (DZ.afterHero) para adelantar en reposo lo que sigue. */
(function () {
  'use strict';
  var DZ = window.DZ;

  DZ.buildHero = function (sec, vis, pin) {
    var x = vis[0], el = x.el; gsap.set(el, { opacity: 1 });
    var img = el.querySelector('.hero-img'), scrim = el.querySelector('.scrim'), txt = el.querySelector('.hero-text');
    var tl = gsap.timeline({ paused: true });
    tl.fromTo(img, { scale: 2.6 }, { scale: 1, duration: 3.7, ease: 'power2.inOut' })
      .to({}, { duration: 0.6 })
      .fromTo(scrim, { opacity: 0 }, { opacity: 1, duration: 0.5 })
      .fromTo(txt, { opacity: 0 }, { opacity: 1, duration: 0.5 });
    var cue = el.querySelector('.cue'); if (cue) tl.fromTo(cue, { opacity: 0 }, { opacity: 1, duration: 0.4 });
    var logo = el.querySelector('.hero-logo'); if (logo) tl.fromTo(logo, { opacity: 0 }, { opacity: 1, duration: 0.6 }, 0);
    var told = false;
    tl.call(function () { if (!told && DZ.afterHero) { told = true; DZ.afterHero(); } });
    ScrollTrigger.create({ id: pin.id, trigger: sec, pin: true, start: 'top top',
      end: function () { return '+=' + (x.s.E * window.innerHeight); },
      onEnterBack: function () { tl.restart(); } });
    tl.restart();
    sec._wf = { total: x.s.E, labels: [[x.s.id, 0, x]], vis: vis };
  };
})();
