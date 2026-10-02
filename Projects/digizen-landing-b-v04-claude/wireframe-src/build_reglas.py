# -*- coding: utf-8 -*-
"""Wireframe de la página «Las reglas de ADA» (Fase 2 de esta pieza).

Genera 02-wireframe-reglas.html: escala de grises a propósito, con el copy de producción LITERAL en su
bloque para revisar la ocupación real en desktop, tablet y teléfono (la página es responsiva: se abre
en cada tamaño). Las notas de intención van en cajas punteadas y no son copy.

Al final corre la auditoría fuente → artefacto contra 00-context/REGLAS-DE-ADA-fuente-A.html:
las palabras del copy, en el mismo orden, y los textos alternativos de las imágenes.

    python3 -B wireframe-src/build_reglas.py
"""
import html, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import reglas as R

SRC = os.path.join(ROOT, '00-context', 'REGLAS-DE-ADA-fuente-A.html')
OUT = os.path.join(ROOT, '02-wireframe-reglas.html')

e = lambda t: html.escape(t, quote=True)
rich = lambda t: e(t).replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>')   # solo las negritas de la fuente


def ph(spec, label, cls=''):
    """Imagen como caja gris con su proporción real y el nombre del archivo."""
    name, w, h = spec
    return (f"<div class='ph {cls}' style='aspect-ratio:{w}/{h}'><span>{e(label)}<br>{e(name)} · {w} × {h}</span></div>")


def note(bid, text):
    return f"<aside class='wf-note'><b>{bid}</b> {text}</aside>"


def btn(label, kind, what):
    return (f"<span class='wf-btn {kind}' data-copy>{e(label)}</span>"
            f"<span class='wf-act'>→ {what}</span>")


def checks(items, cls, index=False):
    if index:   # la lista completa es también el índice: cada punto lleva a su tarjeta
        lis = ''.join(f"<li><i class='chk'></i><a href='#regla-{i}' data-copy>{e(t)}</a></li>" for i, t in enumerate(items))
    else:
        lis = ''.join(f"<li><i class='chk'></i><span data-copy>{e(t)}</span></li>" for t in items)
    return f"<ul class='checks {cls}'>{lis}</ul>"


def card(i, rule):
    label, title, sub, body = rule
    first = i == 0
    fig = ''
    if first:
        fig = ("<div class='rule-fig'>"
               + ph(R.RULE1_IMAGE['desktop'], 'IMAGEN · desktop', 'only-d')
               + ph(R.RULE1_IMAGE['mobile'], 'IMAGEN · tablet y teléfono', 'only-m')
               + f"<p class='wf-alt'>texto alternativo: «<span data-alt>{e(R.RULE1_IMAGE['alt'])}</span>»</p></div>")
    return (f"<article class='rule{' wide' if first else ''}' id='regla-{i}'>"
            f"<div class='rule-txt'><p class='lab' data-copy>{e(label)}</p><h3 class='scan' data-copy>{e(title)}</h3>"
            f"<p class='sub' data-copy>{e(sub)}</p><p class='body' data-copy>{e(body)}</p></div>{fig}</article>")


