// Critically damped analytic spring; retargeting retains position and velocity.
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
export function spring(update, initial = 1, response = .11) {
  let position = initial, velocity = 0, target = initial, frame = 0, previous = 0;
  const omega = 2 / response;
  const tick = (time) => {
    const dt = Math.min((time - previous) / 1000 || 1 / 60, .05);
    previous = time;
    const distance = position - target;
    const coefficient = velocity + omega * distance;
    const decay = Math.exp(-omega * dt);
    position = target + (distance + coefficient * dt) * decay;
    velocity = (velocity - omega * coefficient * dt) * decay;
    update(position);
    if (Math.abs(position - target) + Math.abs(velocity) < .0005) { position = target; velocity = 0; update(target); frame = 0; return; }
    frame = requestAnimationFrame(tick);
  };
  return (next) => {
    target = next;
    if (reduced.matches) { cancelAnimationFrame(frame); frame = 0; position = next; velocity = 0; update(next); return; }
    if (!frame) { previous = performance.now(); frame = requestAnimationFrame(tick); }
  };
}

export function setupButtons(scope = document) {
  scope.querySelectorAll('[data-btn]').forEach(button => {
    if (button.dataset.springReady) return;
    button.dataset.springReady = 'true';
    const animate = spring(value => { button.style.scale = String(reduced.matches ? 1 : value); });
    button.addEventListener('pointerdown', event => { if (event.button === 0 && !button.disabled) animate(.98); });
    ['pointerup', 'pointerleave', 'pointercancel', 'blur'].forEach(name => button.addEventListener(name, () => animate(1)));
    button.addEventListener('keydown', event => { if (event.key === ' ' || event.key === 'Enter') animate(.98); });
    button.addEventListener('keyup', () => animate(1));
  });
}
