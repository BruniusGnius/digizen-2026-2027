#!/usr/bin/env python3
"""Prepara un paquete local aislado para digizen-demo.gnius.club; no publica nada."""
from pathlib import Path
import shutil
import re
import hashlib
import zipfile
import argparse
import stage

HERE = Path(__file__).resolve().parent
PACKAGE = HERE / 'preview-package'
ORIGIN = 'https://digizen-demo.gnius.club'
PRODUCTION = 'https://digizen.gnius.club'
BANNER = ('<div role="status" style="position:relative;z-index:2147483647;'
          'padding:10px 16px;text-align:center;background:#ffe18a;color:#171717;'
          'font:600 14px/1.4 system-ui">DIGIZEN · sitio de prueba. '
          'Usa datos ficticios; pagos y acceso real a ADA aún no están activos.</div>')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--real-api', action='store_true', help='Usa PHP/MySQL real en el subdominio de pruebas')
    args = parser.parse_args()
    stage.stage()
    if PACKAGE.exists():
        shutil.rmtree(PACKAGE)
    public = PACKAGE / 'public'
    private = PACKAGE / 'private'
    shutil.copytree(stage.STAGE, public)
    shutil.copytree(HERE / 'api/src', private / 'src')
    (private / 'config').mkdir(parents=True)
    shutil.copy2(HERE / 'api/config/secrets.preview.example.php', private / 'config/secrets.preview.example.php')
    shutil.copy2(HERE / 'api/schema.sql', private / 'schema.sql')

    # La API real requiere código y configuración privados fuera de public_html.
    shutil.rmtree(public / 'api')
    if args.real_api:
        shutil.copytree(HERE / 'api/public', public / 'api')
        loader = public / 'api/_load.php'
        loader.write_text(loader.read_text().replace(
            '/home/u502287134/digizen-conversion-api',
            '/home/u502287134/digizen-conversion-api-preview'))
    else:
        shutil.copytree(HERE / 'api/preview-public', public / 'api')
    shutil.rmtree(public / 'conversion-admin')

    for file in public.rglob('*'):
        if file.is_file() and file.suffix in ('.html', '.xml', '.txt'):
            data = file.read_text()
            data = data.replace(PRODUCTION, ORIGIN)
            if file.suffix == '.html' and '<head>' in data:
                data = data.replace('<head>', '<head>\n<meta name="robots" content="noindex,nofollow,noarchive">', 1)
                if '<body' in data and file != public / 'index.html':
                    data = re.sub(r'(<body[^>]*>)', r'\1' + BANNER, data, count=1)
            file.write_text(data)
    for relative in ('a/sitemap.xml', 'a/robots.txt', 'a/llms.txt'):
        (public / relative).unlink(missing_ok=True)
    shutil.rmtree(public / 'a/ai-context', ignore_errors=True)
    (public / 'robots.txt').write_text('User-agent: *\nDisallow: /\n')
    archive = PACKAGE / 'digizen-demo-public.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for file in sorted(public.rglob('*')):
            if file.is_file():
                z.write(file, file.relative_to(public))
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    print('Paquete local de pruebas:', PACKAGE)
    print('public/ usa API real de QA.' if args.real_api else 'public/ usa API simulada sin MySQL ni Acumbamail.')
    print('private/ requiere despliegue separado fuera de public_html.' if args.real_api else 'private/ es una preparación futura.')
    print('ZIP público:', archive, 'SHA256:', digest)
    print('No se ha modificado Hostinger.')


if __name__ == '__main__':
    main()
