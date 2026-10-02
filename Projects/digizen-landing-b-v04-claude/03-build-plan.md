---
project: digizen-landing-b-v04-claude
fase: 3 - build
documento: plan de componentes y archivos (paso 4 de phases/03-build.md: se aprueba ANTES de escribir el código)
estado: aprobado
fecha: 2026-09-29
aprobado: 2026-09-29 — «confirmados»: nombres del menú de recorrido (§4.5) y textos del formulario tomados de A (§4.6). Vertical única 2:3 con sufijo -v. Fuentes desde Google Fonts.
---

# Plan de construcción — Digizen Landing B v04

**Base:** `01-design-system.md` (aprobado 2026-09-26) y el wireframe de recorrido `02-wireframe.html` + `02-wireframe.md` (aprobado 2026-09-29).
**Criterio del usuario para esta fase:** refinar lo que está, sin cambios drásticos salvo que sea un error.
**Decisiones del usuario (2026-09-29):**
1. Prototipo en HTML + Tailwind + GSAP, y ese es el producto: no se lleva a Angular. HTML/CSS/JS bien construido, con buenas convenciones.
2. Formulario y datos: como en la propuesta A.
3. Menú de recorrido del lado derecho, con escalas, simplificado a lo más importante.
4. Unificar composiciones y anchos de columna.
5. Refinar los botones.

6. **No desviarse del wireframe (2026-09-29):** esta fase es de refinamiento. Se unifican constantes de diseño y estilos, y se desarrolla más la estética de las tarjetas y los botones. **No se modifican las estaciones, los scrubs ni la forma de scrollear.**

## 0. Qué queda congelado y qué se refina

**Congelado (igual que en el wireframe aprobado):**
- El orden, los pines, las paradas y su estacionamiento en E.
- Los kinds de cada parada y sus tiempos internos (entradas, pasos, puentes, salidas), el scrub (0.4), el snap a etiquetas, el carrusel horizontal que estaciona el 70 %, el mazo, las secuencias (incluida la del cruce al revés), el Hero de 3.7 s.
- La composición de cada parada, la gramática narrativa, las negritas y el copy literal.

**Se refina:**
- Constantes de diseño unificadas (tokens) y estilos consolidados, sin cambiar la ocupación de ninguna parada.
- Color (escenas, logos, roles de la paleta, bisagras oscuras con su acento).
- La estética de las tarjetas y de los botones.
- El menú de recorrido de la derecha (se agrega encima; no toca el scroll).

**Cómo se garantiza que no se desvíe:**
- El `index.html` se genera desde la **misma fuente** del wireframe (`wireframe-src/content.py`) con una plantilla de producción: mismas paradas, mismo HTML de cada composición, sin la regla, el HUD ni las notas.
- El motor de scroll es **el mismo código del wireframe** (buildPin, buildSeq, buildH, buildHero, mazo), extraído a módulos sin cambiar su lógica.
- Una verificación automática compara wireframe y producción: misma lista de paradas, mismos kinds, mismas E y los 151 fragmentos del copy en orden. Si algo difiere, el build falla.
- **Movimiento reducido** (para quien lo tenga activado): se comporta como el modo reducido del wireframe y §7 del sistema de diseño aprobado: sin pin, sin scrub y sin zoom; cada parada es un bloque en flujo normal que aparece con un fundido corto. Se degrada, no se cancela.

---

## 1. Stack y convenciones

- **HTML estático semántico**, sin framework. `index.html` se genera desde `wireframe-src/content.py` (§0) y se entrega como archivo estático; no hay nada que compilar en el navegador.
- **Tailwind CSS v4** con su CLI (`@tailwindcss/cli`, dependencia de desarrollo por npm). Los tokens del sistema de diseño van en `@theme`; las composiciones repetidas van en `@layer components` con nombres del sistema (`.b01`, `.l07`, `.card`, `.btn`…), para que el HTML no cargue cadenas de utilidades sueltas. Sale un solo `dist/styles.css` minificado.
- **GSAP 3 + ScrollTrigger + ScrollToPlugin**, copiados a `assets/vendor/` desde el paquete oficial de npm (sin CDN en producción).
- **JS en archivos por responsabilidad, como scripts clásicos con `defer`** y un espacio de nombres (`window.DZ`), sin bundler. Se descartaron los módulos ES al construir: el navegador los bloquea cuando la página se abre directo desde el disco, y así se puede revisar con doble clic.
- **Fuentes desde Google Fonts** (decisión del usuario, 2026-09-29): un solo `<link>` con `preconnect` y `display=swap`, pidiendo solo lo que se usa: Playfair Display 500, 700, 800 y 700 itálica, e Inter 500–800. Si más adelante hace falta exprimir la velocidad en móvil, se autoalojan esos mismos archivos sin cambiar nada más.
- **Sin dependencias en ejecución** fuera de GSAP.

