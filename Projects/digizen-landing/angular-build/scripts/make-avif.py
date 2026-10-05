# -*- coding: utf-8 -*-
"""Versiones AVIF de las imágenes que ya se publican en WebP, sin tocar los WebP ni los originales.

Uso (desde angular-build/):   python3 scripts/make-avif.py

Regla del proyecto: nunca perder calidad sin tener el original. Por eso cada AVIF se compara con su referencia
y solo se conserva si es al menos tan fiel (SSIM) como el WebP que acompaña y pesa menos:

- Escenas dentro de un <picture> de app.html: la referencia es su PNG original (el mismo nombre, en public/).
  Se prueba de menor a mayor calidad y gana la primera que iguala la fidelidad del WebP.
- Cuadros de ADA (assets/digizen/ada-wave): solo existen en WebP, así que su AVIF debe ser casi idéntico a ese
  cuadro (SSIM >= 0.995), con una sola calidad para los 130, calibrada en 5 de muestra.

El WebP queda de respaldo: el <picture> ofrece primero el AVIF y el navegador que no lo entiende toma el WebP.
Lo que se generó, con qué calidad y cuánto pesa queda en scripts/avif-report.json.
Requiere Pillow (con AVIF) y numpy.
"""
import json, os, re, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, 'public')
REPORT = os.path.join(ROOT, 'scripts', 'avif-report.json')
SCENE_QS = (44, 48, 52, 56, 60, 64, 68, 72, 76)   # de menor a mayor calidad
ADA_QS = (44, 48, 52, 56, 60, 65, 70)
ADA_MIN_SSIM = 0.995
MIN_GAIN = 0.95                                    # el AVIF debe pesar como máximo el 95 % del WebP
PAGE_BG = (246, 248, 251)                          # --dg-canvas: sobre él se compara lo que lleva transparencia


def ssim(a, b, win=8):
    """Fidelidad estructural (0–1) sobre la luminancia, en bloques de 8 px."""
    def luma(im):
        x = np.asarray(im.convert('RGB'), dtype=np.float64)
        return 0.299 * x[..., 0] + 0.587 * x[..., 1] + 0.114 * x[..., 2]
    x, y = luma(a), luma(b)
    h, w = x.shape
    h -= h % win
    w -= w % win
    blocks = lambda z: z[:h, :w].reshape(h // win, win, w // win, win).swapaxes(1, 2).reshape(-1, win * win)
    X, Y = blocks(x), blocks(y)
    mx, my, vx, vy = X.mean(1), Y.mean(1), X.var(1), Y.var(1)
    cxy = ((X - mx[:, None]) * (Y - my[:, None])).mean(1)
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    return float((((2 * mx * my + c1) * (2 * cxy + c2)) / ((mx ** 2 + my ** 2 + c1) * (vx + vy + c2))).mean())


def flat(im):
    if im.mode != 'RGBA':
        return im.convert('RGB')
    return Image.alpha_composite(Image.new('RGBA', im.size, PAGE_BG + (255,)), im).convert('RGB')


def keep_alpha(im):
    return im.convert('RGBA') if im.mode in ('RGBA', 'LA', 'P') else im.convert('RGB')


def scenes_in_pictures():
    html = open(os.path.join(ROOT, 'src', 'app', 'app.html'), encoding='utf-8').read()
    out = []
    for block in re.findall(r'<picture>.*?</picture>', html, flags=re.S):
        for url in re.findall(r'(?:srcset|src)="([^"]+\.webp)"', block):
            if url not in out:
                out.append(url)
    return out


def main():
    report = {}
    print('== escenas ==')
    for url in scenes_in_pictures():
        webp = os.path.join(PUBLIC, url)
        png = webp[:-5] + '.png'
        avif = webp[:-5] + '.avif'
        cur = Image.open(webp)
        if os.path.exists(png) and Image.open(png).size == cur.size:
            ref = keep_alpha(Image.open(png))
            bar = ssim(flat(ref), flat(cur))
            source = 'png'
        else:   # sin original del mismo tamaño: la referencia es el propio WebP publicado
            ref = keep_alpha(cur)
            bar = 0.985
            source = 'webp'
        limit = os.path.getsize(webp) * MIN_GAIN
        chosen = None
        for q in SCENE_QS:
            ref.save(avif, 'AVIF', quality=q, speed=4)
            got = ssim(flat(ref), flat(Image.open(avif)))
            if got >= bar:
                if os.path.getsize(avif) <= limit:
                    chosen = (q, got)
                break
        if not chosen and os.path.exists(avif):
            os.remove(avif)
        report[url] = {'webp': os.path.getsize(webp), 'avif': os.path.getsize(avif) if chosen else None,
                       'q': chosen[0] if chosen else None, 'ssim_avif': round(chosen[1], 4) if chosen else None,
                       'ssim_webp': round(bar, 4) if source == 'png' else None, 'referencia': source}
        r = report[url]
        print(f"  {os.path.basename(url):52s} " + (f"WebP {r['webp'] // 1024:4d} KB -> AVIF {r['avif'] // 1024:4d} KB · q{r['q']} · {r['ssim_avif']} vs {r['ssim_webp']}" if chosen else 'sin AVIF (no mejora al WebP)'))

    print('== ADA ==')
    d = os.path.join(PUBLIC, 'assets', 'digizen', 'ada-wave')
    frames = [f for f in sorted(os.listdir(d)) if re.fullmatch(r'f\d{3}\.webp', f)]
    sample = [frames[round(i * (len(frames) - 1) / 4)] for i in range(5)]
    q_ada = None
    tmp = os.path.join(d, '_cal.avif')
    for q in ADA_QS:
        ok = True
        for f in sample:
            ref = keep_alpha(Image.open(os.path.join(d, f)))
            ref.save(tmp, 'AVIF', quality=q, speed=4)
            if ssim(flat(ref), flat(Image.open(tmp))) < ADA_MIN_SSIM:
                ok = False
                break
        if ok:
            q_ada = q
            break
    if os.path.exists(tmp):
        os.remove(tmp)
    if q_ada:
        for f in frames:
            keep_alpha(Image.open(os.path.join(d, f))).save(os.path.join(d, f[:-5] + '.avif'), 'AVIF', quality=q_ada, speed=4)
        webp = sum(os.path.getsize(os.path.join(d, f)) for f in frames)
        avif = sum(os.path.getsize(os.path.join(d, f[:-5] + '.avif')) for f in frames)
        report['assets/digizen/ada-wave'] = {'frames': len(frames), 'q': q_ada, 'webp': webp, 'avif': avif}
        print(f'  {len(frames)} cuadros · WebP {webp / 1048576:.2f} MB -> AVIF {avif / 1048576:.2f} MB · q{q_ada}')
    else:
        report['assets/digizen/ada-wave'] = {'frames': len(frames), 'q': None}
        print('  sin AVIF')
    json.dump(report, open(REPORT, 'w', encoding='utf-8'), indent=1, sort_keys=True)


if __name__ == '__main__':
    sys.exit(main())
