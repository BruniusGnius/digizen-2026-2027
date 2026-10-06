# -*- coding: utf-8 -*-
"""Construye el sistema de diseño de Digizen (index.html) a partir de lo que está construido en la landing A.

Uso (desde Projects/digizen-sistema-de-diseno/):   python3 construir.py

Solo LEE la landing; no modifica ninguno de sus archivos. El resultado es autosuficiente: index.html, css/, js/ y
assets/ (las imágenes que usan los ejemplos se copian aquí), para poder usarlo en otro proyecto.

Qué lee:
- plantilla.html ............ el texto de la guía, con marcas <!--@...--> donde va lo generado.
- fuente/landing.html y fuente/reglas.html ... instantáneas de la página ya renderizada (portada y reglas).
  De ahí se extrae el marcado real de cada componente; no se redibuja nada.
- ../digizen-landing/angular-build/src/styles.css ... los tokens y las reglas tipográficas (valores reales, claro y oscuro).
- css/digizen-a.css ......... copia del CSS compilado de la landing: los ejemplos se ven igual que en producción.
- css/digizen-ajustes.css ... la regla del sistema que la landing aún no aplica (se carga después; ver la guía).

Para actualizar tras un cambio en la landing, ver LEEME.md.
"""
import html, json, os, re, shutil
from html.parser import HTMLParser

AQUI = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(AQUI, '..', 'digizen-landing', 'angular-build')   # la landing A: solo lectura
PUBLIC = os.path.join(APP, 'public')
ASSETS = ''                                   # las rutas quedan como en la landing (assets/…); los archivos se copian aquí
SVG_ATTR = {'viewbox': 'viewBox', 'preserveaspectratio': 'preserveAspectRatio'}
VOID = {'img', 'source', 'input', 'br', 'wbr', 'hr', 'meta', 'link'}


# ------------------------------------------------------------------ mini DOM
class Node:
    def __init__(self, tag, attrs=None, parent=None):
        self.tag, self.attrs, self.parent, self.kids = tag, list(attrs or []), parent, []

    def get(self, k, d=''):
        for a, v in self.attrs:
            if a == k: return v or ''
        return d

    def set(self, k, v):
        for i, (a, _) in enumerate(self.attrs):
            if a == k: self.attrs[i] = (k, v); return
        self.attrs.append((k, v))

    def drop(self, k):
        self.attrs = [(a, v) for a, v in self.attrs if a != k]

    @property
    def classes(self):
        return self.get('class').split()

    def walk(self):
        yield self
        for k in self.kids:
            if isinstance(k, Node): yield from k.walk()

    def all(self, cls=None, tag=None):
        return [n for n in self.walk() if (cls is None or cls in n.classes) and (tag is None or n.tag == tag)]

    def one(self, cls=None, tag=None, i=0):
        r = self.all(cls, tag)
        if len(r) <= i: raise KeyError(f'no se encontró {tag or ""}.{cls or ""} [{i}]')
        return r[i]

    def text(self):
        return ''.join(k if isinstance(k, str) else k.text() for k in self.kids)


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('root'); self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur); self.cur.kids.append(n)
        if tag not in VOID: self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.kids.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag: n = n.parent
        if n is not self.root: self.cur = n.parent

    def handle_data(self, data):
        self.cur.kids.append(data)


def limpiar(root):
    """Quita lo que deja Angular y las animaciones, y apunta las imágenes a la carpeta de la landing."""
    for n in list(root.walk()):
        n.attrs = [(SVG_ATTR.get(a, a), v) for a, v in n.attrs if not (a.startswith('_ng') or a.startswith('ng-') or a.startswith('lucide'))]
        if n.tag == 'source' and n.get('type') == 'image/png' and n.parent:   # el PNG original no se publica: sobra como fuente
            n.parent.kids.remove(n); continue
        if n.tag == 'img' and n.get('src').endswith('.png') and os.path.exists(os.path.join(PUBLIC, n.get('src')[:-4] + '.webp')):
            n.set('src', n.get('src')[:-4] + '.webp')
        if n.tag == 'dialog': n.set('open', '')   # en la guía se muestra abierto
        st = n.get('style')
        if st and ('translate:' in st or 'visibility:' in st or 'opacity:' in st):   # estilos que pone GSAP al animar
            keep = '; '.join(p.strip() for p in st.split(';') if p.strip().startswith('--'))
            n.set('style', keep) if keep else n.drop('style')
        for a in ('src', 'poster', 'href'):
            v = n.get(a)
            if v.startswith('assets/'): n.set(a, ASSETS + v)
        v = n.get('srcset')
        if v: n.set('srcset', ', '.join(ASSETS + p.strip() if p.strip().startswith('assets/') else p.strip() for p in v.split(',')))
        if n.tag == 'canvas' and 'dg-ada-render' in n.classes:   # el lienzo animado no se puede copiar: se muestra su primer cuadro
            n.tag = 'img'; n.kids = []
            n.attrs = [('class', 'dg-ada-render is-ready'), ('src', ASSETS + 'assets/digizen/ada-wave/f000.webp'),
                       ('alt', 'ADA saludando a la cámara'), ('width', '400'), ('height', '616')]
        if n.tag == 'video':
            n.set('preload', 'none'); n.drop('src')   # en la guía basta el póster
    return root


