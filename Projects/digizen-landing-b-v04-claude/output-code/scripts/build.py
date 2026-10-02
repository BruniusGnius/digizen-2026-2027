# -*- coding: utf-8 -*-
"""
Build de producción — Digizen landing B v04 (Fase 3).

    python3 -B scripts/build.py            → prueba.html (estación de prueba) + index.html (página completa)
    python3 -B scripts/build.py --prueba   → solo prueba.html

1. Assets: escenas optimizadas en varios anchos (srcset), verticales 2:3 si existen (<nombre>-v.webp),
   secuencias, avatares y logos copiados a output-code/assets/.
2. HTML: se genera desde la MISMA fuente del wireframe aprobado (wireframe-src/content.py), con las mismas
   paradas, kinds y E; se quitan las notas del wireframe y entran el color, las tarjetas, los botones,
   el menú de recorrido y el diálogo de «Conversar con ADA primero».
3. Auditoría sobre el HTML final: los segmentos de COPY-PUBLICADO.md, literales y en orden (desktop y móvil),
   + lista de adiciones aprobadas.
4. Verificación contra el wireframe: misma lista de paradas (pin, id, kind, E, bp, oscuro). Si difiere, falla.
"""
import os, re, sys, shutil, html, time, json
from html.parser import HTMLParser
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
PROJ = os.path.dirname(OUT)
sys.path.insert(0, os.path.join(PROJ, 'wireframe-src'))
import content as C          # fuente única del copy y de las paradas (la del wireframe)
import build as WF           # find_vertical, source_segments (auditoría del wireframe)

# ------------------------------------------------------------------ configuración
# menú «qué vas a encontrar» (opción A elegida por el usuario, 2026-09-30): cada nombre dice qué hay en la sección;
# «Qué es ADA» incluye probarla (cap. 09), así ningún nombre repite el botón «Conversar con ADA primero»
TRAMOS = [(1, 'Lo que casi todos creemos'), (2, 'Por qué no te escucha'), (3, 'Lo que sí funciona'), (4, 'Qué es ADA'),
          (5, 'Tu papel'), (6, 'Precio e inscripción'), (7, 'Antes de decidir')]
MENU_FAQ = 'Preguntas frecuentes'
MENU_RULES = 'Reglas de ADA'   # entrada del menú a la página de reglas (pedido del usuario, 2026-10-02; el mismo nombre que usa la A)
PIN_TRAMO = {'P-01': 1, 'P-02b': 1, 'P-03a': 2, 'P-03b': 2, 'P-04': 2, 'P-05a': 3, 'P-05b': 3, 'P-06': 3,
             'P-07a': 4, 'P-07c': 4, 'P-08a': 4, 'P-08b': 4, 'P-09': 4, 'P-10a': 5, 'P-10b': 5,
             'P-11a': 6, 'P-11b': 6, 'P-12a': 7, 'P-12b': 7, 'FAQ': 7, 'FOOT': 7}
TEST_PINS = ['P-H0', 'P-H', 'P-01', 'P-08b', 'P-11b', 'FOOT']        # estación de prueba (plan §6)
ADA_CARD_STOPS = {'08.5', '08.5m'}                                     # tarjetas en el color de ADA (cian)
# psicología de color de V05 «Misión Clara» (el origen del sistema): el acento de cada golpe según su función
# (una lista = un color por acento, en orden: 03.5 es una antítesis «no» / «cómo», pedido del usuario)
ACC_ROLE = {'H.2': 'coral', '01.3': 'coral', '03.5': 'azul', '05.7': 'azul', '07.5': 'azul', '12.2': 'azul', '12.7': 'azul'}  # 07.5 «idea propia.»: color en el texto (azul = criterio), no banda (pedido del usuario)
# conceptos fuertes resaltados solo con color (<span class='hl'>, sin cambio tipográfico; pedido del usuario, 2026-09-29)
HL_ROLE = {'12.7': ['azul', 'coral', 'plain', 'coral'],  # Presencia, / vigilancia. / no (blanco, como el texto) / candado.
            '10.5': 'coral', '03.3': 'coral', '03.5': 'coral', '03.7': 'coral', '05.3': 'coral', '05.4': 'coral', '08.4': 'coral', '12.4': 'coral',
           '05.8': 'azul', '10.4': 'azul', '10.1': 'azul', '09.1': 'ia',
           '07.6': ['coral', 'azul']}   # evolución: el antes en coral (el problema), el después en azul (el criterio)
# voz citada en color: coral cuando es alerta o negativa (creencias falsas, objeción); azul cuando es positiva (la pregunta de 10.3)
VOICE_STOPS = {'02.2': 'coral', '02.3': 'coral', '02.4': 'coral', '02.5': 'coral', '08.1': 'coral', '10.3': 'azul'}  # 10.5: solo «cuando ve el celular» en coral (HL_ROLE)
IA_STOPS = {'08.3'}                                                     # dato sobre IA en violeta
PRICING_CTA_STOPS = {'12.4'}                                            # su «Inscribir a mi hijo» lleva a las tarjetas de precio
SCENE_W, VERT_W, QUALITY = (1280, 1920, 2560), (800, 1200), 72
FOOT_LINKS = {'Gnius Club ↗': 'https://gnius.club/', 'Aviso de privacidad': 'https://gnius.club/aviso-de-privacidad.html'}
DIALOG_TEXTS = ['Conversar con ADA primero (título del diálogo, copy existente)', 'Nombre del papá o mamá', 'Tu nombre',
                'Canal de entrega', 'Correo', 'WhatsApp', 'Correo electrónico', 'Número de WhatsApp', 'tu@correo.com',
                '+52 55 0000 0000', 'Conversa con ADA', 'Se manda la liga de acceso; no abre WhatsApp directo.']
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}

# ------------------------------------------------------------------ 1. assets
def newer(src, dst):
    return not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst)

def save_webp(im, w, dst):
    r = im if w == im.width else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    r.save(dst, 'WEBP', quality=QUALITY, method=6)

def variants(src, name, widths):
    im = Image.open(src).convert('RGB')
    ws = sorted({w for w in widths if w < im.width} | {min(im.width, max(widths))})
    for w in ws:
        dst = os.path.join(OUT, 'assets', 'scenes', f'{name}-{w}.webp')
        if newer(src, dst): save_webp(im, w, dst)
    return ws

SCENES, VERTS = {}, {}
def build_assets(names):
    os.makedirs(os.path.join(OUT, 'assets', 'scenes'), exist_ok=True)
    for nm in names:
        src = os.path.join(PROJ, '00-context', 'scenes', f'{nm}.webp')
        if os.path.exists(src):
            SCENES[nm] = variants(src, nm, SCENE_W)
        v = WF.find_vertical(nm)
        if v:
            VERTS[nm] = variants(os.path.join(PROJ, v), f'{nm}-v', VERT_W)
    for sub in ('seq', 'avatars'):
        s = os.path.join(PROJ, 'assets', sub)
        if os.path.isdir(s): shutil.copytree(s, os.path.join(OUT, 'assets', sub), dirs_exist_ok=True)
    os.makedirs(os.path.join(OUT, 'assets', 'logo'), exist_ok=True)
    for f in os.listdir(os.path.join(PROJ, '00-context', 'logo')):
        if f.endswith('.svg'): shutil.copy2(os.path.join(PROJ, '00-context', 'logo', f), os.path.join(OUT, 'assets', 'logo', f))

