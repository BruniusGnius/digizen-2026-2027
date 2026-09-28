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

def l06(title, paras, title_cls="pf w7 t-head", tag="h2"):
    ps = "\n".join(f"<p class='in w5 t-body'>{p}</p>" for p in paras)
    return f"<div class='c l06'>\n<{tag} class='{title_cls} bw'>{title}</{tag}>\n<div class='sup'>\n{ps}\n</div>\n</div>"

def l07(paras):
    ps = "\n".join(f"<p class='in w5 t-body'>{p}</p>" for p in paras)
    return f"<div class='c l07'>\n<div class='essay'>\n{ps}\n</div>\n</div>"

def seal(fn):
    return f"<figure class='c-seal'><img src='{S}{fn}' alt='' loading='lazy'><figcaption class='wf-file'>{fn}</figcaption></figure>"

def l05(quote, prose):
    return (f"<div class='c l05'>\n<h3 class='pf w7 t-semi bw w-q'>{quote}</h3>\n"
            f"<div class='def'>\n<p class='in w5 t-body'>{prose}</p>\n</div>\n</div>")

def entry(leadin, rest, span=4):
    return f"<div class='entry s{span}'>\n<p class='in w5 t-body'><b class='w7'>{leadin}</b> {rest}</p>\n</div>"

def l08(head, entries, head_tag="h3"):
    h = f"<div class='c l08'>\n"
    if head:
        h += f"<{head_tag} class='pf w7 t-head bw'>{head}</{head_tag}>\n"
    return h + "<div class='entries'>\n" + "\n".join(entries) + "\n</div>\n</div>"

CTA_INNER = ("<div class='cta'>\n"
             "<a class='btn' data-role='azul · inscripción'>Inscribir a mi hijo ↗</a>\n"
             "<a class='btn' data-role='violeta · ADA'>Conversar con ADA primero</a>\n</div>")
CTA = "<div class='c ctr stack cta-wrap'>\n" + CTA_INNER + "\n</div>"

def acc(w):
    return f"<em class='acc'>{w}</em>"

def st(id, comp, kind, E, html, note, night=False, scan=False, bp="all"):
    return dict(id=id, comp=comp, kind=kind, E=E, html=html, note=note, night=night, scan=scan, bp=bp)

# ---------- recorrido ----------
PINS = []
def pin(id, cap, type_, stops=None, **kw):
    d = dict(id=id, cap=cap, type=type_, stops=stops or []); d.update(kw); PINS.append(d)