def cargar(nombre):
    s = open(os.path.join(AQUI, 'fuente', nombre), encoding='utf-8').read()
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    p = Parser(); p.feed(s)
    return limpiar(p.root)


INLINE = {'a', 'span', 'strong', 'em', 'b', 'i', 'cite', 'wbr', 'br', 'svg', 'path', 'circle', 'rect', 'line', 'polyline',
          'button', 'img', 'input', 'label', 'small', 'sup', 'sub', 'u', 'abbr'}


def ser(n, compact=False):
    """HTML del nodo, tal cual (para pintarlo)."""
    if isinstance(n, str): return html.escape(n, quote=False)
    if n.tag == 'root': return ''.join(ser(k) for k in n.kids)
    at = ''.join(f' {a}' if v is None or (v == '' and a not in ('alt', 'value', 'class')) else f' {a}="{html.escape(v, quote=True)}"' for a, v in n.attrs)
    if n.tag in VOID: return f'<{n.tag}{at}>'
    return f'<{n.tag}{at}>' + ''.join(ser(k) for k in n.kids) + f'</{n.tag}>'


def codigo(n, nivel=0):
    """HTML con sangría, para mostrarlo como código. Los trazos de los iconos se resumen."""
    pad = '  ' * nivel
    if isinstance(n, str):
        t = ' '.join(n.split())
        return (pad + html.escape(t, quote=False) + '\n') if t else ''
    at = ''.join(f' {a}' if v is None or (v == '' and a not in ('alt',)) else f' {a}="{v}"' for a, v in n.attrs)
    if n.tag == 'svg':
        return f'{pad}<svg{at}>…</svg>\n'
    if n.tag in VOID: return f'{pad}<{n.tag}{at}>\n'
    kids = [k for k in n.kids if not (isinstance(k, str) and not k.strip())]
    if all(isinstance(k, str) or (k.tag in INLINE and k.tag != 'svg' and not any(isinstance(g, Node) and g.tag not in INLINE for g in k.walk())) for k in kids) and len(ser(n)) < 220:
        inner = ' '.join(''.join(k if isinstance(k, str) else re.sub(r'<svg.*?</svg>', '<svg>…</svg>', ser(k), flags=re.S) for k in kids).split())
        return f'{pad}<{n.tag}{at}>{inner}</{n.tag}>\n'
    return f'{pad}<{n.tag}{at}>\n' + ''.join(codigo(k, nivel + 1) for k in kids) + f'{pad}</{n.tag}>\n'


# ------------------------------------------------------------------ tokens y reglas del CSS real
CSS = open(os.path.join(APP, 'src', 'styles.css'), encoding='utf-8').read()


def bloque_tokens(selector):
    m = re.search(re.escape(selector) + r'\s*\{(.*?)\n\}', CSS, flags=re.S)
    body = re.sub(r'/\*.*?\*/', '', m.group(1), flags=re.S)
    out = {}
    for d in re.finditer(r'(--[\w-]+)\s*:\s*([^;]+);', body): out[d.group(1)] = ' '.join(d.group(2).split())
    return out


CLARO = bloque_tokens(':root')
OSCURO = bloque_tokens(":root[data-theme='dark']")


def regla(sel):
    """Declaraciones de la primera regla cuyo selector es exactamente `sel`."""
    for m in re.finditer(r'(^|\n)([^{}\n@]*)\{([^{}]*)\}', CSS):
        if sel in [x.strip() for x in m.group(2).split(',')]:
            body = re.sub(r'/\*.*?\*/', '', m.group(3), flags=re.S)
            return {d.group(1): ' '.join(d.group(2).split()) for d in re.finditer(r'([\w-]+)\s*:\s*([^;]+);', body)}
    return {}


