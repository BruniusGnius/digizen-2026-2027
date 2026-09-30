# Cómo pedirle a Codex que mejore su versión (v04-codex)

## 1. Por qué costaba pedirlo

Lo que quieres es un **ensayo editorial que se lee con el scroll**. Lo estabas pidiendo con palabras de web estática: "landing", "secciones", "wireframe", "insumos". Cualquier IA traduce eso al proceso de siempre: tokens → cajas grises → código con animaciones de entrada. Pasaron tres cosas:

1. **Tus referencias estaban rotuladas como opcionales.** El metaprompt v1 decía "insumos opcionales como punto de partida, nunca copiar 1:1 sin evaluar". Codex lo dejó escrito en su auditoría: «composiciones B/L como vocabulario… No se copia 1:1».
2. **La idea central no tenía nombre.** Que el scroll se **estaciona** en pantallas 16:8.6 / 9:15.3, y que cada frase vive en una de esas pantallas, no estaba escrito como regla. Sin esa regla, "Pin + Scrub dominante" se leyó como "pin en algunas secciones y fundidos de entrada en el resto". Eso es justo lo que hizo Codex.
3. **"Wireframe" invoca cajas.** El de Codex lo dice textual: «intencionalmente de baja fidelidad: cajas, grises conceptuales».

Las tres frases tuyas que lo destrabaron, y que conviene poner siempre primero:
- "Toma Tipografía esencial como sistema de diseño."
- "Todo está en proporción 16:8.6, calculando el estacionado del scroll en cada sección."
- "El wireframing tiene que tener las escalas de scroll."

**Vocabulario mínimo:**

| Palabra | Qué significa |
|---|---|
| **Encuadre** | La pantalla estacionada: 16:8.6 = 1440 × 774 (laptop), 9:15.3 = 390 × 663 (iPhone, `100svh`). |
| **Parada** | Una composición que se queda quieta en un encuadre mientras el usuario hace scroll. Tiene que caber completa. |
| **Estacionamiento (E)** | Cuánto scroll dura una parada. 1 E = una pantalla de scroll. |
| **Pin** | Un tramo de paradas seguidas. Su largo es la suma de sus E. |
| **Reveal / aparición** | Patrón 1: un bloque aparece al llegar y sigue de largo. **No es una parada.** |
| **Ocupación** | Qué % del encuadre llena una parada, medido en el móvil de 360 px. |
| **Composición B01…L08** | Las 17 piezas de `Tipografía esencial`. |

**Cómo pedir:**
1. Declara el sistema: "X **es** el sistema".
2. Nombra la prueba: "cada parada cabe en su encuadre".
3. **Prohíbe explícitamente lo que no quieres:** "ningún capítulo se resuelve con reveals".
4. Pide criterios que se puedan verificar, más una tabla de resultados.
5. Da el feedback por ID de parada.

## 2. Qué revisé de la versión de Codex (solo lectura)

Revisé `Projects/digizen-landing-b-v04-codex/`: `01-design-system.md`, `02-wireframe.md`, `03-build-notes.md`, `index.html` y `src/main.js`, y le corrí a su `index.html` la auditoría de copy de mi wireframe.

### Problema n.º 1: pines y patrones solo en las primeras secciones

| Capítulo (`id` en su `index.html`) | Qué hace hoy su `main.js` |
|---|---|
| Hero (`#hero`) | ✓ Pin de 3.1 pantallas, scrub, snap a etiquetas |
| 01 (`#creemos`) | ✓ Pin de 5.2 pantallas: título → filas → puente → remate |
| 02 (`#falsas`) | ✓ Pin horizontal con 4 láminas + lámina de imagen |
| 03 (`#favor`) | ✗ `revealIn`: todo el capítulo aparece de golpe al llegar al 52 % de la pantalla |
| 04 (`#culpa`) | ✗ `revealIn` |
| 05 (`#como`) | ✗ `revealIn` |
| 06 (`#preguntas`) | ✗ `revealIn` |
| 07 (`#ada`) | ✗ `revealIn`: las 4 burbujas del diálogo aparecen juntas |
| 08 (`#seguridad`) | ✗ `revealIn` |
| 09 (`#prueba`) | ✗ Sin ningún movimiento |
| 10 (`#tu`) | ✗ `revealIn` |
| 11 (`#inscripcion`) | ✗ `revealIn` |
| 12 (`#cierre`) | ✗ `revealIn` |
| Escenas (`.scene-seal`) | Parallax con scrub, sin pin (no se estacionan) |

