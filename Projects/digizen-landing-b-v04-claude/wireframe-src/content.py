# -*- coding: utf-8 -*-
"""
Contenido del wireframe de recorrido (Fase 2).
Todo el copy de producción vive aquí UNA sola vez, literal, tomado de 00-context/COPY-PUBLICADO.md.
build.py lo renderiza a 02-wireframe.html y audita que esté completo y en orden.

Campos de cada parada:
  id    identificador de parada
  comp  composición del catálogo de 01-design-system.md (§3)
  kind  comportamiento en el pin: read | lead | golpe | two | seal | dialog | cta | hero | panel
  E     estacionamiento en encuadres de scroll (1 E = 100svh)
  night escenario oscuro (bisagra)
  scan  entra en el escaneo de 3 segundos
  bp    'all' | 'd' (solo desktop) | 'm' (solo móvil)
  note  anotación de intención (no es UI)
"""
import re

WIDE_MIN = 230  # regla del usuario (2026-09-28): si algún párrafo pasa de 230 caracteres, columna ancha; si no, angosta (umbral ajustado el 2026-09-29 para incluir 11.1)

S = "00-context/scenes/"

# ---------- helpers de composición (clases = pasos de la escala del espécimen) ----------
def b01(close, cap=None, size="mon", w=8, align="ctr"):
    h = f"<div class='c {align} stack b01'>\n<h2 class='pf w{w} t-{size} bw'>{close}</h2>\n"
    if cap:
        h += f"<p class='in w5 t-body'>{cap}</p>\n"
    return h + "</div>"

def b03(lead, close, size="mon", w=8, lead_cls="in w5 t-sub", lead_tag="p"):
    return (f"<div class='c ctr stack b03'>\n<{lead_tag} class='{lead_cls} lead-l bw' data-beat='lead'>{lead}</{lead_tag}>\n"
            f"<p class='pf w{w} t-{size} bw' data-beat='close'>{close}</p>\n</div>")

def lead(text, cls="in w5 t-sub"):
    return f"<div class='c ctr stack solo-lead'>\n<p class='{cls} lead-l bw' data-beat='lead'>{text}</p>\n</div>"

def l06(title, paras, title_cls="pf w7 t-head", tag="h2", wide=None):
    ps = "\n".join(f"<p class='in w5 t-body'>{p}</p>" for p in paras)
    if wide is None:
        wide = bool(paras) and max(len(re.sub(r"<[^>]+>", "", p)) for p in paras) >= WIDE_MIN
    return f"<div class='c l06{' wide' if wide else ''}'>\n<{tag} class='{title_cls} bw'>{title}</{tag}>\n<div class='sup'>\n{ps}\n</div>\n</div>"

def l07(paras, wide=None):
    ps = "\n".join(f"<p class='in w5 t-body'>{p}</p>" for p in paras)
    if wide is None:
        wide = max(len(re.sub(r"<[^>]+>", "", p)) for p in paras) >= WIDE_MIN
    w = " wide" if wide else ""
    return f"<div class='c l07{w}'>\n<div class='essay'>\n{ps}\n</div>\n</div>"

def seal(fn, zoom=None, direction="out", origin=None, fit=None, origin_m=None):
    """origin_m: punto del zoom en la vertical (móvil/tablet), si el objeto está en otro lugar que en la horizontal."""
    z = f" data-zoom='{zoom}' data-zoom-dir='{direction}'" if zoom else ""
    z += f" data-fit='{fit}'" if fit else ""
    z += f" data-origin='{origin}'" if origin else ""
    z += f" data-origin-m='{origin_m}'" if origin_m else ""
    return f"<figure class='c-seal'{z}><img src='{S}{fn}' alt=''><figcaption class='wf-file'>{fn}</figcaption></figure>"

def seq(folder, n, poster, reverse=False):
    """Secuencia de cuadros controlada con el scroll (scrub de video), dibujada en canvas. El póster se ve mientras carga y en modo reducido."""
    rv = " data-reverse='1'" if reverse else ""
    return (f"<figure class='c-seal c-seq' data-seq='{folder}' data-n='{n}'{rv}><canvas></canvas>"
            f"<img class='seq-poster' src='{folder}/{poster}' alt=''><figcaption class='wf-file'>{folder} · {n} frames · scrub</figcaption></figure>")

def l05(quote, prose):
    return (f"<div class='c l05'>\n<h3 class='pf w7 it t-semi bw w-q'>{quote}</h3>\n"
            f"<div class='def'>\n<p class='in w5 t-body'>{prose}</p>\n</div>\n</div>")

def entry(leadin, rest, span=4):
    return f"<div class='entry s{span}'>\n<p class='in w5 t-body'><b class='w7'>{leadin}</b> {rest}</p>\n</div>"

def card(title, body, extra="", span=4, new=False):
    """Tarjeta de L08 con subtítulo (subhead del espécimen, Playfair romana) + párrafo (+ botón opcional).
    new=True: el subtítulo NO está en COPY-PUBLICADO.md; es una adición aprobada por el usuario y se rotula en el wireframe."""
    mark = "<span class='wf-new'>copy agregado · aprobado</span>" if new else ""
    dn = " data-new='aprobado'" if new else ""
    return f"<div class='entry card s{span}'>{mark}\n<h4 class='pf w5 t-sub bw card-t'{dn}>{title}</h4>\n<p class='in w5 t-body'>{body}</p>{extra}\n</div>"

def l08(head, entries, head_tag="h3", deck=False):
    """deck=True: mazo apilado en móvil (< 600 px) y tarjetas una debajo de otra en tablet (kind 'deck')."""
    h = f"<div class='c l08'>\n"
    if head:
        h += f"<{head_tag} class='pf w7 t-head bw'>{head}</{head_tag}>\n"
    return h + f"<div class='entries{' deck' if deck else ''}'>\n" + "\n".join(entries) + "\n</div>\n</div>"

CTA_INNER = ("<div class='cta'>\n"
             "<a class='btn' data-role='azul · inscripción'>Inscribir a mi hijo <span class='arr' data-dir='ne'>↗</span></a>\n"
             "<a class='btn alt' data-role='violeta · ADA'>Conversar con ADA primero<span class='arr' data-dir='e' data-icon='→' aria-hidden='true'></span></a>\n</div>")
# Botones = filas de acción (criterio del usuario, 2026-09-29): texto a la izquierda, flecha en un círculo a la derecha.
# La flecha que trae el copy (↗, ↓) es texto real dentro del círculo; si el copy no trae flecha, el ícono va por CSS (data-icon), sin texto.
CTA = "<div class='c ctr stack cta-wrap'>\n" + CTA_INNER + "\n</div>"

CUE = "<div class='cue' aria-hidden='true'><span></span><span></span><span></span></div>"
CUE_PATH = "<div class='cue cue-path' aria-hidden='true'><span></span><span></span><span></span></div>"

def acc(w):
    return f"<em class='acc'>{w}</em>"

def hl(w):
    """Concepto fuerte resaltado SOLO con color (sin itálica ni cambio tipográfico); el color lo pone el build según su función."""
    return f"<span class='hl'>{w}</span>"

def st(id, comp, kind, E, html, note, night=False, scan=False, bp="all"):
    return dict(id=id, comp=comp, kind=kind, E=E, html=html, note=note, night=night, scan=scan, bp=bp)

# ---------- recorrido ----------
PINS = []
def pin(id, cap, type_, stops=None, **kw):
    d = dict(id=id, cap=cap, type=type_, stops=stops or []); d.update(kw); PINS.append(d)