def lum(hexa):
    h = hexa.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contraste(a, b):
    return (max(lum(a), lum(b)) + 0.05) / (min(lum(a), lum(b)) + 0.05)


# ------------------------------------------------------------------ piezas generadas
GRUPOS = [   # (título, [(token, para qué se usa)])
    ('Superficies', [('--dg-canvas', 'Fondo general de la página.'), ('--dg-canvas-end', 'Cierre del degradado del fondo.'),
                     ('--dg-surface', 'Arranque del degradado del fondo; campos de solo lectura.'), ('--dg-raised', 'Tarjetas, controles y diálogo.'),
                     ('--dg-subtle', 'Superficie secundaria y marco de las imágenes.'), ('--dg-decision', 'Fondo de la tarjeta de precio destacada.'),
                     ('--dg-nav', 'Barra de navegación y barra móvil (con desenfoque).')]),
    ('Texto y líneas', [('--dg-ink', 'Texto principal y titulares.'), ('--dg-muted', 'Texto de lectura, notas y ayudas.'),
                        ('--dg-soft', 'Fragmento gris de los titulares. No se usa en texto pequeño.'),
                        ('--dg-line', 'Bordes y divisores.'), ('--dg-line-strong', 'Borde reforzado.')]),
    ('Color con significado: relleno', [('--dg-blue', 'Estructura, navegación y progreso.'), ('--dg-cyan', 'ADA y acompañamiento.'),
                                        ('--dg-violet', 'Reflexión y voz del alumno; enlaces de «Ver más».'), ('--dg-coral', 'Señal de cuidado. Nunca una acción.'),
                                        ('--dg-orange', 'Energía y avance.'), ('--dg-gold', 'Hito o logro.'), ('--dg-green', 'Confirmación; borde de la opción destacada.'),
                                        ('--dg-teal', 'Acento auxiliar.')]),
    ('Color con significado: texto', [('--dg-text-blue', 'Énfasis azul dentro de un titular.'), ('--dg-text-cyan', 'Énfasis de ADA.'),
                                      ('--dg-text-violet', 'Énfasis de reflexión.'), ('--dg-text-coral', 'Énfasis de cuidado o dolor.'),
                                      ('--dg-text-green', 'Énfasis de confirmación.'), ('--dg-kicker-ink', 'Antetítulos (kicker).')]),
    ('Acción y estado', [('--dg-btn-fill', 'Relleno del botón principal: el degradado del círculo del logo.'), ('--dg-btn-bg', 'Color base del botón: sombras, barra de progreso y marca del antetítulo.'),
                         ('--dg-btn-ink', 'Texto del botón principal.'), ('--dg-selected', 'Opción elegida.'), ('--dg-focus', 'Anillo de foco del teclado.')]),
]


def tabla_color():
    out = []
    for titulo, filas in GRUPOS:
        out.append(f'<h4 class="ds-h4">{titulo}</h4>\n<div class="ds-tokens">')
        for tok, uso in filas:
            c, o = CLARO.get(tok, ''), OSCURO.get(tok, CLARO.get(tok, ''))
            out.append(f'<div class="ds-token"><span class="ds-swatch" style="background:var({tok})"></span>'
                       f'<div class="ds-token-txt"><code class="ds-code-inline">{tok}</code><span class="ds-token-uso">{uso}</span>'
                       f'<span class="ds-token-val"><b>Claro</b> {html.escape(c)} · <b>Oscuro</b> {html.escape(o)}</span></div></div>')
        out.append('</div>')
    return '\n'.join(out)


