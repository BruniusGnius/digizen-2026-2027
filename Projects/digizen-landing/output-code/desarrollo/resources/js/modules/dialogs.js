import { setupForm } from './ada-form';
import { setupButtons, spring } from '../lib/spring';

export function setupDialogs(config) {
  const ada = document.querySelector('#ada-dialog');
  const checkout = document.querySelector('#checkout-dialog');
  const original = document.querySelector('[data-ada-form]');
  const clone = original.cloneNode(true);
  // The two forms have independent accessible IDs and no duplicated identifiers.
  clone.querySelectorAll('[id]').forEach(element => { element.id = element.id.replace('-inline', '-dialog'); });
  clone.querySelectorAll('[aria-describedby]').forEach(element => { element.setAttribute('aria-describedby', element.getAttribute('aria-describedby').replaceAll('-inline', '-dialog')); });
  ada.querySelector('[data-dialog-form]').append(clone);
  setupForm(original, config);
  setupForm(clone, config);
  setupButtons(ada);
  let origin;
  let previousOverflow = '';
  let closeTimer;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const transitions = new Map();
  for (const dialog of [ada, checkout]) {
    transitions.set(dialog, spring(value => {
      dialog.style.opacity = String(value);
      dialog.style.transform = reduced.matches ? 'none' : `translateY(${(1 - value) * (matchMedia('(max-width: 767px)').matches ? 32 : 8)}px) scale(${.985 + value * .015})`;
    }, 0, .1));
    dialog.querySelectorAll('[data-close]').forEach(button => button.addEventListener('click', () => close(dialog)));
    dialog.addEventListener('cancel', event => { event.preventDefault(); close(dialog); });
    dialog.addEventListener('click', event => { if (event.target === dialog) { const rect = dialog.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) close(dialog); } });
    dialog.addEventListener('close', () => {
      dialog.querySelector('form')?.cancelRequest?.();
      document.documentElement.style.overflow = previousOverflow;
      origin?.focus({ preventScroll: true });
    });
  }
  function open(dialog, trigger) {
    clearTimeout(closeTimer);
    origin = trigger;
    if (!dialog.open) {
      previousOverflow = document.documentElement.style.overflow;
      document.documentElement.style.overflow = 'hidden';
      dialog.showModal();
    }
    const rect = trigger.getBoundingClientRect();
    const box = dialog.getBoundingClientRect();
    dialog.style.transformOrigin = `${Math.max(0, Math.min(box.width, rect.x + rect.width / 2 - box.x))}px ${Math.max(0, Math.min(box.height, rect.y - box.y))}px`;
    transitions.get(dialog)(1);
    (dialog.querySelector('input') || dialog.querySelector('[data-close]')).focus({ preventScroll: true });
  }
  function close(dialog) {
    dialog.querySelector('form')?.cancelRequest?.();
    transitions.get(dialog)(0);
    clearTimeout(closeTimer);
    closeTimer = setTimeout(() => dialog.close(), reduced.matches ? 0 : 180);
  }
  document.querySelectorAll('[data-action="ada"]').forEach(button => button.addEventListener('click', () => open(ada, button)));
  const labels = { monthly: 'Plan mensual · $599/mes + $900 inscripción única', cycle: 'Ciclo completo · $5,990 · hasta 12 MSI', cash: 'Contado · $5,990 por el ciclo completo' };
  document.querySelectorAll('[data-action="checkout"]').forEach(button => button.addEventListener('click', () => {
    const plan = button.dataset.plan;
    const destination = config.checkout?.[plan];
    if (config.mode !== 'preview' && destination) {
      try {
        const url = new URL(destination, location.origin);
        if (url.protocol === 'https:' || (url.origin === location.origin && url.protocol === 'http:')) { location.assign(url.href); return; }
      } catch { /* Missing/invalid integration falls back to an honest state. */ }
    }
    checkout.querySelector('.checkout-selected').textContent = labels[plan];
    if (config.mode !== 'preview') {
      checkout.querySelector('.dg-kicker').textContent = 'Inscripción';
      checkout.querySelector('.checkout-selected + p').textContent = 'La inscripción no está disponible por el momento. Inténtalo más tarde.';
    }
    open(checkout, button);
  }));
}
