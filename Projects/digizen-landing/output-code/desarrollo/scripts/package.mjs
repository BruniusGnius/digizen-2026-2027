import { cp, mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
const destination = path.resolve(root, '../produccion/laravel');
await mkdir(destination, { recursive: true });
for (const directory of ['resources/views', 'config', 'public/build']) {
  await cp(path.join(root, directory), path.join(destination, directory), { recursive: true });
}
await writeFile(path.resolve(root, '../produccion/LEEME.md'), `# Entrega de frontend DIGIZEN\n\n- laravel/: vistas Blade, configuración y public/build con manifest Vite. Integrar dentro de una aplicación Laravel; NO es una aplicación PHP independiente. El document root de Laravel es public/.\n- preview/: demostración estática compilada del mismo contenido; no envía datos ni realiza pagos. Servir por HTTP con npm run preview desde desarrollo/.\n- Los fuentes editables y el contrato de backend están en desarrollo/.\n- Las fotos Picsum son temporales y requieren conexión a Internet.\n- Compilación generada: ${new Date().toISOString()}.\n`);