## 2. Estructura de archivos (`output-code/`)

```
output-code/
  index.html                  ← generado desde wireframe-src/content.py con la plantilla de producción
  package.json                ← solo @tailwindcss/cli; scripts: build, watch, audit
  src/
    main.css                  ← @import "tailwindcss" + tokens + componentes
    tokens.css                ← @theme: paleta del logo y neutros, fuentes, escala de 8 pasos, anchos, espacios, radios
    components.css            ← composiciones del espécimen usadas (B01, B03, B06, B09, L03–L08), tarjeta, precio, botón, diálogo, FAQ, menú de recorrido
  dist/styles.css             ← generado (no se edita)
  js/
    dz-core.js                ← estado compartido, lectura del DOM, posiciones del recorrido, parada activa, saltos (data-goto)
    dz-seq.js                 ← secuencias en canvas (el buildSeq del wireframe) + cargador con anticipación y carga progresiva
    dz-pins.js                ← motor de pines: el buildPin del wireframe sin cambios (incluye el mazo apilado)
    dz-carousel.js            ← horizontal del cap. 02 (el buildH del wireframe)
    dz-hero.js                ← Hero (el buildHero del wireframe) + aviso al cargador al terminar
    dz-rail.js                ← menú de recorrido (derecha) + barra fina en móvil
    dz-actions.js             ← botones: diálogo de ADA con los datos de A, evento de pago, destinos pendientes, respuesta en pointerdown
    dz-main.js                ← arranque: modo completo (pines) o modo reducido del wireframe (flujo y fundidos)
  assets/
    vendor/                   ← gsap.min.js, ScrollTrigger.min.js, ScrollToPlugin.min.js
    scenes/  scenes/vertical/  seq/  avatars/  logo/
  scripts/
    build_html.py             ← plantilla de producción: content.py → index.html
    audit.py                  ← auditoría fuente → index.html (los 151 segmentos, literales y en orden, desktop y móvil; adiciones aprobadas aparte) + verificación de paradas, kinds y E contra el wireframe
```

**Marcado:** cada pin es una `<section class="pin">` con su `.stage` y sus `.stop` con `data-kind`, `data-e`, `data-bp` y `data-night`, escritos en el HTML (no en un JSON incrustado). La regla, el HUD y las notas del wireframe no pasan al producto.

## 3. Traducción de las fases anteriores

- **Tokens (Fase 1):** escala de 8 pasos en px fijos con corte a 860 (sin clamp); Playfair 500/700/800 e Inter 500–800 según el paso; paleta del logo con los roles y contrastes medidos (azul-900 = inscripción y enlaces, violeta = ADA, coral solo ≥ 24 px y nunca en botones, ámbar = valor); radios 0 en lo que se lee, 16 px en botones y 999 px en indicadores; aire 32/48 entre golpe y párrafo.
- **Wireframe (Fase 2):** el mismo orden, las mismas paradas y E, los mismos kinds (read, lead, golpe, two, reveal, seal, seq, dialog, deck, hero), la misma gramática narrativa (`02-gramatica-narrativa.md`) y las mismas notas de intención de interacción.
- **Movimiento (`Skills/apple-design/SKILL.md`):** el del wireframe, tal cual. Lo que se toca (botones, menú, FAQ, diálogo) responde en `pointerdown` y es interrumpible, con springs de amortiguación crítica; solo transform y opacidad; con «reducir movimiento», el modo reducido del wireframe (flujo normal y fundidos).
- **Color:** entra aquí. Las escenas y los logos pasan a color; las bisagras oscuras (01.3, 03.5, 05.7, 10.5, 12.7) con su acento.

