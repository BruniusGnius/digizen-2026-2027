# Visión narrativa — Digizen Landing B-v3

Este documento es dirección creativa del usuario, insumo directo para la Fase 1 (sistema de
diseño) del proceso `Skills/landing-builder/SKILL.md`. No es plantilla de código ni de
wireframe todavía — es la lógica que debe informar esas fases.

El mapeo capítulo por capítulo de la sección 4 es un **borrador de trabajo**, hecho por
Claude leyendo el copy fuente (`00-context/COPY-PUBLICADO.md`), no una decisión cerrada.
Está ahí para que el usuario lo corrija, no para que la sesión que construya la landing lo
dé por bueno sin revisarlo con él.

## 0. Glosario rápido

Términos que se usan todo el tiempo en este documento, explicados en corto:

- **Registro A / Registro B** — dos "modos" de tipografía, como dos voces distintas del
  mismo narrador. Registro A = habla normal, cálida, explicando. Registro B = se detiene y
  suelta una frase seca, a manera de sentencia. No son tamaños de letra, son *tonos*.
- **Golpe** — el momento donde aparece el Registro B. Una frase corta y contundente que
  detiene al lector.
- **Puente (semibrutalista)** — una frase de transición, a medio camino entre A y B. Avisa
  "viene un golpe" sin ser el golpe todavía. Ejemplo: *"Ahora te digo cuál es la verdad."*
- **Frase lapidaria** — el golpe más fuerte, el que cierra una idea de forma definitiva,
  como si estuviera grabado en piedra. Ejemplo: *"El control caduca. El criterio no."*
- **Aforismo** — una frase corta que suena a verdad/regla general, no a explicación.
  ("El criterio se construye con preguntas" es un aforismo; explicar por qué, no lo es.)
- **Pin** — el scroll se "congela": la sección se queda fija en pantalla mientras el
  usuario sigue moviendo el mouse/dedo, y lo que cambia es el contenido adentro, no la
  posición de la página.
- **Scrub** — la animación avanza y retrocede exactamente al ritmo del scroll (como una
  barra de video que arrastras con el dedo). Si subes, se revierte. No es "reproducir una
  animación una vez", es "la animación ES la posición del scroll".
- **Pin + Scrub juntos** — lo más común en esta landing: la sección se congela (pin) y,
  mientras sigue congelada, el contenido va cambiando según cuánto scrolleas (scrub).

## 1. Principio rector: el texto es el protagonista

La landing no es "texto ilustrado con imágenes que van marcando el ritmo". Es al revés: la
tipografía y su composición cargan el peso narrativo y emocional; las imágenes/ilustraciones
son atmósfera y contexto, nunca el punto focal de una escena. Esto tiene consecuencias
prácticas para Fase 1 y Fase 2:

- Las composiciones tipográficas grandes (frases que ocupan una pantalla completa, tratadas
  como objeto gráfico) no son un adorno — son la unidad narrativa mínima de esta landing,
  al mismo nivel que una escena ilustrada.
- Cuando haya que elegir entre "dar más espacio a la imagen" o "dar más espacio al texto"
  en una composición, el texto gana por defecto, salvo que el copy mismo lo pida distinto.
- El scroll (pines, scrub) existe para controlar el *ritmo de lectura* del texto, no para
  lucir movimiento de imágenes.

### 1.1 Regla de las imágenes: sellan el concepto, no lo abren

Verificado contra la estructura real del sitio de referencia
(`Digizen-Cinco-Creencias-Diseno-2026-09-22/sitio/dist/index.html`), observación del
usuario: **las imágenes redondean/cierran el concepto de cada sección — no la abren, no la
ilustran de entrada.** En casi todos los capítulos, la imagen aparece en el DOM *después*
de que el argumento en texto ya se hizo, justo antes de pasar a la siguiente sección. Es un
sello visual del punto ya hecho en palabras, no un gancho.

