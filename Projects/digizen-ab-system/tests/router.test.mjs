import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const html = readFileSync(new URL('../router/index.html', import.meta.url), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert.ok(script);
const local = new Map();
const cookies = new Map();
function run(search, random = 0.2) {
  let destination;
  const document = {
    get cookie() { return [...cookies].map(([k, v]) => `${k}=${v}`).join('; '); },
    set cookie(value) { const [k, v] = value.split(';')[0].split('='); cookies.set(k, v); },
  };
  const location = { search, hash: '#prueba', origin: 'https://digizen.gnius.club',
    href: 'https://digizen.gnius.club/' + search,
    replace(url) { destination = url; } };
  const context = { document, location, URL, URLSearchParams,
    localStorage: { getItem: (k) => local.get(k) || null, setItem: (k, v) => local.set(k, v) },
    crypto: { randomUUID: () => '00000000-0000-4000-8000-000000000001' },
    Math: { random: () => random } };
  vm.runInNewContext(script, context);
  return new URL(destination);
}

let url = run('?utm_source=meta&utm_campaign=octubre');
assert.equal(url.pathname, '/a/');
assert.equal(url.searchParams.get('utm_source'), 'meta');
assert.equal(url.searchParams.get('utm_campaign'), 'octubre');
assert.equal(url.searchParams.get('ab_variant'), 'A');
assert.equal(url.hash, '#prueba');
assert.equal(cookies.get('digizen_landing_ab_2026_10_variant'), 'A');
assert.ok(local.get('digizen_landing_ab_2026_10_visitor_id'));

url = run('?utm_medium=cpc', 0.9);
assert.equal(url.pathname, '/a/', 'la variante persiste aunque cambie el azar');
assert.equal(url.searchParams.get('utm_medium'), 'cpc');

url = run('?variant=B&utm_term=ada', 0.2);
assert.equal(url.pathname, '/b/', 'QA puede forzar la variante');
assert.equal(url.searchParams.get('variant'), null);
assert.equal(url.searchParams.get('utm_term'), 'ada');
assert.equal(local.get('digizen_landing_ab_2026_10_variant'), 'B');
cookies.delete('digizen_landing_ab_2026_10_variant');
local.set('digizen_landing_ab_2026_10_variant_expires_at', '1');
url = run('', 0.2);
assert.equal(url.pathname, '/a/', 'una asignación vencida se renueva');
console.log('Router A/B: persistencia, QA, UTM y cookies OK');
