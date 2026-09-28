# -*- coding: utf-8 -*-
"""
Convierte un video en una secuencia de cuadros WebP optimizada para scrub con el scroll.
Uso (desde la carpeta del proyecto):
    python3 wireframe-src/make_seq.py <video> <nombre> [--frames 49] [--width 1280] [--poster N] [--quality 62]
Salida: assets/seq/<nombre>/f001.webp … fNNN.webp  +  assets/seq/<nombre>/<nombre>-poster.webp
- Toma cuadros repartidos de forma pareja en todo el video (49 por defecto ≈ uno de cada dos en 4 s a 24 fps).
- WebP calidad 62 (secuencia) y 70 (póster). Con 1280 px y 49 cuadros, ~3 MB.
- --poster: número de cuadro del video original (base 0) para el póster; por defecto, el del medio.
Requiere ffmpeg y Pillow. (Este ffmpeg no trae libwebp: se extraen PNG y se codifican con Pillow.)
"""
import argparse, glob, os, shutil, subprocess, sys, tempfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('video'); ap.add_argument('nombre')
    ap.add_argument('--frames', type=int, default=49)
    ap.add_argument('--width', type=int, default=1280)
    ap.add_argument('--poster', type=int, default=None)
    ap.add_argument('--quality', type=int, default=62)
    a = ap.parse_args()
    out = os.path.join(ROOT, 'assets', 'seq', a.nombre)
    os.makedirs(out, exist_ok=True)
    for f in glob.glob(os.path.join(out, '*.webp')): os.remove(f)
    tmp = tempfile.mkdtemp()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a.video, '-vf', f'scale={a.width}:-2:flags=lanczos',
                    os.path.join(tmp, 's%04d.png')], check=True)
    src = sorted(glob.glob(os.path.join(tmp, 's*.png')))
    if not src: sys.exit('No se extrajeron cuadros.')
    n = min(a.frames, len(src))
    idx = [round(i * (len(src) - 1) / (n - 1)) for i in range(n)] if n > 1 else [0]
    tot = 0
    for k, i in enumerate(idx, 1):
        d = os.path.join(out, f'f{k:03d}.webp')
        Image.open(src[i]).convert('RGB').save(d, 'WEBP', quality=a.quality, method=6); tot += os.path.getsize(d)
    p = a.poster if a.poster is not None else len(src) // 2
    p = max(0, min(len(src) - 1, p))
    poster = os.path.join(out, f'{a.nombre}-poster.webp')
    Image.open(src[p]).convert('RGB').save(poster, 'WEBP', quality=70, method=6)
    w, h = Image.open(os.path.join(out, 'f001.webp')).size
    shutil.rmtree(tmp)
    print(f'{a.nombre}: {n} cuadros de {len(src)} · {w}×{h} · {tot/1048576:.1f} MB · póster = cuadro {p}')
    print(f'→ {os.path.relpath(out, ROOT)}/')

if __name__ == '__main__':
    main()