# HERO — autoplay (única imagen antes del texto)
pin("P-H0", "Hero", "hero", [
    st("H.1", "Hero", "hero", 1.5,
       f"<img class='hero-img' src='{S}01-dinner.webp' alt=''><div class='scrim'></div><img class='hero-logo' src='00-context/logo/digizen-logo-dark.svg' alt=''>"
       "<div class='c ctr hero-text'>\n<h1 class='pf w8 t-semi bw'>Te voy a decir cinco cosas que crees sobre tu hijo y el celular.</h1>\n</div>" + CUE,
       "Autoplay (no scrub): zoom-out extremo de 01-dinner en 3.7 s → pausa → velo → aparece la frase en semimonumental. Desktop con su propia configuración: texto abajo a la izquierda (7 columnas, 3 líneas, 24 % del encuadre) y velo solo en el tercio inferior, para no tapar las caras. Móvil: centrado, 4 líneas. Se repite al regresar (onEnterBack). Al final aparece el indicador de continuar.",
       scan=True),
])
pin("P-H", "Hero · apertura", "pin", [
    st("H.2", "B01", "golpe", 1.25,
       b01(f"Cuatro son {acc('falsas.')}", "Y sé cuál <b class='w7'>te va a doler.</b>"),
       "Golpe lapidario del Hero. Composición B01 literal del espécimen (mismas dos frases). El caption va en ink (decisión 2).",
       scan=True),
    st("H.3", "Puente (lead)", "lead", 1,
       lead("Esto te va a doler un poco. Y te va a servir mucho."),
       "Puente solo, en la línea lead de B03. Empuja hacia el cap. 01."),
])

# 01 · Lo que casi todos creemos
pin("P-01", "01 · Lo que casi todos creemos · 02 título", "pin", [
    st("01.1", "B01 (secundario)", "golpe", 1.25,
       b01("Lo que casi todos creemos", size="semi"),
       "Título = golpe (confirmado). Secundario → baja un paso: semimonumental.",
       scan=True),
    st("01.2", "L03", "read", 1,
       "<div class='c l03'>\n"
       "<div class='row'><span class='n pf w8 t-head'>01</span><p class='in w7 t-body'>El problema es cuánto tiempo pasa en el celular.</p></div>\n"
       "<div class='row'><span class='n pf w8 t-head'>02</span><p class='in w7 t-body'>Si configuro bien la app de control (Family Link, Tiempo en pantalla), se acaba el problema.</p></div>\n"
       "<div class='row'><span class='n pf w8 t-head'>03</span><p class='in w7 t-body'>Si le pongo contraseña, se acaba el problema.</p></div>\n"
       "<div class='row'><span class='n pf w8 t-head'>04</span><p class='in w7 t-body'>Los chavos de hoy son más hábiles que uno. Ya perdí.</p></div>\n"
       "<div class='row last'><span class='n pf w8 t-head'>05</span><p class='in w7 t-body'>No me escucha.</p><span class='acc-mark' data-at='exit'>acento</span></div>\n"
       "</div>",
       "L03 = la lista 01–05. La fila 05 recibe el acento del espécimen recién al salir de la parada (anticipa la revelación, no la delata antes).",
       scan=True),
    st("01.3", "B03 (revelación en tres tiempos)", "reveal", 1.75,
       "<div class='c ctr reveal b03'>\n<p class='in w5 t-sub lead-l bw' data-beat='lead'>Ahora te digo cuál es la verdad.</p>\n"
       "<div class='ctr stack' data-beat='close'>\n<p class='pf w8 t-semi bw' data-step='1'>La cinco.</p>\n<p class='pf w8 t-mon bw' data-step='2'>No te <em class='acc'>escucha.</em></p>\n</div>\n</div>",
       "Bisagra 1 (oscuro). Tres tiempos (pedido del usuario): 1) el puente solo; 2) el puente se desvanece y aparece «La cinco.» (semimonumental, solo señala); 3) cae «No te escucha.» (monumental, revela, con acento). Puente y revelación ocupan el mismo lugar: nunca hay más de dos tamaños en pantalla.",
       night=True, scan=True),
    st("01.4", "B01 (golpe + remate)", "golpe", 1.25,
       b01("Pero no por lo que crees.", "Y ahí es donde se pone interesante.", size="semi"),
       "Sigue en oscuro. Gramática «golpe + remate», como H.2: «Pero no por lo que crees.» es el giro (grande); «Y ahí es donde se pone interesante.» solo anuncia (remate). Al salir vuelve la luz.",
       night=True),
    st("02.1", "B01 (título en display)", "golpe", 1,
       "<div class='c ctr stack b01'>\n<h2 class='pf w8 t-semi bw'>Las cuatro falsas, una por una</h2>\n</div>" + CUE_PATH,
       "Título en semimonumental con la gramática de los títulos que golpean (B01, centrado). Camino de triángulos centrado abajo, fuera del bloque del título (así no hereda su transform ni choca con el texto).", scan=True),
])