Además:
- **En móvil no hay nada:** `setupDesktopMotion()` solo corre desde 861 px, así que no se ejecuta ni el pin del Hero.
- **Con "reducir movimiento" se cancela todo** (`clearProps` + `return`) en vez de degradarse. Para quien lo tenga activado, eso deja la página sin su recorrido.

### Otros hallazgos

**Qué conservar (va bien):**
- `gsap.matchMedia()`.
- Timelines de nivel superior con etiquetas.
- `refreshPriority` en orden.
- `stationSnap()`.
- Progreso con `scaleX`.
- Las estaciones del Hero, el cap. 01 y el carrusel del cap. 02.
- El orden narrativo.

| # | Dónde | Qué pasa |
|---|---|---|
| 2 | `01-design-system.md` | Escala propia (92/76/48/38/25/19/15/12, tracking 0) en vez de la del espécimen (144/96/56/32/24/18/14/12). Las 17 composiciones se usan solo como "vocabulario". |
| 3 | `02-wireframe.md` | Wireframe de cajas, sin encuadres ni estacionamiento. |
| 4 | `index.html` ~l.183 | **Falta** «Pero hay un dato que quiero que te lleves en la cabeza:». |
| 5 | `index.html` ~l.230 | **Falta** «Tu inscripción fundadora incluye:». |
| 6 | `index.html` ~l.245–251 | **Precio reescrito:** «Todo hoy» + «$4,990» y «10 pagos mensuales» + «$599». El literal es «Todo hoy, de una vez: $4,990.» y «En 10 pagos mensuales de $599.». |
| 7 | `index.html` l.67, 74, 81, 88 | Etiquetas inventadas: «Las cuatro falsas · 01…04». |
| 8 | `index.html` ~l.302–303 | CTA flotante con etiquetas que no están en el copy: «Inscribir» y «Hablar con ADA». |
| 9 | `index.html` ~l.279 | «(FAQ)» visible. Es una etiqueta de extracción; el título es «Por si te quedó una duda.». |

**Decisiones que tomaste en mi sesión y que Codex no tiene.** Borra la línea de las que no apliquen:
- a) La paleta completa del logo.
- b) Los dos CTA con el mismo peso.
- c) `03-eyes` como escena final.
- d) Tono "directo, empático, sin sermón".

## 3. Prompt para Codex (listo para pegar)

