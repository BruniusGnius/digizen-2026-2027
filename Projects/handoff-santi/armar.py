# -*- coding: utf-8 -*-
"""Arma la copia de handoff de las landings A y B (repositorio digizen-a-b-handoff-santi).

Uso (desde la raíz del proyecto):   python3 Projects/handoff-santi/armar.py [carpeta-destino]

Destino por defecto: la carpeta vecina del proyecto, ../digizen-a-b-handoff-santi.

Qué lleva y de dónde sale:
- landing-a/ .......... Projects/digizen-landing/angular-build, tal como está en el último commit (HEAD),
                        sin respaldos ni lo que la propia landing excluye al publicar (PNG, PSD, video fuente).
- landing-b/ .......... Projects/digizen-landing-b-v04-claude/output-code del último commit, sin las páginas de prueba.
- README.md ........... el README.md de esta carpeta, más una línea con el commit de origen.

El sistema de diseño no va en esta copia: el usuario lo quitó el 5 de octubre de 2026 porque puede confundir.

Solo LEE el proyecto. En el destino reemplaza esas dos carpetas y el README; no toca nada más (ni .git).
"""
import datetime, fnmatch, io, json, os, shutil, subprocess, sys, tarfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, '..', '..'))
A = 'Projects/digizen-landing/angular-build'
B = 'Projects/digizen-landing-b-v04-claude/output-code'
MARCA = '.handoff-generado'          # el destino se reconoce por este archivo: sin él no se reemplaza nada
PARTES = ['landing-a', 'landing-b']
MESES = 'enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre'.split()


def git(*args):
    return subprocess.run(['git', '-C', RAIZ, *args], check=True, capture_output=True).stdout


def extraer(ruta, destino, fuera):
    """Copia una carpeta del último commit a `destino`, saltando lo que `fuera(relativa)` marque."""
    n = 0
    with tarfile.open(fileobj=io.BytesIO(git('archive', 'HEAD', ruta))) as tar:
        for m in tar.getmembers():
            if not m.isfile(): continue
            rel = os.path.relpath(m.name, ruta).replace(os.sep, '/')
            if rel.endswith('.DS_Store') or fuera(rel): continue
            dst = os.path.join(destino, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with tar.extractfile(m) as f, open(dst, 'wb') as g: shutil.copyfileobj(f, g)
            n += 1
    return n


def excluye_a():
    """Lo mismo que la landing A deja fuera al publicar: la lista `ignore` de su angular.json."""
    cfg = json.loads(git('show', f'HEAD:{A}/angular.json'))
    build = list(cfg['projects'].values())[0]['architect']['build']['options']
    patrones = [p for a in build['assets'] if isinstance(a, dict) for p in a.get('ignore', [])]

    def fuera(rel):
        if rel.startswith(('asset-backups/', '.vscode/')): return True
        if not rel.startswith('public/'): return False
        partes = rel.split('/')
        for p in patrones:
            p = p[3:] if p.startswith('**/') else p
            if p.endswith('/**'):
                if p[:-3] in partes[:-1]: return True
            elif fnmatch.fnmatch(partes[-1], p): return True
        return False
    return fuera


def pesa(carpeta):
    n = t = 0; mayor = (0, '')
    for d, _, fs in os.walk(carpeta):
        for f in fs:
            s = os.path.getsize(os.path.join(d, f)); n += 1; t += s
            if s > mayor[0]: mayor = (s, os.path.relpath(os.path.join(d, f), carpeta))
    return n, t, mayor


def main():
    destino = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.normpath(os.path.join(RAIZ, '..', 'digizen-a-b-handoff-santi'))
    if os.path.isdir(destino) and os.listdir(destino) and not os.path.exists(os.path.join(destino, MARCA)):
        sys.exit(f'ALTO · {destino} ya tiene contenido y no es una copia de handoff (falta {MARCA}). No se tocó nada.')
    os.makedirs(destino, exist_ok=True)
    for p in PARTES: shutil.rmtree(os.path.join(destino, p), ignore_errors=True)

    na = extraer(A, os.path.join(destino, 'landing-a'), excluye_a())
    nb = extraer(B, os.path.join(destino, 'landing-b'), lambda rel: '/' not in rel and rel.endswith('.html') and rel.startswith(('prueba', 'archivo-')))

    commit = git('rev-parse', '--short', 'HEAD').decode().strip()
    hoy = datetime.date.today()
    leeme = open(os.path.join(AQUI, 'README.md'), encoding='utf-8').read().rstrip('\n')
    leeme += f'\n\n---\n\nCopia generada el {hoy.day} de {MESES[hoy.month - 1]} de {hoy.year} desde el commit `{commit}` del repositorio de trabajo.\n'
    open(os.path.join(destino, 'README.md'), 'w', encoding='utf-8').write(leeme)
    open(os.path.join(destino, '.gitignore'), 'w', encoding='utf-8').write('node_modules/\nlanding-a/dist/\n.angular/\n.DS_Store\n')   # landing-b/dist/ SÍ va: es su hoja de estilos compilada
    open(os.path.join(destino, MARCA), 'w', encoding='utf-8').write('Carpeta generada por Projects/handoff-santi/armar.py del repositorio de trabajo. No editar a mano.\n')

    total = 0
    for p in PARTES:
        n, t, (ms, mf) = pesa(os.path.join(destino, p)); total += t
        print(f'{p:20s} {n:5d} archivos · {t / 1048576:6.1f} MB · mayor: {mf} ({ms / 1048576:.1f} MB)')
    print(f'total {total / 1048576:.1f} MB · origen {commit} · destino {destino}')
    if (na, nb) == (0, 0): sys.exit('ALTO · no se copió nada de las landings')
    # comprobación: nada de lo copiado debe quedar fuera de git por culpa del .gitignore
    if os.path.isdir(os.path.join(destino, '.git')):
        r = subprocess.run(['git', '-C', destino, 'ls-files', '--others', '--ignored', '--exclude-standard', '--', *PARTES], capture_output=True, text=True)
        fuera = [f for f in r.stdout.split('\n') if f and 'node_modules/' not in f and '/.angular/' not in f and not f.startswith('landing-a/dist/')]
        if fuera: sys.exit(f'ALTO · git dejaría fuera {len(fuera)} archivos de la copia: {fuera[:5]}')
        print('git: ningún archivo de la copia queda ignorado')


if __name__ == '__main__':
    main()