**Única excepción, a propósito: el Hero.** Ahí la imagen va primero — arranca con un
extreme-zoom-out de la imagen para dar dramatismo (esto es lo que ya construimos en b-v2 y
se valida aquí: la imagen es el primer golpe visual, el texto llega después, encima de
ella). El Hero invierte la regla general porque su trabajo es distinto: engancha, no cierra.

Mapeo verificado, capítulo por capítulo (imagen ausente o presente, y en qué punto):

| Cap. | Imagen | Posición |
|---|---|---|
| Hero | `01-cena-absorto.png` | Antes del texto en efecto visual (zoom-out inicial), aunque en el DOM va después — es la excepción de apertura. |
| 01 · creemos | **ninguna** | Capítulo 100% tipográfico. Ya lo construimos así en b-v2 sin saberlo — esto lo confirma. |
| 02 · las cuatro falsas | `02-candados.png` | Al final, después de los 4 argumentos — sella el capítulo completo. |
| 03 · un favor | `08-fastidio-cejas.png` + `03-escudos-mama.png` | **Dos imágenes**: una a la mitad (sella el beat de "los ojos al techo") y otra al final (sella todo el capítulo, tras la frase lapidaria). |
| 04 · no eres mala mamá | **ninguna** | El capítulo "de descanso" — sin golpe de Registro B (sección 4/5) y sin imagen. Consistente: es puro texto amable, sin remate que sellar. |
| 05 · el cómo | `04-calle-mama.png` | A la mitad — sella la metáfora de cruzar la calle. La frase lapidaria ("El control caduca. El criterio no.") viene *después* de la imagen, sola, sin imagen propia — el golpe más fuerte del capítulo no lleva imagen. |
| 06 · mirar a los dos lados | **ninguna** | Capítulo de puras preguntas socráticas — nada que sellar visualmente todavía. |
| 07 · Esto se llama ADA | *(sin vignette; tiene el bloque de chat ADA/HIJO, que es otro tipo de figura, no ilustración)* | El chat funciona como su propio "sello", no una imagen. Nota: este capítulo no tiene `scroll-cue`/pausa de cierre en el HTML — fluye directo al capítulo 8. |
| 08 · «Espera...» | `05-reglas.png` | Al final, tras la lista de garantías — sella la tranquilización. |
| 09 · la prueba no es por fe | **ninguna** | Capítulo instruccional/CTA — sin imagen. |
| 10 · lo más importante eres tú | `06-mesa.png` | Al final, tras la cita del niño — sella el capítulo emocionalmente más fuerte de la pieza. |
| 11 · inscríbelo hoy | **ninguna** | Capítulo de precio/oferta — sin imagen, puro texto transaccional. |
| 12 · una última cosa | `07-cruzar-mochila.png` | Cerca del final, antes del tagline de cierre — es el pago visual de la metáfora completa (el hijo cruza solo, el papá observa sin celular). |

**Patrón resultante:** los capítulos sin golpe de Registro B (04, 06, 09, 11 — ver sección
5) tampoco tienen imagen. Los capítulos con un golpe fuerte casi siempre lo sellan con una
imagen inmediatamente después (02, 08, 10, 12) o alrededor de él (03, 05). Esto le da a
Fase 1/Fase 2 una regla operativa clara: **una imagen solo aparece cuando hay un concepto ya
argumentado en texto que necesita sellarse — nunca como decoración de entrada de sección.**

## 2. Dos registros tipográficos

No es "un solo sistema tipográfico con variaciones de tamaño". Son **dos registros con
personalidad distinta**, y la Fase 1 debe formalizar cada uno como un set de tokens propio
(familia/peso/tracking/color/escala — no solo "más grande"):

### Registro A — Default (amable, cálido)
- Es el tono de la narración/conversación con el usuario: explicaciones, contexto, el
  cuerpo de cada capítulo, las preguntas retóricas suaves.