# 02 · Las cuatro falsas, una por una
pin("P-02b", "02 · Las cuatro falsas (horizontal)", "h", [
    st("02.2", "L05 (cita-eco + prosa)", "panel", 1,
       ("<div class='c l05'>\n<h3 class='pf w7 it t-semi bw w-q'>«El problema es el tiempo.»</h3>\n<div class='def'>\n"
        "<p class='in w5 t-body'>Eso ya lo intentaste medir. <b class='w7'>Negociaste «una hora y ya».</b> Y cuando por fin cumplía la hora, ¿se sentía resuelto? Una mamá nos lo dijo así, y no se nos ha borrado:</p>\n"
        "<p class='pf it w7 t-sub q-in bw'>«Ni siquiera me mira a los ojos.»</p>\n"
        "<p class='in w5 t-body'>Eso no se mide en minutos.</p>\n</div>\n</div>"),
       "Patrón 3+5: pin + desplazamiento horizontal. Cada panel llega y se estaciona el 70 % de su E; el paso al siguiente ocurre en el 30 % restante. Snap a la mitad de cada estacionamiento, sin inercia (corrección del usuario: antes cambiaba casi en automático). Panel 1/4. La cita-eco es micro-golpe de apertura del bloque.",
       scan=True),
    st("02.3", "L05", "panel", 1,
       l05("«Si configuro bien la app de control…»",
           "Un papá escribió esto en una reseña de Family Link: <b class='w7'>«falsa sensación de control»</b>. No lo escribió un experto. Lo escribió alguien que ya lo configuró bien."),
       "Panel 2/4. Entra desde la derecha; si regresas, sale por la derecha.", scan=True),
    st("02.4", "L05", "panel", 1,
       l05("«Si le pongo contraseña, se acaba el problema.»",
           "La frase que más hemos escuchado, de papás distintos, en ciudades distintas: <b class='w7'>«en dos días encontró cómo saltárselo»</b>. Tu hijo tiene todo el día para resolver un acertijo que tú revisas dos minutos en la noche. <b class='w7'>No es mala suerte. Es aritmética.</b>"),
       "Panel 3/4.", scan=True),
    st("02.5", "L05", "panel", 1,
       l05("«Ya perdí.»",
           "Ésta es la más cómoda de las cuatro, porque si ya perdiste, no tienes que hacer nada. Aguanta. Ahorita llegamos ahí."),
       "Panel 4/4. «Aguanta. Ahorita llegamos ahí.» es el puente de cierre, pero vive dentro del párrafo: no se separa.", scan=True),
])
# 03 · Ahora, un favor.
pin("P-03a", "02 sello · 03 · Ahora, un favor.", "pin", [
    st("02.6", "Sello (zoom-in largo)", "seal", 1.5, seal("02-facial-recognition.webp", zoom=1.5, direction="in", origin="57% 62%", origin_m="72% 50%"),
       "Sella el capítulo completo. Zoom-in largo con scroll (pedido del usuario): de 1× a 1.5× en 1.5 E, hacia el celular con el candado y el reloj; en el encuadre final siguen la cara del chico, el celular y parte de la laptop. El snap se detiene al terminar el zoom. La referencia usa «candados»; aquí la pantalla del celular muestra candado y reloj de arena (tiempo + contraseña). Alternativa: 02-facial-recognition-alt."),
    st("03.1", "L06", "read", 1,
       l06("Ahora, un favor.", ["Acuérdate de lo que acabas de leer sobre el candado."]),
       "Título-puente («Ahora…») + primera línea.", scan=True),
    st("03.2", "L06 (título en voz de puente)", "read", 1,
       "<div class='c l06'>\n<p class='pf w7 t-sub bw lead-l'>¿Qué sentiste?</p>\n<div class='sup essay'>\n"
       "<p class='in w5 t-body'>No fue enojo. Apuesto a que fue otra cosa: esa angustia de <b class='w7'>«ya lo sé… ¿y entonces qué hago?»</b>. Ver a tu hijo ahí, con el celular, y no saber qué más hacer.</p>\n"
       "<p class='in w5 t-body'>Quédate con eso un segundo. <b class='w7'>Porque te acabo de hacer exactamente lo que tú le haces a él.</b></p>\n</div>\n</div>",
       "Gramática «puente + lectura»: el encabezado en el subhead del espécimen (Playfair 500 romana, 24/19; corrección del usuario); los párrafos en body (Inter), con negritas según el criterio editorial: la voz citada «ya lo sé… ¿y entonces qué hago?» y el remate que gira el argumento."),
    st("03.3", "B03 (cierre secundario)", "two", 1.5,
       b03("Ahora acuérdate de la cara de tu hijo la quinta vez que le dijiste <b class='w7'>«ya deja el cel»</b>.",
           "<span class='hl'>Los ojos al techo. En señal de fastidio.</span>", size="semi"),
       "Puente → golpe secundario (semimonumental). La escena lo sella en la siguiente parada.", scan=True),
    st("03.4", "Secuencia con scrub (desktop)", "seq", 1.5, seq("assets/seq/03-fastidio", 49, "fastidio-f064.webp"),
       "Desktop: video con scrub (decisión del usuario). 49 cuadros WebP de 1280 px (3.0 MB) sacados de «initial_image»; el scroll recorre el gesto completo (mira el celular → ojos al techo → cabeza atrás) en 1.5 E y se estaciona al final. Póster = cuadro 64 (modo reducido y mientras carga).", bp="d"),
    st("03.4m", "Sello (imagen fija)", "seal", 1,
       "<figure class='c-seal'><img src='assets/seq/03-fastidio/fastidio-f064.webp' alt=''><figcaption class='wf-file'>PROVISIONAL · cuadro 64 del video · se reemplaza por la imagen fija nueva</figcaption></figure>",
       "Móvil y tablet: imagen fija (decisión del usuario: ahí el scrub de video es más frágil). PROVISIONAL: el cuadro más expresivo del video, hasta generar la imagen fija nueva.", bp="m"),
])
pin("P-03b", "03 · Ahora, un favor. (cont.)", "pin", [
    st("03.5", "B03", "two", 1.5,
       b03("No siente lo mismo que tú. <b class='w7'>Tú sientes angustia. Él ya está harto de oírlo.</b> Pero los dos están parados en el mismo lugar:",
           f"Alguien les dijo {hl('«no»')}, y nadie les dijo {acc('«cómo»')}."),
       "Bisagra 2 (oscuro). Lapidario del capítulo (confirmado). El lead termina en dos puntos: anuncia el corte. «no» y «cómo» en acento como antítesis (pedido del usuario, 2026-09-29): en el build, «no» en coral (la prohibición) y «cómo» en azul (el método).",
       night=True, scan=True),
    st("03.6", "L07", "read", 1,
       l07(["Yo te dije <b class='w7'>«el candado no sirve»</b> y no te di nada a cambio. Tú le dices <b class='w7'>«deja el cel»</b> y tampoco. Y con un <b class='w7'>«no» no se construye nada</b>. Ni criterio, ni conversación. <b class='w7'>Solo un hijo que busca el «cómo»</b> por su cuenta. Y lo encuentra: en dos días. Solo que fue el cómo saltárselo."]),
       "Vuelve la luz. Lectura."),
    st("03.7", "B01 (golpe dentro de párrafo)", "golpe", 1.25,
       "<div class='c left stack b01 b01-l'>\n<p class='pf w8 t-semi bw'>Por eso <span class='hl'>«no me escucha»</span> era la única verdadera.</p>\n<p class='in w5 t-body'>Pero la razón no es que sea rebelde. Es que <b class='w7'>un «no» sin «cómo» no le deja nada que hacer</b>. Y a un «no» sin «cómo» nadie responde con criterio. Se responde con <b class='w7'>un candado abierto en dos días</b>.</p>\n</div>",
       "Gramática «golpe dentro de párrafo» (layout de 03.7, 08.4 y 12.4): la primera frase paga la revelación del cap. 01 y va en grande y centrada (ajuste del usuario); el resto del párrafo sigue en la columna de lectura, 32/48 px debajo, en el mismo encuadre.", scan=True),
    st("03.8", "Sello", "seal", 1, seal("04-shield.webp", zoom=1),
       "Sella el capítulo: mamá e hija, cada una con su escudo, separadas. Cubre todo el contenedor en desktop, como las demás escenas (pedido del usuario, 2026-09-29; antes se mostraba completa con franjas). Movimiento: solo disolvencia de entrada, sin zoom (pedido del usuario)."),
])

# 04 · respiro
pin("P-04", "04 · No eres mala mamá ni mal papá", "pin", [
    st("04.1", "L06", "read", 1,
       l06("Antes de seguir: no eres mala mamá ni mal papá.",
           ["Lo digo en serio, y lo digo <b class='w7'>como papá que también trae el celular en la mano</b> todo el día."]),
       "Capítulo de respiro: solo composiciones L, sin acento, sin oscuro, sin imagen.", scan=True),
    st("04.2", "L07", "read", 1,
       l07(["A ti te tocó un mundo de calles y bicicletas. A tu hijo le tocó uno que se inventa cada mañana, que nadie te enseñó a leer, y que cambió las reglas mientras tú trabajabas para darle de comer. <b class='w7'>Nadie te dio el manual.</b> Tus papás no estaban preparados. Tampoco el papá de junto.",
            "Todo lo que has hecho, quitar, vigilar, negociar, <b class='w7'>lo hiciste por amor</b>. Por eso duele que no funcione."]),
       "Lectura."),
    st("04.3", "L07", "read", 1,
       l07(["<b class='w7'>Tu instinto no está roto.</b> Te ayudó a resolver otros problemas. Éste necesita algo distinto.",
            "<b class='w7'>Suéltate la culpa.</b> Necesitas espacio para lo que sigue."]) + CUE,
       "Lectura. VISION §4 proponía un golpe aquí; se respeta §1.1/§5 (sin golpe) — ver decisión en 02-wireframe.md."),
])