def srcset(nm, ws, v=False):
    tag = f'{nm}-v' if v else nm
    return ', '.join(f'assets/scenes/{tag}-{w}.webp {w}w' for w in ws)

# ------------------------------------------------------------------ 2. HTML de cada parada
IMG_SCENE = re.compile(r"<img([^>]*?) src='00-context/scenes/([^'/]+)\.webp'([^>]*)>")

def scene_img(m):
    before, nm, after = m.group(1), m.group(2), m.group(3)
    hero = 'hero-img' in before + after
    ws = SCENES[nm]
    load = " fetchpriority='high' decoding='async'" if hero else " loading='lazy' decoding='async'"
    img = f"<img{before} src='assets/scenes/{nm}-{ws[-1]}.webp' srcset='{srcset(nm, ws)}' sizes='100vw'{after}{load}>"
    if nm in VERTS:
        img = img.replace('<img', "<img data-v='1'", 1)
        return f"<picture><source media='(max-width: 859px)' srcset='{srcset(nm, VERTS[nm], True)}' sizes='100vw'>{img}</picture>"
    return img

def button(m):
    attrs, inner = m.group(1), m.group(2)
    role = re.search(r"data-role='([^']*)'", attrs)
    role = role.group(1) if role else ''
    attrs = re.sub(r"\s*data-role='[^']*'", '', attrs)
    cls = re.search(r"class='([^']*)'", attrs).group(1)
    if 'sec' in cls.split():
        rc = 'r-ada' if 'violeta' in role else 'r-ins'
        attrs = attrs.replace(f"class='{cls}'", f"class='{cls} {rc}'")
        goto = re.search(r"data-goto='([^']+)'", attrs)
        if goto:  # salto dentro de la página: enlace con destino real (funciona también sin JS)
            return f"<a{attrs} href='#{pin_of(goto.group(1))}'>{inner}</a>"
        # «Conocer las reglas de ADA ↗»: abre la página de reglas en una pestaña nueva, para no romper la narrativa;
        # la landing se queda en su estación (decisión del usuario, 2026-10-02)
        return f"<a{attrs} href='{RULES_FILE}' target='_blank' rel='opener'>{inner}</a>"   # rel=opener: la página de reglas sabe que vino de la landing (mismo sitio)
    if 'alt' in cls.split():
        return f"<button type='button'{attrs} data-action='ada' aria-haspopup='dialog'>{inner}</button>"
    return f"<button type='button'{attrs} data-action='checkout'>{inner}</button>"

ACC_ROW = re.compile(r"(<div class='row last'>(<span class='n [^']*'>[^<]*</span>)<p class='([^']*)'>(.*?)</p>)<span class='acc-mark' data-at='exit'>[^<]*</span>(</div>)")

def prod(h, sid=None):
    h = re.sub(r"<figcaption class='wf-file'>.*?</figcaption>", '', h, flags=re.S)
    h = re.sub(r"<span class='wf-new'>.*?</span>", '', h, flags=re.S)
    h = h.replace(" data-new='aprobado'", '')
    # L03: la última fila pasa a acento al final de su parada (copia de color sobre la misma fila, oculta a lectores)
    h = ACC_ROW.sub(lambda m: f"{m.group(1)}<span class='acc-copy' data-at='exit' aria-hidden='true'>{m.group(2)}<span class='{m.group(3)}'>{m.group(4)}</span></span>{m.group(5)}", h)
    h = IMG_SCENE.sub(scene_img, h)
    h = h.replace("src='00-context/logo/", "src='assets/logo/")
    h = re.sub(r"<a( class='btn[^']*'[^>]*)>(.*?)</a>", button, h, flags=re.S)
    for txt, url in FOOT_LINKS.items():
        h = h.replace(f"<a class='lnk'>{txt}</a>", f"<a class='lnk' href='{url}' target='_blank' rel='noopener'>{txt}</a>")
    h = re.sub(r"<p class='in w8 t-head amt'>(.*?)\s*(\$[\d,]+\.)</p>",
               lambda m: f"<p class='amt'><span class='in w6 t-body amt-l'>{m.group(1)}</span> <span class='in w8 t-semi amt-n'>{m.group(2)}</span></p>", h)
    if sid == '03.4m' and '03-fastidio' in VERTS:  # móvil/tablet: la vertical del fastidio reemplaza al cuadro provisional
        ws = VERTS['03-fastidio']
        h = h.replace("<img src='assets/seq/03-fastidio/fastidio-f064.webp' alt=''>",
                      f"<img data-v='1' src='assets/scenes/03-fastidio-v-{ws[-1]}.webp' srcset='{srcset('03-fastidio', ws, True)}' sizes='100vw' alt='' loading='lazy' decoding='async'>")
    if sid in ADA_CARD_STOPS:
        h = h.replace("class='entry card ", "class='entry card r-ada ")
    role = ACC_ROLE.get(sid)
    roles = role if isinstance(role, list) else ([role] * h.count("<em class='acc'>") if role else [])
    for r in roles:  # azul es el acento por defecto: no lleva clase
        h = h.replace("<em class='acc'>", f"<em class='acc r-{r}'>" if r != 'azul' else "<em class='acc r-azul'>", 1)
    h = h.replace("<em class='acc r-azul'>", "<em class='acc'>")
    hr = HL_ROLE.get(sid)
    for r in (hr if isinstance(hr, list) else [hr] * h.count("<span class='hl'>") if hr else []):
        h = h.replace("<span class='hl'>", f"<span class='hl r-{r}'>", 1)
    h = h.replace("<span class='hl r-azul'>", "<span class='hl'>")
    if sid in VOICE_STOPS:  # elementos en voz citada: Playfair itálica
        h = re.sub(r"class='(pf [^']*\bit\b[^']*)'", lambda m: f"class='{m.group(1)} voz{' r-azul' if VOICE_STOPS[sid] == 'azul' else ''}'" if re.search(r'\bt-(semi|mon|mxl)\b', m.group(1)) else m.group(0), h)  # coral solo ≥ 24 px
    if sid in IA_STOPS:
        h = h.replace("<p class='pf w8 t-mxl'", "<p class='pf w8 t-mxl c-ia'", 1)
    if sid in PRICING_CTA_STOPS:  # «Inscribir a mi hijo» final: lleva a las tarjetas de precio, como en el menú (decisión del usuario)
        h = h.replace("data-action='checkout'", "data-action='pricing'")
    return h