# HERO — autoplay (única imagen antes del texto)
pin("P-H0", "Hero", "hero", [
    st("H.1", "Hero", "hero", 1.5,
       f"<img class='hero-img' src='{S}01-dinner.webp' alt=''><div class='scrim'></div>"
       "<div class='c ctr hero-text'>\n<h1 class='pf w7 t-head bw'>Te voy a decir cinco cosas que crees sobre tu hijo y el celular.</h1>\n</div>",
       "Secuencia autoplay (no scrub): zoom-out extremo de 01-dinner → pausa → velo → aparece la frase. Se repite si regresas a este punto (onEnterBack). Sin texto de 'scroll'.",
       scan=True),
])
pin("P-H", "Hero · apertura", "pin", [
    st("H.2", "B01", "golpe", 1.25,
       b01(f"Cuatro son {acc('falsas.')}", "Y sé cuál te va a doler."),
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
    st("01.3", "B03", "two", 1.5,
       b03("Ahora te digo cuál es la verdad.", f"La cinco. No te {acc('escucha.')}"),
       "Bisagra 1 (oscuro). Dos tiempos: puente → golpe lapidario por corte.",
       night=True, scan=True),
    st("01.4", "B01 (secundario)", "golpe", 1.25,
       b01("Pero no por lo que crees. Y ahí es donde se pone interesante.", size="semi"),
       "Sigue en oscuro. Golpe secundario (semimonumental, 4 líneas en móvil 360). Al salir vuelve la luz.",
       night=True),
    st("02.1", "L06 (solo título)", "read", 1,
       "<div class='c l06 ctr'>\n<h2 class='pf w7 t-head bw'>Las cuatro falsas, una por una</h2>\n</div>",
       "Título A. Parada corta que abre el carrusel.", scan=True),
])

# 02 · Las cuatro falsas, una por una
pin("P-02b", "02 · Las cuatro falsas (horizontal)", "h", [
    st("02.2", "L05 (cita-eco + prosa)", "panel", 1,
       l05("«El problema es el tiempo.»",
           "Eso ya lo intentaste medir. Negociaste «una hora y ya». Y cuando por fin cumplía la hora, ¿se sentía resuelto? Una mamá nos lo dijo así, y no se nos ha borrado: «Ni siquiera me mira a los ojos.» Eso no se mide en minutos."),
       "Patrón 3+5: pin + desplazamiento horizontal (ease none), snap por panel. Panel 1/4. La cita-eco es micro-golpe de apertura del bloque.",
       scan=True),
    st("02.3", "L05", "panel", 1,
       l05("«Si configuro bien la app de control…»",
           "Un papá escribió esto en una reseña de Family Link: «falsa sensación de control». No lo escribió un experto. Lo escribió alguien que ya lo configuró bien."),
       "Panel 2/4. Entra desde la derecha; si regresas, sale por la derecha.", scan=True),
    st("02.4", "L05", "panel", 1,
       l05("«Si le pongo contraseña, se acaba el problema.»",
           "La frase que más hemos escuchado, de papás distintos, en ciudades distintas: «en dos días encontró cómo saltárselo». Tu hijo tiene todo el día para resolver un acertijo que tú revisas dos minutos en la noche. No es mala suerte. Es aritmética."),
       "Panel 3/4.", scan=True),
    st("02.5", "L05", "panel", 1,
       l05("«Ya perdí.»",
           "Ésta es la más cómoda de las cuatro, porque si ya perdiste, no tienes que hacer nada. Aguanta. Ahorita llegamos ahí."),
       "Panel 4/4. «Aguanta. Ahorita llegamos ahí.» es el puente de cierre, pero vive dentro del párrafo: no se separa.", scan=True),
])
# 03 · Ahora, un favor.
pin("P-03a", "02 sello · 03 · Ahora, un favor.", "pin", [
    st("02.6", "Sello", "seal", 1, seal("02-facial-recognition.webp"),
       "Sella el capítulo completo. La referencia usa «candados»; aquí la pantalla del celular muestra candado y reloj de arena (tiempo + contraseña). Alternativa: 02-facial-recognition-alt."),
    st("03.1", "L06", "read", 1,
       l06("Ahora, un favor.", ["Acuérdate de lo que acabas de leer sobre el candado."]),
       "Título-puente («Ahora…») + primera línea.", scan=True),
    st("03.2", "L06 (título en voz de puente)", "read", 1,
       "<div class='c l06'>\n<p class='pf w6 t-head bw lead-l'>¿Qué sentiste?</p>\n<div class='sup essay'>\n"
       "<p class='in w5 t-body'>No fue enojo. Apuesto a que fue otra cosa: esa angustia de «ya lo sé… ¿y entonces qué hago?». Ver a tu hijo ahí, con el celular, y no saber qué más hacer.</p>\n"
       "<p class='in w5 t-body'>Quédate con eso un segundo. Porque te acabo de hacer exactamente lo que tú le haces a él.</p>\n</div>\n</div>",
       "La pregunta va en la línea lead de B05 (Playfair 600, heading). Dos párrafos de lectura debajo."),
    st("03.3", "B03 (cierre secundario)", "two", 1.5,
       b03("Ahora acuérdate de la cara de tu hijo la quinta vez que le dijiste «ya deja el cel».",
           "Los ojos al techo. En señal de fastidio.", size="semi"),
       "Puente → golpe secundario (semimonumental). La escena lo sella en la siguiente parada.", scan=True),
    st("03.4", "Sello", "seal", 1, seal("03-eyes.webp"),
       "Sella el beat de «los ojos al techo» (primera de las dos imágenes del capítulo). Alternativa: 03-eyes-wide."),
])
pin("P-03b", "03 · Ahora, un favor. (cont.)", "pin", [
    st("03.5", "B03", "two", 1.5,
       b03("No siente lo mismo que tú. Tú sientes angustia. Él ya está harto de oírlo. Pero los dos están parados en el mismo lugar:",
           f"Alguien les dijo «no», y nadie les dijo «{acc('cómo')}»."),
       "Bisagra 2 (oscuro). Lapidario del capítulo (confirmado). El lead termina en dos puntos: anuncia el corte.",
       night=True, scan=True),
    st("03.6", "L07", "read", 1,
       l07(["Yo te dije «el candado no sirve» y no te di nada a cambio. Tú le dices «deja el cel» y tampoco. Y con un «no» no se construye nada. Ni criterio, ni conversación. Solo un hijo que busca el «cómo» por su cuenta. Y lo encuentra: en dos días. Solo que fue el cómo saltárselo."]),
       "Vuelve la luz. Lectura."),
    st("03.7", "L07", "read", 1,
       l07(["Por eso «no me escucha» era la única verdadera. Pero la razón no es que sea rebelde. Es que un «no» sin «cómo» no le deja nada que hacer. Y a un «no» sin «cómo» nadie responde con criterio. Se responde con un candado abierto en dos días."]),
       "Lectura. Va aparte de 03.6: juntos pasan de ~100 palabras."),
    st("03.8", "Sello", "seal", 1, seal("04-shield.webp"),
       "Sella el capítulo: mamá e hija, cada una con su escudo, separadas."),
])

# 04 · respiro
pin("P-04", "04 · No eres mala mamá ni mal papá", "pin", [
    st("04.1", "L06", "read", 1,
       l06("Antes de seguir: no eres mala mamá ni mal papá.",
           ["Lo digo en serio, y lo digo como papá que también trae el celular en la mano todo el día."]),
       "Capítulo de respiro: solo composiciones L, sin acento, sin oscuro, sin imagen.", scan=True),
    st("04.2", "L07", "read", 1,
       l07(["A ti te tocó un mundo de calles y bicicletas. A tu hijo le tocó uno que se inventa cada mañana, que nadie te enseñó a leer, y que cambió las reglas mientras tú trabajabas para darle de comer. Nadie te dio el manual. Tus papás no estaban preparados. Tampoco el papá de junto.",
            "Todo lo que has hecho, quitar, vigilar, negociar, lo hiciste por amor. Por eso duele que no funcione."]),
       "Lectura."),
    st("04.3", "L07", "read", 1,
       l07(["Tu instinto no está roto. Te ayudó a resolver otros problemas. Éste necesita algo distinto.",
            "Suéltate la culpa. Necesitas espacio para lo que sigue."]),
       "Lectura. VISION §4 proponía un golpe aquí; se respeta §1.1/§5 (sin golpe) — ver decisión en 02-wireframe.md."),
])

# 05 · el cómo
pin("P-05a", "05 · Ahora sí: el «cómo»", "pin", [
    st("05.1", "L06", "read", 1,
       l06("Ahora sí: el «cómo». Y ya lo sabes hacer.", ["Te pongo un ejemplo."]),
       "Título-puente («Ahora sí:»).", scan=True),
    st("05.2", "L07", "read", 1,
       l07(["Piensa en algo que parece no tener nada que ver con el celular: cruzar la calle.",
            "Al principio le das la mano. Te detienes con él. Miras a los dos lados. Le explicas por qué ese coche, aunque esté lejos, importa. No lo haces para llevarlo de la mano hasta los cuarenta. Lo haces para que un día cruce sin ti."]),
       "Lectura: la metáfora de cruzar la calle."),
    st("05.3", "L06 (título en voz de puente)", "read", 1,
       "<div class='c l06'>\n<p class='in w5 t-sub bw lead-l'>Ahora imagina que la única lección hubiera sido: «No cruces.»</p>\n<div class='sup essay'>\n"
       "<p class='in w5 t-body'>Funciona mientras estás en la esquina. Y el día que tiene que cruzar solo, se para en la banqueta sin saber mirar. Nadie le enseñó. Solo le dijeron que no.</p>\n</div>\n</div>",
       "Puente (línea lead de B03) + lectura."),
    st("05.4", "B01 (secundario)", "golpe", 1.25,
       b01("Bloquearle el celular es «no cruces».", size="semi"),
       "Golpe intermedio, secundario (semimonumental).", scan=True),
    st("05.5", "Sello", "seal", 1, seal("05-crossing.webp"),
       "Sella la metáfora a mitad del capítulo. El lapidario viene después, sin imagen propia. Alternativa: 05-crossing-alt."),
])
pin("P-05b", "05 · el «cómo» (cont.)", "pin", [
    st("05.6", "Puente (lead)", "lead", 1,
       lead("Y el día en que cruce solo va a llegar. A los 13, a los 17, a los 25, en un mundo que ni tú ni yo podemos imaginar todavía."),
       "Puente solo que prepara la tesis."),
    st("05.7", "B03", "two", 1.5,
       b03("El control caduca.", f"El criterio {acc('no.')}"),
       "Bisagra 3 (oscuro). Tesis de la pieza. B03 del espécimen: lead «El control caduca.» → cierre «El criterio no.» (misma línea del copy, en dos tiempos).",
       night=True, scan=True),
    st("05.8", "L07", "read", 1,
       l07(["Ese día, lo único que va a cruzar la calle con él es lo que le hayas enseñado antes."]),
       "Vuelve la luz. Una sola frase de lectura cierra el capítulo."),
])

# 06 · respiro
pin("P-06", "06 · ¿Y cómo se enseña a mirar a los dos lados?", "pin", [
    st("06.1", "L06", "read", 1,
       l06("¿Y cómo se enseña a mirar a los dos lados?",
           ["Aquí viene la parte que casi nadie quiere oír, porque es más lenta que un candado."]),
       "Respiro: solo L.", scan=True),
    st("06.2", "L07", "read", 1,
       l07(["Acuérdate del «no» sin «cómo». Ya viste lo difícil que es escuchar cuando uno está a la defensiva. Entonces, ¿cómo entra?",
            "Piensa en la última vez que tú cambiaste de opinión sobre algo importante. Apuesto a que no fue porque alguien te gritó. Fue porque alguien te hizo una pregunta que te quedaste pensando en el coche, de regreso a la casa."]),
       "Lectura."),
    st("06.3", "L07", "read", 1,
       l07(["El criterio se construye con preguntas. No con «deja el cel». Con «¿quién hizo este video y qué quiere de ti?». Con «¿esto te sirve, o te está usando?». Con «¿qué crees que siente la persona de esa foto?»."]),
       "Lectura. VISION §4 proponía golpe con la primera frase; está dentro del párrafo y el capítulo es de respiro — ver decisión."),
    st("06.4", "L07", "read", 1,
       l07(["Esas preguntas no salen en un sermón de domingo que él ya dejó de oír. Salen en una conversación. En su idioma. En el momento en que está pasando.",
            "Y ahí está el problema práctico: tú no puedes estar ahí en cada momento. Ni yo. Nadie."]),
       "Lectura."),
    st("06.5", "Puente (lead)", "lead", 1,
       lead("Pero sí hay alguien que puede estar ahí cada vez que él practique. Todas las veces que haga falta."),
       "Puente de cierre hacia ADA."),
])

# 07 · Esto se llama ADA.
pin("P-07a", "07 · Esto se llama ADA. + conversación", "pin", [
    st("07.1", "L06", "read", 1,
       l06("Esto se llama ADA.",
           ["Tu hijo entra a la página de Digizen y ahí conversa con ADA: un mentor de inteligencia artificial que le habla en su idioma, uno a uno. Y conversa como conversa con sus amigos: por mensajes, a su ritmo. Sin un adulto mirando por encima del hombro. Sin nadie que lo juzgue por lo que pregunta."]),
       "Título A + primer párrafo.", scan=True),
    st("07.2", "L07", "read", 1,
       l07(["No es un salón de clases. No es un robot que suelta tareas. No es un Kumon digital. Y no es un vigilante metido en su celular leyendo sus chats. Eso rompería su confianza, y la tuya."]),
       "Lectura."),
    st("07.3", "L07", "read", 1,
       l07(["Es un lugar al que va a entrenar el criterio. ADA lo lleva, conversando, a ver cómo funciona lo digital por dentro: cómo un video está hecho para convencerlo, por qué le cuesta dejar de ver videos, qué siente antes y después de pasar un rato en redes. Y en vez de decirle qué hacer, le hace la pregunta. La que se queda pensando de regreso a casa."]),
       "Lectura."),
    st("07.4", "Diálogo", "dialog", 4,
       "<div class='c dlg'>\n<p class='pf w7 t-sub'>Una pregunta que abre otra puerta</p>\n<p class='in w5 t-micro dlg-k'>— Conversación de ejemplo</p>\n"
       "<div class='msg ada'><span class='who in w6 t-micro'>ADA</span><p class='in w5 t-body'>Antes de decidir si la compartes: ¿qué crees que siente la persona de la foto?</p></div>\n"
       "<div class='msg hijo'><span class='who in w6 t-micro'>HIJO</span><p class='in w5 t-body'>Pues pena. Pero yo no la tomé.</p></div>\n"
       "<div class='msg ada'><span class='who in w6 t-micro'>ADA</span><p class='in w5 t-body'>Es cierto. ¿Y qué cambia para él si tú la mandas a otro grupo?</p></div>\n"
       "<div class='msg hijo'><span class='who in w6 t-micro'>HIJO</span><p class='in w5 t-body'>Que la ve más gente. Yo también lo estaría haciendo más grande.</p></div>\n</div>",
       "Un mensaje por paso de scroll (4 snaps). ADA entra por la izquierda, HIJO por la derecha; al regresar salen por el mismo lado. Burbujas: tinte violeta (ADA) / cian (HIJO) en el build.",
       scan=True),
])
pin("P-07c", "07 · cierre", "pin", [
    st("07.5", "B01", "golpe", 1.25,
       b01(f"Una pausa. Una consecuencia. Una idea {acc('propia.')}"),
       "Lapidario del capítulo: staccato de tres tiempos (candidato a SplitText por frase, patrón 9).", scan=True),
    st("07.6", "L07", "read", 1,
       l07(["Lo que construye ahí adentro se lo lleva puesto a sus juegos, a sus chats, a su vida. Y empieza a cruzar de «lo que veo en redes me dice quién soy» a «yo decido qué me sirve y qué quiero compartir»."]),
       "Lectura."),
    st("07.7", "L07", "read", 1,
       l07(["Te lo digo derecho: ADA está viva y está creciendo. Tu hijo empieza con ella el día que lo inscribas, y las familias que entran ahora la moldean: lo que tu familia necesite se construye primero. No te pido que confíes en una promesa bonita. Más abajo te explico cómo hablar tú con ADA antes de pagar un peso."]),
       "Lectura. Sin pausa de cierre: fluye directo al cap. 08 (como en la referencia)."),
])

# 08 · «Espera...»
pin("P-08a", "08 · «Espera. ¿Una IA hablando con mi hijo?»", "pin", [
    st("08.1", "B01 (secundario)", "golpe", 1.25,
       b01("«Espera. ¿Una IA hablando con mi hijo?»", size="semi"),
       "Título = golpe (confirmado). Secundario: semimonumental.", scan=True),
    st("08.2", "L07", "read", 1,
       l07(["Sí. Y si has leído las noticias sobre inteligencia artificial y algo en ti se cerró, tienes razón en desconfiar. Nosotros también las leemos. Y también nos preocupan. Por eso ADA existe.",
            "Hay aplicaciones que simulan amistades o relaciones románticas. Common Sense Media advirtió en 2025 que los compañeros de inteligencia artificial presentaban riesgos inaceptables para menores. ADA tiene un propósito educativo: ayudarle a pensar y a tomar sus propias decisiones. No está planteada como pareja, terapeuta ni sustituto de las personas que lo acompañan."]),
       "Lectura (~88 palabras: al límite de un encuadre móvil)."),
    st("08.3", "B09", "golpe", 1.25,
       "<div class='c ctr stack b09'>\n<p class='in w5 t-small'>Pero hay un dato que quiero que te lleves en la cabeza:</p>\n"
       "<p class='pf w8 t-mxl' data-beat='close'>7 de cada 10</p>\n"
       "<p class='in w5 t-small it'>adolescentes ya conversan con inteligencias artificiales. Solos, sin reglas, en plataformas hechas para adultos. México es tercer lugar mundial en adopción juvenil de IA.</p>\n</div>",
       "Dato = Registro B (confirmado). B09: el numeral en su lugar dentro de la frase, sin duplicarlo ni reordenar. Lapidario del capítulo. Candidato a patrón 10 (contador).",
       scan=True),
    st("08.4", "Puente (lead)", "lead", 1,
       lead("No es que vaya a pasar. Ya está pasando. Lo único que queda por decidir es cuál: una IA hecha para adultos, o una hecha para tu hijo, con reglas y con tu participación."),
       "El puente («No es que vaya a pasar. Ya está pasando.») abre un párrafo que no se parte: todo el párrafo va en voz lead."),
])
_b1 = entry("Cero rol romántico.", "Cero secretos peligrosos. Sus reglas están escritas y las vas a poder leer antes de empezar: qué hace ADA y qué no. <a class='lnk' data-role='violeta · destino pendiente'>Conocer las reglas de ADA ↗</a>")
_b2 = entry("Tú también participas.", "Recibes su avance, qué está construyendo, qué está aprendiendo a decidir, sin espiar sus conversaciones. Un hijo espiado deja de hablar. Y si algo de lo que dice indica que necesita ayuda de un adulto, te avisamos. ADA puede equivocarse: no diagnostica ni garantiza detectarlo todo. Antes de empezar vas a saber exactamente en qué casos te llega ese aviso.")
_b3 = entry("Con un tiempo definido para cada conversación.", "ADA no quiere sus horas. Quiere su criterio.")
pin("P-08b", "08 · reglas", "pin", [
    st("08.5", "L08", "read", 1, l08("ADA es lo segundo, por diseño:", [_b1, _b2, _b3]),
       "Desktop: una parada, tres columnas. Viñetas completas; la primera frase en 700 como etiqueta.", scan=True, bp="d"),
    st("08.5a", "L08", "read", 1, l08("ADA es lo segundo, por diseño:", [_b1]),
       "Móvil: la lista se reparte en dos paradas (juntas pasan de la capacidad del encuadre). Ninguna viñeta se corta.", scan=True, bp="m"),
    st("08.5b", "L08 (cont.)", "read", 1, l08(None, [_b2, _b3]),
       "Móvil, segunda parada de la lista.", bp="m"),
    st("08.6", "Sello", "seal", 1, seal("06-rules.webp"),
       "Sella la tranquilización: papá revisando las reglas. Alternativa: 06-rules-alt."),
])

# 09 · respiro / instruccional
pin("P-09", "09 · Y la prueba no te la pido por fe.", "pin", [
    st("09.1", "L06", "read", 1,
       l06("Y la prueba no te la pido por fe.", ["Habla tú con ADA primero."]),
       "Respiro instruccional: solo L.", scan=True),
    st("09.2", "L07", "read", 1,
       l07(["Pide tu acceso al final de esta página para conversar tú con ADA antes de inscribir a tu hijo. Interrógala. Trata de sacarla de sus reglas. Pregúntale lo que un niño le preguntaría. Pregúntale qué no va a hacer nunca con tu hijo. Te va a contestar sin rodeos.",
            "Queremos que conozcas a la inteligencia artificial con la que hablará tu hijo antes de pagar. Por eso la ponemos por delante."]),
       "Lectura."),
    st("09.3", "Enlace + puente", "read", 1,
       "<div class='c ctr stack'>\n<p class='in w5 t-body'><a class='lnk' data-goto='11.1' data-role='azul · ancla #inscripcion'>Si ya viste suficiente, la inscripción está al final de esta página ↓</a></p>\n"
       "<p class='in w5 t-sub bw lead-l'>Si no, sigue leyendo; falta lo más importante.</p>\n</div>",
       "PRIMER CTA del recorrido: el salto a la inscripción que ya trae el copy. Toque → feedback inmediato; el scroll animado se interrumpe si el usuario hace scroll. El puente empalma con el título del cap. 10.",
       scan=True),
])

# 10 · Lo más importante no es ADA.
pin("P-10a", "10 · Lo más importante no es ADA.", "pin", [
    st("10.1", "B03", "two", 1.5,
       b03("Lo más importante no es ADA.", "Eres tú.", lead_tag="h2"),
       "Título + primera línea = un solo golpe (confirmado). Dos tiempos. Secundario (el lapidario del capítulo es la cita del niño): cierre en monumental.",
       scan=True),
    st("10.2", "L07", "read", 1,
       l07(["Esto no es una app que le instalas en el teléfono y te olvidas. Los incluye a los dos.",
            "Tú no quedas afuera vigilando. Quedas adentro, del lado de tu hijo, enseñándole a cruzar mientras todavía puedes caminar a su lado. Al terminar cada sesión, él revisa un resumen de lo que pensó y decide compartírtelo. Y a ti te llega algo mejor que «hoy estuvo en el celular»: un tema real para la cena."]),
       "Lectura."),
    st("10.3", "L04 (cita + remate)", "read", 1,
       "<div class='c ctr stack l04'>\n<p class='pf it w4 t-sub q bw'>«Oye, ¿a ti te ha tocado ver algo así en un grupo?»</p>\n"
       "<p class='in w5 t-body'>Quizá te cuenta. Quizá hoy no. Pero la puerta queda abierta, y no es un interrogatorio.</p>\n</div>",
       "L04: la cita en Playfair itálica; el remate debajo en lectura (no se inventa fuente).", scan=True),
    st("10.4", "Puente (lead)", "lead", 1,
       lead("Y aquí pasa algo que no te esperas. Cuando dejas de ser tú-contra-la-pantalla, se vuelven ustedes dos, del mismo lado. El criterio que lo cuida es el mismo puente que te lo regresa."),
       "Párrafo completo en voz lead: arranca con el puente «Y aquí pasa algo que no te esperas.»"),
])
pin("P-10b", "10 · (cont.)", "pin", [
    st("10.5", "B03", "two", 1.5,
       b03("Un niño, en otra parte, dijo esto. Léelo despacio:",
           "«Mi mamá se ríe más cuando ve el celular que cuando está conmigo.»", size="semi"),
       "Bisagra 4 (oscuro). Lapidario (confirmado). Semimonumental porque en monumental serían 6 líneas en móvil 360. Sin acento: la cita ya pesa sola.",
       night=True, scan=True),
    st("10.6", "L07", "read", 1,
       l07(["Esa pausa antes de decidir no es solo para él. Con lo que te comparte, y con SAFE, los cursos breves para mamás y papás que van incluidos, tú también vas entrenando el tuyo: qué preguntar, cuándo escuchar, cómo acompañar sin interrogar. Él aprende a mirar a los dos lados. Tú aprendes a caminar a su lado."]),
       "Vuelve la luz. Lectura."),
    st("10.7", "Sello", "seal", 1, seal("07-together-mother-daughter.webp"),
       "Sella el capítulo más emocional: mamá e hija juntas, celulares boca abajo. Alternativa: 07-together-father-son."),
])

# 11 · Inscríbelo hoy.
_i1 = lambda s: entry("ADA, su mentor personal, todo el ciclo.", "Uno a uno, por mensajes, en su idioma. Un espacio para conversar, hacer preguntas y practicar decisiones con ayuda de la inteligencia artificial.", s)
_i2 = lambda s: entry("Cada semana pasa algo.", "Una semana ADA le trae un tema nuevo, pensado para su etapa y para lo que usa a su edad. La siguiente, lo pone a prueba con una situación real. Veinte temas a lo largo del ciclo. Para él, misiones.", s)
_i3 = lambda s: entry("Y entre semana, para lo que traiga.", "Le mandaron algo raro, un juego le pidió dinero, no sabe si algo es cierto: se lo cuenta y ADA le hace las preguntas para que él decida.", s)
_i4 = lambda s: entry("Un resumen de su avance.", "Ves su avance sin vigilarlo.", s)
_i5 = lambda s: entry("SAFE gratis todo el ciclo.", "Los cursos breves de Gnius Club para mamás y papás.", s)
_i6 = lambda s: entry("Código de descuento en Alquimistas de I.A.", "El curso para aprender a usar inteligencia artificial en tu trabajo, para ti. Tu hijo entrena criterio; tú entrenas tu ventaja.", s)
_i7 = lambda s: entry("Precio fundador congelado cuando lo reinscribas al siguiente nivel.", "Nunca te sube mientras sigas.", s)
HEAD11 = "Tu inscripción fundadora incluye:"
pin("P-11a", "11 · Inscríbelo hoy. Generación Fundadora.", "pin", [
    st("11.1", "L06", "read", 1,
       l06("Inscríbelo hoy. Generación Fundadora.",
           ["Hay algo que hace más sencillo empezar: no hay grupo que esperar, ni temporada, ni lista. Pagas hoy y ADA se presenta con tu hijo hoy mismo. Su ciclo de 12 meses empieza el día que ustedes deciden, no el día que a un calendario le conviene."]),
       "Destino del ancla #inscripcion. Sin golpe B: capítulo transaccional.", scan=True),
    st("11.2", "L06 (solo título)", "read", 1,
       "<div class='c l06 ctr'>\n<p class='pf w7 t-head bw'>Doce meses, no diez: el verano va incluido, porque las redes no salen de vacaciones.</p>\n</div>",
       "Copy de venta punchy: NO entra en B (decisión Fase 1). Va como título Playfair 700.", scan=True),
    st("11.3", "L08", "read", 1, l08(HEAD11, [_i1(3), _i2(3), _i3(3), _i4(3)]),
       "Desktop: la lista de 7 se reparte en dos paradas (4 + 3). Viñetas completas.", scan=True, bp="d"),
    st("11.3b", "L08 (cont.)", "read", 1, l08(None, [_i5(4), _i6(4), _i7(4)]),
       "Desktop, segunda parada de la lista.", bp="d"),
    st("11.3m1", "L08", "read", 1, l08(HEAD11, [_i1(12), _i2(12)]),
       "Móvil: la lista de 7 se reparte en tres paradas.", scan=True, bp="m"),
    st("11.3m2", "L08 (cont.)", "read", 1, l08(None, [_i3(12), _i4(12), _i5(12)]),
       "Móvil, 2/3.", bp="m"),
    st("11.3m3", "L08 (cont.)", "read", 1, l08(None, [_i6(12), _i7(12)]),
       "Móvil, 3/3.", bp="m"),
])
pin("P-11b", "11 · precio y garantía", "pin", [
    st("11.4", "L07 + título", "read", 1,
       "<div class='c l07'>\n<div class='essay'>\n<p class='in w5 t-body'>El programa va de tercero de primaria a tercero de prepa. Tu hijo arranca en el primer nivel de su sección y cada año sube uno.</p>\n"
       "<h3 class='pf w7 t-head bw'>¿Cuánto cuesta y cómo se paga?</h3>\n"
       "<p class='in w5 t-body'>El ciclo completo de 12 meses cuesta $5,990. Es un solo precio. No hay cuota de inscripción aparte ni cargos escondidos. Tú eliges cómo pagarlo:</p>\n</div>\n</div>",
       "Lectura con subtítulo del copy.", scan=True),
    st("11.5", "Bloque de precio", "read", 1,
       "<div class='c price-wrap'>\n<div class='price'>\n"
       "<div class='piece'><p class='in w8 t-head amt'>Todo hoy, de una vez: $4,990.</p>\n<p class='in w5 t-body'><mark class='val'>Te ahorras $1,000 por pagarlo completo.</mark> Es el precio fundador y vale hasta el 31 de octubre.</p></div>\n"
       "<div class='piece'><p class='in w8 t-head amt'>En 10 pagos mensuales de $599.</p>\n<p class='in w5 t-body'>Son los mismos $5,990, divididos en diez. Terminas de pagar en el mes diez; ADA sigue con tu hijo hasta el doce.</p></div>\n"
       "</div>\n</div>",
       "Dos piezas iguales (el párrafo que sigue pasa a 11.6 para no llenar el encuadre). Monto en su lugar (Inter 800), nunca duplicado. El marcador gris = ámbar de valor en el build.", scan=True),
    st("11.6", "Cierre de pago + garantía + par de CTA", "cta", 1,
       "<div class='c ctr stack'>\n<p class='in w5 t-body guar'>En los dos casos tu hijo empieza hoy y tiene el ciclo completo. No es una suscripción: es el ciclo entero, pagado de una vez o en diez partes.</p>\n<p class='in w5 t-body guar'>Y una garantía que nadie más da: pruébalo un mes. Los 30 días cuentan desde la primera conversación de tu hijo con ADA, no desde que pagas. Si no es para ustedes, cancelas en un clic y no pagas. Sin llamadas de venta. Sin letras chicas.</p>\n"
       + CTA_INNER + "\n</div>",
       "Cierre del pago + garantía pegada al par de CTA. Los dos botones pesan igual (en el build: azul / violeta). Feedback en pointerdown. Destinos pendientes.",
       scan=True),
])

# 12 · Una última cosa
pin("P-12a", "12 · Una última cosa, y ya te dejo.", "pin", [
    st("12.1", "B01 (secundario)", "golpe", 1.25,
       b01("Una última cosa, y ya te dejo.", size="semi"),
       "Título = golpe y puente a la vez (confirmado).", scan=True),
    st("12.2", "B03", "two", 1.5,
       b03("Al principio te dije un «no» y te debí el «cómo» un buen rato.", f"Ya lo {acc('tienes.')}"),
       "Lapidario del capítulo, en paralelo con «Eres tú.» (cap. 10).", scan=True),
    st("12.3", "Puente (lead)", "lead", 1,
       lead("Ahora te toca dárselo a él. Ésa es la lección completa. Lo demás son detalles."),
       "Puente («Ahora…»)."),
    st("12.4", "B01 (secundario, a la izquierda)", "golpe", 1.25,
       "<div class='c left stack b01 b01-l'>\n<p class='pf w8 t-semi bw'>No inscribirlo también es una decisión. La diferencia es que ésa no tiene botón de cancelar.</p>\n"
       "<p class='in w5 t-body'>No te lo digo para asustarte; te la digo porque el día en que cruce solo va a llegar de todos modos, y lo único que cambia es si llega sabiendo mirar.</p>\n</div>",
       "El golpe son las dos primeras frases del párrafo; la tercera sigue en lectura dentro del MISMO encuadre (el párrafo no se parte entre paradas). Semimonumental: 6 líneas en móvil 360 (excepción a la regla de ≤5, anotada).",
       scan=True),
])
pin("P-12b", "12 · decisión y cierre", "pin", [
    st("12.5", "Par de CTA", "cta", 1, CTA,
       "Parada de decisión: solo los dos botones, mismo peso.", scan=True),
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
footer_html = ("<div class='foot'>\n<p class='pf w8 t-head logo-ph'>digizen</p>\n"
               "<p class='in w5 t-small'>Presencia, no vigilancia.</p>\n<p class='in w5 t-small'>Criterio, no candado.</p>\n"
               "<p class='in w5 t-small foot-links'><a class='lnk'>Gnius Club ↗</a> · <a class='lnk'>Aviso de privacidad</a> · © 2026 Gnius Club</p>\n</div>")
pin("FOOT", "Footer", "flow", html=footer_html, comp="Footer",
    note="Flujo normal. «digizen» = logo (00-context/logo/digizen-logo-light.svg). Enlaces del copy: gnius.club y aviso de privacidad.")