def tabla_contraste():
    pares = [('--dg-ink', 'Texto principal'), ('--dg-muted', 'Texto de lectura y notas'), ('--dg-soft', 'Fragmento gris del titular (solo texto grande)'),
             ('--dg-text-blue', 'Énfasis azul'), ('--dg-text-cyan', 'Énfasis cian'), ('--dg-text-violet', 'Énfasis violeta'),
             ('--dg-text-coral', 'Énfasis coral'), ('--dg-text-green', 'Énfasis verde'), ('--dg-kicker-ink', 'Antetítulo')]
    filas = []
    for tok, nombre in pares:
        celdas = []
        for tema, T in (('claro', CLARO), ('oscuro', OSCURO)):
            fg = T.get(tok, CLARO[tok])
            for fondo in ('--dg-raised', '--dg-canvas'):
                bg = T.get(fondo, CLARO[fondo]); r = contraste(fg, bg)
                ok = 'ok' if r >= 4.5 else ('gr' if r >= 3 else 'no')
                celdas.append(f'<td class="ds-cr ds-cr-{ok}">{r:.2f}</td>')
        filas.append(f'<tr><th scope="row"><code class="ds-code-inline">{tok}</code><span>{nombre}</span></th>{"".join(celdas)}</tr>')
    return ('<div class="ds-table-wrap"><table class="ds-table ds-table-cr"><thead><tr><th rowspan="2">Texto</th><th colspan="2">Tema claro</th><th colspan="2">Tema oscuro</th></tr>'
            '<tr><th>sobre tarjeta</th><th>sobre fondo</th><th>sobre tarjeta</th><th>sobre fondo</th></tr></thead><tbody>'
            + ''.join(filas) + '</tbody></table></div>')


def css_de(sel):
    d = regla(sel)
    orden = [('font-size', 'tamaño'), ('font-weight', 'peso'), ('letter-spacing', 'espaciado'), ('line-height', 'interlínea'), ('color', 'color'), ('max-width', 'ancho máx.')]
    partes = [f'<span><b>{n}</b> {html.escape(d[k])}</span>' for k, n in orden if k in d]
    return f'<p class="ds-spec"><code class="ds-code-inline">{sel}</code>{"".join(partes)}</p>'


def var(tok):
    return html.escape(CLARO.get(tok, '?'))


# ------------------------------------------------------------------ librería: qué se extrae y de dónde
def ejemplo(ident, titulo, nodos, nota='', clase='', ancho=''):
    """Un ejemplo de la librería: el componente pintado y su marcado."""
    if not isinstance(nodos, list): nodos = [nodos]
    pint = '\n'.join(ser(n) for n in nodos)
    cod = ''.join(codigo(n) for n in nodos).rstrip()
    lineas = cod.count('\n') + 1
    if lineas > 70: cod = '\n'.join(cod.split('\n')[:70]) + f'\n… ({lineas - 70} líneas más: ver la página)'
    if 'ds-stage--wide' in clase: nota = (nota + ' ' if nota else '') + '<span class="ds-ex-wide">Composición de escritorio: si no cabe, se desplaza dentro del recuadro.</span>'
    nota = f'<p class="ds-ex-note">{nota}</p>' if nota else ''
    return (f'<article class="ds-ex" id="lib-{ident}"><header class="ds-ex-head"><h4 class="ds-ex-title">{titulo}</h4>{nota}</header>'
            f'<div class="ds-stage {clase}"{f' style="--ds-ancho:{ancho}"' if ancho else ""}>{pint}</div>'
            f'<details class="ds-codeblock"><summary>Ver el marcado</summary><pre><code>{html.escape(cod)}</code></pre></details></article>')