def pin_of(stop_id):
    for p in C.PINS:
        for s in p.get('stops', []):
            if s['id'] == stop_id: return p['id']
    return ''

def stop_html(pin, s):
    cls = ['stop', 'k-' + s['kind']]
    if s.get('night'): cls.append('nightc')
    if s['bp'] == 'd': cls.append('only-d')
    if s['bp'] == 'm': cls.append('only-m')
    if pin['type'] == 'h': cls.append('panel')
    e = ('%g' % CURRENT['E'].get(s['id'], s['E']))
    return (f"<div class='{' '.join(cls)}' data-id='{s['id']}' data-kind='{s['kind']}' data-e='{e}' "
            f"data-bp='{s['bp']}' data-night='{1 if s.get('night') else 0}'>\n{prod(s['html'], s['id'])}\n</div>")

def pin_html(pin):
    tramo = PIN_TRAMO.get(pin['id'], 0)
    if pin['type'] == 'flow':
        tag = 'footer' if pin['id'] == 'FOOT' else 'section'
        return f"<{tag} class='pin t-flow' id='{pin['id']}' data-pin data-type='flow' data-tramo='{tramo}'>\n{prod(pin['html'])}\n</{tag}>"
    body = '\n'.join(stop_html(pin, s) for s in pin['stops'])
    inner = f"<div class='track'>\n{body}\n</div>" if pin['type'] == 'h' else f"<div class='night'></div>\n{body}"
    return (f"<section class='pin t-{pin['type']}' id='{pin['id']}' data-pin data-type='{pin['type']}' data-tramo='{tramo}'>\n"
            f"<div class='stage'>\n{inner}\n</div>\n</section>")

BRAND = ("<a class='brand' href='#P-H0' aria-label='Digizen'>"
         "<img class='brand-dark' src='assets/logo/digizen-logo-dark.svg' alt='' width='275' height='116'>"
         "<img class='brand-light' src='assets/logo/digizen-logo-light.svg' alt='' width='275' height='116'></a>")

MENU_A11Y = ['Abrir menú / Cerrar menú (nombre accesible del botón)', 'Menú (nombre del panel)']

def menu_html(pins):
    """Menú de hamburguesa (pedido del usuario, 2026-09-29): tramos + FAQ + los dos CTA. Solo textos existentes o aprobados."""
    present = {PIN_TRAMO.get(p['id'], 0) for p in pins}
    items = '\n'.join(f"    <li><button type='button' class='menu-item' data-tramo='{n}'>{t}</button></li>" for n, t in TRAMOS if n in present)
    if any(p['id'] == 'FAQ' for p in pins):
        # la página de reglas abre en una pestaña nueva, igual que el botón «Conocer las reglas de ADA ↗»: la landing no se mueve
        items += f"\n    <li><a class='menu-item faq' href='{RULES_FILE}' target='_blank' rel='opener'>{MENU_RULES}</a></li>"
        items += f"\n    <li><button type='button' class='menu-item faq' data-menu-goto='FAQ'>{MENU_FAQ}</button></li>"
    cta = re.sub(r"<a( class='btn[^']*'[^>]*)>(.*?)</a>", button, C.CTA_INNER, flags=re.S)
    cta = cta.replace("data-action='checkout'", "data-action='pricing'")  # en el menú, «Inscribir a mi hijo» lleva a las tarjetas de precio (pedido del usuario)
    return ("<button class='menu-btn' type='button' aria-expanded='false' aria-controls='menu' aria-label='Abrir menú'>"
            "<span></span><span></span><span></span></button>\n"
            "<div class='menu' id='menu' hidden>\n  <div class='menu-backdrop'></div>\n"
            "  <nav class='menu-panel' aria-label='Menú'>\n"
            "    <img class='menu-logo' src='assets/logo/digizen-logo-light.svg' alt='' width='275' height='116'>\n"
            f"    <ul class='menu-list'>\n{items}\n    </ul>\n    {cta}\n  </nav>\n</div>")

def rail_html(pins):
    present = {PIN_TRAMO.get(p['id'], 0) for p in pins}
    items = '\n'.join(f"  <button class='rail-item' type='button' data-tramo='{n}'><span class='rail-label'>{t}</span>"
                      f"<span class='rail-dot' aria-hidden='true'></span></button>" for n, t in TRAMOS if n in present)
    return ("<div class='progress' aria-hidden='true'></div>\n<nav class='rail' aria-label='Recorrido'>\n"
            "  <span class='rail-line' aria-hidden='true'></span><span class='rail-fill' aria-hidden='true'></span>\n"
            f"{items}\n</nav>")

DIALOG = """<dialog class='ada-dialog' id='ada-dialog' aria-labelledby='ada-dialog-title'>
<form>
  <div class='dlg-head'><h2 id='ada-dialog-title' class='pf w7 t-head bw'>Conversar con ADA primero</h2><button type='button' class='close' data-close aria-label='Cerrar'>×</button></div>
  <label>Nombre del papá o mamá<input name='name' autocomplete='name' placeholder='Tu nombre' required></label>
  <fieldset><legend>Canal de entrega</legend>
    <div class='channel'><button type='button' data-channel='correo' aria-pressed='true'>Correo</button><button type='button' data-channel='whatsapp' aria-pressed='false'>WhatsApp</button></div>
  </fieldset>
  <label><span data-contact-label>Correo electrónico</span><input name='contact' type='email' autocomplete='email' placeholder='tu@correo.com' required></label>
  <button type='submit' class='btn alt'>Conversa con ADA<span class='arr' data-dir='e' data-icon='→' aria-hidden='true'></span></button>
  <p class='in w5 t-small note'>Se manda la liga de acceso; no abre WhatsApp directo.</p>
</form>
</dialog>"""

# ------------------------------------------------------------------ versión vigente y archivo (03-auditoria-scroll.md)
# Decisión del usuario (2026-10-02): la versión final es «una estación por gesto» (la que fue la prueba de scroll 3,
# js/dz-pager.js). El scroll animado y las pruebas 1 y 2 se conservan ARCHIVADAS y rotuladas como no vigentes:
# no se enlazan desde la página ni se indexan. Los enlaces viejos de las pruebas redirigen para no romperse.
FINAL_CFG = {'flow': True, 'pager': True}
# Más rango en las paradas con varios tiempos (sin agregar paradas): E por prueba, sin tocar la fuente del wireframe.
E_MAS_RANGO = {'07.6': 3.0, '01.3': 2.25, '07.5': 2.25, '09.1': 2.25, '11.3m': 2.25, '11.3bm': 2.0, '08.5m': 2.25}
BASE_CFG = {'stepFade': 0.07, 'closeFade': 0.12, 'msgFade': 0.10, 'minUnit': 900}
ARCHIVE = [   # cfg vacío = el motor del wireframe aprobado (scroll animado), que es el valor por defecto de js/dz-core.js
    ('archivo-scroll-animado.html', 'Archivada · no vigente por ahora · scroll animado', {}, {}),
    ('archivo-prueba-scroll-1.html', 'Archivada · no vigente por ahora · prueba 1: más rango y recorrido mínimo', E_MAS_RANGO, dict(BASE_CFG)),
    ('archivo-prueba-scroll-2.html', 'Archivada · no vigente por ahora · prueba 2: inercia del dedo limitada', E_MAS_RANGO, dict(BASE_CFG, touchMomentum=True)),
]
REDIRECTS = {'prueba-scroll-1.html': 'archivo-prueba-scroll-1.html', 'prueba-scroll-2.html': 'archivo-prueba-scroll-2.html',
             'prueba-scroll-3.html': './'}   # la prueba 3 es ahora la página principal