# 05 · el cómo
pin("P-05a", "05 · Ahora sí: el «cómo»", "pin", [
    st("05.1", "L06", "read", 1,
       l06("Ahora sí: el «cómo». Y ya lo sabes hacer.", ["Te pongo un ejemplo."]),
       "Título-puente («Ahora sí:»).", scan=True),
    st("05.2", "L07", "read", 1,
       l07(["Piensa en algo que parece no tener nada que ver con el celular: <b class='w7'>cruzar la calle</b>.",
            "Al principio le das la mano. Te detienes con él. <b class='w7'>Miras a los dos lados.</b> Le explicas por qué ese coche, aunque esté lejos, importa. No lo haces para llevarlo de la mano hasta los cuarenta. <b class='w7'>Lo haces para que un día cruce sin ti.</b>"]),
       "Lectura: la metáfora de cruzar la calle."),
    st("05.3", "B01 (golpe dentro de párrafo)", "golpe", 1.25,
       "<div class='c left stack b01 b01-l'>\n<p class='pf w8 t-semi bw'>Ahora imagina que la única lección hubiera sido: <span class='hl'>«No cruces.»</span></p>\n"
       "<p class='in w5 t-body'>Funciona mientras estás en la esquina. Y el día que tiene que cruzar solo, <b class='w7'>se para en la banqueta sin saber mirar</b>. Nadie le enseñó. <b class='w7'>Solo le dijeron que no.</b></p>\n</div>",
       "Mismo layout que 03.7 (pedido del usuario): la frase en semimonumental y centrada; el párrafo en la columna de lectura, 32/48 px debajo, en el mismo encuadre.", scan=True),
    st("05.4", "B01 (golpe en dos alturas)", "reveal", 1.5,
       "<div class='c ctr stack b01'>\n<p class='pf w8 t-semi bw' data-step='1'>Bloquearle el celular es</p>\n<p class='pf w8 t-mon bw' data-step='2'><span class='hl'>«no cruces»</span>.</p>\n</div>",
       "Golpe en dos alturas (pedido del usuario, mismo patrón que 01.3): «Bloquearle el celular es» señala → semimonumental; «no cruces». revela → monumental. Dos tiempos: primero lo que señala, al seguir scrolleando lo que revela.", scan=True),
    st("05.5", "Secuencia con scrub (desktop)", "seq", 1.5, seq("assets/seq/05-crossing", 49, "05-crossing-poster.webp", reverse=True),
       "Desktop: video con scrub (pedido del usuario), REPRODUCIDO AL REVÉS (pedido del usuario, 2026-09-29; se estaciona en el cuadro inicial del video, que es la escena fija): el feed de la calle fluye mientras la mamá señala. 49 cuadros WebP de 1280 px, calidad 50 (4.5 MB; el detalle de las fichas pesa más que en fastidio), sacados del video «Style_Hybrid…» (1908×1084, 5 s). Se estaciona al final. Sella la metáfora a mitad del capítulo; el lapidario viene después, sin imagen propia.", bp="d"),
    st("05.5m", "Sello (imagen fija)", "seal", 1, seal("05-crossing.webp"),
       "Móvil y tablet: imagen fija. Falta su versión vertical (00-context/scenes/vertical/05-crossing-v.webp). Alternativa: 05-crossing-alt.", bp="m"),
])
pin("P-05b", "05 · el «cómo» (cont.)", "pin", [
    st("05.6", "Puente (lead)", "lead", 1,
       lead("Y <b class='w7'>el día en que cruce solo va a llegar</b>. A los 13, a los 17, a los 25, en un mundo que ni tú ni yo podemos imaginar todavía."),
       "Puente solo que prepara la tesis."),
    st("05.7", "B06 (antítesis)", "golpe", 1.25,
       "<div class='c ctr stack b06'>\n<p class='pf w8 t-mon bw'>El control caduca.</p>\n<p class='pf w8 t-mon bw'><em class='acc'>El criterio no.</em></p>\n</div>",
       "Bisagra 3 (oscuro). Tesis de la pieza. Gramática «antítesis»: la misma forma que el cierre de marca (12.7), dos líneas iguales con acento en la segunda, para que al final el lector reconozca la tesis en «Presencia, no vigilancia. / Criterio, no candado.».",
       night=True, scan=True),
    st("05.8", "B03 (entrada → revelación)", "two", 1.5,
       b03("Ese día, lo único que va a cruzar la calle con él es", "<span class='hl'>lo que le hayas enseñado antes.</span>", size="semi"),
       "Vuelve la luz. La frase se parte en entrada y revelación (pedido del usuario): «lo que le hayas enseñado antes.» en semimonumental, un paso abajo de la tesis (05.7, monumental) para no competir con ella.", scan=True),
])

# 06 · respiro
pin("P-06", "06 · ¿Y cómo se enseña a mirar a los dos lados?", "pin", [
    st("06.1", "L06", "read", 1,
       l06("¿Y cómo se enseña a mirar a los dos lados?",
           ["Aquí viene la parte que casi nadie quiere oír, porque es <b class='w7'>más lenta que un candado</b>."]),
       "Respiro: solo L.", scan=True),
    st("06.2", "L07", "read", 1,
       l07(["Acuérdate del <b class='w7'>«no» sin «cómo»</b>. Ya viste lo difícil que es escuchar cuando uno está a la defensiva. Entonces, ¿cómo entra?",
            "Piensa en la última vez que tú cambiaste de opinión sobre algo importante. Apuesto a que no fue porque alguien te gritó. Fue porque <b class='w7'>alguien te hizo una pregunta</b> que te quedaste pensando en el coche, de regreso a la casa."]),
       "Lectura."),
    st("06.3", "L07", "read", 1,
       l07(["<b class='w7'>El criterio se construye con preguntas.</b> No con <b class='w7'>«deja el cel»</b>. Con «¿quién hizo este video y qué quiere de ti?». Con «¿esto te sirve, o te está usando?». Con «¿qué crees que siente la persona de esa foto?»."]),
       "Lectura. VISION §4 proponía golpe con la primera frase; está dentro del párrafo y el capítulo es de respiro — ver decisión."),
    st("06.4", "L07", "read", 1,
       l07(["Esas preguntas no salen en un sermón de domingo que él ya dejó de oír. <b class='w7'>Salen en una conversación.</b> En su idioma. En el momento en que está pasando.",
            "Y ahí está el problema práctico: <b class='w7'>tú no puedes estar ahí en cada momento</b>. Ni yo. Nadie."]),
       "Lectura."),
    st("06.5", "Puente (lead)", "lead", 1,
       lead("Pero <b class='w7'>sí hay alguien que puede estar ahí</b> cada vez que él practique. Todas las veces que haga falta.") + CUE,
       "Puente de cierre hacia ADA."),
])

