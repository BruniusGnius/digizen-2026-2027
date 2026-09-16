import { readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
export async function expandIncludes(content) {
  const pattern = /@include\('([\w.-]+)'\)/g;
  for (const match of [...content.matchAll(pattern)]) {
    const file = path.join(root, 'resources/views', `${match[1].replaceAll('.', '/')}.blade.php`);
    content = content.replace(match[0], await expandIncludes(await readFile(file, 'utf8')));
  }
  return content;
}
export async function renderPreview() {
  let layout = await readFile(path.join(root, 'resources/views/layouts/landing.blade.php'), 'utf8');
  const page = await readFile(path.join(root, 'resources/views/landing.blade.php'), 'utf8');
  const content = page.match(/@section\('content'\)([\s\S]*?)@endsection/)[1];
  layout = layout.replace("@yield('content')", await expandIncludes(content));
  layout = layout.replace(/@vite\([^\n]+\)/, '<link rel="stylesheet" href="/resources/css/app.css"><script type="module" src="/resources/js/app.js"></script>');
  layout = layout.replace('{{ csrf_token() }}', '').replace(/\{!! json_encode\([^\n]+!!\}/, JSON.stringify({ mode: 'preview', leadEndpoint: '', checkout: {} }));
  await writeFile(path.join(root, 'index.html'), layout);
  return layout;
}
if (process.argv[1] === fileURLToPath(import.meta.url)) await renderPreview();
