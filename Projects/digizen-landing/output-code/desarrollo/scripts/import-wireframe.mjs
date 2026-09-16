// One-time, mechanical migration. The approved reference is read only.
// Run once; afterward the Blade views are the editable source of the frontend.
import { parseHTML } from 'linkedom';
import { readFile, writeFile, mkdir, access } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
const project = path.resolve(root, '../..');
const workspace = path.resolve(project, '../..');
const target = path.join(root, 'resources/views/landing.blade.php');
try { await access(target); throw new Error('Migration already applied. Edit the existing Blade views.'); } catch (error) { if (error.code !== 'ENOENT') throw error; }
const source = await readFile(path.join(project, 'Digizen Landing Refinado.dc.html'), 'utf8');
const { document } = parseHTML(source);
const originalCss = document.querySelector('style').textContent;
const main = document.querySelector('main');
const nav = document.querySelector('nav');
const names = ['hero', 'beat-1', 'beat-2', 'decision-early', 'beat-3', 'beat-4', 'beat-5', 'safety', 'decision-trust', 'beat-6', 'founders', 'offer', 'payment-options', 'closure', 'decision-final', 'faq-legal'];
const sections = [...main.children].filter(element => element.tagName === 'SECTION');
if (sections.length !== names.length) throw new Error('Unexpected section topology');
main.id = 'main-content';
main.tabIndex = -1;
main.classList.add('dg-main');
sections.forEach((section, index) => { section.dataset.block = names[index]; section.classList.add('landing-section'); });
sections[13].removeAttribute('aria-labelledby');
sections[13].setAttribute('aria-label', 'Decisión y garantía');

// Preserve the current closed state of all four evidence accordions.
const imageSlots = [];
let figureIndex = 0;
for (const figure of main.querySelectorAll('figure')) {
  if (figure.closest('.ada-product-composite')) { figure.classList.add('ada-preview'); continue; }
  const block = figure.closest('[data-block]').dataset.block;
  const ratioMatch = figure.getAttribute('style').match(/aspect-ratio:([^;]+)/);
  const ratio = ratioMatch?.[1] || '4/5';
  const [x, y = x] = ratio.split('/').map(Number);
  const width = x === y ? 900 : x === 4 && y === 3 ? 1200 : 800;
  const height = Math.round(width * y / x);
  const seed = `digizen-${block}-${++figureIndex}`;
  const horizontal = ['beat-1', 'beat-2', 'beat-4'].includes(block);
  imageSlots.push({ block, seed, ratio, desktop: [width, height], horizontal: horizontal ? [1280, 720] : null, originalLabel: figure.textContent.trim(), temporary: true });
  figure.classList.add('narrative-image');
  figure.innerHTML = `<picture>${horizontal ? `<source media="(max-width: 1023px)" srcset="https://picsum.photos/seed/${seed}-horizontal/1280/720">` : ''}<img src="https://picsum.photos/seed/${seed}/${width}/${height}" width="${width}" height="${height}" alt="" ${block === 'hero' ? 'fetchpriority="high" loading="eager"' : 'loading="lazy"'} decoding="async"></picture>`;
}

// Add functional hooks without changing labels or order.
for (const button of main.querySelectorAll('button')) {
  if (button.closest('form')) continue;
  const isAda = /ADA/.test(button.textContent);
  button.dataset.action = isAda ? 'ada' : 'checkout';
  if (!isAda) {
    const card = button.closest('.pricing-card');
    const cards = [...document.querySelectorAll('.pricing-card')];
    button.dataset.plan = card ? ['monthly', 'cycle', 'cash'][cards.indexOf(card)] : 'cycle';
  }
  button.classList.add('dg-button');
  if (isAda && !button.classList.contains('cta-decision__primary')) button.classList.add('dg-button--secondary');
  if (button.classList.contains('cta-decision__secondary')) button.classList.add('dg-button--on-dark-secondary');
  if (button.classList.contains('cta-decision__primary') || button.closest('.pricing-card--featured')) button.classList.add('dg-button--on-dark');
}

// Visual signatures from the refined reference, mapped onto EXISTING cards.
const icons = [
  '<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 018 0v3"/>',
  '<path d="M3 12h4l3-7 4 14 3-7h4"/>',
  '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  '<path d="M12 3l8 3v6c0 5-8 9-8 9s-8-4-8-9V6z"/><path d="M8 12l3 3 5-6"/>',
];
for (const [index, card] of [...main.querySelectorAll('.safety-guard-grid article')].entries()) {
  card.classList.add('principle-card', `principle-card--${['privacy', 'ada', 'conversation', 'care'][index]}`);
  const label = card.firstElementChild;
  label.classList.add('guard-label');
  card.insertAdjacentHTML('afterbegin', `<span class="dg-principle-icon" aria-hidden="true"><svg viewBox="0 0 24 24">${icons[index]}</svg></span>`);
}
for (const [index, card] of [...main.querySelectorAll('[data-block="founders"] article, [data-block="offer"] article')].entries()) {
  card.classList.add('principle-card', `principle-card--${['ada', 'privacy', 'conversation'][index % 3]}`);
}