# 07 · Esto se llama ADA.
pin("P-07a", "07 · Esto se llama ADA. + conversación", "pin", [
    st("07.1", "Presentación de ADA (texto 7 col + ADA 5 col)", "read", 1,
       "<div class='c ada-intro'>\n<div class='ada-text'>\n<h2 class='pf w7 t-head bw'>Esto se llama ADA.</h2>\n"
       "<p class='in w5 t-body'>Tu hijo entra a la página de Digizen y ahí conversa con ADA: <b class='w7'>un mentor de inteligencia artificial que le habla en su idioma, uno a uno</b>. Y conversa como conversa con sus amigos: por mensajes, a su ritmo. Sin un adulto mirando por encima del hombro. <b class='w7'>Sin nadie que lo juzgue por lo que pregunta.</b></p>\n</div>\n"
       "<figure class='ada-fig' data-seq='assets/seq/ada-wave' data-n='130' data-start='0' data-fit='contain' data-play='time' data-fps='24' data-mobile='still'>"
       "<canvas></canvas><img class='ada-still' src='assets/seq/ada-wave/f000.webp' alt=''><figcaption class='wf-file'>ADA · 130 cuadros de la versión A · saludo en tiempo real</figcaption></figure>\n</div>",
       "ADA de la versión A (copiada sin modificar A; sin su animación de chat). Texto a la izquierda y ADA a la derecha (pedido del usuario). Desktop: el saludo se reproduce SOLO, en tiempo real (130 cuadros a 24 fps ≈ 5.4 s), cuando la parada entra en pantalla, y se repite al regresar. No va atado al scroll: con scrub era demasiado sensible (ajuste del usuario); es un gesto de un solo uso, como el Hero. Móvil y tablet: primer cuadro fijo, abajo del párrafo, sin descargar el resto.", scan=True),
    st("07.2", "L07", "read", 1,
       l07(["No es un salón de clases. No es un robot que suelta tareas. No es un Kumon digital. Y <b class='w7'>no es un vigilante</b> metido en su celular leyendo sus chats. <b class='w7'>Eso rompería su confianza, y la tuya.</b>"]),
       "Lectura."),
    st("07.3", "L07", "read", 1,
       l07(["<b class='w7'>Es un lugar al que va a entrenar el criterio.</b> ADA lo lleva, conversando, a ver cómo funciona lo digital por dentro: cómo un video está hecho para convencerlo, por qué le cuesta dejar de ver videos, qué siente antes y después de pasar un rato en redes. Y <b class='w7'>en vez de decirle qué hacer, le hace la pregunta</b>. La que se queda pensando de regreso a casa."]),
       "Lectura."),
    st("07.4", "Diálogo", "dialog", 4,
       "<div class='c dlg'>\n<p class='pf w7 t-sub'>Una pregunta que abre otra puerta</p>\n<p class='in w5 t-micro dlg-k'>— Conversación de ejemplo</p>\n"
       "<div class='msg-row ada'><span class='avatar'><img src='assets/avatars/ada-avatar-136.webp' alt=''></span><div class='msg ada'><span class='who in w6 t-micro'>ADA</span><p class='in w5 t-body'>Antes de decidir si la compartes: ¿qué crees que siente la persona de la foto?</p></div></div>\n"
       "<div class='msg-row hijo'><span class='avatar'><img src='assets/avatars/hijo-avatar-136.webp' alt=''></span><div class='msg hijo'><span class='who in w6 t-micro'>HIJO</span><p class='in w5 t-body'>Pues pena. Pero yo no la tomé.</p></div></div>\n"
       "<div class='msg-row ada'><span class='avatar'><img src='assets/avatars/ada-avatar-136.webp' alt=''></span><div class='msg ada'><span class='who in w6 t-micro'>ADA</span><p class='in w5 t-body'>Es cierto. ¿Y qué cambia para él si tú la mandas a otro grupo?</p></div></div>\n"
       "<div class='msg-row hijo'><span class='avatar'><img src='assets/avatars/hijo-avatar-136.webp' alt=''></span><div class='msg hijo'><span class='who in w6 t-micro'>HIJO</span><p class='in w5 t-body'>Que la ve más gente. Yo también lo estaría haciendo más grande.</p></div></div>\n</div>",
       "Un mensaje por paso de scroll (4 snaps). ADA entra por la izquierda, HIJO por la derecha; al regresar salen por el mismo lado. Avatares como en la versión A (pedido del usuario): cuadrados de 34 px con radio 10, ADA a la izquierda y el hijo a la derecha; imágenes de A copiadas sin modificar A. Burbujas: tinte violeta (ADA) / cian (HIJO) en el build.",
       scan=True),
])
pin("P-07c", "07 · cierre", "pin", [
    st("07.5", "B01 (golpe en dos alturas, tres tiempos)", "reveal", 1.75,
       "<div class='c ctr stack b01'>\n<p class='pf w8 t-semi bw' data-step='1'>Una pausa.</p>\n<p class='pf w8 t-semi bw' data-step='2'>Una consecuencia.</p>\n"
       "<p class='pf w8 t-mon bw' data-step='3'>Una <em class='acc'>idea propia.</em></p>\n</div>",
       "Lapidario del capítulo (ajuste del usuario): «Una pausa.» y «Una consecuencia.» en semimonumental, una por línea; «Una idea propia.» completa en monumental, con el acento subrayado en «idea propia.». Patrón «golpe en dos alturas» en tres tiempos: cada frase aparece al seguir scrolleando y «idea propia.» cae al final.", scan=True),
    st("07.6", "Evolución (de → a, dos columnas)", "reveal", 1.5,
       "<div class='c evo'>\n<p class='in w5 t-body evo-pre' data-step='1'>Lo que construye ahí adentro se lo lleva puesto a sus juegos, a sus chats, a su vida. Y empieza a cruzar de</p>\n<div class='evo-cols'>\n"
       "<div class='evo-col a' data-step='2'><p class='pf w5 t-head bw'><span class='hl'>«lo que veo en redes me dice quién soy»</span></p></div>\n"
       "<div class='evo-conn' data-step='3'><span class='in w6 t-micro'>a</span><span class='evo-arrow' aria-hidden='true'></span></div>\n"
       "<div class='evo-col b' data-step='4'><p class='pf w8 t-head bw'><span class='hl'>«yo decido qué me sirve y qué quiero compartir»</span>.</p></div>\n</div>\n</div>",
       "Evolución en dos columnas (pedido del usuario): el antes en Playfair 400 y el después en Playfair 800; en medio, el «a» del copy con una flecha que se dibuja (→ en desktop, ↓ en móvil). Entra en tiempos: frase → antes → flecha → después. Mismas palabras, mismo orden.", scan=True),
    st("07.7", "L07", "read", 1,
       l07(["Te lo digo derecho: <b class='w7'>ADA está viva y está creciendo.</b> Tu hijo empieza con ella el día que lo inscribas, y las familias que entran ahora la moldean: lo que tu familia necesite se construye primero. No te pido que confíes en una promesa bonita. Más abajo te explico <b class='w7'>cómo hablar tú con ADA antes de pagar un peso</b>."]),
       "Lectura. Sin pausa de cierre: fluye directo al cap. 08 (como en la referencia)."),
])

# 08 · «Espera...»
pin("P-08a", "08 · «Espera. ¿Una IA hablando con mi hijo?»", "pin", [
    st("08.1", "B01 (secundario)", "golpe", 1.25,
       "<div class='c ctr stack b01'>\n<h2 class='pf w8 it t-semi bw'>«Espera. ¿Una IA hablando con mi hijo?»</h2>\n</div>",
       "Título = golpe (confirmado), semimonumental. Es la objeción del lector entre «»: va en voz citada (itálica), como las creencias del cap. 02.", scan=True),
    st("08.2", "L07", "read", 1,
       l07(["Sí. Y si has leído las noticias sobre inteligencia artificial y algo en ti se cerró, <b class='w7'>tienes razón en desconfiar</b>. Nosotros también las leemos. Y también nos preocupan. <b class='w7'>Por eso ADA existe.</b>",
            "Hay aplicaciones que simulan amistades o relaciones románticas. Common Sense Media advirtió en 2025 que los compañeros de inteligencia artificial presentaban <b class='w7'>riesgos inaceptables para menores</b>. <b class='w7'>ADA tiene un propósito educativo</b>: ayudarle a pensar y a tomar sus propias decisiones. No está planteada como pareja, terapeuta ni sustituto de las personas que lo acompañan."], wide=True),
       "Lectura con columna ancha (~60 caracteres por línea; pedido del usuario: con ~88 palabras la columna estándar quedaba angosta y muy alta). En móvil, igual que las demás."),
    st("08.3", "B09", "golpe", 1.25,
       "<div class='c ctr stack b09'>\n<p class='in w5 t-small'>Pero hay un dato que quiero que te lleves en la cabeza:</p>\n"
       "<p class='pf w8 t-mxl' data-beat='close'>7 de cada 10</p>\n"
       "<p class='in w7 t-body'>adolescentes ya conversan con inteligencias artificiales. Solos, sin reglas, en plataformas hechas para adultos. México es tercer lugar mundial en adopción juvenil de IA.</p>\n</div>",
       "Dato = Registro B (confirmado). B09: el numeral en su lugar dentro de la frase, sin duplicarlo ni reordenar. Lapidario del capítulo. Candidato a patrón 10 (contador).",
       scan=True),
    st("08.4", "B01 (golpe dentro de párrafo)", "golpe", 1.25,
       "<div class='c left stack b01 b01-l'>\n<p class='pf w8 t-semi bw'>No es que vaya a pasar. <span class='hl'>Ya está pasando.</span></p>\n<p class='in w5 t-body'>Lo único que queda por decidir es cuál: una IA hecha para adultos, o <b class='w7'>una hecha para tu hijo, con reglas y con tu participación</b>.</p>\n</div>",
       "Gramática «golpe dentro de párrafo» (layout de 12.4): «No es que vaya a pasar. Ya está pasando.» en grande; el resto del párrafo en lectura, mismo encuadre.", scan=True),
])
_b1 = card("Cero rol romántico.", "Cero secretos peligrosos. Sus reglas están escritas y las vas a poder leer antes de empezar: qué hace ADA y qué no.",
           "\n<a class='btn sec' data-role='violeta · destino pendiente'>Conocer las reglas de ADA <span class='arr' data-dir='ne'>↗</span></a>")
