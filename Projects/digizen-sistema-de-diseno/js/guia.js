/* Guía del sistema de diseño de Digizen: tema claro/oscuro, índice y ejemplos que se pueden tocar. */
(function () {
  'use strict';
  var root = document.documentElement;
  var SOL = '<circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"></path>';
  var LUNA = '<path d="M20.2 15.2A8.4 8.4 0 0 1 8.8 3.8 8.4 8.4 0 1 0 20.2 15.2Z"></path>';

  /* ---------- tema: el mismo mecanismo de la landing (data-theme en <html>) ---------- */
  function setTheme(t) {
    root.setAttribute('data-theme', t);
    var b = document.querySelector('.ds-theme');
    if (b) {
      b.setAttribute('aria-pressed', t === 'dark' ? 'true' : 'false');
      b.setAttribute('aria-label', t === 'dark' ? 'Activar tema claro' : 'Activar tema oscuro');
      b.querySelector('svg').innerHTML = t === 'dark' ? SOL : LUNA;
    }
    try { localStorage.setItem('ds-theme', t); } catch (e) {}
  }
  var saved = null;
  try { saved = localStorage.getItem('ds-theme'); } catch (e) {}
  setTheme(saved === 'dark' ? 'dark' : 'light');
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-ds-theme]');
    if (b) setTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
  });

  /* ---------- índice: cerrado en pantallas chicas; marca la sección visible ---------- */
  var box = document.querySelector('.ds-side-box');
  if (box && window.matchMedia('(max-width: 1023px)').matches) box.removeAttribute('open');
  var links = Array.prototype.slice.call(document.querySelectorAll('.ds-side-list a'));
  var byId = {};
  links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) { a.classList.remove('is-current'); });
        var a = byId[en.target.id];
        if (a) a.classList.add('is-current');
      });
    }, { rootMargin: '-18% 0px -72% 0px' });
    Object.keys(byId).forEach(function (id) { var el = document.getElementById(id); if (el) io.observe(el); });
  }
  if (box) box.addEventListener('click', function (e) {
    if (e.target.closest('a') && window.matchMedia('(max-width: 1023px)').matches) box.removeAttribute('open');
  });

  /* ---------- ejemplos: nada navega ni envía; «Ver más» sí abre su panel ---------- */
  document.addEventListener('click', function (e) {
    var stage = e.target.closest && e.target.closest('.ds-stage');
    if (!stage) return;
    var more = e.target.closest('.dg-readmore-trigger');
    if (more) {
      var panel = stage.querySelector('.dg-readmore-panel');
      if (panel) {
        var open = panel.classList.toggle('ds-open');
        more.setAttribute('aria-expanded', open ? 'true' : 'false');
        more.firstChild.textContent = open ? ' Ver menos' : ' Ver más';
      }
      e.preventDefault(); return;
    }
    if (e.target.closest('a')) e.preventDefault();
  });
  document.addEventListener('submit', function (e) { if (e.target.closest('.ds-stage')) e.preventDefault(); });
})();