def libreria():
    L, R = cargar('landing.html'), cargar('reglas.html')
    E = {}
    sec = L.all(tag='section')
    # --- acción
    dec = L.one('dg-decision')
    E['botones'] = ejemplo('botones', 'Botón principal y secundario', dec.one('dg-decision-actions'),
                           'El principal avanza; el secundario ofrece la salida de bajo riesgo. Van juntos y en ese orden.', 'ds-stage--pad')
    E['decision'] = ejemplo('decision', 'Panel de decisión', dec, 'Aparece después de cada tramo fuerte del relato. Retrato, pregunta, promesa y las dos acciones.')
    # --- texto
    hero = sec[0].one('dg-grid-2').kids
    hero_txt = [k for k in hero if isinstance(k, Node)][0]
    E['hero'] = ejemplo('hero', 'Apertura: título, entrada y nota', hero_txt, 'El título de apertura no lleva antetítulo. La entrada usa el tamaño grande y un solo énfasis de color.', 'ds-stage--pad')
    s1 = sec[1]
    E['titular'] = ejemplo('titular', 'Antetítulo y titular en dos tonos', [s1.one('dg-kicker'), s1.one('dg-h2')],
                           'Primero el fragmento gris, después el mensaje en tinta.', 'ds-stage--pad')
    E['titular-enfasis'] = ejemplo('titular-enfasis', 'Titular con énfasis de color', [sec[2].one('dg-kicker'), sec[2].one('dg-h2')],
                                   'Un solo énfasis por titular, con el color de su significado.', 'ds-stage--pad')
    copy = s1.one('dg-copy')
    E['copy'] = ejemplo('copy', 'Texto de lectura', copy, 'Negritas en tinta para el golpe; cursiva para las voces citadas.', 'ds-stage--pad')
    # --- notas
    E['nota'] = ejemplo('nota', 'Nota', sec[0].one('dg-note'), 'La voz que acompaña. Avatar con icono de línea, frase fuerte y remate en cursiva.', 'ds-stage--pad')
    notas = [L.one('dg-note--coral'), L.one('dg-note--gold'), L.one('dg-note--green')]
    E['nota-variantes'] = ejemplo('nota-variantes', 'Nota: coral, dorado y verde', notas, 'El color cambia con el sentido: cuidado, hito y confirmación.', 'ds-stage--pad ds-stage--stack')
    # --- imagen
    E['media'] = ejemplo('media', 'Marco de imagen', sec[0].one('dg-media'), 'Vertical en desktop; en tablet y móvil entra la versión horizontal por <code>&lt;picture&gt;</code>. AVIF primero, WebP de respaldo.', 'ds-stage--pad', '360px')
    # --- lectura progresiva
    E['acordeon'] = ejemplo('acordeon', 'Acordeón con índice', L.one('dg-accordion'), 'El primero abre; cada uno lleva número y la flecha indica que se despliega.', 'ds-stage--pad')
    leer = sec[2].all('dg-copy')[0]
    E['leer-mas'] = ejemplo('leer-mas', 'Leer más', [leer, sec[2].one('dg-readmore-panel')], 'Corta un párrafo largo en el punto de tensión. «Ver más» va en violeta y subrayado.', 'ds-stage--pad')
    # --- tarjetas
    E['tarjetas'] = ejemplo('tarjetas', 'Tarjetas con placa de icono', L.one('dg-criteria-card-grid'), 'Cuatro ideas cortas. Cada placa toma el color de su significado con <code>--accent</code>.', 'ds-stage--pad')
    E['tarjetas-lado'] = ejemplo('tarjetas-lado', 'Tarjetas con icono al lado', L.one('dg-feature-grid'), 'Para beneficios con una frase de énfasis y texto de apoyo.', 'ds-stage--pad')
    E['tarjetas-guardia'] = ejemplo('tarjetas-guardia', 'Tarjetas de garantía de seguridad', L.one('dg-guard-grid'), 'Icono y título en la misma línea; el texto puede llevar un enlace en línea.', 'ds-stage--pad ds-stage--wide')
    E['inclusion'] = ejemplo('inclusion', 'Tarjetas de lo que incluye', L.one('dg-inclusion-grid'), 'Cuatro columnas en escritorio; icono y título en la misma línea.', 'ds-stage--pad ds-stage--wide')
    E['aviso-reglas'] = ejemplo('aviso-reglas', 'Tarjeta con acción secundaria', L.one('dg-rules-callout'), 'Lleva a la página de reglas con un botón secundario.', 'ds-stage--pad')
    # --- producto
    E['chat'] = ejemplo('chat', 'Chat de producto', L.one('dg-product'), 'Muestra una conversación real con ADA. En la página los mensajes entran uno a uno al llegar con el scroll.', 'ds-stage--pad', '640px')
    E['formulario'] = ejemplo('formulario', 'Formulario «Conversa con ADA»', L.one('dg-ada-cta'), 'Etiqueta arriba de cada campo, campos de 48 px y un solo botón. En escritorio va en una fila junto a ADA.', 'ds-stage--form ds-stage--wide')
    # --- precio
    E['precio'] = ejemplo('precio', 'Tarjetas de precio', L.one('dg-pricing-grid'), 'La opción destacada es más grande a propósito: es la única excepción a la regla de altura. Lleva borde verde y fondo propio.', 'ds-stage--pad')
    E['garantia'] = ejemplo('garantia', 'Sello de garantía', L.one('dg-guarantee-seal'), '', 'ds-stage--pad', '420px')
    # --- preguntas
    E['faq'] = ejemplo('faq', 'Preguntas frecuentes', L.one('dg-pending'), 'Cada pregunta se despliega en su sitio.', 'ds-stage--pad')
    # --- navegación y marco
    E['nav'] = ejemplo('nav', 'Barra de navegación', L.one('dg-nav'), 'Fija arriba. Lleva los temas, el cambio de tema, la acción principal y la barra de progreso de lectura.', 'ds-stage--nav ds-stage--wide')
    E['movil'] = ejemplo('movil', 'Barra de acción en móvil', L.one('dg-mobile-cta'), 'Solo en móvil, fija abajo. Antes de la oferta invita a conversar con ADA; en la oferta, a inscribir.', 'ds-stage--movil', '420px')
    E['dialogo'] = ejemplo('dialogo', 'Diálogo', L.one('dg-dialog'), 'Se abre desde «Conversar con ADA». En móvil sube desde abajo.', 'ds-stage--dialog')
    E['pie'] = ejemplo('pie', 'Pie de página', L.one('dg-footer'), 'Logo, quién lo desarrolla, enlaces y contacto.', 'ds-stage--wide')
    # --- reglas de ADA
    rs = R.one('dg-rules-summary')
    E['reglas-resumen'] = ejemplo('reglas-resumen', 'Entrada de la página de reglas', rs, 'Título, promesa, ADA con la tableta y el índice de las 13 reglas.', 'ds-stage--wide')
    cards = R.all('dg-rule-card')
    rejilla = Node('div', [('class', 'dg-rules-grid')]); rejilla.kids = cards[1:7]   # dos filas en su rejilla real: se ve que todas miden lo mismo
    E['regla'] = ejemplo('regla', 'Tarjeta de regla', rejilla, 'Icono con el color que rota, número, título, la regla en una frase y su explicación. Todas miden lo mismo de alto, en la fila y entre filas.', 'ds-stage--pad ds-stage--wide')
    E['regla-principal'] = ejemplo('regla-principal', 'Tarjeta de la regla principal', cards[0], 'La primera regla ocupa todo el ancho y lleva imagen.', 'ds-stage--pad ds-stage--wide')
    return E