## 4. Lo nuevo que pediste

### 4.1 Unificar anchos de columna (propuesta)

Hoy conviven 17 anchos. Propongo **tres anchos de contenido y dos medidas para texto grande**, como tokens. Solo se juntan valores que ya son casi iguales: ninguna parada cambia de composición y se vuelve a medir la ocupación de todas (ninguna debe pasar de su límite):

| Token | Valor | Reemplaza a | Se usa en |
|---|---|---|---|
| `--w-read` | 27rem (~38 caracteres) | 27rem, 32ch, 34ch | lectura corta (L07 y L06 con párrafos < 230 caracteres), párrafo debajo de un golpe, puentes, texto de ADA, CTA de 12.4 |
| `--w-wide` | 42rem (~60 caracteres) | 42rem, 44ch, 52ch, 64ch, 560px, 720px, 760px | lectura larga, 09.2, 11.4 con el precio, 11.6, lista L03, diálogo, FAQ |
| `--w-grid` | 1180px, 12 columnas | 1180px | tarjetas, citas-eco del cap. 02, presentación de ADA, Hero, footer (la evolución 07.6 conserva sus 1040 px: es su composición) |
| `--m-display` | 18ch | 18ch, 24ch | golpes en semimonumental y monumental |
| `--m-head` | 22ch | 22ch | títulos en heading |

Siguen los dos ejes: el centro y el borde izquierdo de la columna de lectura.

### 4.2 Unificar composiciones (propuesta)

- **Una tarjeta** (`.card`): la misma en 08.5 y 11.3; en fila en desktop, una debajo de otra en tablet y en mazo en móvil.
- **Un bloque de precio**: el mismo dentro de la lectura (11.4) y como parada propia en móvil (11.5m).
- **Un par de CTA** (`.cta`) que siempre toma el ancho de la columna de su lámina (11.6 y 12.4).
- **Una voz citada**: 10.3 y las citas-eco del cap. 02 con el mismo estilo (Playfair 700 itálica en semimonumental).
- **Una voz de puente**: el puente solo y la entrada de B03 con el mismo estilo y la misma medida.

### 4.3 Tarjetas (desarrollar la estética)

- Misma familia que los botones: superficie clara, borde fino, esquinas redondeadas (propuesta: 16 px, como los botones; hoy el sistema dice 0 en lo que se lee, así que lo confirmas en la prueba).
- Jerarquía interna: título en subhead Playfair, párrafo en body, botón secundario al pie cuando lo hay; aire interno de 24 px (16 px en móvil).
- Un detalle de marca discreto por rol (propuesta: una línea o punto en el color del tramo), sin sombras ni degradados.
- El mazo apilado de móvil conserva su comportamiento; solo cambia la piel.

### 4.4 Botones (refinar)

Parto de la fila de acción aprobada y la llevo a color:
- «Inscribir a mi hijo ↗» en azul-900 y «Conversar con ADA primero» en violeta, texto blanco (contraste 9.11 y 6.77); el círculo de la flecha en blanco al 16 %.
- Secundarios en superficie clara con borde fino, y la flecha en el color de su rol (azul o violeta).
- Estados: al pasar el cursor sube 2 px y la flecha avanza hacia donde lleva; `pointerdown` a 0.98 al instante (spring crítico); foco con anillo de 2 px; con «reducir movimiento», 1 px y sin mover la flecha.
- Los reviso en la estación de prueba (§6) antes de repetirlos en toda la página.

### 4.5 Menú de recorrido (derecha), simplificado

- Se agrega encima del recorrido y no cambia el scroll. Un riel vertical fino a la derecha, que aparece al terminar el Hero: una línea que se llena con el avance y **7 puntos**, uno por tramo principal (no las 100 paradas).
- Al pasar el cursor o enfocar un punto se ve su nombre; con clic o Enter salta al inicio del tramo (interrumpible si el usuario hace scroll).
- En móvil y tablet: solo una barra fina de progreso arriba, sin puntos.
- `<nav aria-label>`, botones con nombre accesible, y el tramo actual con `aria-current`.

**Nombres de los tramos: copy NUEVO, para que lo apruebes o lo cambies** (propuesta, lo más breve posible):

