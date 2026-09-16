export function setupNavigation() {
  const fill = document.querySelector('#dg-pill-fill');
  const links = [...document.querySelectorAll('.dg-nav__links a')];
  let scheduled = false;
  const update = () => {
    const root = document.documentElement;
    const available = root.scrollHeight - root.clientHeight;
    fill.style.transform = `scaleX(${available > 0 ? Math.max(0, Math.min(1, root.scrollTop / available)) : 0})`;
    const active = links.filter(link => document.querySelector(link.hash)?.getBoundingClientRect().top <= 180).at(-1);
    links.forEach(link => link === active ? link.setAttribute('aria-current', 'location') : link.removeAttribute('aria-current'));
    scheduled = false;
  };
  const schedule = () => { if (!scheduled) { scheduled = true; requestAnimationFrame(update); } };
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule);
  new ResizeObserver(schedule).observe(document.body);
  document.querySelectorAll('a[href^="#"]').forEach(link => link.addEventListener('click', event => {
    const target = document.querySelector(link.hash);
    if (!target) return;
    event.preventDefault();
    target.tabIndex = -1;
    target.focus({ preventScroll: true });
    target.scrollIntoView({ block: 'start', behavior: 'instant' });
    history.replaceState(null, '', link.hash);
    schedule();
  }));
  update();
}
