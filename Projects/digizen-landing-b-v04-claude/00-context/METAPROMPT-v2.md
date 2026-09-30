# Metaprompt v2 — Digizen Landing B · landing de recorrido (scroll)

> Reemplaza a `METAPROMPT.md` (v1), que se conserva al lado para comparar. Pega este archivo completo como primer mensaje de una conversación nueva **que empieza desde cero**. Para pedirle a Codex que mejore la versión que ya entregó (`Projects/digizen-landing-b-v04-codex/`), usa `../PROMPT-Codex-mejorar-v04.md`.

## 0. Antes de responder nada

1. **Lee `AGENTS.md`** en la raíz del vault. Pide seguir `Skills/landing-builder/SKILL.md` completo, con sus gates de aprobación.
   - **Este metaprompt adapta ese proceso a una landing de recorrido** (§5). Donde choquen, manda este metaprompt. El skill está pensado para landings de bloques, con wireframe de cajas; esta landing se estructura por el scroll.
2. **Lee completos:**
   - `Skills/apple-design/SKILL.md`.
   - `Skills/gsap/ORIGEN.md`, que dice qué skill oficial de GSAP abrir para cada cosa. Las skills están en `Skills/gsap/*/SKILL.md`.
3. **Reglas duras, sin excepción:**
   - **No toques la carpeta madre fuera de tu carpeta de proyecto.**
   - **Solo lectura:**
     - `Projects/digizen-landing`: landing A, funcional; no se modifica nada.
     - `Projects/digizen-landing-b`: original de Codex.
     - `Projects/digizen-landing-b-v2` y `Projects/digizen-landing-b-v3`: iteraciones anteriores.
   - Leerlas está permitido; copiar un asset a tu proyecto, también.
   - Trabaja solo en `Projects/<tu-proyecto>/`. El usuario te dice el nombre.
   - Haz commit solo de tu carpeta, y solo si el usuario lo pide.
4. **Reglas del usuario sobre cómo trabajar:**
   - Cambia solo lo que se pide.
   - Nunca toques tipografía (tamaño, peso, tracking, mayúsculas) sin permiso.
   - Para decisiones de gusto, ofrece opciones numeradas, con la opción por defecto marcada.
   - Imágenes: una por escena (no versiones distintas para móvil y desktop) y sin captions visibles.
   - Con **"reducir movimiento"** (para quien lo tenga activado; el Mac del usuario no lo tiene, lo verificó el 2026-09-29), en la landing real se degrada la animación, nunca se cancela.
   - **Pide permiso antes de abrir cualquier navegador**, incluso uno aislado o headless, para tomar capturas.

## 1. Qué es esto

Es una landing de Digizen, producto de Gnius Club: un mentor de IA para que niños y adolescentes entrenen criterio digital. Está escrita como **ensayo editorial de scroll**:
- el texto es el protagonista;
- las imágenes sellan conceptos ya argumentados;
- el scroll controla el ritmo de lectura.

**No es una página de secciones:** es un recorrido de pantallas estacionadas.

## 2. Fuentes y cómo tratar cada una (esto faltaba en la v1)

| Archivo (en `00-context/`) | Qué es | Cómo tratarlo |
|---|---|---|
| `COPY-PUBLICADO.md` | Copy de producción | **Fuente de verdad literal:** no se omite, resume, parafrasea ni inventa. **Ojo:** «## Footer», el «(FAQ)» del encabezado y la «Nota de procedencia» del final son notas de extracción, no copy de la página (verificado contra el sitio de referencia). En el sitio, las etiquetas del diálogo son `ADA` / `HIJO`, sin dos puntos. |
| `Tipografía esencial.html` | **EL sistema de diseño base** | **No es un insumo opcional ni vocabulario.** Se adopta tal cual (§3). Cualquier cambio se propone como opción numerada, con el espécimen como opción por defecto. Los textos de ejemplo que contiene («Basta.», «Sin miedo.», «30 / días de garantía…») **no son copy**. |
| `Scroll Patterns — Especimen Completo.html` | **EL catálogo de movimiento** y su código de referencia | Se usan sus 14 patrones a fondo, según el mapa de §4, no solo pin + scrub. Al portarlo: el patrón 11 (matchMedia) es una demostración y en producción va `gsap.matchMedia()`. |
| `VISION-NARRATIVA.md` | Dirección creativa: registros, regla de imágenes, Pin + Scrub dominante | El mapeo por capítulo (§4) es un borrador. Tiene erratas: ver §7 de este documento. |
| `scenes/` | Las 14 escenas reales (`.webp`) | Son finales. Los nombres de VISION son del sitio de referencia y no coinciden con estos archivos: ver la tabla de §7. |
| `logo/` | SVG del logo | Paleta del logo: degradado azul `#1A75EA → #2C1DDB`, cian `#00C4F0`, ámbar `#EF9600`, coral `#E65C4D`, violeta `#7B27D6`. En v04 el usuario la fijó completa. |