| # | Capítulos | Propuesta |
|---|---|---|
| 1 | 01–02 | Lo que creemos |
| 2 | 03–04 | Por qué no escucha |
| 3 | 05–06 | El cómo |
| 4 | 07–08 | ADA |
| 5 | 09–10 | Tú |
| 6 | 11 | Inscripción |
| 7 | 12 | Tu decisión |

**Vigente (2026-09-30), opción A «qué vas a encontrar», elegida por el usuario** (el menú debe tener una lógica clara y enfocarse en la experiencia de usuario): cada nombre dice qué hay en la sección, en el orden de la historia; las acciones se quedan como botones.

| # | Capítulos | Nombre |
|---|---|---|
| 1 | 01–02 | Lo que casi todos creemos |
| 2 | 03–04 | Por qué no te escucha |
| 3 | 05–06 | Lo que sí funciona |
| 4 | 07–09 | Qué es ADA (incluye probarla, para no repetir el botón «Conversar con ADA primero») |
| 5 | 10 | Tu papel |
| 6 | 11 | Precio e inscripción |
| 7 | 12 | Antes de decidir |
| — | página aparte | Reglas de ADA (agregada el 2026-10-02, pedido del usuario; abre `reglas-de-ada.html` en una pestaña nueva) |
| — | FAQ | Preguntas frecuentes (antes «Por si te quedó una duda.») |

### 4.6 Formulario y datos (como en la propuesta A)

- «Conversar con ADA primero» abre un `<dialog>` con los mismos datos que A: **Nombre del papá o mamá**, **Canal de entrega** (Correo / WhatsApp) y **Correo electrónico** o **Número de WhatsApp**, según el canal; botón de envío y la nota «Se manda la liga de acceso; no abre WhatsApp directo.».
- Esos textos vienen de A, no de `COPY-PUBLICADO.md`: entran como adiciones aprobadas por ti y la auditoría los lista aparte.
- Como en A, el formulario todavía no envía a ningún servicio; «Inscribir a mi hijo ↗» emite el evento `digizen:checkout` para conectar el pago después. Los dos destinos quedan marcados como pendientes.
- El texto de A «Formulario de datos del adulto.» era una nota de maqueta: propongo no mostrarlo.

## 5. Rendimiento y accesibilidad

### 5.1 Precarga: que nada llegue tarde (pedido del usuario, 2026-09-29)

**Qué pesa hoy (medido):**

| Recurso | Peso | Dónde se usa |
|---|---|---|
| Hero `01-dinner.webp` (2560×1440) | **2.1 MB** | primera pantalla: es lo primero que se carga, hay que bajarlo |
| Secuencia 05-crossing (49 cuadros) | 4.7 MB | 05.5, solo desktop |
| Secuencia ada-wave (130 cuadros) | 4.5 MB | 07.1, solo desktop (móvil: cuadro fijo) |
| Secuencia 03-fastidio (49 cuadros) | 3.1 MB | 03.4, solo desktop |
| Otras 6 escenas | 0.17–0.5 MB cada una | sellos |

Total aproximado: ~16 MB en desktop y ~3 MB en móvil (en móvil no hay secuencias).

**Estrategia:**
1. **Primera pantalla ligera.** El Hero se recomprime (misma imagen, meta ≤ 500 KB) y se sirve con `srcset` en tres anchos (1280 / 1920 / 2560) más la vertical en móvil; `preload` con `fetchpriority="high"`. Las fuentes con `preconnect`. Nada más compite con el Hero.
2. **Cargador propio con anticipación, no `loading="lazy"` del navegador.** Los pines alargan la página con espaciadores y el `lazy` nativo dispara tarde. Cada pin declara sus recursos, y el cargador los pide cuando el lector está **a unos 2 pines (≈ 6–8 E) de llegar**, con una cola por prioridad: el pin actual primero, luego el siguiente, luego los demás. Máximo ~6 descargas a la vez para no ahogar la conexión.
3. **Secuencias progresivas.** Primero se bajan los cuadros clave (1 de cada 4) y el scrub ya funciona con ellos; después se rellenan los intermedios. Mientras falta un cuadro se dibuja el más cercano ya cargado (hoy busca solo hacia atrás). Los cuadros se decodifican antes de dibujarlos (`decode()` / `createImageBitmap`) para que el scrub no dé tirones.
4. **Precarga en reposo.** Cuando termina el Hero y el navegador está desocupado (`requestIdleCallback`), se adelantan en segundo plano las secuencias de desktop, en orden de aparición.
5. **Respeto a la conexión.** Con «ahorro de datos» o conexión lenta (`navigator.connection`), las secuencias no se descargan: se muestra su cuadro fijo, como en móvil. El recorrido y los tiempos no cambian.
6. **Nada de lo que no se ve.** Las paradas de otro tamaño de pantalla (solo desktop / solo móvil) no descargan sus imágenes.
7. **Tamaños por pantalla.** Las escenas con `srcset` (y la vertical en móvil cuando exista), para que un teléfono no baje imágenes de 2560 px.
8. **Caché.** Nombres de archivo estables y encabezados de caché largos en el hosting (se documenta en `03-build-notes.md`).