def page():
    I, H, C = R.INTRO, R.RULES_HEAD, R.CLOSING
    paras = ''.join(f"<p data-copy>{rich(p)}</p>" for p in I['paras'])
    acts = {'pricing': 'va a las tarjetas de precio de la landing (11.4 en desktop, 11.5m en teléfono)',
            'back': 'regresa a la landing, a la estación de donde se salió (08.5)',
            'ada': 'abre el formulario «Conversar con ADA primero», que nace del botón'}
    b1 = ''.join(f"<div class='wf-b'>{btn(t, 'pri' if k == 'pricing' else 'sec', acts[k])}</div>" for t, k in I['buttons'])
    b3 = ''.join(f"<div class='wf-b'>{btn(t, 'pri' if k == 'pricing' else 'alt', acts[k])}</div>" for t, k in C['buttons'])
    cards = ''.join(card(i, r) for i, r in enumerate(R.RULES))
    notes_int = ''.join(f"<li>{e(n)}</li>" for n in R.NOTES)
    return f"""<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Wireframe · Las reglas de ADA · Digizen B</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..800&display=swap">
<style>
/* Grises a propósito: aquí no se decide color ni estética, solo orden, ocupación y jerarquía. */
:root{{--bg:#f1f1f1;--panel:#fff;--ink:#111;--muted:#666;--line:#c8c8c8;--fill:#dcdcdc;
  --t-small:.8125rem;--t-body:1rem;--t-sub:1.1875rem;--t-head:1.5rem;--t-semi:2.125rem;
  --gap:16px;--pad-x:24px;--w-grid:1180px;--w-wide:42rem}}
@media (min-width:860px){{:root{{--t-small:.875rem;--t-body:1.125rem;--t-sub:1.5rem;--t-head:2rem;--t-semi:3.5rem;--gap:24px;--pad-x:48px}}}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:500 var(--t-body)/1.5 Inter,system-ui,sans-serif}}
p,h1,h2,h3,ul{{margin:0;padding:0}} ul{{list-style:none}}
.wrap{{max-width:var(--w-grid);margin:0 auto;padding:0 var(--pad-x)}}
.wf-top{{background:#111;color:#fff;font:600 12px/1.4 ui-monospace,Menlo,monospace;padding:10px var(--pad-x)}}
.wf-top span{{opacity:.7}}
.wf-note{{display:block;font:500 12px/1.45 ui-monospace,Menlo,monospace;color:#333;border:1px dashed #555;background:#fafafa;padding:8px 10px;margin:14px 0}}
.wf-note b{{background:#111;color:#fff;padding:1px 6px;margin-right:6px}}
.wf-act{{display:block;font:500 11px/1.35 ui-monospace,Menlo,monospace;color:#444;margin-top:4px}}
.wf-alt{{font:500 11px/1.4 ui-monospace,Menlo,monospace;color:#444;margin-top:6px}}
.scan{{box-shadow:-6px 0 0 #111}}   /* lo que se lee en un escaneo de 3 segundos */
@media (min-width:860px){{.only-m{{display:none!important}}}} @media (max-width:859px){{.only-d{{display:none!important}}}}
.ph{{background:repeating-linear-gradient(45deg,var(--fill),var(--fill) 10px,#cfcfcf 10px,#cfcfcf 20px);border:1px solid #999;display:flex;align-items:center;justify-content:center;width:100%}}
.ph span{{background:#fff;border:1px solid #999;font:600 11px/1.4 ui-monospace,Menlo,monospace;padding:4px 8px;text-align:center}}
/* R0 encabezado */
.hdr{{display:flex;justify-content:space-between;align-items:center;padding:20px var(--pad-x)}}
.hdr .logo{{width:120px;height:44px;border:1px solid #999;background:var(--fill);font:600 11px/44px ui-monospace,monospace;text-align:center}}
.hdr .menu{{width:44px;height:44px;border:1px solid #999;background:var(--panel);font:600 18px/42px ui-monospace,monospace;text-align:center}}
section{{padding:28px 0 56px;border-top:1px solid var(--line)}}
.kick{{font-size:var(--t-small);font-weight:700;color:var(--muted)}}
h1{{font-size:var(--t-semi);font-weight:800;line-height:1.05;letter-spacing:-.02em;margin-top:8px}}
h2{{font-size:var(--t-head);font-weight:800;line-height:1.15;letter-spacing:-.015em;margin-top:8px;max-width:26ch}}
h2 span{{display:block;color:var(--muted)}}
/* R1 entrada: el orden del HTML es el del teléfono (texto, imagen, lista, botones) */
.intro{{display:grid;gap:24px;grid-template-areas:"copy" "fig" "list" "acts"}}
.intro .copy{{grid-area:copy}} .intro .fig{{grid-area:fig;justify-self:center;width:min(100%,300px)}}
.intro .list{{grid-area:list}} .intro .acts{{grid-area:acts}}
.intro .copy p{{max-width:var(--w-wide);margin-top:1em;line-height:1.6}}
.checks{{display:grid;gap:10px}} .checks li{{display:flex;align-items:center;gap:10px;font-weight:600}}
.chk{{flex:none;width:22px;height:22px;border:1px solid #777;background:var(--fill)}}
.checks.full{{display:none}} .checks a{{color:inherit;text-underline-offset:3px}}
@media (max-width:599px){{.intro .fig{{width:auto}} .intro .fig .ph{{height:40svh;width:auto}}}}   /* teléfono: la imagen no pasa de 40 % del alto de la pantalla */
.acts{{display:grid;gap:12px}} .wf-b{{max-width:27rem}}
.wf-btn{{display:flex;align-items:center;min-height:56px;padding:12px 20px;border:2px solid #111;font-weight:700;border-radius:16px}}
.wf-btn.pri{{background:#111;color:#fff}} .wf-btn.alt{{background:var(--fill)}} .wf-btn.sec{{background:var(--panel)}}
@media (min-width:600px) and (max-width:859px){{
  .intro{{grid-template-columns:1.1fr .8fr;grid-template-areas:"copy fig" "list fig" "acts fig";column-gap:24px}}
  .intro .fig{{align-self:center}}
}}
@media (min-width:860px){{
  .intro{{grid-template-columns:3fr 5fr 4fr;grid-template-areas:"fig copy list" "fig acts list";column-gap:var(--gap);align-items:center}}
  .intro .fig{{width:100%;align-self:end}} .checks.short{{display:none}} .checks.full{{display:grid}}
  .acts{{grid-template-columns:repeat(auto-fit,minmax(230px,1fr));align-items:start}}
}}
/* R2 reglas */
.grid{{display:grid;gap:var(--gap);grid-template-columns:1fr;margin-top:32px}}
.rule{{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:24px;display:flex;flex-direction:column;gap:10px}}
.rule::before{{content:"";display:block;width:24px;height:3px;background:#111}}
.rule .rule-txt{{display:flex;flex-direction:column;gap:8px}}
.rule .lab{{font-size:var(--t-small);font-weight:700;color:var(--muted)}}
.rule h3{{font-size:var(--t-sub);font-weight:700;line-height:1.25;letter-spacing:-.01em}}
.rule .sub{{font-weight:700}} .rule .body{{color:#333}}
.rule-fig{{margin-top:10px}}
@media (min-width:600px){{.grid{{grid-template-columns:1fr 1fr}} .rule.wide{{grid-column:1/-1}}}}
@media (min-width:860px){{
  .rule.wide{{display:grid;grid-template-columns:7fr 5fr;column-gap:var(--gap);align-items:start}}
  .rule.wide::before{{grid-column:1/-1}} .rule.wide .rule-fig{{margin-top:0}}
}}
@media (min-width:1100px){{.grid{{grid-template-columns:repeat(3,1fr)}}}}   /* 3 columnas solo cuando el renglón no queda angosto */
/* R3 cierre */
.close{{display:grid;gap:24px;align-items:center}}
.close .por{{width:min(100%,260px);justify-self:center}}
.close .t{{font-size:var(--t-semi);font-weight:800;line-height:1.05;letter-spacing:-.02em;margin-top:8px}}
.close .s{{margin-top:14px;max-width:var(--w-wide)}}
@media (min-width:860px){{.close{{grid-template-columns:4fr 8fr;column-gap:var(--gap)}} .close .por{{width:100%;max-width:340px}} .close .acts{{margin-top:8px}}}}
.foot{{border:1px solid #999;background:var(--fill);padding:28px;text-align:center;font:600 12px/1.5 ui-monospace,monospace;margin:0 0 40px}}
.ledger{{font:500 12px/1.5 ui-monospace,Menlo,monospace;border:1px dashed #555;background:#fafafa;padding:12px 14px 12px 30px;margin:0 0 40px}}
.ledger li{{list-style:disc;margin:6px 0}}
</style>
</head>
<body>
<div class='wf-top'>WIREFRAME · página «Las reglas de ADA» · Digizen B <span>· en grises a propósito · copy literal de la landing A · scroll libre · la barra negra a la izquierda marca lo que se lee en 3 segundos · ábrelo en desktop, tablet y teléfono</span></div>

<div class='wrap'>
{note('R0', 'Encabezado, igual que en la landing: logo flotante arriba a la izquierda (lleva a la landing) y botón de menú a la derecha, con el mismo menú; sus opciones llevan a las secciones de la landing. Sin riel lateral ni barra de progreso: aquí no hay recorrido por estaciones.')}
</div>
<div class='hdr'><div class='logo'>LOGO</div><div class='menu'>≡</div></div>

<section><div class='wrap'>
{note('R1', 'Entrada. Dice qué es esta página y por qué importa antes de pedir que se lea la lista. Desktop (≥ 860 px): imagen · texto y botones · lista completa de 13 puntos, en una sola pantalla. Tablet: texto, lista corta y botones a la izquierda, imagen a la derecha. Teléfono: texto → imagen → lista corta de 3 puntos → botones. La lista corta y la completa son las de la A: corta en teléfono y tablet, completa en desktop. En desktop la lista completa sirve de índice: cada punto lleva a su tarjeta. En teléfono la imagen se limita al 40 % del alto de la pantalla para que la lista y los botones queden cerca.')}
<div class='intro'>
  <div class='copy'>
    <p class='kick' data-copy>{e(I['kicker'])}</p>
    <h1 class='scan' data-copy>{e(I['title'][0])} {e(I['title'][1])}</h1>
    {paras}
  </div>
  <div class='fig'>
    {ph(I['image']['desktop'], 'IMAGEN · desktop', 'only-d')}
    {ph(I['image']['mobile'], 'IMAGEN · tablet y teléfono', 'only-m')}
    <p class='wf-alt'>texto alternativo: «<span data-alt>{e(I['image']['alt'])}</span>»</p>
  </div>
  <div class='list'>
    {checks(I['checks_short'], 'short')}
    {checks(I['checks_full'], 'full', index=True)}
  </div>
  <div class='acts'>{b1}</div>
</div>
{note('R1 · interacción', 'Los dos botones responden al instante al tocarlos (se hunden, como todos los de la landing). «Volver a Digizen» sale por donde se entró: regresa a la estación 08.5, donde está el botón «Conocer las reglas de ADA», no al inicio.')}
</div></section>

<section><div class='wrap'>
{note('R2', 'Las 13 reglas, abiertas y completas: es contenido de consulta, así que nada va en acordeón. Cada tarjeta se entiende con su rótulo y su título; el subtítulo y el cuerpo son la profundidad. La primera ocupa todo el ancho y lleva la imagen. Desde 1100 px: 3 columnas (4 filas de 3). De 600 a 1099 px: 2 columnas, para que el renglón no quede angosto. Teléfono: 1 columna. Tarjeta de la landing: superficie blanca, radio 16, barra corta de acento arriba.')}
<p class='kick' data-copy>{e(H['kicker'])}</p>
<h2 class='scan'><span data-copy>{e(H['title'][0])}</span><em style='font-style:normal' data-copy>{e(H['title'][1])} {e(H['title'][2])}</em></h2>
<div class='grid'>{cards}</div>
</div></section>

<section><div class='wrap'>
{note('R3', 'Cierre: después de leer las reglas, las dos acciones con el mismo peso. Desktop: retrato a la izquierda, texto y botones a la derecha. Teléfono: retrato, texto, botones. El retrato es decorativo (sin texto alternativo, como en la A).')}
<div class='close'>
  <div class='por'>{ph(C['image']['file'], 'IMAGEN · decorativa')}</div>
  <div>
    <p class='kick' data-copy>{e(C['kicker'])}</p>
    <p class='t scan' data-copy>{e(C['title'])}</p>
    <p class='s' data-copy>{e(C['support'])}</p>
    <div class='acts' style='margin-top:24px'>{b3}</div>
  </div>
</div>
{note('R3 · interacción', '«Tengo dudas · CONVERSAR CON ADA» abre el mismo formulario de la landing: nace del botón, se puede cerrar a medio camino y regresa al botón. «Inscribir a mi hijo · EMPIEZA HOY» lleva a las tarjetas de precio de la landing, como el botón del menú.')}
</div></section>

<div class='wrap'>
{note('R4', 'Pie: el mismo de la landing, sin cambios.')}
<div class='foot'>PIE DE LA LANDING B · componente compartido, sin cambios</div>
<p class='wf-note' style='margin-bottom:6px'><b>NOTAS INTERNAS</b> No son UI. Se conservan completas.</p>
<ul class='ledger'>{notes_int}</ul>
</div>
</body>
</html>
"""


