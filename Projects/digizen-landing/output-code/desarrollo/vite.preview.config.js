import { defineConfig } from 'vite';
import { renderPreview } from './scripts/preview.mjs';

export default defineConfig({
  base: './',
  plugins: [{
    name: 'digizen-blade-preview',
    configureServer(server) {
      server.watcher.add('resources/views/**/*.blade.php');
      server.watcher.on('change', async (path) => {
        if (!path.endsWith('.blade.php')) return;
        await renderPreview();
        server.ws.send({ type: 'full-reload' });
      });
    },
  }],
  build: { outDir: '../produccion/preview', emptyOutDir: false, sourcemap: false },
});