_b2 = card("Tú también participas.", "Recibes su avance, qué está construyendo, qué está aprendiendo a decidir, sin espiar sus conversaciones. <b class='w7'>Un hijo espiado deja de hablar.</b> Y si algo de lo que dice indica que necesita ayuda de un adulto, te avisamos. ADA puede equivocarse: no diagnostica ni garantiza detectarlo todo. Antes de empezar vas a saber exactamente en qué casos te llega ese aviso.")
_b3 = card("Práctica y breve", "Con un tiempo definido para cada conversación. ADA no quiere sus horas. <b class='w7'>Quiere su criterio.</b>", new=True)  # «Práctica y breve»: adición de copy aprobada por el usuario (02-wireframe.md §8)
pin("P-08b", "08 · reglas", "pin", [
    st("08.5", "L08", "read", 1, l08("ADA es lo segundo, por diseño:", [_b1, _b2, _b3]),
       "Tres tarjetas separadas (pedido del usuario): subtítulo (subhead Playfair) + párrafo; «Conocer las reglas de ADA ↗» como botón secundario; la tercera lleva el título «Práctica y breve», adición de copy aprobada por el usuario. Desktop: tres columnas.", scan=True, bp="d"),
    st("08.5m", "L08 (mazo apilado)", "deck", 1.75, l08("ADA es lo segundo, por diseño:", [_b1, _b2, _b3], deck=True),
       "Móvil y tablet: las tres tarjetas en la MISMA parada (pedido del usuario). Tablet (600–859 px): caben juntas; aparecen una debajo de otra con el scroll. Móvil (< 600 px): no caben (~150 % a 360 px), así que van en mazo apilado (decisión del usuario; patrón 3 + 8 del catálogo): el título se queda, cada tarjeta sube desde abajo y se apila sobre la anterior, que queda asomada por su subtítulo. Snap por tarjeta. Al volver hacia arriba reaparece el botón «Conocer las reglas de ADA ↗» de la primera tarjeta.", scan=True, bp="m"),
])

# 09 · respiro / instruccional
pin("P-09", "09 · Y la prueba no te la pido por fe.", "pin", [
    st("09.1", "B01 (golpe en dos alturas)", "reveal", 1.5,
       "<div class='c ctr stack b01'>\n<h2 class='pf w8 t-semi bw' data-step='1'>Y la prueba no te la pido por fe.</h2>\n<p class='pf w8 t-mon bw' data-step='2'><span class='hl'>Habla tú con ADA primero.</span></p>\n</div>",
       "Golpe en dos alturas (pedido del usuario, mismo patrón que 01.3 y 05.4): «Y la prueba no te la pido por fe.» señala → semimonumental; «Habla tú con ADA primero.» revela → monumental. Dos tiempos.", scan=True),
    st("09.2", "Sello", "seal", 1, seal("06-rules.webp", zoom=1),
       "El papá con la tableta, después de «Habla tú con ADA primero.» (pedido del usuario, 2026-09-29; antes sellaba las reglas en 08.6). Sin zoom, solo disolvencia de entrada (pedido del usuario). Alternativa: 06-rules-alt."),
    st("09.3", "L07 + botón + puente", "read", 1.25,
       "<div class='c l07 wide'>\n<div class='essay'>\n"
       "<p class='in w5 t-body'>Pide tu acceso al final de esta página para <b class='w7'>conversar tú con ADA antes de inscribir a tu hijo</b>. Interrógala. Trata de sacarla de sus reglas. Pregúntale lo que un niño le preguntaría. Pregúntale qué no va a hacer nunca con tu hijo. <b class='w7'>Te va a contestar sin rodeos.</b></p>\n"
       "<p class='in w5 t-body'>Queremos que conozcas a la inteligencia artificial con la que hablará tu hijo <b class='w7'>antes de pagar</b>. Por eso la ponemos por delante.</p>\n"
       "<div class='ctr stack go-stack go-in'>\n<a class='btn sec' data-goto='11.1' data-role='azul · ancla #inscripcion'>Si ya viste suficiente, la inscripción está al final de esta página <span class='arr' data-dir='s'>↓</span></a>\n"
       "<p class='in w5 t-body bw tc'>Si no, sigue leyendo; falta lo más importante.</p>\n</div>\n</div>\n</div>" + CUE,
       "UNA sola lámina (pedido del usuario): lectura en la columna ancha (como 08.2), y debajo, centrados a lo ancho (pedido del usuario), el botón secundario (mismo estilo que «Conocer las reglas de ADA ↗») y el texto debajo. PRIMER CTA del recorrido: el salto a la inscripción que ya trae el copy. Toque → feedback inmediato; el scroll animado se interrumpe si el usuario hace scroll. El puente empalma con el título del cap. 10.",
       scan=True),
])

# 10 · Lo más importante no es ADA.
pin("P-10a", "10 · Lo más importante no es ADA.", "pin", [
    st("10.1", "B03", "two", 1.5,
       b03("Lo más importante no es ADA.", "Eres <span class='hl'>tú.</span>", size="mxl", lead_tag="h2"),
       "Título + primera línea = un solo golpe (confirmado). Rima con «Ya lo tienes.» (12.2): los dos momentos en que la pieza le devuelve el protagonismo al papá van en monumental-xl.",
       scan=True),
    st("10.2", "L07", "read", 1,
       l07(["Esto no es una app que le instalas en el teléfono y te olvidas. <b class='w7'>Los incluye a los dos.</b>",
            "Tú no quedas afuera vigilando. <b class='w7'>Quedas adentro, del lado de tu hijo</b>, enseñándole a cruzar mientras todavía puedes caminar a su lado. Al terminar cada sesión, él revisa un resumen de lo que pensó y decide compartírtelo. Y a ti te llega algo mejor que «hoy estuvo en el celular»: <b class='w7'>un tema real para la cena</b>."], wide=True),
       "Lectura en la columna ancha (pedido del usuario, como 08.2 y 09.2). «Los incluye a los dos.» sigue corrido, en negrita (se probó aparte y se revirtió: se leía como subtítulo)."),
    st("10.3", "L04 (cita + remate)", "read", 1,
       "<div class='c ctr stack l04'>\n<p class='pf it w7 t-semi q bw'>«Oye, ¿a ti te ha tocado ver algo así en un grupo?»</p>\n"
       "<p class='in w5 t-body'>Quizá te cuenta. Quizá hoy no. Pero <b class='w7'>la puerta queda abierta</b>, y no es un interrogatorio.</p>\n</div>",
       "L04: la cita en voz citada a semimonumental (Playfair 700 itálica, como las citas-eco del cap. 02; pedido del usuario); el remate debajo en lectura, con aire amplio de 32/48 px (pedido del usuario). No se inventa fuente.", scan=True),
    st("10.4", "B03 (puente → golpe)", "two", 1.5,
       b03("Y aquí pasa algo que no te esperas. Cuando dejas de ser tú-contra-la-pantalla, <b class='w7'>se vuelven ustedes dos, del mismo lado</b>.", "<span class='hl'>El criterio</span> que lo cuida es el mismo <span class='hl'>puente que te lo regresa.</span>", size="semi"),
       "Puente → golpe (pedido del usuario, mismo layout que 05.8): el puente en voz lead; «El criterio que lo cuida es el mismo puente que te lo regresa.» cae después en semimonumental."),
])
pin("P-10b", "10 · (cont.)", "pin", [
    st("10.5", "B03", "two", 1.5,
       ("<div class='c ctr stack b03'>\n<p class='in w5 t-sub lead-l bw' data-beat='lead'>Un niño, en otra parte, dijo esto. Léelo despacio:</p>\n"
        "<p class='pf w8 it t-semi bw' data-beat='close'>«Mi mamá se ríe más cuando ve el celular que cuando está conmigo.»</p>\n</div>"),
       "Bisagra 4 (oscuro). Lapidario (confirmado). Semimonumental porque en monumental serían 6 líneas en móvil 360. Habla el niño: voz citada (itálica). En el build va en coral, «para que se sienta» (pedido del usuario, 2026-09-29; antes: sin acento).",
       night=True, scan=True),
    st("10.6", "L07", "read", 1,
       l07(["Esa pausa antes de decidir no es solo para él. Con lo que te comparte, y con SAFE, los cursos breves para mamás y papás que van incluidos, <b class='w7'>tú también vas entrenando el tuyo</b>: qué preguntar, cuándo escuchar, cómo acompañar sin interrogar. <b class='w7'>Él aprende a mirar a los dos lados. Tú aprendes a caminar a su lado.</b>"], wide=True),
       "Vuelve la luz. Lectura en la columna ancha (pedido del usuario, como 08.2, 09.2 y 10.2)."),
    st("10.7", "Sello", "seal", 1, seal("07-together-mother-daughter.webp", zoom=1),
       "Sella el capítulo más emocional: mamá e hija juntas, celulares boca abajo. Sin zoom, solo disolvencia de entrada (pedido del usuario). Alternativa: 07-together-father-son."),
])

