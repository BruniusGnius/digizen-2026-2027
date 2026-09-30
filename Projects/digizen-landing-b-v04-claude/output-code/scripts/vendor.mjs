// Copia GSAP (versión fijada en package.json: la misma del wireframe aprobado) a assets/vendor/.
// La página no depende de un CDN en producción.
import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const src = join(root, 'node_modules', 'gsap', 'dist');
const out = join(root, 'assets', 'vendor');
mkdirSync(out, { recursive: true });
for (const f of ['gsap.min.js', 'ScrollTrigger.min.js', 'ScrollToPlugin.min.js']) {
  copyFileSync(join(src, f), join(out, f));
  console.log('vendor →', join('assets', 'vendor', f));
}