## 3. Conceptos clave (el vocabulario que faltaba)

- **Encuadre.** Los dos marcos del espécimen son la pantalla real donde se estaciona el scroll:
  - **16:8.6 = 1440 × 774**: un laptop de 1440 × 900 menos la barra del navegador.
  - **9:15.3 = 390 × 663**: un iPhone con la interfaz de Safari visible, o sea **`100svh`**.
  
  Por debajo de 860 px (teléfonos y tablets en vertical) se usan la escala y el encuadre móvil.
- **Parada.** Una composición estacionada en un encuadre. **Debe caber completa en su encuadre, en desktop y en móvil, sin scroll interno.** La prueba se hace en el móvil más angosto: 360 × 612, que deja 312 × 556 útiles.
- **Estacionamiento (E).** 1 E = un encuadre de scroll (`100svh`). Cada parada tiene su E. Valores iniciales de v04, a calibrar:

  | Tipo de parada | E |
  |---|---:|
  | Golpe | 1.25 |
  | Puente + golpe | 1.5 |
  | Lectura | 1 |
  | Escena | 1 |
  | Panel horizontal | 1 |
  | Hero (autoplay) | 1.5 |
- **Pin.** Un tramo del recorrido con sus paradas.
  - Su largo es `end = ΣE × innerHeight`.
  - El snap cae en una etiqueta por parada.
  - Lleva **máximo 6 paradas** (los pines largos fueron frágiles en v2).
  - Entre dos pines hay **1 E de tránsito sin contenido**: es tiempo muerto y conviene reducirlo (pines encadenados, patrón 13).
- **Capacidad.** Una parada de lectura lleva **como máximo ~100 palabras** (medido con Inter 500 en el móvil de 360). **Un párrafo nunca se parte entre paradas.**
- **Tamaño de un golpe.** Es el paso más grande del grupo B que, en el móvil de 360, quepa en **5 líneas o menos y ocupe como máximo el 60 % del alto útil**. Se mide con las fuentes reales: Inter y Playfair variables están instaladas en `~/Library/Fonts/`.
- **Registros de VISION, mapeados al espécimen:**
  - **Golpe (B)** = grupo B (B01–B09).
  - **Puente** = la línea lead de B03, B04, B05 y B08.
  - **Narración (A)** = grupo L (L01–L08).
- **Bisagra.** Golpe lapidario a pantalla completa en escenario oscuro. **Máximo 5** en toda la landing.

**Sistema del espécimen, tal cual:**
- **Escala de 8 pasos, fija, sin `clamp()`:**
  - micro 12/11 · small 14/13 · body 18/16 · subhead 24/19 · heading 32/24;
  - semimonumental 56/34 · monumental 96/48 · monumental-xl 144/64 (desktop / móvil).
- Playfair Display + Inter.
- Retícula de 12 columnas (separación 24/16) y contenedor de 1180 px.
- **Reglas de composición:**
  - como máximo 2 pasos de tamaño por pieza;
  - un acento por pieza;
  - espacio negativo generoso;
  - centrado vertical casi siempre;
  - toda asimetría con `grid-column: span N`.

## 4. Mapa: tipo de parada → composición → patrón de scroll (esto faltaba en la v1)

| Tipo de parada | Composiciones del espécimen | Patrón de Scroll Patterns |
|---|---|---|
| Golpe de 1–2 palabras | B07, B02 | 3 + 8 · 9 (dividir por palabra) |
| Golpe + remate | B01 | 3 + 8, entrada por corte |
| Puente → golpe | B03, B04, B05, B08 | 3 en dos tiempos (lead → cierre) |
| Golpe de dos tiempos cortos | B06 | 3 · 9 |
| Dato o cifra | B09, L01 | 10 (contador) |
| Lista numerada | L03 | 4 (entrada escalonada) |
| Contraste / dos voces | L02 | 3, columna a columna |
| Cita | L04 | 3 |
| Serie de citas-eco con prosa | L05 | 5 (horizontal) |
| Apertura de capítulo | L06 | 3 |
| Ensayo | L07 | 3 |
| Lista de elementos paralelos | L08 | 4 · 7 |
| Escena (sello) | — | 6 (parallax dentro del pin) |
| Bisagra oscura | Lapidario del grupo B | 14 (reel, con barras de cine) |
| Paso entre capítulos | — | 13 (recorrido de cámara) para no dejar tránsitos muertos |
| Hero | — | Timeline autoplay en `onEnter` (lección v2), no scrub |
| FAQ / footer | Acordeón | Flujo normal · 1 / 7 |

