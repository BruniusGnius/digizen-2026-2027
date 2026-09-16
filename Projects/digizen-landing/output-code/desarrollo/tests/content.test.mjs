import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { parseHTML } from 'linkedom';
import { renderPreview } from '../scripts/preview.mjs';
import { validateLead, leadPayload } from '../resources/js/lib/lead.js';

test('16 approved sections retain all non-placeholder text, punctuation and order', async () => {
  const source = parseHTML(await readFile(new URL('../../../Digizen Landing Refinado.dc.html', import.meta.url), 'utf8')).document;
  const result = parseHTML(await renderPreview()).document;
  const original = [...source.querySelector('main').children].filter(node => node.tagName === 'SECTION');
  const built = [...result.querySelector('main').children].filter(node => node.tagName === 'SECTION');
  assert.equal(built.length, original.length);
  const text = node => { const clone = node.cloneNode(true); clone.querySelectorAll('figure, form, svg').forEach(element => element.remove()); return clone.textContent.replace(/\s+/g, ''); };
  original.forEach((section, index) => assert.equal(text(built[index]), text(section), `Section ${index + 1} changed`));
});
test('source ledger remains byte-identical', async () => {
  assert.equal(await readFile(new URL('../docs/copy-fuente-inmutable.md', import.meta.url), 'utf8'), await readFile(new URL('../../../00-context/digizen-copy-ola.md', import.meta.url), 'utf8'));
});
test('refined tokens are preserved byte-for-byte', async () => {
  const current = await readFile(new URL('../resources/css/tokens.css', import.meta.url), 'utf8');
  const source = await readFile(new URL('../../../../../creador de landings/insumos/sistema-diseno-refinado/tokens.css', import.meta.url), 'utf8');
  assert.equal(current, source);
});
test('contact validation accepts names and international phones without imposing Spanish-only characters', () => {
  assert.deepEqual(validateLead({ parent_name: 'María José', channel: 'email', contact: 'maria@example.com' }), {});
  assert.deepEqual(validateLead({ parent_name: '李明', channel: 'whatsapp', contact: '+52 (55) 1234-5678' }), {});
  assert.ok(validateLead({ parent_name: '1', channel: 'email', contact: 'bad@' }).parent_name);
  assert.ok(validateLead({ parent_name: 'Ana', channel: 'whatsapp', contact: '5512345678' }).contact);
  assert.ok(validateLead({ parent_name: 'Ana', channel: 'email', contact: 'a@b' }).contact);
});
test('backend payload contains only expected fields and normalized contact', () => {
  assert.deepEqual(leadPayload({ parent_name: ' Ana ', channel: 'whatsapp', contact: '+52 (55) 1234-5678' }), { parent_name: 'Ana', channel: 'whatsapp', contact: '+525512345678', source: 'digizen_landing' });
});