- Es la mayoría del copy. Debe leerse fácil, cálido, cercano — sin perder peso visual (ver
  la lección de la v2: nunca gris en texto pequeño/cercano a body, peso base arriba de
  Regular).

### Registro B — Tensión / reflexión (brutalista pero estético)
- Reservado para **momentos de golpe**: frases que cierran una idea, la reencuadran, o
  detienen al lector a propósito. No es "el texto más grande de la página" por sistema —
  es el texto que **funciona narrativamente como un golpe**, sea corto o no.
- "Brutalista pero estético" = simplicidad radical (poco o ningún adorno, alto contraste,
  composición limpia), no agresividad visual gratuita. Sigue siendo parte del mismo sistema
  de marca, no un estilo ajeno insertado.
- Debe sentirse como una pausa real en el ritmo de lectura — un cambio de registro que el
  usuario percibe antes de leer la palabra siguiente, solo por cómo se ve.

### Cómo reconocer una frase candidata a Registro B en el copy
No hay una regla mecánica (no es "toda frase de menos de 6 palabras"), pero estas señales
ayudan a detectarlas al leer el copy fuente:
- Funciona sola, fuera de su párrafo — tiene sentido completo aislada.
- Es una afirmación/aforismo, no una explicación (dice una conclusión, no la argumenta).
- Cambia de tono respecto a la frase anterior: de razonar → a sentenciar.
- Suele cerrar un bloque de ideas o abrir el siguiente (funciona como puente o como remate).
- En el copy fuente casi siempre ya está aislada tipográficamente en su propio párrafo,
  a veces entre comillas «como cita».

**Corrección del usuario, importante:** el título/heading de un capítulo no es
automáticamente Registro A "funcional". Varios títulos SON el golpe de Registro B —
confirmado explícitamente por el usuario para: *"Lo que casi todos creemos"* (cap. 1),
*"«Espera. ¿Una IA hablando con mi hijo?»"* (cap. 8), *"Lo más importante no es ADA. / Eres
tú."* (cap. 10, título + primera línea juntos) y *"Una última cosa, y ya te dejo."* (cap. 12).
El mapeo de la sección 4 ya quedó corregido con esto.

## 3. El patrón de 4 partes del capítulo 1 (hipótesis, no plantilla)

Lo que el usuario recuerda del capítulo "01 · Lo que casi todos creemos" en la v2:

1. Título de la sección (Registro A, funcional).
2. Contenido/viñetas del capítulo (Registro A, lectura).
3. Frase semibrutalista de puente — un registro intermedio, más suave que el B puro, que
   anuncia que viene un golpe ("Ahora te digo cuál es la verdad.").