**Regla de coherencia (corrige una regla de variedad que se probó y el usuario rechazó el 2026-09-28):**
- **Cada función narrativa tiene UN layout, y se repite siempre igual.** El lector aprende la gramática: cuando ve ese layout, sabe qué tipo de momento es.
- **No se usan composiciones por variedad.** No hace falta usar las 17: se eligen las que sirven a la narrativa y se repiten. Una columna de lectura repetida es consistencia, no monotonía.
- La variación del ritmo sale de la narrativa (qué función aparece), no de cambiar de composición.
- El tamaño de un golpe lo da su jerarquía (lapidario > golpe), no el gusto por la diversidad.
- La parte grande de una composición de dos partes es siempre la de más impacto: se sostiene sola, concluye, reencuadra y es la que el lector repetiría. Un puente (anuncia, pregunta o conecta) nunca es la parte grande.

## 5. Proceso: el landing-builder en "modo recorrido"

Las 3 fases y sus gates siguen, pero cambia qué se entrega en cada una:

- **Fase 0 (igual que el skill).**
  - `project.config.md` + cuestionario (público, legibilidad, tono, conversión, restricciones fijas).
  - En v04 el usuario respondió:
    - público frío;
    - tono: "directo, empático, sin sermón";
    - dos CTA con el mismo peso;
    - fijos: escenas tal cual, Playfair + Inter y paleta completa del logo.
  - Pregunta si se mantienen.
- **Fase 1: sistema de diseño.**
  - Base: el espécimen (§3).
  - Se agregan:
    - encuadres y estacionamiento;
    - **tabla medida de cabida** (palabras por encuadre y tamaño de cada golpe candidato, con las fuentes reales);
    - roles de la paleta del logo, con contraste medido;
    - componentes de UI que el espécimen no tiene (CTA, diálogo, precio, FAQ);
    - reglas de GSAP.
  - Los ajustes al espécimen van como opciones numeradas.
- **Fase 2: wireframe de recorrido, NO un wireframe de cajas.**
  - Un HTML en **escala de grises** con:
    - tipografía y escala reales (la ocupación depende de ellas);
    - pines, E y snap reales con GSAP;
    - **regla lateral con la escala del recorrido completo** (clic para saltar a cada parada);
    - HUD con parada, composición, E, pin y nota de intención;
    - **% de ocupación medido por parada** (marcado cuando desborda);
    - botón para ver el modo reducido;
    - escenas en gris.
  - Se genera desde **una sola fuente de contenido** (el copy escrito una vez), con **auditoría automática**: el copy completo y en orden, en desktop y en móvil.
  - Se acompaña de una partitura en `.md`: pin → parada → composición → E → nota.
  - Ejemplo funcionando: `Projects/digizen-landing-b-v04-claude/wireframe-src/`.
- **Fase 3: build.**
  - Color, movimiento final con los patrones del mapa §4 y paso a producción.
  - Recomendación: prototipo HTML + GSAP primero y framework después. Se decide con el usuario.

**Rúbrica:** además de los 3 lentes del skill, el Guardián de Lectura evalúa el **ritmo**:
- largo total en E;
- ocupación por parada (ni desbordes ni pantallas vacías sin intención);
- coherencia: cada función narrativa con su mismo layout en toda la pieza;
- tiempo muerto entre pines.

## 6. Lecciones técnicas (v2 + v04)

- **Secuencias:**
  - Una secuencia de un solo uso (Hero) va como pin + timeline autoplay en `onEnter`/`onEnterBack`, sin scrub.
  - Una secuencia de lectura va con `scrub` real (0.4) + snap a etiquetas: bidireccional. Nunca un disparo de un solo uso para contenido que se puede regresar.
- **ScrollTriggers:**
  - Un ScrollTrigger por timeline, siempre en el nivel superior.
  - Se crean de arriba hacia abajo.
  - Se pinea el contenedor y se animan sus hijos.
  - `scrub` y `toggleActions` nunca juntos.