CURRENT = {'E': {}, 'cfg': FINAL_CFG, 'tag': None}   # lo que se está generando (por defecto, la versión vigente)

# ------------------------------------------------------------------ SEO y búsqueda generativa (03-seo-geo-plan.md)
# PREVIEW = True mientras la A esté en producción: la B no se indexa y declara a la A como página oficial,
# para no competir con ella. Al pasar a producción: PREVIEW = False y PUBLIC_URL = su dirección final.
PREVIEW = True
PUBLIC_URL = 'https://bruniusgnius.github.io/digizen-2026-2027/b-v04-claude/'
OFFICIAL_URL = 'https://digizen.gnius.club/'
SEO = {  # textos de SEO aprobados en la propuesta A (reutilizados por pedido del usuario); og:title está en el copy de B (05.7)
    'title': 'DIGIZEN | Ciudadanía digital para hijos: criterio, no control',
    'description': 'Tu hijo no necesita más vigilancia. Necesita criterio. DIGIZEN lo acompaña con ADA para pensar, decidir y construir una relación más sana con el mundo digital.',
    'og_title': 'El control caduca. El criterio no.',
    'og_description': 'DIGIZEN ayuda a tu hijo a construir criterio digital con ADA, sin convertirte en policía de su celular.',
    'og_image': 'assets/og/digizen-ogp-1200x630.jpg',  # la imagen para compartir vigente (elegida por el usuario, 2026-09-30)
    'og_image_alt': 'DIGIZEN: ciudadanía digital para hijos con criterio, voz propia y acompañamiento familiar.',
    'webpage_description': 'DIGIZEN es un programa de ciudadanía digital que acompaña a niños, niñas y jóvenes a construir criterio, identidad y responsabilidad digital con ADA.',
    'course_description': 'Programa de cultura y ciudadanía digital para la era de la inteligencia artificial. Acompaña a estudiantes a trabajar privacidad, identidad, pensamiento crítico, convivencia, bienestar, autoría, derechos y responsabilidad digital.',
}

def seo_head(indexable):
    """Metadatos, tarjetas para compartir y JSON-LD. Con PREVIEW (o en prueba.html) la página no se indexa."""
    canon = OFFICIAL_URL if (PREVIEW or not indexable) else PUBLIC_URL
    robots = 'index,follow,max-image-preview:large' if (indexable and not PREVIEW) else 'noindex,nofollow'
    img = PUBLIC_URL + SEO['og_image']
    org = OFFICIAL_URL + '#organization'
    graph = [
        {'@type': 'Organization', '@id': org, 'name': 'DIGIZEN', 'url': OFFICIAL_URL,
         'logo': OFFICIAL_URL + 'assets/digizen/logo-SVG/digizen-logo-dark.svg',
         'parentOrganization': {'@type': 'Organization', 'name': 'Gnius Club', 'url': 'https://gnius.club/'}},
        {'@type': 'WebSite', '@id': OFFICIAL_URL + '#website', 'url': OFFICIAL_URL, 'name': 'DIGIZEN', 'inLanguage': 'es-MX', 'publisher': {'@id': org}},
        {'@type': 'WebPage', '@id': PUBLIC_URL + '#webpage', 'url': PUBLIC_URL, 'name': SEO['title'], 'description': SEO['webpage_description'],
         'inLanguage': 'es-MX', 'isPartOf': {'@id': OFFICIAL_URL + '#website'},
         'audience': {'@type': 'Audience', 'audienceType': 'Madres, padres y cuidadores de niños, niñas y jóvenes'}},
        {'@type': 'Course', '@id': PUBLIC_URL + '#course', 'name': 'DIGIZEN', 'description': SEO['course_description'],
         'provider': {'@id': org}, 'inLanguage': 'es-MX', 'courseMode': 'online', 'url': PUBLIC_URL,
         'educationalLevel': 'De tercero de primaria a tercero de prepa',            # copy de B
         'offers': [                                                                 # montos literales del copy de B
             {'@type': 'Offer', 'name': 'El ciclo completo de 12 meses', 'price': '5990', 'priceCurrency': 'MXN', 'url': PUBLIC_URL},
             {'@type': 'Offer', 'name': 'Todo hoy, de una vez', 'price': '4990', 'priceCurrency': 'MXN', 'priceValidUntil': '2026-10-31', 'url': PUBLIC_URL}]},
        {'@type': 'FAQPage', '@id': PUBLIC_URL + '#faq',                            # las 7 preguntas literales del FAQ de B
         'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in C.FAQ]},
    ]
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1).replace('</', '<\\/')
    e = lambda t: html.escape(t, quote=True)
    return f"""<meta name="description" content="{e(SEO['description'])}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">
<link rel="alternate" type="text/plain" href="{OFFICIAL_URL}llms.txt" title="DIGIZEN">
<link rel="alternate" type="text/html" href="{OFFICIAL_URL}ai-context" title="DIGIZEN AI context">
<meta property="og:site_name" content="DIGIZEN">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_MX">
<meta property="og:url" content="{PUBLIC_URL}">
<meta property="og:title" content="{e(SEO['og_title'])}">
<meta property="og:description" content="{e(SEO['og_description'])}">
<meta property="og:image" content="{img}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(SEO['og_image_alt'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(SEO['og_title'])}">
<meta name="twitter:description" content="{e(SEO['og_description'])}">
<meta name="twitter:image" content="{img}">
<meta name="twitter:image:alt" content="{e(SEO['og_image_alt'])}">
<script type="application/ld+json">
{ld}
</script>"""

SCRIPTS = ['assets/vendor/gsap.min.js', 'assets/vendor/ScrollTrigger.min.js', 'assets/vendor/ScrollToPlugin.min.js',
           'js/dz-core.js', 'js/dz-spring.js', 'js/dz-seq.js', 'js/dz-pins.js', 'js/dz-carousel.js', 'js/dz-hero.js',
           'js/dz-rail.js', 'js/dz-brand.js', 'js/dz-menu.js', 'js/dz-faq.js', 'js/dz-actions.js', 'js/dz-main.js']

def cfg_script():
    return f"<script>window.DZ_CFG = {json.dumps(CURRENT['cfg'])};</script>" if CURRENT['cfg'] else ''