4. Frase lapidaria brutalista que da pie a la siguiente sección (Registro B pleno: "La
   cinco. No te escucha." + "Pero no por lo que crees. Y ahí es donde se pone interesante.").

**Por qué esto no debe copiarse igual en los otros 11 capítulos:** el capítulo 1 tiene esta
forma porque el copy mismo la tiene — es una lista de creencias que termina en una revelación
explícita. Otros capítulos tienen una forma narrativa distinta en el copy fuente. Ver el
mapeo de la sección 4: algunos tienen dos golpes de Registro B, otros ninguno claro, otros
un golpe pero sin "puente" previo.

## 4. Mapeo capítulo por capítulo (borrador — revisar con el usuario)

Formato: **Título** (heading real del copy) → contenido en Registro A → candidatas a
Registro B con la razón.

### 01 · Lo que casi todos creemos
- **Título = golpe (Registro B), confirmado por el usuario** — no es un encabezado neutro.
- Registro A: las 5 creencias numeradas.
- Puente (semibrutal): *"Ahora te digo cuál es la verdad."*
- Golpe (Registro B): *"La cinco. No te escucha."* + *"Pero no por lo que crees. Y ahí es
  donde se pone interesante."*
- Patrón de 4 partes, con una quinta capa (el título también es golpe) — es el caso de
  origen de la hipótesis, y resulta más denso en golpes de lo que parecía al principio.

### 02 · Las cuatro falsas, una por una

**Nota de animación del usuario:** *"Aquí es un carrusel que hace un recorrido de scroll
lateral hacia la derecha o un movimiento de cámara sobre X. Aquí hay un pin y un scrub o
algo parecido."*

Esto corresponde a dos patrones del catálogo `Scroll Patterns — Especimen Completo.html`
(ver sección 7 de este documento): **5 · Horizontal** (el carrusel lateral en sí, un
`.hz-track` de paneles que se desplaza en X en vez de Y) montado sobre **3 · Pin + Scrub**
(la sección se congela y el avance lateral está atado al scroll). Encaja de forma natural
con la estructura de "eco + respuesta" ×4 de este capítulo — un panel por creencia. También
podría inspirarse en **13 · Recorrido de cámara** si en vez de 4 paneles separados se quiere
sensación de una sola cámara moviéndose por una escena continua.

- No sigue el patrón de 4 partes. Es una estructura de **eco + respuesta** repetida 4 veces:
  cada creencia se cita textual («El problema es el tiempo.», «Si configuro bien la app de
  control…», «Si le pongo contraseña, se acaba el problema.», «Ya perdí.») y luego se
  desmonta en prosa.
- Candidata a Registro B: las 4 citas mismas — funcionan como micro-golpes que abren cada
  bloque, no como cierre. Esto sugiere que el Registro B puede aparecer *al inicio* de un
  bloque, no solo al final.
- No hay una frase lapidaria de cierre para todo el capítulo, pero sí un **puente de
  cierre** hacia el 03: *"Aguanta. Ahorita llegamos ahí."* (última línea del capítulo).

### 03 · Ahora, un favor.
- Registro A: la narración en segunda persona ("Acuérdate de lo que acabas de leer...").
- Puentes: *"¿Qué sentiste?"* (pregunta de apertura) y *"Quédate con eso un segundo. Porque
  te acabo de hacer exactamente lo que tú le haces a él."* — conecta la experiencia del
  lector con el argumento. También *"...Pero los dos están parados en el mismo lugar:"*,
  que anuncia directamente el golpe que sigue.
- Golpe (Registro B): *"Los ojos al techo. En señal de fastidio."* y, confirmado por el
  usuario, *"Alguien les dijo «no», y nadie les dijo «cómo»."* — el remate del capítulo.
- Este capítulo tiene **dos golpes y varios puentes**, no un solo par — señal de que el
  patrón de 4 partes no aplica igual en todos lados.

### 04 · Antes de seguir: no eres mala mamá ni mal papá.
- Registro A: el tono es deliberadamente cálido/absolutorio, casi todo el capítulo.
- Candidata a Registro B: *"Tu instinto no está roto. Éste necesita algo distinto."* —
  aforismo de cierre, funciona como remate.
- Puente de cierre: *"Suéltate la culpa. Necesitas espacio para lo que sigue."* — anuncia
  explícitamente la transición al capítulo 05.
- Nota: este capítulo es de los que menos "brutalismo" necesita por diseño — es el momento
  de descanso emocional entre dos golpes (cap. 3 y cap. 5), y tampoco tiene imagen (ver
  sección 1.1). Consistente: puro Registro A, sin nada que sellar todavía.

### 05 · Ahora sí: el «cómo». Y ya lo sabes hacer.
- El título arranca con *"Ahora sí:"* — mismo mecanismo puente que el título del capítulo 09
  y que "Ahora, un favor." del capítulo 03 (ver el patrón de la palabra "Ahora" como
  conector, nota general al final de esta sección).
- Registro A: la analogía de cruzar la calle, extendida.
- Puente: *"Ahora imagina que la única lección hubiera sido: «No cruces.»"*
- Candidatas a Registro B:
  - *"Bloquearle el celular es «no cruces»."* — metáfora condensada, golpe intermedio.
  - *"El control caduca. El criterio no."* — confirmado por el usuario como golpe, y
    probablemente la tesis central de toda la pieza. Nota de la sección 1.1: este golpe no
    lleva imagen propia — el remate más fuerte del capítulo se queda solo, sin sellar
    visualmente.

### 06 · ¿Y cómo se enseña a mirar a los dos lados?
- El título arranca con *"¿Y..."* — puente directo, continúa literalmente el pensamiento
  del capítulo 05 (que terminó hablando de cruzar la calle).
- Candidata a Registro B: *"El criterio se construye con preguntas. No con «deja el cel»."*
  — ya estaba marcada como `lead` en la v2, buena candidata a mantener.
- Puente de cierre: *"Pero sí hay alguien que puede estar ahí cada vez que él practique.
  Todas las veces que haga falta."* — hacia el capítulo 07.

### 07 · Esto se llama ADA.
- Mayormente Registro A (tono explicativo/producto).
- Candidata a Registro B: *"Una pausa. Una consecuencia. Una idea propia."* — ritmo
  staccato de tres golpes cortos, distinto a las demás candidatas (aquí el golpe es el
  ritmo, no una sola frase).
- Este capítulo también tiene el bloque de conversación de ejemplo (ADA/HIJO) — no es
  Registro B, es su propio tratamiento (diálogo), a definir aparte en Fase 1.
- Nota de estructura: en el HTML fuente, este capítulo no tiene pausa/`scroll-cue` de
  cierre — fluye directo al capítulo 08, sin el respiro que sí tienen los demás.

### 08 · «Espera. ¿Una IA hablando con mi hijo?»
- **Título = golpe (Registro B), confirmado por el usuario.**
- Casi todo el cuerpo es Registro A (tono de manejo de objeciones, tranquilizador).
- El dato *"7 de cada 10 adolescentes ya conversan con inteligencias artificiales..."*
  **confirmado por el usuario como Registro B** — no hace falta un tercer tratamiento
  aparte: los datos duros entran en Registro B igual que los aforismos.
- Puente: *"No es que vaya a pasar. Ya está pasando."* — dos frases cortas en paralelo,
  anuncian la conclusión ("Lo único que queda por decidir es cuál...").

### 09 · Y la prueba no te la pido por fe.
- El título arranca con *"Y..."*, mismo mecanismo puente que el capítulo 06 — continúa el
  hilo del capítulo 08.
- Registro A completo en el cuerpo — es copy transaccional/instruccional (cómo pedir acceso
  a ADA). No se le detectó golpe de Registro B propio, y tampoco tiene imagen (sección 1.1)
  — confirma que no todos los capítulos necesitan un golpe.
- Puente de cierre, el más explícito de todo el copy: *"Si ya viste suficiente, la
  inscripción está al final de esta página. Si no, sigue leyendo; falta lo más
  importante."* — la frase "falta lo más importante" empalma literalmente con el título
  del capítulo 10, "Lo más importante no es ADA."

### 10 · Lo más importante no es ADA.
- **Título + primera línea = golpe (Registro B), confirmado por el usuario**: *"Lo más
  importante no es ADA. / Eres tú."* — dos líneas, un solo golpe de apertura.
- Puente interno: *"Y aquí pasa algo que no te esperas."*
- Golpe adicional (Registro B), confirmado por el usuario: *"«Mi mamá se ríe más cuando ve
  el celular que cuando está conmigo.»"* — cita de un niño, el momento más duro
  emocionalmente de todo el copy.
- Este capítulo tiene **dos** golpes de Registro B en momentos distintos (apertura y cierre),
  no uno solo — otra variación del patrón.

### 11 · Inscríbelo hoy. Generación Fundadora.
- Registro A (copy de producto/precio), con un matiz: *"Doce meses, no diez: el verano va
  incluido, porque las redes no salen de vacaciones."* es punchy pero de un sabor distinto
  — es un golpe de **copywriting de venta**, no un golpe emocional/reflexivo. Probablemente
  no debería llevar el mismo tratamiento visual que el Registro B narrativo — a decidir en
  Fase 1 si necesita un tercer registro o si entra en B igual.

### 12 · Una última cosa, y ya te dejo.
- **Título = golpe (Registro B), confirmado por el usuario** — y funciona a la vez como
  puente (anuncia explícitamente "esto ya se acaba"), un caso donde golpe y puente son la
  misma frase.
- Puente interno: *"Al principio te dije un «no» y te debí el «cómo» un buen rato."* —
  recapitula todo el arco de la landing antes del cierre.
- Golpe adicional: *"Ya lo tienes."* — corto, paralelo a "Eres tú." del capítulo 10.
- Candidata a Registro B: *"No inscribirlo también es una decisión. La diferencia es que
  ésa no tiene botón de cancelar."* — aforismo de tensión, cierre del argumento completo.
- El tagline final *"Presencia, no vigilancia. Criterio, no candado."* ya se trata aparte en
  el sitio (pantalla tipográfica de cierre) — es el Registro B a su expresión más pura, el
  resumen de toda la marca en 6 palabras.

**Nota general sobre los puentes:** varios arrancan con la palabra **"Ahora"** ("Ahora, un
favor.", "Ahora te digo cuál es la verdad.", "Ahora sí: el «cómo»...", "Ahora imagina...",
"Ahora acuérdate...") o con **"Y"** ("¿Y cómo se enseña...?", "Y la prueba no te la pido por
fe.", "Y aquí pasa algo que no te esperas."). No parece casual — son casi palabras-marca de
transición en este copy. Vale la pena que Fase 1 les dé un tratamiento tipográfico
reconocible como conectores, distinto tanto del Registro A como del B pleno.

## 5. Lo que falta decidir en Fase 1 (no en este documento)

Este documento da la lógica narrativa; Fase 1 debe convertirla en decisiones concretas de
sistema de diseño:
- Tokens tipográficos exactos para Registro A, Registro B, y un tercer tratamiento más
  discreto para los puentes/conectores ("Ahora", "Y" — ver nota al final de la sección 4).
- Si el copy de venta/producto punchy del capítulo 11 ("Doce meses, no diez...") entra en
  Registro B tal cual o necesita su propia variante (dato de cifra ya se resolvió: entra en
  Registro B, confirmado por el usuario).
- Cómo se trata visualmente un capítulo que **no** tiene golpe de Registro B (cap. 4, 6, 9,
  11) — el silencio también es una decisión de diseño, no un vacío. Nota: estos capítulos
  tampoco tienen imagen (sección 1.1) — la ausencia de golpe y la ausencia de imagen van
  juntas, otra señal a favor de esa correlación.
- Regla de composición para cuando un capítulo tiene más de un golpe de Registro B (cap. 1,
  3, 10, 12) — ¿todos con el mismo peso visual, o se jerarquizan?

## 6. Estrategia de animación: Pin + Scrub como patrón dominante

Regla explícita del usuario, no negociable a nivel arquitectura (aplica a Fase 1 y Fase 3):

- La landing completa es **un recorrido continuo de scroll**, resuelto con la librería
  **GSAP + ScrollTrigger**. No es una página de secciones independientes que cada una decide
  su propio efecto suelto.
- **Patrón 3 · Pin + Scrub predomina.** Las secciones no son bloques que simplemente
  aparecen al llegar (Patrón 1 · Reveal on Enter) — son **paradas ("escalas")** dentro de un
  recorrido: la sección se congela (pin) y su contenido avanza/retrocede exactamente atado
  a la posición del scroll (scrub), igual que ya se validó en el capítulo 01 de la v2
  (título → creencias → puente → revelación, las 4 pantallas dentro de un mismo pin,
  reversible con `snap` a cada parada — ver la lección correspondiente en `METAPROMPT.md`).
  **Ese es el modelo a generalizar a toda la landing, no solo al capítulo 1.**
- Los demás patrones del catálogo (Horizontal, Parallax, Batch Reveal, Snap, etc.) se usan
  **dentro** de esa lógica de pin+scrub cuando una sección puntual lo pida — no como
  alternativas que compitan con el patrón dominante. Reveal on Enter simple queda para casos
  puntuales y menores (ej. un botón, un ícono), no para el paso entre capítulos.
- El usuario considera `Scroll Patterns — Especimen Completo.html` un catálogo limpio y bien
  resuelto — la Fase 1/3 debe apoyarse en su código de referencia directamente, no
  reinventar la implementación de cada patrón desde cero.

## 7. Vocabulario de animación — 14 patrones de referencia

Archivo completo (con código funcional de cada uno):
`Projects/digizen-landing-b-v2/Scroll Patterns — Especimen Completo.html`

Estos son los 14 nombres que va a usar cualquier anotación de animación en este documento
o en la Fase 2 (wireframe). En vez de describir la animación en prosa larga, basta con
anotar "Patrón 3" o "Patrón 3 + 5" y todos entendemos lo mismo:

1. **Reveal on Enter** — aparece una vez, al llegar a esa parte de la página. No está atado
   al scroll después de aparecer (no usa pin ni scrub).
2. **Scrub** — la animación avanza/retrocede exactamente con la posición del scroll, sin
   pin (el contenido se sigue moviendo en la página mientras cambia).
3. **Pin + Scrub** — la sección se congela en pantalla y su contenido cambia según el
   scroll (ver glosario). El más usado en esta landing.
4. **Timeline + Stagger** — varios elementos entran uno tras otro con un pequeño retraso
   entre cada uno (ej. palabras que aparecen en cascada).
5. **Horizontal** — el scroll vertical normal del usuario mueve contenido de forma
   horizontal en pantalla (un carrusel/recorrido lateral).
6. **Parallax** — capas que se mueven a velocidades distintas entre sí al hacer scroll (da
   sensación de profundidad). Sin pin.
7. **Batch Reveal** — varios elementos parecidos (ej. tarjetas) aparecen agrupados/en oleada
   al entrar en pantalla, en vez de uno por uno.
8. **Snap** — el scroll "cae" y se acomoda solo en paradas fijas, no se queda a medias entre
   dos estados. Es lo que usamos para las 4 pantallas del capítulo 01 en la v2.
9. **Text Split / Stagger** — un bloque de texto se divide en letras o palabras que entran
   por separado (variante de Timeline + Stagger, pero para tipografía).
10. **Scroll-linked Counter** — un número que cuenta hacia arriba/abajo según el scroll (ej.
    una cifra que sube de 0 a 100).
11. **matchMedia** — no es una animación en sí, es la regla que decide *cuál* patrón usar
    según el ancho de pantalla (ej. en móvil usa el patrón 1, en desktop el patrón 3).
12. **ScrollSmoother** — una inercia global suave (como en sitios de Apple) que envuelve
    todo el scroll de la página, no una sección puntual.
13. **Recorrido de cámara** — varias "escenas" o datos aparecen como si una cámara recorriera
    un espacio continuo, en vez de secciones separadas.
14. **Reel de cards** — combina Pin + Scrub (patrón 3) con Snap por paradas (patrón 8): una
    fila de tarjetas que se recorre con el scroll y se acomoda tarjeta por tarjeta.

Al anotar cada capítulo en la Fase 2, usar este vocabulario en vez de describir la animación
desde cero cada vez — reduce ambigüedad y es más rápido de escribir para el usuario.
