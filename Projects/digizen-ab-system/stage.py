#!/usr/bin/env python3
"""Crea artefactos LOCALES de publicación. Nunca conecta ni escribe en Hostinger."""
from pathlib import Path
import shutil
import re
import hashlib

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
STAGE = HERE / 'staging'
A = ROOT / 'Projects/digizen-landing/angular-build/dist/angular-build/browser'
B = ROOT / 'Projects/digizen-landing-b-v04-claude/output-code'


def inject(text: str, variant: str) -> str:
    version = hashlib.sha256((HERE / 'frontend/digizen-ab.js').read_bytes()).hexdigest()[:12]
    script = f'<script defer src="/{variant}/digizen-ab.js?v={version}"></script>'
    if '</head>' not in text:
        raise SystemExit('El HTML no tiene </head>')
    text = text.replace('</head>', script + '\n</head>', 1)
    return text


def canonical(text: str, url: str) -> str:
    return re.sub(r'<link rel="canonical" href="[^"]*"\s*/?>',
                  f'<link rel="canonical" href="{url}">', text, count=1)


def stage() -> None:
    if not A.is_dir() or not (B / 'index.html').is_file():
        raise SystemExit('Faltan builds de A o B. Ejecuta los comandos de build del README.')
    if STAGE.exists():
        shutil.rmtree(STAGE)
    (STAGE / 'a').mkdir(parents=True)
    (STAGE / 'b').mkdir(parents=True)
    shutil.copytree(A, STAGE / 'a', dirs_exist_ok=True)
    a_index = STAGE / 'a/index.html'
    a_html = a_index.read_text()
    if '<base href="/a/"' not in a_html:
        raise SystemExit('El build A requiere --base-href /a/.')
    a_html = a_html.replace('https://digizen.gnius.club/assets/', 'https://digizen.gnius.club/a/assets/')
    a_html = a_html.replace('<meta property="og:url" content="https://digizen.gnius.club/"',
                            '<meta property="og:url" content="https://digizen.gnius.club/a/"')
    a_index.write_text(inject(canonical(a_html, 'https://digizen.gnius.club/a/'), 'a'))
    rules_a = STAGE / 'a/reglas-de-ada'
    rules_a.mkdir()
    rules_a_html = a_html.replace('<meta property="og:url" content="https://digizen.gnius.club/a/"',
                                  '<meta property="og:url" content="https://digizen.gnius.club/a/reglas-de-ada/"')
    (rules_a / 'index.html').write_text(inject(canonical(rules_a_html, 'https://digizen.gnius.club/a/reglas-de-ada/'), 'a'))
    shutil.copy2(HERE / 'frontend/digizen-ab.js', STAGE / 'a/digizen-ab.js')

    for directory in ['assets', 'dist', 'js']:
        shutil.copytree(B / directory, STAGE / 'b' / directory)
    shutil.copy2(HERE / 'frontend/digizen-ab.js', STAGE / 'b/digizen-ab.js')
    for source, target, url in [
        (B / 'index.html', STAGE / 'b/index.html', 'https://digizen.gnius.club/b/'),
        (B / 'reglas-de-ada.html', STAGE / 'b/reglas-de-ada/index.html', 'https://digizen.gnius.club/b/reglas-de-ada/'),
    ]:
        target.parent.mkdir(parents=True, exist_ok=True)
        html = source.read_text()
        html = html.replace('reglas-de-ada.html', '/b/reglas-de-ada/')
        html = html.replace('https://bruniusgnius.github.io/digizen-2026-2027/b-v04-claude/', 'https://digizen.gnius.club/b/')
        html = canonical(html, url)
        # El <base> debe preceder a cualquier URL relativa (CSS, fuentes, imágenes).
        html = html.replace('<head>', '<head>\n<base href="/b/">', 1)
        target.write_text(inject(html, 'b'))

    (STAGE / 'index.html').write_text((HERE / 'router/index.html').read_text())
    demo = STAGE / 'demo-ada-confirmado'
    demo.mkdir()
    shutil.copy2(HERE / 'frontend/demo-ada-confirmado.html', demo / 'index.html')
    api = STAGE / 'api'
    shutil.copytree(HERE / 'api/public', api)
    admin = STAGE / 'conversion-admin'
    shutil.copytree(HERE / 'api/admin', admin)
    print('Artefactos locales creados en', STAGE)
    print('No se ha conectado a Hostinger ni publicado nada.')


if __name__ == '__main__':
    stage()