# 11 · Inscríbelo hoy.
_i1 = lambda s: card("ADA, su mentor personal, todo el ciclo.", "Uno a uno, por mensajes, en su idioma. Un espacio para conversar, hacer preguntas y practicar decisiones con ayuda de la inteligencia artificial.", span=s)
_i2 = lambda s: card("Cada semana pasa algo.", "Una semana ADA le trae un tema nuevo, pensado para su etapa y para lo que usa a su edad. La siguiente, lo pone a prueba con una situación real. Veinte temas a lo largo del ciclo. Para él, misiones.", span=s)
_i3 = lambda s: card("Y entre semana, para lo que traiga.", "Le mandaron algo raro, un juego le pidió dinero, no sabe si algo es cierto: se lo cuenta y ADA le hace las preguntas para que él decida.", span=s)
_i4 = lambda s: card("Un resumen de su avance.", "Ves su avance sin vigilarlo.", span=s)
_i5 = lambda s: card("SAFE gratis todo el ciclo.", "Los cursos breves de Gnius Club para mamás y papás.", span=s)
_i6 = lambda s: card("Código de descuento en Alquimistas de I.A.", "El curso para aprender a usar inteligencia artificial en tu trabajo, para ti. Tu hijo entrena criterio; tú entrenas tu ventaja.", span=s)
_i7 = lambda s: card("Precio fundador congelado cuando lo reinscribas al siguiente nivel.", "Nunca te sube mientras sigas.", span=s)
HEAD11 = "Tu inscripción fundadora incluye:"
pin("P-11a", "11 · Inscríbelo hoy. Generación Fundadora.", "pin", [
    st("11.1", "L06", "read", 1,
       l06("Inscríbelo hoy. Generación Fundadora.",
           ["Hay algo que hace más sencillo empezar: no hay grupo que esperar, ni temporada, ni lista. <b class='w7'>Pagas hoy y ADA se presenta con tu hijo hoy mismo.</b> Su ciclo de 12 meses empieza <b class='w7'>el día que ustedes deciden</b>, no el día que a un calendario le conviene."]),
       "Destino del ancla #inscripcion. Sin golpe B: capítulo transaccional. Columna ancha (pedido del usuario; regla por largo, párrafo de 240 caracteres).", scan=True),
    st("11.2", "L06 (solo título)", "read", 1,
       "<div class='c l06'>\n<p class='pf w7 t-head bw'>Doce meses, no diez: el verano va incluido, porque las redes no salen de vacaciones.</p>\n</div>",
       "Copy de venta punchy: NO entra en B (decisión Fase 1). Va como título Playfair 700.", scan=True),
    st("11.3", "L08 (tarjetas)", "read", 1, l08(HEAD11, [_i1(3), _i2(3), _i3(3), _i4(3)]),
       "Tarjetas con título (pedido del usuario; mismo estilo que 08.5). El título de cada tarjeta es la primera frase de su viñeta, literal; el párrafo es el resto. Desktop: 4 tarjetas en una fila.", scan=True, bp="d"),
    st("11.3b", "L08 (tarjetas, cont.)", "read", 1, l08(None, [_i5(4), _i6(4), _i7(4)]),
       "Desktop: las otras 3 tarjetas en una fila.", bp="d"),
    st("11.3m", "L08 (mazo apilado)", "deck", 1.75, l08(HEAD11, [_i1(12), _i2(12), _i3(12), _i4(12)], deck=True),
       "Móvil y tablet: las 4 tarjetas en una parada. Tablet: una debajo de otra. Móvil < 600 px: mazo apilado, como 08.5m.", scan=True, bp="m"),
    st("11.3bm", "L08 (mazo apilado, cont.)", "deck", 1.5, l08(None, [_i5(12), _i6(12), _i7(12)], deck=True),
       "Móvil y tablet: las otras 3 tarjetas, mismo comportamiento.", bp="m"),
])
pin("P-11b", "11 · precio y garantía", "pin", [
    st("11.4", "L07 + título + bloque de precio", "read", 1.25,
       "<div class='c l07 wide'>\n<div class='essay'>\n<p class='in w5 t-body'>El programa va <b class='w7'>de tercero de primaria a tercero de prepa</b>. Tu hijo arranca en el primer nivel de su sección y cada año sube uno.</p>\n<h3 class='pf w8 t-head bw'>¿Cuánto cuesta y cómo se paga?</h3>\n<p class='in w5 t-body'>El ciclo completo de 12 meses cuesta $5,990. <b class='w7'>Es un solo precio.</b> No hay cuota de inscripción aparte ni cargos escondidos. Tú eliges cómo pagarlo:</p>\n"
       "<div class='price'>\n"
       "<div class='piece'><p class='in w8 t-head amt'>Todo hoy, de una vez: $4,990.</p>\n<p class='in w5 t-body'><mark class='val'>Te ahorras $1,000 por pagarlo completo.</mark> Es el precio fundador y vale hasta el 31 de octubre.</p><a class='btn' data-new='aprobado' data-plan='contado' data-role='azul · pago de contado (texto de la propuesta A)'>Pagar de contado<span class='arr' data-dir='ne' data-icon='↗' aria-hidden='true'></span></a></div>\n"
       "<div class='piece'><p class='in w8 t-head amt'>En 10 pagos mensuales de $599.</p>\n<p class='in w5 t-body'>Son los mismos $5,990, divididos en diez. Terminas de pagar en el mes diez; ADA sigue con tu hijo hasta el doce.</p><a class='btn' data-new='aprobado' data-plan='diferido' data-role='azul · pagos diferidos (texto de la propuesta A)'>Elegir pagos diferidos<span class='arr' data-dir='ne' data-icon='↗' aria-hidden='true'></span></a></div>\n"
       "</div>\n</div>\n</div>",
       "UNA lámina (pedido del usuario): lectura con subtítulo del copy en la columna ancha y, debajo, las dos piezas de precio al ancho de esa columna. Monto en su lugar (Inter 800), nunca duplicado. El marcador gris = ámbar de valor en el build.", scan=True, bp="d"),
    st("11.4m", "L07 + título", "read", 1,
       "<div class='c l07 wide'>\n<div class='essay'>\n<p class='in w5 t-body'>El programa va <b class='w7'>de tercero de primaria a tercero de prepa</b>. Tu hijo arranca en el primer nivel de su sección y cada año sube uno.</p>\n<h3 class='pf w8 t-head bw'>¿Cuánto cuesta y cómo se paga?</h3>\n<p class='in w5 t-body'>El ciclo completo de 12 meses cuesta $5,990. <b class='w7'>Es un solo precio.</b> No hay cuota de inscripción aparte ni cargos escondidos. Tú eliges cómo pagarlo:</p>\n</div>\n</div>",
       "Móvil y tablet: juntas no caben en el teléfono (~125 % a 360 px), así que la lectura y el precio van en paradas seguidas.", scan=True, bp="m"),
    st("11.5m", "Bloque de precio", "read", 1,
       "<div class='c price-wrap'>\n<div class='price'>\n"
       "<div class='piece'><p class='in w8 t-head amt'>Todo hoy, de una vez: $4,990.</p>\n<p class='in w5 t-body'><mark class='val'>Te ahorras $1,000 por pagarlo completo.</mark> Es el precio fundador y vale hasta el 31 de octubre.</p><a class='btn' data-new='aprobado' data-plan='contado' data-role='azul · pago de contado (texto de la propuesta A)'>Pagar de contado<span class='arr' data-dir='ne' data-icon='↗' aria-hidden='true'></span></a></div>\n"
       "<div class='piece'><p class='in w8 t-head amt'>En 10 pagos mensuales de $599.</p>\n<p class='in w5 t-body'>Son los mismos $5,990, divididos en diez. Terminas de pagar en el mes diez; ADA sigue con tu hijo hasta el doce.</p><a class='btn' data-new='aprobado' data-plan='diferido' data-role='azul · pagos diferidos (texto de la propuesta A)'>Elegir pagos diferidos<span class='arr' data-dir='ne' data-icon='↗' aria-hidden='true'></span></a></div>\n"
       "</div>\n</div>",
       "Móvil y tablet: las dos piezas apiladas.", scan=True, bp="m"),
    st("11.6", "Cierre de pago + garantía + par de CTA", "cta", 1,
       "<div class='c stack colbox'>\n<p class='in w5 t-body guar'>En los dos casos tu hijo empieza hoy y tiene el ciclo completo. <b class='w7'>No es una suscripción</b>: es el ciclo entero, pagado de una vez o en diez partes.</p>\n<p class='in w5 t-body guar'>Y una garantía que nadie más da: <b class='w7'>pruébalo un mes</b>. Los 30 días cuentan desde la primera conversación de tu hijo con ADA, no desde que pagas. Si no es para ustedes, <b class='w7'>cancelas en un clic y no pagas</b>. Sin llamadas de venta. Sin letras chicas.</p>\n"
       + CTA_INNER + "\n</div>",
       "Cierre del pago + garantía pegada al par de CTA, en la columna ancha; el par de botones mide lo mismo que la columna (pedido del usuario). Los dos botones pesan igual (en el build: azul / violeta). Feedback en pointerdown. Destinos pendientes.",
       scan=True),
])