// Class extraction preserves the approved dimensions and responsive grouping.
const declarations = new Map();
let ruleIndex = 0;
for (const element of [...nav.querySelectorAll('*'), nav, ...main.querySelectorAll('*'), main]) {
  const inline = element.getAttribute('style');
  if (!inline) continue;
  if (inline.includes('display:flex') && inline.includes('flex-wrap:wrap')) element.classList.add('wf-wrap');
  if (inline.includes('min-width:')) element.classList.add('wf-min');
  if (!declarations.has(inline)) declarations.set(inline, `wf-${++ruleIndex}`);
  element.classList.add(declarations.get(inline));
  element.removeAttribute('style');
  element.removeAttribute('style-hover');
}
const literalColors = {
  '#F2F4F7': '--dg-canvas', '#F6F8FB': '--dg-canvas', '#F0F4F8': '--dg-surface-end', '#fff': '--dg-raised', '#ffffff': '--dg-raised',
  '#152033': '--dg-ink', '#617085': '--dg-muted', '#8B98AA': '--dg-soft', '#A0AEBB': '--dg-muted', '#E8EDF3': '--dg-line', '#DFE7EE': '--dg-line', '#EEF2F6': '--dg-subtle', '#C8D4DF': '--dg-line-strong',
};
function colorTokens(css) {
  for (const [hex, token] of Object.entries(literalColors)) css = css.replace(new RegExp(`${hex}(?![a-fA-F0-9])`, 'gi'), `var(${token})`);
  return css;
}
const literalValues = new Map();
function extractTokens(body) {
  return body.replace(/([\w-]+)\s*:\s*([^;{}]+)(?=[;}])/g, (all, property, raw) => {
    let value = colorTokens(raw.trim());
    if (!/(\d(?:px|rem|em|ch|vw|vh|%)|rgba?\(|clamp\(|#[a-f\d])/i.test(value)) return `${property}:${value}`;
    const important = value.endsWith('!important');
    value = value.replace(/\s*!important$/, '');
    const key = `${property}:${value}`;
    if (!literalValues.has(key)) literalValues.set(key, { name: `--dg-layout-${literalValues.size + 1}`, value });
    return `${property}:var(${literalValues.get(key).name})${important ? ' !important' : ''}`;
  });
}
let layoutCss = colorTokens(originalCss)
  .replace('main div[style*="display:flex"][style*="flex-wrap:wrap"]', 'main .wf-wrap')
  .replaceAll('main div[style*="min-width:"]', 'main div.wf-min')
  .replaceAll('main figure[style*="min-width:"]', 'main figure.wf-min');
layoutCss = extractTokens(layoutCss);
for (const [inline, className] of declarations) layoutCss += `\n.${className}{${extractTokens(inline + (inline.endsWith(';') ? '' : ';'))}}`;
const geometryTokens = `/* Geometry extracted from the approved wireframe; centralized, not redesigned. */\n:root {\n${[...literalValues.values()].map(({ name, value }) => `  ${name}: ${value};`).join('\n')}\n}\n`;

const directories = ['resources/views/landing/sections', 'resources/views/components/digizen', 'resources/css', 'docs'];
for (const directory of directories) await mkdir(path.join(root, directory), { recursive: true });
const form = main.querySelector('form');
form.outerHTML = '<div data-form-include></div>';
for (const [index, section] of sections.entries()) {
  await writeFile(path.join(root, `resources/views/landing/sections/${names[index]}.blade.php`), section.outerHTML.replace('<div data-form-include=""></div>', "@include('components.digizen.ada-form')") + '\n');
}
await writeFile(path.join(root, 'resources/views/components/digizen/navigation.blade.php'), nav.outerHTML + '\n');
await writeFile(target, `@extends('layouts.landing')\n@section('content')\n@include('components.digizen.navigation')\n${main.cloneNode(false).outerHTML.replace('</main>', '')}\n${names.map(name => `@include('landing.sections.${name}')`).join('\n')}\n</main>\n@include('components.digizen.dialogs')\n@endsection\n`);
await writeFile(path.join(root, 'resources/css/wireframe-tokens.css'), geometryTokens);
await writeFile(path.join(root, 'resources/css/wireframe.css'), `/* Approved layout, mechanically extracted. Visual skin in components.css. */\n${layoutCss}\n`);
await writeFile(path.join(root, 'resources/css/tokens.css'), await readFile(path.join(workspace, 'creador de landings/insumos/sistema-diseno-refinado/tokens.css'), 'utf8'));
await writeFile(path.join(root, 'docs/assets.json'), JSON.stringify(imageSlots, null, 2));
await writeFile(path.join(root, 'docs/copy-fuente-inmutable.md'), await readFile(path.join(project, '00-context/digizen-copy-ola.md'), 'utf8'));
console.log(`Imported ${sections.length} sections, ${imageSlots.length} Picsum slots, ${declarations.size} preserved style rules.`);