- **Horizontal (`containerAnimation`):** `ease: "none"`, y el snap va en el trigger principal.
- **`gsap.matchMedia()`** con el corte de 860 px del espécimen y `prefers-reduced-motion`.
- **Movimiento reducido:** sin pin, flujo normal, fundidos cortos. Degradar, nunca cancelar. El prototipo de revisión trae un botón para verlo.
- **Visibilidad y accesibilidad:**
  - `autoAlpha` solo en capas decorativas. El texto de lectura usa `opacity` + `pointer-events`, para seguir en el árbol de accesibilidad.
  - SplitText por palabras, sin `text-wrap: balance`, con `autoSplit` + `onSplit`.
- **Refresh:** `ScrollTrigger.refresh()` después de `document.fonts.ready` y de cargar las imágenes.
- **Tipografía:**
  - Peso base 500, nunca 400.
  - Nunca gris en texto romano pequeño.
  - Playfair itálica necesita 700 o más para que el peso se note.
  - Sin numerales de capítulo ni doble numeración.
- **Fidelidad del copy:**
  - Nada de eyebrows ni subtítulos inventados.
  - Las viñetas van completas, nunca colapsadas en un párrafo.
  - Auditoría fuente → artefacto antes de cada gate.
- **Entorno:** el volumen externo `/Volumes/SACHI` no dispara file-watching de forma confiable. Para verificar, reinicia el servidor. Para medir en un navegador, haz scroll gradual y espera a `document.fonts.ready`.

## 7. Erratas de `VISION-NARRATIVA.md` (aplicar al leerla)

1. **Contradicción en los caps. 04 y 06.** §4 propone golpes («Tu instinto no está roto…», «El criterio se construye con preguntas…»), pero §1.1 y §5 dicen que esos capítulos no tienen golpe. **Manda §1.1/§5** (capítulos de respiro), salvo que el usuario diga otra cosa. Las dos frases van dentro de su párrafo, completas.
2. **Cita recortada en el cap. 04.** Lo literal es «Tu instinto no está roto. Te ayudó a resolver otros problemas. Éste necesita algo distinto.».
3. **Cap. 12.** «No inscribirlo también es una decisión. La diferencia es que ésa no tiene botón de cancelar.» son 2 de las 3 frases de un párrafo. La tercera va en el mismo encuadre.
4. **Cap. 09.** VISION escribe el enlace con punto final. En el copy es «Si ya viste suficiente, la inscripción está al final de esta página ↓» (con flecha, y enlazado a `#inscripcion`), seguido de otra línea: «Si no, sigue leyendo; falta lo más importante.».
5. **"Registro C" / puentes.** Se resuelven con las líneas lead del espécimen, no con un estilo nuevo.
6. **Tabla de imágenes (§1.1).** Usa los nombres del sitio de referencia. Equivalencias con `scenes/`:

   | VISION (sitio de referencia) | Archivo real en `scenes/` |
   |---|---|
   | 01-cena-absorto | `01-dinner.webp` |
   | 02-candados | Sin equivalente exacto. `02-facial-recognition.webp` muestra candado y reloj en pantalla (+ `-alt`). |
   | 08-fastidio-cejas | `03-eyes.webp` (+ `03-eyes-wide.webp`) |
   | 03-escudos-mama | `04-shield.webp` |
   | 04-calle-mama | `05-crossing.webp` (+ `-alt`) |
   | 05-reglas | `06-rules.webp` (+ `-alt`) |
   | 06-mesa | `07-together-mother-daughter.webp` / `07-together-father-son.webp` (una por escena) |
   | 07-cruzar-mochila | `08-autonomy-father.webp` / `08-autonomy-mother.webp` (una por escena) |

## 8. Qué se espera de ti ahora mismo

1. Confirma que leíste:
   - `AGENTS.md`;
   - el landing-builder y la adaptación de §5;
   - apple-design;
   - `Skills/gsap/ORIGEN.md`;
   - el espécimen completo: los estilos y las 17 composiciones, no solo los títulos.
2. Fase 0: pide el nombre de tu carpeta de proyecto, crea la estructura, copia los insumos a `00-context/` y confirma las respuestas del cuestionario.
3. Fase 1 con el espécimen como base, más la tabla medida de cabida. Detente en el gate.
4. **No hagas un wireframe de cajas.** La Fase 2 es el recorrido en grises de §5.
