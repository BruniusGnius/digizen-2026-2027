(() => {
  'use strict';
  const config = window.DIGIZEN_CONFIG || {};
  const allowedUrl = value => { try { const u = new URL(value); return u.protocol === 'https:' ? u.href : null; } catch { return null; } };
  const emit = (event, extra = {}) => {
    const detail = { event, variant: 'narrativa_b', ...extra };
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(detail);
    window.dispatchEvent(new CustomEvent('digizen:analytics', { detail }));
    const endpoint = allowedUrl(config.analyticsEndpoint);
    if (endpoint) navigator.sendBeacon(endpoint, new Blob([JSON.stringify(detail)], { type: 'application/json' }));
  };
  let lastTrigger;
  document.querySelectorAll('[data-open]').forEach(button => button.addEventListener('click', () => {
    const id = button.dataset.open;
    const direct = id === 'rules-dialog' ? allowedUrl(config.rulesUrl) : id === 'ada-dialog' ? allowedUrl(config.adaAccessFormUrl) : null;
    if (direct) { window.location.assign(direct); return; }
    lastTrigger = button;
    document.getElementById(id).showModal();
    emit(id === 'checkout-dialog' ? 'CheckoutIntent' : id === 'ada-dialog' ? 'DemoIntent' : 'RulesOpened');
  }));
  document.querySelectorAll('dialog').forEach(dialog => {
    dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
    dialog.addEventListener('close', () => lastTrigger?.focus());
    dialog.addEventListener('click', e => { if(e.target === dialog) { const r = dialog.getBoundingClientRect(); if(e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close(); } });
  });
  document.getElementById('checkout-form').addEventListener('submit', event => {
    event.preventDefault();
    const plan = new FormData(event.currentTarget).get('payment');
    const url = allowedUrl(config.checkout?.[plan]);
    if (url) { emit('CheckoutRedirect', { plan }); window.location.assign(url); return; }
    document.getElementById('checkout-status').textContent = 'El pago aún no está habilitado en esta versión. Puedes consultar al equipo con el enlace de abajo.';
  });
  document.getElementById('ada-form').addEventListener('submit', event => {
    event.preventDefault();
    document.getElementById('ada-status').textContent = 'No se han enviado ni guardado tus datos. La entrega de accesos aún no está conectada; puedes pedir información al equipo con el enlace de abajo.';
  });
  const milestones = new Set();
  let ticking = false;
  const trackScroll = () => {
    const total = document.documentElement.scrollHeight - innerHeight;
    const percentage = total > 0 ? Math.min(100, (scrollY / total) * 100) : 100;
    document.querySelector('.reading-progress').style.transform = `scaleX(${percentage / 100})`;
    for (const mark of [25, 50, 75, 100]) if (percentage >= (mark === 100 ? 99.5 : mark) && !milestones.has(mark)) { milestones.add(mark); emit('ReadingDepth', { percent: mark }); }
    ticking = false;
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(trackScroll); } }, { passive: true });
  addEventListener('resize', trackScroll);
  let activeMs = 0, started = document.hidden ? null : performance.now();
  const flushTime = () => { if (started !== null) { activeMs += performance.now() - started; started = null; } if (activeMs > 0) emit('ReadingTime', { seconds: Math.round(activeMs / 1000) }); };
  document.addEventListener('visibilitychange', () => { if (document.hidden) flushTime(); else started = performance.now(); });
  addEventListener('pagehide', flushTime);
  trackScroll();
})();