# ------------------------------------------------------------------ armado
def construir():
    t = open(os.path.join(AQUI, 'plantilla.html'), encoding='utf-8').read()
    E = libreria()
    usados = set()

    def sub(m):
        tipo, arg = m.group(1), m.group(2).strip()
        if tipo == 'lib':
            usados.add(arg); return E[arg]
        if tipo == 'css': return css_de(arg)
        if tipo == 'var': return var(arg)
        if tipo == 'tabla-color': return tabla_color()
        if tipo == 'tabla-contraste': return tabla_contraste()
        raise KeyError(tipo)

    out = re.sub(r'<!--@([\w-]+)(.*?)-->', sub, t)
    faltan = set(E) - usados
    open(os.path.join(AQUI, 'index.html'), 'w', encoding='utf-8').write(out)
    # las imágenes que usan los ejemplos se copian desde la landing (que no se toca), para que la guía sea autosuficiente
    refs = set(re.findall(r'(assets/[\w./-]+\.(?:webp|avif|svg|jpg|jpeg|ico))', out)); copiados = peso = 0; sin = []
    for r in sorted(refs):
        src, dst = os.path.join(PUBLIC, r), os.path.join(AQUI, r)
        if not os.path.exists(src): sin.append(r); continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst): shutil.copy2(src, dst)
        copiados += 1; peso += os.path.getsize(dst)
    print(f'imágenes de los ejemplos: {copiados} archivos · {peso / 1048576:.1f} MB' + (f' · no encontradas: {sin}' if sin else ''))
    print(f'index.html: {len(out) // 1024} KiB · ejemplos de librería: {len(usados)} de {len(E)}' + (f' · sin colocar: {sorted(faltan)}' if faltan else ''))
    # comprobación: ningún identificador repetido y ningún enlace de la guía sin destino
    # (los enlaces que traen los ejemplos no cuentan: dentro del recuadro no navegan)
    ids = re.findall(r'\sid="([^"]+)"', out)
    repetidos = sorted({i for i in ids if ids.count(i) > 1})
    sin_destino = sorted(set(re.findall(r'href="#([^"]+)"', t)) - set(ids))
    if repetidos: print(f'AVISO · identificadores repetidos: {repetidos}')
    if sin_destino: print(f'AVISO · enlaces de la guía sin destino: {sin_destino}')
    if not repetidos and not sin_destino: print('enlaces e identificadores: sin problemas')


if __name__ == '__main__':
    construir()