def test_tag():
    return f"<div class='test-tag' aria-hidden='true'>{CURRENT['tag']}</div>\n" if CURRENT['tag'] else ''

def page(pins, title, indexable=True):
    main = '\n'.join(pin_html(p) for p in pins if p['id'] != 'FOOT')
    foot = '\n'.join(pin_html(p) for p in pins if p['id'] == 'FOOT')
    hero = SCENES.get('01-dinner')
    pre = ''
    if hero:
        if '01-dinner' in VERTS:
            pre = (f"<link rel='preload' as='image' media='(max-width: 859px)' imagesrcset='{srcset('01-dinner', VERTS['01-dinner'], True)}' imagesizes='100vw' fetchpriority='high'>\n"
                   f"<link rel='preload' as='image' media='(min-width: 860px)' imagesrcset='{srcset('01-dinner', hero)}' imagesizes='100vw' fetchpriority='high'>")
        else:
            pre = f"<link rel='preload' as='image' imagesrcset='{srcset('01-dinner', hero)}' imagesizes='100vw' fetchpriority='high'>"
    ver = time.strftime('%Y%m%d%H%M%S')  # versión por build: el navegador no reutiliza CSS/JS viejos de la caché
    used = SCRIPTS[:-1] + (['js/dz-pager.js'] if (CURRENT['cfg'] or {}).get('pager') else []) + SCRIPTS[-1:]  # el paginador, solo donde la página lo pide (la versión vigente)
    scripts = '\n'.join(f"<script defer src='{s}?v={ver}'></script>" for s in used)
    return f"""<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
{seo_head(indexable)}
{cfg_script()}
<meta name="theme-color" content="#F4F3F0">
<link rel="icon" type="image/svg+xml" href="assets/logo/Favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,400..800;1,14..32,400..800&display=swap">
{pre}
<link rel="stylesheet" href="dist/styles.css?v={ver}">
</head>
<body>
{test_tag()}{BRAND}
{menu_html(pins)}
{rail_html(pins)}
<main id="recorrido">
{main}
</main>
{foot}
{DIALOG}
{scripts}
</body>
</html>
"""

# ------------------------------------------------------------------ 3. auditoría sobre el HTML final
class Stream(HTMLParser):
    """Texto visible de cada parada con su bp (all / d / m), en orden. Salta lo oculto a lectores."""
    BLOCK = {'p', 'h1', 'h2', 'h3', 'h4', 'div', 'li', 'summary', 'details', 'section', 'figure', 'button', 'footer'}  # <span> es en línea: no separa palabras
    def __init__(self):
        super().__init__(); self.stack = []; self.parts = []; self.stops = []
    def cur(self):
        bp, skip, inpin = 'all', False, False
        for t, a in self.stack:
            if 'data-pin' in a: inpin = True
            if 'data-bp' in a: bp = a['data-bp']
            if a.get('aria-hidden') == 'true' or 'acc-copy' in (a.get('class') or ''): skip = True
        return bp, skip, inpin
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'img' and a.get('data-copy'):
            bp, skip, inpin = self.cur()
            if inpin and not skip: self.parts.append((bp, ' ' + (a.get('alt') or '') + ' '))
        if tag in VOID: return
        self.stack.append((tag, a))
        if 'data-kind' in a:
            self.stops.append((self.pin_id(), a['data-id'], a['data-kind'], a['data-e'], a['data-bp'], a['data-night']))
        if tag in self.BLOCK: self.parts.append((self.cur()[0], ' '))
    def pin_id(self):
        for t, a in reversed(self.stack):
            if 'data-pin' in a: return a.get('id')
    def handle_endtag(self, tag):
        if tag in VOID: return
        while self.stack:
            t, a = self.stack.pop()
            if t == tag: break
        if tag in self.BLOCK: self.parts.append(('all', ' '))
    def handle_data(self, d):
        bp, skip, inpin = self.cur()
        if inpin and not skip: self.parts.append((bp, d))

def audit_file(path):
    p = Stream(); p.feed(open(path, encoding='utf-8').read())
    segs, _ = WF.source_segments()
    res = {}
    for bp in ('d', 'm'):
        txt = re.sub(r'\s+', ' ', html.unescape(''.join(d for b, d in p.parts if b in ('all', bp))))
        pos, miss = 0, []
        for sgm in segs:
            i = txt.find(sgm, pos)
            if i < 0: miss.append((sgm, 'fuera de orden' if txt.find(sgm) >= 0 else 'FALTA'))
            else: pos = i + len(sgm)
        res[bp] = (len(segs), miss)
    return res, p.stops

def expected_stops(pins):
    return [(p['id'], s['id'], s['kind'], '%g' % CURRENT['E'].get(s['id'], s['E']), s['bp'], '1' if s.get('night') else '0')
            for p in pins if p['type'] != 'flow' for s in p['stops']]

# ------------------------------------------------------------------ main
def render(pins, name, title, full, indexable=None):
    path = os.path.join(OUT, name)
    open(path, 'w', encoding='utf-8').write(page(pins, title, indexable=full if indexable is None else indexable))
    res, stops = audit_file(path)
    print(f'\n== {name} ==')
    if full:
        for bp in ('d', 'm'):
            n, miss = res[bp]
            print(f"  auditoría {'desktop' if bp == 'd' else 'móvil  '}: {n} segmentos · {len(miss)} problemas")
            for m in miss: print('     ', m)
    ok = stops == expected_stops(pins)
    print(f"  paradas vs wireframe: {len(stops)} · {'IGUALES' if ok else 'DIFIEREN'}")
    if not ok:
        exp = expected_stops(pins)
        for i, (a, b) in enumerate(zip(stops, exp)):
            if a != b: print('     primera diferencia:', a, '≠', b); break
        sys.exit(1)
    if full and any(res[bp][1] for bp in res): sys.exit(1)

# ------------------------------------------------------------------ 5. página «Las reglas de ADA» (03-build-plan-reglas.md)
# Página aparte, de lectura con scroll libre, con las mismas piezas de la landing (tokens, logo, menú, tarjeta, botones,
# formulario y pie). El contenido es literal de la landing A (wireframe-src/reglas.py) y se audita contra su fuente.
import reglas as RG
RULES_FILE = 'reglas-de-ada.html'
RULES_TITLE = 'Las reglas de ADA · DIGIZEN'           # título de la pestaña, aprobado por el usuario (2026-10-02)
RULES_SRC = os.path.join(PROJ, '00-context', 'REGLAS-DE-ADA-fuente-A.html')
RULES_BACK = 'P-08b'                                    # la estación de «Conocer las reglas de ADA ↗» (08.5 / 08.5m)
RULES_W = {'ada-rule-desktop': (480, 853), 'dg-scene-a10-ada-rules-closing': (420, 720),
           'dg-scene-a09-rules-presence': (900, 1400), 'dg-scene-a09-rules-presence-mobile': (800, 1200),
           'dg-scene-cta-father-son-team-1-1': (480, 800)}
