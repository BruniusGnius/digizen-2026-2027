#!/usr/bin/env python3
"""Detecta recursos locales faltantes respetando el orden real de <base>."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
import re
import sys

ROOT = Path(__file__).resolve().parent / 'staging'
ORIGIN = 'https://digizen.gnius.club'


class References(HTMLParser):
    def __init__(self, page: Path):
        super().__init__()
        self.base = ORIGIN + '/' + page.relative_to(ROOT).as_posix()
        self.references: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == 'base' and values.get('href'):
            self.base = urljoin(self.base, values['href'])
        if tag in ('script', 'img', 'source', 'video', 'audio') and values.get('src'):
            self.references.append((values['src'], self.base))
        if tag == 'link' and values.get('href') and values.get('rel') in ('stylesheet', 'icon', 'preload'):
            self.references.append((values['href'], self.base))
        for key in ('srcset', 'imagesrcset'):
            if values.get(key):
                self.references.extend((entry.strip().split()[0], self.base)
                                       for entry in values[key].split(',') if entry.strip())


def local_file(reference: str, base: str) -> Path | None:
    parsed = urlparse(urljoin(base, reference))
    if parsed.netloc != urlparse(ORIGIN).netloc or not parsed.path:
        return None
    candidate = ROOT / parsed.path.lstrip('/')
    return candidate / 'index.html' if parsed.path.endswith('/') else candidate


def main() -> int:
    missing: list[str] = []
    html_count = 0
    reference_count = 0
    for page in ROOT.rglob('*.html'):
        parser = References(page)
        parser.feed(page.read_text())
        html_count += 1
        for reference, base in parser.references:
            file = local_file(reference, base)
            if file is None:
                continue
            reference_count += 1
            if not file.is_file():
                missing.append(f'{page.relative_to(ROOT)} -> {reference} -> {file.relative_to(ROOT)}')
    for css in ROOT.rglob('*.css'):
        text = css.read_text()
        base = ORIGIN + '/' + css.relative_to(ROOT).as_posix()
        for reference in re.findall(r'url\([\'\"]?([^\)\'\"]+)', text):
            file = local_file(reference, base)
            if file is None or reference.startswith('data:'):
                continue
            reference_count += 1
            if not file.is_file():
                missing.append(f'{css.relative_to(ROOT)} -> {reference} -> {file.relative_to(ROOT)}')
    print(f'HTML: {html_count}; referencias locales: {reference_count}; faltantes: {len(missing)}')
    for item in missing[:50]:
        print(item)
    return 1 if missing else 0


if __name__ == '__main__':
    sys.exit(main())