# 12 · Una última cosa
pin("P-12a", "12 · Una última cosa, y ya te dejo.", "pin", [
    st("12.1", "B01 (secundario)", "golpe", 1.25,
       b01("Una última cosa, y ya te dejo.", size="semi"),
       "Título = golpe y puente a la vez (confirmado).", scan=True),
    st("12.2", "B03", "two", 1.5,
       b03("Al principio <b class='w7'>te dije un «no»</b> y <b class='w7'>te debí el «cómo»</b> un buen rato.", f"Ya lo {acc('tienes.')}", size="mxl"),
       "Lapidario del capítulo. Rima con «Eres tú.» (10.1): monumental-xl.", scan=True),
    st("12.3", "Puente (lead)", "lead", 1,
       lead("<b class='w7'>Ahora te toca dárselo a él.</b> Ésa es la lección completa. Lo demás son detalles."),
       "Puente («Ahora…»)."),
    st("12.4", "B01 (golpe dentro de párrafo)", "golpe", 1.25,
       "<div class='c left stack b01 b01-l'>\n<p class='pf w8 t-semi bw'>No inscribirlo también es una decisión. La diferencia es que <span class='hl'>ésa no tiene botón de cancelar.</span></p>\n"
       "<p class='in w5 t-body'>No te lo digo para asustarte; te la digo porque <b class='w7'>el día en que cruce solo va a llegar</b> de todos modos, y lo único que cambia es <b class='w7'>si llega sabiendo mirar</b>.</p>\n" + CTA_INNER + "\n</div>",
       "El golpe son las dos primeras frases del párrafo; la tercera sigue en lectura dentro del MISMO encuadre (el párrafo no se parte entre paradas). Debajo, el par de CTA al ancho de la columna (pedido del usuario; antes era la parada 12.5). Semimonumental: 6 líneas en móvil 360 (excepción a la regla de ≤5, anotada).",
       scan=True),
])
pin("P-12b", "12 · decisión y cierre", "pin", [
    st("12.6", "Sello", "seal", 1, seal("08-autonomy-father.webp"),
       "Pago visual de la metáfora: el hijo cruza solo, el papá observa sin celular. Alternativa: 08-autonomy-mother."),
    st("12.7", "B06", "golpe", 1.25,
       "<div class='c ctr stack b06'>\n<p class='pf w8 t-mon bw'>Presencia, no vigilancia.</p>\n<p class='pf w8 t-mon bw'><em class='acc'>Criterio, no candado.</em></p>\n</div>",
       "Bisagra 5 (oscuro). B06: dos líneas, la segunda en acento itálico. Resumen de marca.",
       night=True, scan=True),
])

# FAQ y footer — flujo normal (no pineado)
FAQ = [
    ("¿Para qué edades es Digizen?", "De tercero de primaria a tercero de preparatoria. Tu hijo arranca en el primer nivel de su sección (primaria, secundaria o prepa) y cada año sube uno. Los temas están pensados para su etapa y para lo que usa a su edad."),
    ("¿Qué hace mi hijo cada semana?", "Una semana ADA le trae un tema nuevo, pensado para su etapa (para él, una misión). La siguiente, lo pone a prueba con una situación real. Son veinte temas a lo largo del ciclo. Y entre semana, ADA está para lo que traiga: algo raro que le mandaron, un juego que le pidió dinero, una duda de si algo es cierto."),
    ("¿Voy a poder leer todo lo que habla mi hijo con ADA?", "Recibes su avance, los temas que ha visto y un resumen que él revisa antes de compartirlo contigo. No recibes una copia de toda la conversación. Antes de empezar se explican los avisos ante situaciones que puedan necesitar ayuda de un adulto."),
    ("¿Hay que pagar inscripción y además mensualidades?", "No. El ciclo completo cuesta $5,990 y es un solo precio, sin cuota de inscripción aparte. Lo pagas todo hoy ($4,990 con el precio fundador) o en diez pagos mensuales de $599. Nunca las dos cosas."),
    ("¿Los diez pagos son una suscripción?", "No. Son los mismos $5,990 divididos en diez. Terminan en el mes diez; ADA sigue con tu hijo hasta el doce."),
    ("¿Cómo funciona la garantía?", "Pruébalo un mes. Los 30 días cuentan desde la primera conversación de tu hijo con ADA, no desde que pagas. Si no es para ustedes, cancelas en un clic y no pagas. Sin llamadas de venta."),
    ("¿Puedo conocer a ADA antes de pagar?", "Sí, el recorrido contempla que tú converses con ADA primero. Usa el botón «Conversar con ADA primero» al final de la historia para ver la solicitud de acceso."),
]
faq_html = ("<div class='faq'>\n<h2 class='pf w7 t-head bw'>Por si te quedó una duda.</h2>\n"
            + "\n".join(f"<details><summary><span class='in w6 t-body'>{q}</span><span class='ind' aria-hidden='true'></span></summary><p class='in w5 t-body'>{a}</p></details>" for q, a in FAQ)
            + "\n</div>")
pin("FAQ", "FAQ", "flow", html=faq_html, comp="Acordeón",
    note="Flujo normal (no pineado). Todas cerradas por defecto: las 7 preguntas se escanean de un vistazo. Toda la fila es el botón; feedback inmediato; abre hacia abajo y cierra por el mismo camino; se puede interrumpir.")
footer_html = ("<div class='foot'>\n<img class='foot-logo' src='00-context/logo/digizen-logo-light.svg' alt='digizen' data-copy='1'>\n"
               "<p class='in w5 t-small'>Presencia, no vigilancia.</p>\n<p class='in w5 t-small'>Criterio, no candado.</p>\n"
               "<p class='in w5 t-small foot-links'><a class='lnk'>Gnius Club ↗</a> · <a class='lnk'>Aviso de privacidad</a> · © 2026 Gnius Club</p>\n</div>")
pin("FOOT", "Footer", "flow", html=footer_html, comp="Footer",
    note="Flujo normal. «digizen» = logo oficial (00-context/logo/digizen-logo-light.svg; la auditoría lo lee de su alt). En gris en el wireframe; a color en la versión avanzada. Enlaces del copy: gnius.club y aviso de privacidad.")