RULES_SCRIPTS = ['assets/vendor/gsap.min.js', 'assets/vendor/ScrollTrigger.min.js', 'assets/vendor/ScrollToPlugin.min.js',
                 'js/dz-core.js', 'js/dz-spring.js', 'js/dz-menu.js', 'js/dz-actions.js', 'js/dz-pager.js', 'js/dz-rules.js', 'js/dz-main.js']   # el motor de estaciones de la landing

def rules_assets():
    """Las 3 imágenes de la A (5 archivos), optimizadas en dos anchos; conservan su transparencia."""
    dst_dir = os.path.join(OUT, 'assets', 'reglas'); os.makedirs(dst_dir, exist_ok=True)
    out = {}
    for name, widths in RULES_W.items():
        src = os.path.join(PROJ, '00-context', 'reglas', name + '.webp')
        im = Image.open(src); im = im.convert('RGBA' if im.mode in ('RGBA', 'LA', 'P') else 'RGB')
        ws = sorted({min(w, im.width) for w in widths})
        for w in ws:
            dst = os.path.join(dst_dir, f'{name}-{w}.webp')
            if newer(src, dst): save_webp(im, w, dst)
        out[name] = (ws, im.width, im.height)
    return out

def rules_page(pins, imgs):
    """Devuelve (html, estaciones). La página se recorre por estaciones, con el motor de la landing (una estación por gesto):
    entrada · título + la regla más importante · las 12 reglas restantes · cierre. Las reglas van de 3 en 3 en desktop
    (≥ 1100 px), de 2 en 2 en tablet (600–1099 px) y apiladas, una por gesto, en teléfono (decisión del usuario, 2026-10-02).
    Cada variante lleva el copy completo; el CSS muestra solo la que corresponde al ancho."""
    e = lambda t: html.escape(t, quote=True)
    rich = lambda t: e(t).replace('&lt;b&gt;', "<b class='w7'>").replace('&lt;/b&gt;', '</b>')
    name = lambda spec: spec[0].rsplit('.', 1)[0]
    def sset(n): return ', '.join(f'assets/reglas/{n}-{w}.webp {w}w' for w in imgs[n][0])
    def pic(desktop, mobile, alt, sizes_d, sizes_m, eager=False):
        d, m = name(desktop), (name(mobile) if mobile else None)
        ws, w, h = imgs[d]
        load = " fetchpriority='high' decoding='async'" if eager else " loading='lazy' decoding='async'"
        img = f"<img src='assets/reglas/{d}-{ws[-1]}.webp' srcset='{sset(d)}' sizes='{sizes_d}' width='{w}' height='{h}' alt='{e(alt)}'{load}>"
        if not m: return img
        _, mw, mh = imgs[m]
        return (f"<picture><source media='(max-width: 859px)' srcset='{sset(m)}' sizes='{sizes_m}' width='{mw}' height='{mh}'>{img}</picture>")
    arr = lambda icon, d: f"<span class='arr' data-dir='{d}' data-icon='{icon}' aria-hidden='true'></span>"
    I, H, CL = RG.INTRO, RG.RULES_HEAD, RG.CLOSING
    back, price = f'./#{RULES_BACK}', './#precio'
    stops = []   # (bp, kind, id, html): en orden; bp = all | n (≥ 600) | s (< 600) | w (≥ 1100) | t (600–1099)
    VIS = {'all': '', 'n': ' rg-n', 's': ' rg-s', 'w': ' rg-w', 't': ' rg-t'}

    # ---- entrada
    def head(v): return (f"<div class='rg-head'>\n  <p class='in w7 t-small'>{e(I['kicker'])}</p>\n"
                         f"  <h1 id='rg-title-{v}' class='pf w8 t-semi bw'>{e(I['title'][0])} <span class='hl r-ia'>{e(I['title'][1])}</span></h1>\n</div>")
    lead = "<div class='rg-lead'>\n" + '\n'.join(f"  <p class='in w5 t-body'>{rich(p)}</p>" for p in I['paras']) + "\n</div>"
    def fig(eager): return ("<figure class='rg-fig'>" + pic(I['image']['desktop'], I['image']['mobile'], I['image']['alt'],
                                                             '(min-width: 1180px) 340px, 30vw', '(min-width: 600px) 300px, 220px', eager=eager) + "</figure>")
    short = '\n'.join(f"    <li class='in w6 t-body'>{e(t)}</li>" for t in I['checks_short'])
    def lists(v):   # la lista completa es el índice: cada punto lleva a la estación de su tarjeta
        full = '\n'.join(f"    <li class='in w7 t-small'><a href='#regla-{i}' data-rule-link='{i}'>{e(t)}</a></li>" for i, t in enumerate(I['checks_full']))
        return f"<div class='rg-list'>\n  <ul class='rg-checks rg-short'>\n{short}\n  </ul>\n  <ul class='rg-checks rg-full'>\n{full}\n  </ul>\n</div>"
    acts = (f"<div class='cta rg-acts'>\n  <a class='btn' href='{price}'>{e(I['buttons'][0][0])}{arr('→', 'e')}</a>\n"
            f"  <a class='btn sec r-ins' href='{back}' data-rules='back'>{e(I['buttons'][1][0])}{arr('←', 'w')}</a>\n</div>")
    stops.append(('n', 'read', 'rg.1', f"<div class='c rg-intro-grid'>\n{head('n')}\n{lead}\n{fig(True)}\n{lists('n')}\n{acts}\n</div>\n{C.CUE}"))
    # teléfono: la entrada en dos estaciones, COMO PRUEBA (decisión del usuario): título y texto; después ADA, la lista y los botones
    stops.append(('s', 'read', 'rg.1a', f"<div class='c rg-intro-a'>\n{head('s')}\n{lead}\n</div>\n{C.CUE}"))
    stops.append(('s', 'read', 'rg.1b', f"<div class='c rg-intro-b'>\n{fig(False)}\n{lists('s')}\n{acts}\n</div>"))

    # ---- las reglas
    def card(i, v):
        label, title, sub, body = RG.RULES[i]
        figure = ''
        if i == 0:
            figure = ("\n  <figure class='rg-rule-fig'>" + pic(RG.RULE1_IMAGE['desktop'], RG.RULE1_IMAGE['mobile'], RG.RULE1_IMAGE['alt'],
                                                               '(min-width: 1180px) 450px, 40vw', '(min-width: 600px) 60vw, 86vw') + "</figure>")
        cid = f'regla-{i}' if v in ('all', 'w') else f'regla-{v}-{i}'
        return (f"<article class='card r-ada rg-rule{' rg-wide' if i == 0 else ''}' id='{cid}' data-rule='{i}'>\n  <div class='rg-rule-txt'>\n"
                f"    <p class='in w7 t-small'>{e(label)}</p>\n    <h3 class='pf w5 t-sub bw card-t'>{e(title)}</h3>\n"
                f"    <p class='in w7 t-body'>{e(sub)}</p>\n    <p class='in w5 t-body'>{e(body)}</p>\n  </div>{figure}\n</article>")
    rules_head = (f"<div class='rg-rules-head'>\n  <p class='in w7 t-small'>{e(H['kicker'])}</p>\n"
                  f"  <h2 class='pf w8 t-head bw'><span class='rg-l1'>{e(H['title'][0])}</span> {e(H['title'][1])} <span class='hl'>{e(H['title'][2])}</span></h2>\n</div>")
    stops.append(('all', 'read', 'rg.2', f"<div class='c rg-first'>\n{rules_head}\n{card(0, 'all')}\n</div>"))
    rest = list(range(1, len(RG.RULES)))
    for bp, per, kind in (('w', 3, 'read'), ('t', 2, 'read'), ('s', 3, 'deck')):   # 3 por gesto · 2 por gesto · mazos de 3, una tarjeta por gesto
        for g, k in enumerate(range(0, len(rest), per)):
            cards = '\n'.join(card(i, bp) for i in rest[k:k + per])
            if kind == 'deck': inner = f"<div class='c l08'>\n<div class='entries deck rg-deck'>\n{cards}\n</div>\n</div>"
            else: inner = f"<div class='c'>\n<div class='rg-grid rg-g{per}'>\n{cards}\n</div>\n</div>"
            stops.append((bp, kind, f'rg.{bp}{g + 1}', inner))

    # ---- cierre: retrato y texto · los botones en un bloque propio (las dos acciones principales juntas y con el mismo peso;
    #      «Regresar a Digizen», secundario, aparte) · y el pie de la landing DENTRO de esta estación, para que no sea una
    #      mini estación extra al final (pedidos del usuario, 2026-10-02)
    foot_pin = [p for p in pins if p['id'] == 'FOOT'][0]
    stops.append(('all', 'read', 'rg.9',
        f"<div class='c rg-close'>\n<div class='rg-close-grid'>\n"
        f"<figure class='rg-por' aria-hidden='true'>{pic(CL['image']['file'], None, '', '(min-width: 860px) 260px, 200px', '')}</figure>\n"
        f"<div class='rg-close-copy'>\n  <p class='in w7 t-small'>{e(CL['kicker'])}</p>\n  <p class='pf w8 t-semi bw'>{e(CL['title'])}</p>\n"
        f"  <p class='in w5 t-body'>{e(CL['support'])}</p>\n</div>\n"
        f"<div class='rg-close-acts'>\n"
        f"  <a class='btn' href='{price}'>{e(CL['buttons'][0][0])}{arr('→', 'e')}</a>\n"
        f"  <button type='button' class='btn alt' data-action='ada' aria-haspopup='dialog'>{e(CL['buttons'][1][0])}{arr('→', 'e')}</button>\n"
        f"  <a class='btn sec r-ins' href='{back}' data-rules='back' data-add='1'>{e(CL['added_button'][0])}{arr('←', 'w')}</a>\n</div>\n"
        f"</div>\n</div>\n<footer class='rg-foot'>\n{prod(foot_pin['html'])}\n</footer>"))

    def stop_div(bp, kind, sid, body):
        end = ' rg-end' if sid == 'rg.9' else ''
        return (f"<div class='stop k-{kind}{VIS[bp]}{end}' data-id='{sid}' data-kind='{kind}' data-e='1' data-bp='{bp}' data-night='0'>\n{body}\n</div>")
    def pin(pid, ids):
        inner = '\n'.join(stop_div(*st) for st in stops if st[2].split('.')[1][0] in ids)
        return (f"<section class='pin t-pin' id='{pid}' data-pin data-type='pin' data-tramo='0'>\n<div class='stage'>\n<div class='night'></div>\n{inner}\n</div>\n</section>")
    main = '\n'.join([pin('RG-1', '1'), pin('RG-2', '2wts'), pin('RG-3', '9')])

    # el mismo menú de la landing; aquí cada opción lleva a su sección de la landing
    first_pin = {}
    for p in pins:
        n = PIN_TRAMO.get(p['id'], 0)
        if n and n not in first_pin: first_pin[n] = p['id']
    items = '\n'.join(f"    <li><a class='menu-item' href='./#{first_pin[n]}'>{t}</a></li>" for n, t in TRAMOS if n in first_pin)
    items += f"\n    <li><a class='menu-item faq' href='#reglas' data-rules='top' aria-current='page'>{MENU_RULES}</a></li>"   # la página actual
    items += f"\n    <li><a class='menu-item faq' href='./#FAQ'>{MENU_FAQ}</a></li>"
    cta = re.sub(r"<a( class='btn[^']*'[^>]*)>(.*?)</a>", button, C.CTA_INNER, flags=re.S).replace("data-action='checkout'", "data-action='pricing'")
    menu = ("<button class='menu-btn on-light' type='button' aria-expanded='false' aria-controls='menu' aria-label='Abrir menú'>"
            "<span></span><span></span><span></span></button>\n"
            "<div class='menu' id='menu' hidden>\n  <div class='menu-backdrop'></div>\n  <nav class='menu-panel' aria-label='Menú'>\n"
            "    <img class='menu-logo' src='assets/logo/digizen-logo-light.svg' alt='' width='275' height='116'>\n"
            f"    <ul class='menu-list'>\n{items}\n    </ul>\n    {cta}\n  </nav>\n</div>")
    brand = BRAND.replace("class='brand' href='#P-H0'", f"class='brand is-on on-light' href='{back}' data-rules='back'")   # el logo regresa a la landing
    desc = re.sub(r'<[^>]+>', '', I['paras'][0])   # descripción: el primer párrafo de la página, literal
    ver = time.strftime('%Y%m%d%H%M%S')
    scripts = '\n'.join(f"<script defer src='{s}?v={ver}'></script>" for s in RULES_SCRIPTS)
    d_intro, m_intro = name(I['image']['desktop']), name(I['image']['mobile'])
    doc = f"""<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{RULES_TITLE}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{'noindex,nofollow' if PREVIEW else 'index,follow,max-image-preview:large'}">
<link rel="canonical" href="{OFFICIAL_URL if PREVIEW else PUBLIC_URL}reglas-de-ada">
<meta property="og:site_name" content="DIGIZEN">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_MX">
<meta property="og:title" content="{RULES_TITLE}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{PUBLIC_URL + SEO['og_image']}">
<meta name="twitter:card" content="summary_large_image">
<script>window.DZ_CFG = {json.dumps(FINAL_CFG)};</script>
<meta name="theme-color" content="#F4F3F0">
<link rel="icon" type="image/svg+xml" href="assets/logo/Favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,400..800;1,14..32,400..800&display=swap">
<link rel='preload' as='image' media='(min-width: 860px)' imagesrcset='{sset(d_intro)}' imagesizes='340px' fetchpriority='high'>
<link rel="stylesheet" href="dist/styles.css?v={ver}">
</head>
<body class='rg-page'>
{brand}
{menu}
<main id='reglas' class='rg'>
{main}
</main>
{DIALOG}
{scripts}
</body>
</html>
"""
    return doc, stops