```
Quiero que MEJORES tu versión en Projects/digizen-landing-b-v04-codex/. No empieces de cero:
conserva lo que funciona (gsap.matchMedia, timelines con labels, refreshPriority, stationSnap,
las estaciones del Hero, del cap. 01 y del carrusel del cap. 02, el orden narrativo).

EL PROBLEMA PRINCIPAL: el recorrido con pines se acaba en el cap. 02.
Hoy, del cap. 03 al 12 cada capítulo se resuelve con revealIn() (toggleActions: todo aparece de
golpe a media pantalla y sigue de largo), el cap. 09 no tiene nada, en móvil no corre ningún
movimiento (setupDesktopMotion solo desde 861 px) y con prefers-reduced-motion se cancela todo.
La regla del proyecto es la contraria: TODA la landing es un recorrido de PARADAS ESTACIONADAS
(Pin + Scrub + Snap), como tu cap. 01, de principio a fin, en desktop Y en móvil.

Qué significa "parada estacionada":
- Los marcos de Tipografía esencial son la pantalla estacionada: 16:8.6 = 1440×774 y
  9:15.3 = 390×663 (= 100svh).
- Cada frase o bloque es una PARADA: se queda quieta en su encuadre mientras el usuario hace
  scroll, y tiene que caber completa (pruébalo en 360×612).
- Cada parada tiene su ESTACIONAMIENTO en E (1 E = 100svh de scroll): golpe 1.25 ·
  puente→golpe 1.5 · lectura 1 · escena 1.
- Cada capítulo es uno o varios pines de máximo 6 paradas: end = ΣE × innerHeight, scrub 0.4,
  snap a un label por parada.
- Una parada de lectura lleva máximo ~100 palabras; ningún párrafo se parte entre paradas.
- Las escenas también son paradas dentro del pin (con parallax adentro), no parallax suelto.

Estructura mínima por capítulo (del cap. 03 en adelante):
- 03 #favor: título → «¿Qué sentiste?» + lectura → puente → golpe «Los ojos al techo. En señal
  de fastidio.» → escena 03-eyes → bisagra oscura (puente → «Alguien les dijo «no», y nadie les
  dijo «cómo».») → lectura → lectura → escena 04-shield.
- 04 #culpa: respiro, solo paradas de lectura (sin golpe, sin imagen, sin acento).
- 05 #como: apertura → lectura → puente + lectura → golpe «Bloquearle el celular es «no cruces».»
  → escena 05-crossing → puente → bisagra oscura en dos tiempos «El control caduca.» →
  «El criterio no.» → cierre de lectura.
- 06 #preguntas: respiro, paradas de lectura + puente final.
- 07 #ada: apertura → lecturas → diálogo con UN mensaje por paso de scroll (4 snaps; ADA entra
  por la izquierda y HIJO por la derecha) → golpe «Una pausa. Una consecuencia. Una idea propia.»
  → lecturas.
- 08 #seguridad: título-golpe → lectura → dato «7 de cada 10» (con el copy completo alrededor)
  → puente → reglas de ADA (lista, entrada escalonada) → escena 06-rules.
- 09 #prueba: respiro: apertura → lectura → enlace a #inscripcion + puente.
- 10 #tu: «Lo más importante no es ADA.» → «Eres tú.» (dos tiempos) → lectura → cita → puente
  → bisagra oscura con la cita del niño → lectura → escena 07-together.
- 11 #inscripcion: apertura → «Doce meses, no diez…» → lista fundadora (repartida si no cabe)
  → precio → garantía + CTA.
- 12 #cierre: título-golpe → «Ya lo tienes.» (dos tiempos) → puente → golpe «No inscribirlo…»
  → CTA → escena 08-autonomy → bisagra oscura «Presencia, no vigilancia. Criterio, no candado.»
- FAQ y footer: flujo normal (acordeón), sin pin.

Usa el catálogo de Scroll Patterns, no solo pin+scrub (mapa en §4 de METAPROMPT-v2):
3 pin+scrub y 8 snap en todo · 5 horizontal (cap. 02) · 4 entrada escalonada en listas ·
9 texto dividido por palabra en golpes monumentales · 10 contador en «7 de cada 10» ·
6 parallax dentro de las escenas · 14 barras de cine en las 5 bisagras oscuras ·
13 recorrido de cámara para no dejar tránsitos muertos entre pines.
El patrón 1 (reveal) solo para elementos menores; NUNCA para resolver un capítulo.

Móvil y movimiento reducido:
- Móvil (<860 px): los mismos pines y paradas (E relativo a 100svh), con la escala móvil del
  espécimen.
- prefers-reduced-motion: degradar, nunca cancelar: sin pin ni scrub, cada parada como bloque
  en flujo que aparece con un fundido de 200 ms. Agrega un botón de revisión para ver ambos
  modos (mi sistema tiene "reducir movimiento" activado).

Sistema tipográfico: Tipografía esencial ES el sistema, no vocabulario. Escala de 8 pasos tal
cual (micro 12/11 · small 14/13 · body 18/16 · subhead 24/19 · heading 32/24 · semimonumental
56/34 · monumental 96/48 · monumental-xl 144/64, sin clamp, corte a 860 px), sus reglas y sus 17
composiciones (B01–B09, L01–L08) como tipos de parada. NO las uses todas ni por variedad: a cada
función narrativa (apertura, golpe, lapidario, puente, lectura, cita, lista, dato, escena) le toca
UN layout y se repite siempre igual. Prefiero coherencia narrativa y consistencia visual a la
diversidad. En composiciones de dos partes, lo grande es la frase de más impacto, nunca el puente.
Cambios al espécimen, solo como opciones numeradas.
Excepciones ya aprobadas: peso base 500 y nada de gris en texto romano pequeño.

Fidelidad del copy (COPY-PUBLICADO.md es literal):
1. ~l.183: falta «Pero hay un dato que quiero que te lleves en la cabeza:».
2. ~l.230: falta «Tu inscripción fundadora incluye:».
3. ~l.245–251: precio literal «Todo hoy, de una vez: $4,990.» y «En 10 pagos mensuales de $599.»
   (el monto se enfatiza en su lugar, sin partir ni resumir la frase).
4. l.67/74/81/88: quita las etiquetas inventadas «Las cuatro falsas · 01…04».
5. CTA flotante: «Inscribir» y «Hablar con ADA» no están en el copy. Usa las etiquetas literales
   o quita el flotante (propónmelo).
6. ~l.279: el título es «Por si te quedó una duda.» («(FAQ)» es una etiqueta de extracción).

Decisiones mías:
a) Paleta = la paleta completa del logo: azul #1A75EA→#2C1DDB, cian #00C4F0, ámbar #EF9600,
   coral #E65C4D, violeta #7B27D6.
b) Los dos CTA pesan lo mismo.
c) Las 14 escenas son finales, incluida 03-eyes.
d) Tono: directo, empático, sin sermón.

Lee antes de proponer:
- Projects/digizen-landing-b-v04-claude/00-context/METAPROMPT-v2.md
- 00-context/Tipografía esencial.html COMPLETO
- 00-context/Scroll Patterns — Especimen Completo.html
- Skills/gsap/ORIGEN.md

Cómo trabajar:
1. Esto reabre las Fases 1 y 2: dilo y trabaja con los gates.
2. Primero un plan numerado; espera mi aprobación.
3. Luego el RECORRIDO EN GRISES (02-wireframe.html): tipografía real, pines/E/snap reales,
   regla lateral con la escala de todo el scroll, HUD (parada, composición, E) y % de ocupación
   por parada. El copy va una sola vez en un archivo de datos, con auditoría automática
   (completo, literal y en orden, en desktop y en móvil).
4. Solo después de que lo apruebe, porta al build (index.html, main.js).

Criterios de aceptación (verifícalos y repórtalos):
- Del cap. 03 al 12, ninguno se resuelve con revealIn/toggleActions: todos tienen pin(es) con
  paradas, scrub y snap.
- Los pines existen también en móvil (<860 px).
- Reduced motion degrada (flujo + fundidos); no hace return vacío.
- Auditoría del copy: 0 faltantes, 0 fuera de orden, sin textos inventados.
- Ninguna parada pasa del 100 % de ocupación en 360×612 ni en 1440×774.
- En 03-build-notes.md, una tabla capítulo → pin(es) → paradas (id, composición) → E →
  patrones usados, y el largo total del recorrido en E.

No toques nada fuera de Projects/digizen-landing-b-v04-codex/. Projects/digizen-landing es la
landing A, funcional: solo lectura. Pide permiso antes de abrir un navegador.
```

**Una línea opcional**, si quieres que Codex vea un ejemplo funcionando (así la comparación deja de ser independiente):

```
Como referencia de formato (no para copiar decisiones): Projects/digizen-landing-b-v04-claude/02-wireframe.html
y su generador en wireframe-src/.
```

## 4. Plantilla para dar feedback del recorrido

| Parada (ID) | Qué veo | Qué quiero |
|---|---|---|
| 05.4 | El golpe se ve chico | B07, monumental-xl |
| 03.4 | La escena corta el ritmo | Que entre con parallax junto al golpe de 03.3 |
| 06.2 | Otra columna de lectura igual | L02 (dos columnas) o L05 |

En "Qué quiero" puedes pedir:
- una composición (B01–L08);
- un tamaño;
- una posición de imagen;
- el estacionamiento (más o menos E);
- un patrón del catálogo.