# ---------------------------------------------------------------- auditoría fuente → artefacto
def words(s):
    s = html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace(' ', ' ')
    return re.findall(r'\S+', s)


def source_words():
    s = open(SRC, encoding='utf-8').read()
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    alts = [html.unescape(a) for a in re.findall(r'alt="([^"]*)"', s) if a]
    s = re.sub(r'<svg.*?</svg>', '', s, flags=re.S)
    return words(s), alts


def artifact_words(doc):
    body = doc[doc.find('<body>'):]
    copy = re.findall(r"<(\w+)[^>]*\bdata-copy\b[^>]*>(.*?)</\1>", body, flags=re.S)
    alts = [html.unescape(a) for a in re.findall(r"<span data-alt>(.*?)</span>", body, flags=re.S)]
    out = []
    for _, inner in copy: out += words(inner)
    return out, alts


def main():
    doc = page()
    open(OUT, 'w', encoding='utf-8').write(doc)
    sw, salt = source_words()
    aw, aalt = artifact_words(doc)
    # el h2 de la fuente pega «improvisa:» con «responde» (salto de línea visual): se comparan sin ese detalle
    norm = lambda ws: re.sub(r'improvisa:\s*responde', 'improvisa: responde', ' '.join(ws)).split()
    sw, aw = norm(sw), norm(aw)
    print(f'== {os.path.basename(OUT)} ==')
    print(f'  copy de la fuente: {len(sw)} palabras · en el wireframe: {len(aw)} palabras')
    ok = sw == aw
    if not ok:
        for i, (a, b) in enumerate(zip(sw, aw)):
            if a != b: print(f'  PRIMERA DIFERENCIA en la palabra {i}: fuente «{" ".join(sw[max(0,i-4):i+5])}» ≠ wireframe «{" ".join(aw[max(0,i-4):i+5])}»'); break
        else: print('  DIFERENCIA de longitud:', len(sw), len(aw))
    print('  mismo texto y en el mismo orden:', 'SÍ' if ok else 'NO')
    alt_ok = sorted(set(salt)) == sorted(set(aalt))
    print(f'  textos alternativos: {len(set(salt))} en la fuente · {len(set(aalt))} en el wireframe ·', 'IGUALES' if alt_ok else 'DIFIEREN')
    print(f'  tarjetas: {len(R.RULES)} · puntos de la lista completa: {len(R.INTRO["checks_full"])} · de la corta: {len(R.INTRO["checks_short"])}')
    print(f'  notas internas conservadas fuera de la UI: {len(R.NOTES)}')
    if not (ok and alt_ok): sys.exit(1)


if __name__ == '__main__':
    main()