**Cómo se comprueba:** con la conexión limitada del navegador (4G y 3G rápida) se recorre la página completa y se verifica que cada secuencia y cada escena estén listas antes de su parada. Esto se hace en el navegador, así que te pediré permiso para abrirlo.

### 5.2 Escenas verticales para móvil y tablet (las hace el usuario)

- **Especificación:** la de `00-context/scenes/vertical/LEEME.md` (2:3, 1200 × 1800 px, un solo archivo para teléfono y tablet, zona segura en el rectángulo central de 80 % × 80 %, sin texto ni viñeta), con la lista de las 8 escenas y qué debe quedar en cuadro en cada una.
- **Cómo entran:** basta con dejar `<nombre>-v.webp` en `00-context/scenes/vertical/`. El build la detecta sola y la sirve con `<picture>` por debajo de 860 px, en el wireframe y en la página final; mientras falte, se usa la horizontal y el build avisa cuál falta. No hay que tocar código.
- **Optimización:** de cada vertical se generan dos anchos (1200 y 800 px) para `srcset`, así un teléfono baja la de 800. La vertical del Hero (`01-dinner-v.webp`) entra en la precarga prioritaria de móvil, con la misma meta de peso que la del Hero de desktop.
- **Donde el desktop tiene una secuencia** (03.4, 05.5), la vertical es la imagen fija de móvil y tablet.
- **Cómo se encuadra** (decisión del usuario, 2026-09-29: una proporción para los dos en un mismo archivo): 2:3, que llena la pantalla en teléfono y en tablet; el recorte (~6 % por lado en teléfono, 5–9 % arriba y abajo en tablet) solo toca el margen fuera de la zona segura.

### 5.3 Accesibilidad y otros

- Canvas con DPR ≤ 2; en móvil, cuadro fijo donde el wireframe lo definió.
- Semántica: `lang="es-MX"`, un `<h1>` (Hero), `<h2>` por capítulo, `<details>` en el FAQ, `<dialog>` nativo con foco atrapado, etiquetas en todos los campos, `aria-pressed` en el selector de canal.
- Contraste según las mediciones de la Fase 1; foco visible en todo lo que se toca.

## 6. Orden de construcción

1. **Estación de prueba (primero):** Hero + capítulo 01 completo (incluida la bisagra oscura 01.3) + las tarjetas de 08.5 + la lámina 11.6 (garantía y botones) + el menú de recorrido. En color, con el scroll del wireframe tal cual. **Se revisa contigo antes de seguir.**
2. Tokens y componentes definitivos con lo que salga de la prueba.
3. La página completa: se genera toda desde la misma fuente, con los estilos aprobados.
4. Auditoría del copy, verificación en desktop, tablet y móvil, y modo reducido.
5. Rúbrica de la fase (Purista 20 %, Arquitecto 40 %, Lectura 40 %) y `03-build-notes.md`.

## 7. Pendientes que no bloquean

- Las 8 escenas verticales (mientras tanto, la horizontal completa).
- Escenas en 16:8.6 para que las bandas sean mínimas.
- Destino del pago, del formulario y de «Conocer las reglas de ADA ↗».
- Zoom de 12.6 (hoy: 106 % → 100 %).
- Metadatos (título, descripción, imagen para redes): propongo reusar los de A; es texto de A, lo confirmo contigo.