def rules_audit(stops):
    """Por cada ancho (desktop, tablet, teléfono): las palabras del copy de la fuente, las mismas y en el mismo orden,
    y los textos alternativos. Las adiciones aprobadas por el usuario se listan aparte."""
    def words(s):
        s = re.sub(r'<svg.*?</svg>', '', s, flags=re.S)
        return re.findall(r'\S+', html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace(' ', ' '))
    glue = lambda ws: re.sub(r'improvisa:\s*responde', 'improvisa: responde', ' '.join(ws)).split()   # en la fuente es un salto de línea visual
    src = re.sub(r'<!--.*?-->', '', open(RULES_SRC, encoding='utf-8').read(), flags=re.S)
    sw = glue(words(src))
    salt = sorted({html.unescape(a) for a in re.findall(r'alt="([^"]*)"', src) if a})
    print(f'\n== {RULES_FILE} ==')
    ok, added = True, set()
    for label, allowed in (('desktop (≥ 1100 px)', {'all', 'n', 'w'}), ('tablet (600–1099 px)', {'all', 'n', 't'}), ('teléfono (< 600 px)', {'all', 's'})):
        body = '\n'.join(st[3] for st in stops if st[0] in allowed)
        body = re.sub(r"<footer.*?</footer>", '', body, flags=re.S)   # el pie es el de la landing: no es copy de esta página
        added |= {re.sub(r'<[^>]+>', '', t).strip() for t in re.findall(r"<a[^>]*\bdata-add='1'[^>]*>(.*?)</a>", body, flags=re.S)}
        body = re.sub(r"<a[^>]*\bdata-add='1'[^>]*>.*?</a>", '', body, flags=re.S)   # adiciones aprobadas: no están en la fuente
        pw = glue(words(body))
        palt = sorted({html.unescape(a) for a in re.findall(r"alt='([^']*)'", body) if a})
        n = sum(1 for st in stops if st[0] in allowed)
        same = sw == pw
        print(f'  {label}: {n} estaciones · {len(pw)} de {len(sw)} palabras · mismo texto y mismo orden: {"SÍ" if same else "NO"} · textos alternativos: {"IGUALES" if salt == palt else "DIFIEREN"}')
        if not same:
            for i, (a, b) in enumerate(zip(sw, pw)):
                if a != b: print(f'     primera diferencia en la palabra {i}: «{" ".join(sw[max(0, i - 4):i + 5])}» ≠ «{" ".join(pw[max(0, i - 4):i + 5])}»'); break
        ok = ok and same and salt == palt
    print(f'  tarjetas: {len(RG.RULES)} · título de la pestaña (aprobado): «{RULES_TITLE}»')
    print('  adiciones de copy aprobadas por el usuario (no están en la fuente): ' + (' · '.join(f'«{a}»' for a in sorted(added)) or 'ninguna'))
    if not ok: sys.exit(1)

def main():
    names = sorted(set(re.findall(r"src='00-context/scenes/([^'/]+)\.webp'", repr([s['html'] for p in C.PINS for s in p.get('stops', [])]))))
    build_assets(names + ['03-fastidio'])
    kb = sum(os.path.getsize(os.path.join(OUT, 'assets', 'scenes', f)) for f in os.listdir(os.path.join(OUT, 'assets', 'scenes'))) / 1024
    print('== assets ==')
    for nm in names: print(f"  {nm}: {SCENES.get(nm)} {'+ vertical ' + str(VERTS[nm]) if nm in VERTS else '(sin vertical todavía)'}")
    print(f'  escenas optimizadas: {kb:.0f} KB en total')
    test = [p for p in C.PINS if p['id'] in TEST_PINS]
    render(test, 'prueba.html', 'Digizen · estación de prueba', full=False)
    if '--prueba' not in sys.argv:
        render(C.PINS, 'index.html', SEO['title'], full=True)
        print('  config (versión vigente):', FINAL_CFG)
        for name, tag, emap, cfg in ARCHIVE:   # archivo: mismas paradas y copy; cambian E de algunas y el motor; no se indexan
            CURRENT.update(E=emap, cfg=cfg, tag=tag)
            render(C.PINS, name, SEO['title'] + ' · ' + tag, full=True, indexable=False)
            print('  config:', cfg or 'motor del wireframe (scroll animado)', '· E cambiadas:', emap or 'ninguna')
        CURRENT.update(E={}, cfg=FINAL_CFG, tag=None)
        for name, target in REDIRECTS.items():   # los enlaces viejos de las pruebas no se rompen
            open(os.path.join(OUT, name), 'w', encoding='utf-8').write(
                "<!doctype html>\n<html lang=\"es-MX\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"robots\" content=\"noindex,nofollow\">\n"
                f"<title>DIGIZEN</title>\n<meta http-equiv=\"refresh\" content=\"0; url={target}\">\n</head>\n"
                f"<body>\n<p><a href=\"{target}\">Esta página cambió de lugar. Continuar</a></p>\n</body>\n</html>\n")
        print('\n== redirecciones ==\n  ' + ' · '.join(f'{a} → {b}' for a, b in REDIRECTS.items()))
        rules_doc, rules_stops = rules_page(C.PINS, rules_assets())   # página «Las reglas de ADA»
        open(os.path.join(OUT, RULES_FILE), 'w', encoding='utf-8').write(rules_doc)
        rules_audit(rules_stops)
    print(f"\n== SEO ==\n  {'PREVIEW: noindex, canonical a la A (' + OFFICIAL_URL + ')' if PREVIEW else 'PRODUCCIÓN: index, canonical ' + PUBLIC_URL}")
    print('  JSON-LD: Organization, WebSite, WebPage, Course (2 ofertas), FAQPage (' + str(len(C.FAQ)) + ' preguntas literales)')
    print('\n== adiciones de copy aprobadas por el usuario (no están en COPY-PUBLICADO.md) ==')
    print('  «Práctica y breve» (08.5)')
    print('  botones de las tarjetas de precio (tomados de la propuesta A): Pagar de contado · Elegir pagos diferidos')
    print('  09.1: «Conversar con ADA primero» (texto del CTA, repetido bajo «Habla tú con ADA primero.» para abrir el formulario)')
    print('  menú de recorrido y menú de hamburguesa: ' + ' · '.join(t for _, t in TRAMOS))
    print(f'  menú de hamburguesa: «{MENU_RULES}», «{MENU_FAQ}» y los dos CTA; nombres accesibles: ' + ' · '.join(MENU_A11Y))
    print('  formulario (tomado de la propuesta A): ' + ' · '.join(DIALOG_TEXTS))
    print(f'  página de reglas: título de la pestaña «{RULES_TITLE}»; el resto de su copy es literal de la landing A (00-context/REGLAS-DE-ADA-fuente-A.html)')

if __name__ == '__main__':
    main()
