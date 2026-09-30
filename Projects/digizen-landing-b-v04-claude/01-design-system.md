---
project: digizen-landing-b-v04-claude
fase: 1 - sistema de diseño
estado: aprobado
revision: 2 — base Tipografía esencial
aprobado: 2026-09-26 — con las decisiones por defecto de §8
---

# Sistema de diseño — Digizen Landing B v04

## 0. Qué es esta revisión

La base del sistema es **`00-context/Tipografía esencial.html`**: su escala de 8 pasos, sus dos encuadres (16:8.6 y 9:15.3), su retícula de 12 columnas, sus reglas de composición y sus 17 composiciones (B01–B09, L01–L08). En la revisión 1 lo había tratado solo como vocabulario, lo sustituí por una escala propia y eso fue un error.

- **Se mantiene del espécimen, tal cual:** familias, escala, breakpoint de 860 px sin `clamp()`, encuadres, retícula, reglas de composición, las 17 composiciones y los neutros.
- **Se agrega**, porque el espécimen no lo cubre:
  - el estacionamiento del scroll por encuadre (§1);
  - los roles de la paleta del logo, que es una restricción fija (§4);
  - los componentes de interfaz: CTA, diálogo, precio, FAQ (§5);
  - las reglas de GSAP (§7).
- **Se ajusta solo donde lo pide una regla tuya** (las lecciones v2 del metaprompt), y cada ajuste está en §8 para que lo confirmes. Todo lo demás que yo cambiaría también está en §8 como opción, **nunca aplicado por defecto**.

---

## 1. El encuadre: la unidad del sistema

### 1.1 Los dos encuadres del espécimen son el viewport real

| Encuadre | Proporción | Viewport de referencia | Qué es |
|---|---|---|---|
| Desktop | 16 : 8.6 | 1440 × 774 | Laptop de 1440 × 900 menos la barra del navegador. |
| Móvil · Tablet | 9 : 15.3 | 390 × 663 | iPhone de 390 × 844 con la interfaz de Safari visible = `100svh`. |

Encuadres cercanos con la misma proporción (medidos):
- **Desktop:** 1280 × 688 · 1440 × 774 · 1536 × 826.
- **Móvil:** 360 × 612 · 375 × 638 · 390 × 663 · 430 × 731.

El breakpoint de 860 px del espécimen reparte así: **por debajo de 860** (teléfonos y tablets en vertical) → encuadre y escala móvil; **desde 860** → encuadre y escala desktop.

**Implementación:** el escenario de cada parada mide `100svh`. Es justo el alto del encuadre, porque el espécimen ya descuenta la barra del navegador, y no salta cuando esa barra se esconde.

### 1.2 El escenario
- **Escenario = encuadre − padding del espécimen:** 24 px en desktop; 28 px arriba y abajo × 24 px a los lados en móvil. En tablet (600–859 px), márgenes más generosos: 36 px arriba y abajo × 48 px a los lados (pedido del usuario, 2026-09-29).
- Contenedor máximo de 1180 px (el `.wrap` del espécimen).
- Nada persistente le quita alto al escenario (ver §8, decisión 6).

### 1.3 Regla madre: una parada = un encuadre
Toda parada de scroll es una composición que **cabe completa en su encuadre**, en desktop y en móvil, sin scroll interno, con el espacio negativo generoso y el centrado vertical casi siempre que pide el espécimen.

### 1.4 Capacidad medida
Medí con Inter 500 instalada y 38 párrafos reales del copy, con el leading 1.5 del espécimen:

| Escenario | Cuerpo | Palabras por línea | Líneas | Palabras al 100 % | **Al 70 %** |
|---|---:|---:|---:|---:|---:|
| Móvil 360 × 612 (conservador) | 16 px | 6.7 | 23 | ~153 | **~107** |
| Móvil 390 × 663 | 16 px | 7.3 | 25 | ~183 | ~128 |
| Desktop 1440 × 774 (medida de 64 caracteres) | 18 px | 11.8 | 26 | ~307 | ~215 |

**Reglas que salen de la tabla** (manda el móvil de 360):
- Una parada de lectura lleva **como máximo ~100 palabras**.
- Un párrafo del copy **nunca se parte** entre dos paradas.
- Si un bloque del copy pasa de ~100 palabras, se reparte en paradas consecutivas, cortando entre párrafos. Las palabras no se tocan.

### 1.5 Tamaño de un golpe = el paso más grande que cabe en el encuadre
Medí cada candidato a golpe del copy con Playfair 800 instalada, en el móvil conservador (312 × 556 útiles) y en desktop. Es medición de capacidad, **no asignación**: cuál es golpe y dónde va se decide en la Fase 2.

| Golpe (literal) | móvil xl 64 | móvil mon 48 | móvil semi 34 | desktop mon 96 |
|---|---:|---:|---:|---:|
| Cuatro son falsas. | 2 líneas | 2 | 1 | 1 |
| La cinco. No te escucha. | 3 | 2 | 2 | 2 |
| Pero no por lo que crees. Y ahí es donde se pone interesante. | 7 | 6 | **4** | 4 |
| Lo que casi todos creemos | 3 | 3 | 2 | 2 |
| Los ojos al techo. En señal de fastidio. | 4 | 4 | 3 | 3 |
| Alguien les dijo «no», y nadie les dijo «cómo». | 6 | **4** | 3 | 3 |
| Bloquearle el celular es «no cruces». | 4 | 3 | 3 | 3 |
| El control caduca. El criterio no. | 4 | 3 | 2 | 2 |
| Una pausa. Una consecuencia. Una idea propia. | 6 | 5 | 3 | 3 |
| «Espera. ¿Una IA hablando con mi hijo?» | 5 | 4 | 3 | 3 |
| 7 de cada 10 | 2 | 1 | 1 | 1 |
| Lo más importante no es ADA. | 4 | 3 | 2 | 2 |
| Eres tú. | 1 | 1 | 1 | 1 |
| «Mi mamá se ríe más cuando ve el celular que cuando está conmigo.» | 9 | 6 | **4** | 4 |
| Una última cosa, y ya te dejo. | 4 | 3 | 2 | 2 |
| Ya lo tienes. | 2 | 1 | 1 | 1 |
| No inscribirlo también es una decisión. La diferencia es que ésa no tiene botón de cancelar. | 11 | 8 | **6** | 6 |
| Presencia, no vigilancia. Criterio, no candado. | 6 | 4 | 3 | 3 |

**Regla:** un golpe usa el paso más grande del grupo B (`monumental-xl` → `monumental` → `semimonumental`) en el que, en el móvil de 360, **quepa en 5 líneas o menos y ocupe como máximo el 60 % del alto útil**. En la práctica:
- `monumental-xl` queda para 1–2 líneas.
- `monumental` para la mayoría.
- `semimonumental` para los golpes largos.

La escala del espécimen resuelve todos los golpes del copy sin ajustes.

**Varios golpes en un capítulo:** hay un solo lapidario por capítulo. Los demás bajan un paso, y el lapidario es el único que puede llevar acento de color o escenario oscuro.

### 1.6 Estacionamiento del scroll (cuánto se queda estacionada cada parada)
**Unidad E = un encuadre de scroll = `100svh`.** Como es relativa al encuadre, vale igual en desktop y en móvil.

| Tipo de parada | Composiciones | Estacionamiento | Timeline interna (proporción de la parada) |
|---|---|---:|---|
| Golpe | B01, B02, B06, B07, B09 | **1.25 E** | Entra por corte en 0–10 % · se sostiene hasta 85 % · sale en 85–100 %. |
| Puente + golpe (dos tiempos) | B03, B04, B05, B08 | **1.5 E** | Lead en 0–15 % · golpe por corte en 30–40 % · se sostiene hasta 85 % · sale. |
| Lectura | L01–L08 y cuerpo | **1 E** | Entra en 0–15 % · se sostiene · sale en 85–100 %. |
| Sello (escena) | — | **1 E** | Escala de 1.06 a 1 durante toda la parada. |
| Panel horizontal (cap. 02) | — | **1 E por panel** | Desplazamiento con `ease: "none"` y snap por panel. |
| Hero | — | **1.5 E** de pin | Secuencia autoplay, sin scrub (§7). |

- **Pin de un capítulo:** `end: () => "+=" + (ΣE × innerHeight)`. Se calcula en una función para que se recalcule en cada refresh. En la Fase 2, cada capítulo lleva su suma de E.
- **Snap:** una etiqueta por parada, a la mitad de su tramo sostenido (`snap: "labels"`).
- **Máximo 6 paradas por pin.** Si un capítulo necesita más, se parte en pines consecutivos (en v2, los pines largos fueron frágiles).
- **Valores iniciales:** se calibran en el prototipo de la Fase 3.

---

## 2. Tipografía (del espécimen)

### 2.1 Familias

> **Todo en sans (decisión del usuario, 2026-09-29):** Inter reemplaza a Playfair Display en golpes (semimonumental, monumental, monumental-xl), títulos, subtítulos y citas. Se conservan la escala, los pesos y el color de cada composición. Espaciado por tamaño (apple-design §9): subhead −0.01em, heading −0.015em / 1.12, semimonumental −0.03em / 1.04, monumental −0.04em / 1.02, monumental-xl −0.045em / 0.96. Las itálicas (acentos, voz citada) usan Inter itálica. El estado anterior, en Playfair, está en el commit a514245. Lo que sigue en esta sección describe el sistema original.

- **Display:** Playfair Display (400–900, roman + itálica). Todos los títulos (`h1`–`h4`) y el grupo B.
- **Cuerpo:** Inter (100–900). Lectura, etiquetas e interfaz.

Carga: `font-display: swap` y, después de `document.fonts.ready`, `ScrollTrigger.refresh()`.

### 2.2 Escala funcional: 8 pasos, sin excepciones
Es la escala del espécimen tal cual: un valor fijo en desktop y uno más chico por debajo de 860 px, **sin `clamp()` ni multiplicadores**. Se escribe en `rem` (mismos valores: 16 px = 1rem) para respetar el tamaño de texto que elija el usuario (apple-design §10).

| Paso | Desktop | Móvil · Tablet | Leading | Tracking | Uso en el espécimen |
|---|---:|---:|---:|---:|---|
| `micro` | 12 px | 11 px | 1.3 | +0.04em | Etiqueta |
| `small` | 14 px | 13 px | 1.5 | 0 | Texto de apoyo, captions |
| `body` (ancla) | 18 px | 16 px | 1.5 | 0 | Párrafo |
| `subhead` | 24 px | 19 px | 1.3 | 0 | Subtítulo, línea lead |
| `heading` | 32 px | 24 px | 1.1 | 0 | Título de sección |
| `semimonumental` | 56 px | 34 px | 1.02 | −0.01em | Componente, golpe largo |
| `monumental` | 96 px | 48 px | 1.02 | −0.01em | Display, golpe |
| `monumental-xl` | 144 px | 64 px | 0.95 | −0.02em | Palabra sola |

- Salen del espécimen: tamaños, `body` 1.5, `monumental` 1.02, `monumental-xl` 0.95 / −0.02em, `.tight` −0.01em y el +0.04em de las etiquetas.
- Completé los huecos siguiendo apple-design §9: a más tamaño, leading más apretado y tracking más negativo.

### 2.3 Reglas de composición (del espécimen, adoptadas como reglas del sistema)
1. **Como máximo dos pasos de tamaño por pieza.** La jerarquía la hacen el peso y el tamaño, nunca una cascada de 3 o 4 tamaños.
2. **Un solo acento de color por pieza.**
3. **Espacio negativo generoso; centrado vertical casi siempre.**
4. **Toda asimetría** (palabra/definición, dato/etiqueta, 2/3–1/3) se resuelve con `grid-column: span N` sobre la retícula de 12. Nunca con porcentajes de `flex-basis`.

### 2.4 Voces: los registros de VISION, mapeados al espécimen
- **Registro B (golpe)** = grupo B (B01–B09).
- **Puente semibrutalista** = la **línea lead** de las composiciones semibrutalistas del espécimen: B03 (Inter 500, `subhead`), B04 (Inter 300, `subhead`), B05 (Playfair 600, `heading`) y B08 (Inter 100, `subhead`).
  - El espécimen ya resuelve "puente → golpe" dentro de un mismo encuadre.
  - Un puente que va solo usa la misma línea lead en su propia parada.
  - *Retiro el "Registro C" en itálica que inventé en la revisión 1.*
- **Registro A (conversa)** = grupo L (L01–L08) y el cuerpo.

Respuestas a VISION §5:

| Pregunta | Decisión |
|---|---|
| ¿Tercer tratamiento para puentes? | La línea lead semibrutalista del espécimen (arriba). |
| ¿El copy de venta del cap. 11 entra en B? | No: va en un componente L (título Playfair 700 `heading` o lead). El grupo B queda para golpes emocionales o reflexivos. El dato «7 de cada 10» sí entra en B, como confirmaste. |
| ¿Capítulo sin golpe? | Solo composiciones L. Sin acento de color, sin escenario oscuro y sin imagen. El silencio se marca por ausencia. |
| ¿Varios golpes, mismo peso? | No: un lapidario por capítulo, los demás un paso abajo (§1.5). |

### 2.5 Microtipografía
- `text-wrap: balance` en títulos y grupo B, como en el espécimen. **Excepción:** lo que se divide con SplitText no lleva `balance` (§7).
- `text-wrap: pretty` en el cuerpo.
- `hyphens: none` siempre.
- Espacios de no separación para que «, ¿ y ¡ se queden pegados a la palabra que abren, y » a la que cierra, y para que la raya nunca termine una línea (`—&nbsp;`).
- No se aplica `text-transform`: se respetan las mayúsculas del copy. El `lowercase` de las etiquetas del espécimen no se usa, porque esas etiquetas no están en el copy.

---

## 3. Catálogo de composiciones (las 17 del espécimen)

Cada una es un tipo de parada. La estructura es la del espécimen. La columna "Sirve para" dice qué forma de copy acomoda; la Fase 2 asigna el copy literal.

**Grupo B — brutalistas / semibrutalistas**

| ID | Estructura (pasos del espécimen) | Sirve para | E |
|---|---|---|---:|
| B01 | Display Playfair 800 `monumental` + caption Inter `body`; acento en itálica | Golpe + una línea de remate | 1.25 |
| B02 | Palabra Playfair 700 `monumental` −0.01em + caption `micro` en acento | Golpe de una palabra | 1.25 |
| B03 | Lead Inter 500 `subhead` → cierre Playfair 800 `monumental` con acento en itálica | Puente + golpe | 1.5 |
| B04 | Lead Inter 300 `subhead` → cierre Playfair 800 `monumental`, todo el cierre en acento | Puente suave + golpe | 1.5 |
| B05 | Lead Playfair 600 `heading` en línea con Playfair 800 `monumental` + punto de acento | Puente y golpe en una sola frase | 1.5 |
| B06 | Dos líneas Playfair 800 `monumental`, la segunda en acento itálico | Golpe de dos tiempos cortos | 1.25 |
| B07 | Palabra Playfair 900 `monumental-xl` + caption Inter `small` | Golpe de 1–2 palabras | 1.25 |
| B08 | Inter 100 `subhead` / Inter 900 `heading` | Par de aforismos con contraste de peso | 1.5 |
| B09 | Numeral Playfair 800 `monumental-xl` + caption itálica `small` | Dato con número | 1.25 |

**Grupo L — componentes de layout**

| ID | Estructura (pasos del espécimen) | Sirve para | E |
|---|---|---|---:|
| L01 | Cifra Playfair 700 `semimonumental` en acento (4 col) + etiqueta Inter 700 `body` (8 col) + apoyo `small` (12 col) | Dato + contexto | 1 |
| L02 | Dos columnas de 6 con línea Playfair `heading` (400 / 800 en acento) | Dos voces o contraste lado a lado | 1 |
| L03 | Filas: numeral Playfair 800 `heading` + texto Inter 700 `body` + apoyo `small`; **la última fila en acento** | La lista 01–05 del copy (la última fila en acento coincide con «La cinco.») | 1 |
| L04 | Cita Playfair itálica 400 `subhead` centrada (col 3–10) + fuente `micro` | Citas del copy | 1 |
| L05 | Palabra Playfair 700 `semimonumental` (5 col) + definición en itálica `body` / `small` (7 col) | Concepto + explicación | 1 |
| L06 | Título Playfair 700 `heading` + apoyo Inter `body` (34ch) | Apertura de capítulo | 1 |
| L07 | Columna de ensayo Inter `body`, leading 1.6, 38ch | Párrafos de lectura | 1 |
| L08 | Encabezado Playfair 700 `heading` (8 col) + descripción itálica + entradas en retícula (3 col c/u; 1 col en móvil) | Listas de elementos paralelos (inscripción, reglas, pago) | 1 |

**Notas del catálogo:**
- Los textos de ejemplo del espécimen que no están en el copy («Basta.», «Sin miedo.», «días de garantía, sin preguntas», «El reframe», etc.) se toman solo como patrón, nunca con su texto.
- En L06, L07 y L08 hay índices y etiquetas que no están en el copy: el número fantasma y el «sección 05» de L06, el «§1» de L07, y el badge y las etiquetas «01 · span 3» de L08. Ver §8, decisión 3.
- Puede que B02 o L05 no encuentren copy que les corresponda. Si en la Fase 2 no se usan, se retiran del catálogo de esta landing.

---

## 4. Color

### 4.1 Neutros (del espécimen)

| Token | Claro | Oscuro (espécimen) | Rol | Contraste |
|---|---|---|---|---|
| `bg` | `#F4F3F0` | `#100F0D` | Fondo | — |
| `panel` | `#FFFFFF` | `#1A1815` | Superficie: opciones de precio, fila de FAQ abierta | — |
| `panel-2` | `#FBFAF8` | `#1F1C18` | Superficie secundaria | — |
| `ink` | `#14120F` | `#F1EDE6` | Texto | 16.85 claro · 16.42 oscuro |
| `muted` | `#6D675F` | `#9D968C` | Texto secundario, con la restricción de §8 decisión 2 | 5.04 · 6.55 |
| `line` | `#DFDAD2` | `#322E28` | Reglas decorativas | 1.25 |
| `line-strong` | `#807E7B` | — | Bordes de controles de formulario (agregado) | 3.65 |

### 4.2 Acento: la paleta del logo (restricción fija)

> **Lógica de color (decisión del usuario, 2026-09-29; sustituye a la decisión 5 de §8):** la paleta sigue la psicología de color de `00-context/digizen-ada-proposal-v05-mision-clara-2026-08-25.html` («Misión Clara», el origen del sistema), con los colores exactos del logo:
> - **Coral = energía humana y conversación** (atención, dilema, calidez; microalerta no punitiva, nunca alarma): la voz citada en tamaños ≥ 24 px (creencias del cap. 02, objeción de 08.1, pregunta de 10.3) y los acentos del problema («falsas», «escucha»). La burbuja del hijo en `coral-tinte` `#F8E1DD`.
> - **Azul = estructura** (orden, progreso, tecnología): acentos del método y la salida («cómo», «El criterio no.», «Criterio, no candado.»), menú de recorrido, enlaces, «Inscribir a mi hijo ↗», foco.
> - **Cian = ADA** (presencia, guía): «Conversar con ADA primero», tarjetas de sus reglas, su burbuja y el formulario; siempre como relleno o tinte con texto `ink`.
> - **Violeta = profundidad / IA**, con moderación: el dato «7 de cada 10».
> - **Navy `#111A34` = confianza**: el escenario de las bisagras (sustituye al negro cálido `#100F0D`). Es el único color que no viene del logo: lo aporta V05.
> - **Ámbar = valor**: piezas de precio y marcador de valor (como relleno, porque no alcanza contraste como texto). En texto, el logro va en coral.
> - **Conceptos fuertes resaltados solo con color** (pedido del usuario, 2026-09-29): además del acento en itálica de los lapidarios, un concepto fuerte puede llevar color sin cambiar su tipografía, según su función: coral para el problema y la prohibición («no me escucha», «no cruces», «Ya está pasando.», «ésa no tiene botón de cancelar.», el «no» de 03.5), azul para el método y el vínculo («lo que le hayas enseñado antes.», «El criterio» y «puente que te lo regresa.» en 10.4), azul también para lo positivo y el logro («Eres tú.» y «Ya lo tienes.», que riman; la pregunta de 10.3) y violeta para ADA escrita (toda la frase «Habla tú con ADA primero.»; el cian de ADA no se lee como texto y V05 reserva el violeta para la IA). **Coral solo para lo que alerta o es negativo** (aclaración del usuario, 2026-09-29): el problema, la prohibición, las creencias falsas, la urgencia. **Siempre color en la tipografía, nunca bandas ni subrayados de color** (pedido del usuario). En la evolución de 07.6, el antes («lo que veo en redes me dice quién soy») en coral y el después («yo decido qué me sirve y qué quiero compartir») en azul. «idea propia.» (07.5) va en azul, el color del criterio. En el cuerpo de lectura no se colorea: ahí el énfasis sigue siendo la negrita.
> - Sigue valiendo **un solo acento por pieza**, con una excepción pedida por el usuario: en 03.5 «Alguien les dijo «no», y nadie les dijo «cómo».» la antítesis va en dos colores, «no» en coral (la prohibición) y «cómo» en azul (el método). 10.5, la cita del niño, va en coral (pedido del usuario, 2026-09-29; antes sin acento).
El espécimen usa un solo acento, `#2F4DFF`. La restricción fija lo sustituye por la paleta del logo. El acento por defecto es **`azul-900` #2C1DDB**: el más cercano a `#2F4DFF` en tono y rol, y con más contraste (8.21 contra 5.22). Los otros colores tienen un rol funcional; la regla del espécimen ("un solo acento por pieza") sigue gobernando.

| Token | Valor | Rol | Texto sobre `bg` | Texto sobre oscuro | Relleno con texto |
|---|---|---|---:|---:|---:|
| `azul-900` | `#2C1DDB` | **Acento por defecto:** Digizen, enlaces, CTA «Inscribir a mi hijo ↗», foco | 8.21 AA | 2.10 ✗ | blanco 9.11 |
| `azul-500` | `#1A75EA` | Acento **sobre fondo oscuro** (solo ≥ 24 px) | 3.96 | 4.36 | — |
| `violeta` | `#7B27D6` | **ADA:** CTA «Conversar con ADA primero», voz de ADA, «Conocer las reglas de ADA ↗» | 6.10 AA | 2.83 ✗ | blanco 6.77 |
| `coral` | `#E65C4D` | **Tensión:** solo ≥ 24 px; nunca en botones | 3.15 | 5.48 | — |
| `ambar` | `#EF9600` | **Valor:** fundador, ahorro, garantía; solo relleno con `ink` | 2.10 ✗ | 8.24 | `ink` 8.04 |
| `cian` | `#00C4F0` | **El hijo:** voz de HIJO; solo relleno/tinte con `ink` | 1.86 ✗ | 9.26 | `ink` 9.04 |

- **Degradado del logo** (`#1A75EA → #2C1DDB`): solo en gráficos, nunca detrás de texto.
- **Tintes sobre `bg`:**
  - `violeta-tinte` `#E8DFED`: burbuja de ADA; `ink` 14.43, etiqueta violeta 5.22.
  - `cian-tinte` `#CDEBF0`: burbuja de HIJO; `ink` 14.90.
  - `ambar-tinte` `#F3E0C0`: marcador de valor; `ink` 14.45.

### 4.3 Materiales, radios, sombras
- Todo opaco, sin blur (apple-design §8).
- Sin sombras.
- **Radios:**
  - **0** en lo que se lee (escenas, piezas, bloques).
  - **16 px** en los botones (filas de acción; criterio del usuario, 2026-09-29) y **999 px** en el indicador del acordeón y en el círculo de la flecha.
  - Excepción: las burbujas del diálogo, 18 px, porque la forma es el significado ("son mensajes").
- **Texto sobre imagen (solo en el Hero):** velo en degradado de `#100F0D` de 0 a 72 %, con texto `#F1EDE6`.

---

## 5. Componentes de interfaz (fuera del espécimen, hechos con sus pasos)

- **Botones = filas de acción (criterio del usuario, 2026-09-29; sustituye a las píldoras).** Una sola familia para todos los botones:
  - Al ancho de la columna de su lámina, 56 px de alto mínimo, esquinas de **16 px** (amable, sin ser píldora), texto Inter 600 `body` alineado a la izquierda; si el texto es largo, se acomoda en varias líneas sin deformar la forma.
  - La flecha va a la derecha dentro de un círculo suave de 36 px y dice adónde lleva: ↗ sale del sitio, → hace una acción aquí, ↓ baja en la página. Si el copy trae la flecha, es ese mismo carácter; si no la trae («Conversar con ADA primero»), el ícono va por CSS, sin agregar texto.
  - **Par de CTA, mismo peso:** dos filas rellenas del mismo tamaño, apiladas en el orden del copy, en desktop y en móvil: «Inscribir a mi hijo ↗» en `azul-900` y «Conversar con ADA primero» en `violeta`.
  - **Secundario** («Conocer las reglas de ADA ↗», «Si ya viste suficiente, la inscripción está al final de esta página ↓»): superficie clara (`panel`) con **borde de 2 px en el color de su rol** (cian para ADA, azul para la inscripción; pedido del usuario, 2026-09-29), el círculo de la flecha en el tinte de ese color y el mismo alto y texto. Al pasar el cursor, el fondo toma el tinte.
  - Estados:
    - Hover: la fila sube 2 px y la flecha se mueve 2–3 px hacia donde lleva; el secundario toma el tinte de su color.
    - `pointerdown`: `scale(0.98)` inmediato.
    - Foco: anillo de 2 px separado 3 px.
    - Movimiento reducido: se degrada (1 px y más rápido; la flecha no se mueve), no se cancela.
- **Enlace de texto.**
  - Inter 600, subrayado de 1 px (2 px en hover), opacidad 0.7 en `pointerdown` y área táctil de 44 px.
  - Color por rol: violeta para ADA, azul para la inscripción, `ink` en el footer.
- **Diálogo ADA / HIJO.**
  - Encabezado «Una pregunta que abre otra puerta» (Playfair 700 `subhead`) + «— Conversación de ejemplo» (`micro`).
  - Burbujas:
    - ADA a la izquierda sobre `violeta-tinte`; HIJO a la derecha sobre `cian-tinte`.
    - Texto `body` 500, ancho máximo de 34ch.
    - Etiquetas `micro`: ADA en violeta, HIJO en `ink`.
  - **Con avatares como en la versión A** (ajuste del usuario, 2026-09-28): cuadrados de 34 px con radio 10; ADA a la izquierda y el hijo a la derecha. Sin horas, "escribiendo…" ni palomitas de leído.
  - Un mensaje por paso de scroll, entrando desde su lado.
  - La conversación (4 mensajes) cabe en un encuadre móvil. Son 4 paradas dentro de un pin: 4 E.
- **Bloque de precio.**
  - Dos piezas iguales sobre `panel`, radio 0, borde `line`.
  - Cada viñeta completa y literal; el monto se enfatiza en su lugar (Inter 800), nunca duplicado.
  - `ambar-tinte` marca el valor.
  - La garantía va pegada al par de CTA.
  - **Refinamiento de la Fase 3 (pedido del usuario, 2026-09-29):** misma familia que las tarjetas (panel, borde, esquinas de 16 px, barra ámbar de valor arriba); el monto es protagonista: la etiqueta («Todo hoy, de una vez:» / «En 10 pagos mensuales de») en body 600 y el monto («$4,990.» / «$599.») en semimonumental Inter 800, sin cambiar el texto ni su orden. En desktop son verticales y con aire (~324 × 400 px, altura limitada a 52svh para que la lámina quepa en 1280 × 688). Cada tarjeta lleva su botón al pie, con los textos de la propuesta A (copy agregado aprobado): «Pagar de contado» y «Elegir pagos diferidos», los dos en azul y con el mismo peso.
- **Viñetas.**
  - Siempre completas.
  - Marcador: barra de 8 × 2 px `ink`.
  - La primera frase va en 700 cuando funciona como etiqueta (la Fase 2 lo aplica lista por lista).
- **Acordeón (FAQ).**
  - Toda la fila es el botón: pregunta Inter 600 `body`, 56 px mínimo, `aria-expanded`.
  - Indicador: círculo de 32 px con contorno `azul-900` y chevron que gira 180°.
  - Respuesta Inter `body`.
  - Apertura con resorte crítico, que se puede interrumpir.
- **Escenas y videos cubren su contenedor (decisión del usuario, 2026-09-29; sustituye a «completas con bandas» del 2026-09-28).** La imagen o la secuencia llena todo el escenario conservando su proporción (`object-fit: cover`; en las secuencias, cuadro que cubre el canvas): sin bandas ni deformación; lo que sobra se recorta por el lado que no cabe. Excepción: la figura de ADA, que es un personaje con transparencia. (03.8, los escudos, también cubre desde el 2026-09-29: pedido del usuario.) En móvil, mientras falte la vertical, la horizontal se ve completa; con la vertical 2:3, cubre.
- **Escenas: dos versiones (decisión del usuario, 2026-09-28).** Horizontal para desktop y tablet horizontal (≥ 860 px); **vertical 2:3** para móvil y tablet vertical (< 860 px): un solo archivo para los dos, que llena la pantalla; lo importante va en el rectángulo central de 80 % × 80 % (ajuste del usuario, 2026-09-29; antes 3:4). Las verticales las hace el usuario en Photoshop a partir de la misma imagen base (especificación en `00-context/scenes/vertical/LEEME.md`). Cada escena define en su estación su encuadre (llenar o completa sin recortar) y su movimiento (zoom-in, zoom-out o solo disolvencia). En 03.4: scrub de video en desktop e imagen fija en móvil.
- **Sello (escena).**
  - Radio 0, sin caption, **sin viñeta ni bordes fundidos**: la escena va con sus bordes limpios (ajuste del usuario, 2026-09-28; antes llevaba una máscara en degradado).
  - `alt=""` (decorativa: el significado lo lleva el texto).
  - Ocupa un encuadre propio: 1 E.
- **Hero.**
  - Única imagen antes del texto.
  - Zoom-out extremo de `01-dinner.webp` → pausa → disolvencia → texto.
- **Logo flotante (pedido del usuario, 2026-09-29; ajusta la decisión 6).** Dos logos, cada uno en su momento y ninguno animado con el scroll: **en el Hero**, grande (160 px de ancho en móvil, 240 px en desktop), arriba a la izquierda y visible desde el primer cuadro; **flotante**, fijo arriba a la izquierda (104 px en móvil, 150 px en desktop), que aparece con un fundido cuando el Hero termina de salir, para que nunca haya dos logos a la vez (decisiones del usuario). Sin animación de escala con el scroll (se probó y se descartó: repetía el menú de la propuesta A). No es una barra: no le quita alto al encuadre. Sobre una escena (sello o secuencia) o una bisagra oscura usa la versión dark, con una sombra suave solo en el logo cuando está sobre una imagen clara; sobre el fondo claro, la clara (pedido del usuario, 2026-09-29). Lleva de vuelta al inicio.
- **Tarjetas (L08: 08.5 y 11.3).** Superficie `panel`, borde `line`, esquinas de 16 px (misma familia que los botones) y una barra de 24 × 3 px en el color del rol arriba (violeta en ADA, azul en inscripción). **Títulos en sans** (pedido del usuario, 2026-09-29): Inter 700 en el paso `subhead`.
- **Footer.**
  - Logo + «Presencia, no vigilancia. / Criterio, no candado.» + enlaces, en `small` y color `ink`.
- **Etiquetas.**
  - Solo las que ya están en el copy. No se inventan eyebrows.

---

## 6. Retícula y espaciado
- **Retícula (del espécimen):** 12 columnas, con separación de 24 px en desktop y 16 px en móvil, y contenedor de 1180 px.
- **Dentro de cada composición**, los espacios son los del espécimen:
  - `stack` 10 px;
  - B09 24 px;
  - filas de L03 16 px;
  - separador de L05 20 px;
  - separación entre las dos columnas de L02: 20 px.
- **Entre paradas no hay espaciado de padding: hay estacionamiento (§1.6).**
- **Escala para el flujo normal** (movimiento reducido, FAQ, footer), en múltiplos de 4 px, alineada con Tailwind:
  - 8 px: etiqueta ↔ texto.
  - 16 px: interno de componente.
  - 24 px: párrafo ↔ párrafo.
  - 48 px: título ↔ contenido.
  - 96 px: bloque ↔ bloque.
  - 144 px: capítulo ↔ capítulo en desktop; 96 px en móvil.

---

## 7. Movimiento (GSAP; reglas contrastadas con `Skills/gsap/`)

**Arquitectura**
- Un recorrido continuo con **3 Pin + Scrub + 8 Snap**: cada capítulo es un pin con sus paradas (§1.6).
- Patrones dentro de esa lógica:
  - 5 Horizontal en el cap. 02.
  - 6 Parallax en los sellos.
  - 9 Split solo en `monumental-xl` / `monumental`.
  - 10 Counter, con moderación.
- ScrollSmoother no se usa de entrada.

**Reglas de construcción** (de las skills oficiales)
1. Un ScrollTrigger por timeline de capítulo, en el nivel superior. Nunca anidado ni en un tween hijo.
2. Se crean de arriba hacia abajo, o con `refreshPriority`.
3. Se pinea el escenario y se animan sus hijos.
4. `scrub` y `toggleActions` nunca juntos.
5. En el horizontal, `ease: "none"` y el snap por panel en el trigger principal.
6. `gsap.matchMedia()` con `{ isDesktop: "(min-width: 860px)", isMobile: "(max-width: 859px)", reduceMotion }`. Es el mismo breakpoint del espécimen.
7. `autoAlpha` en capas decorativas. En el texto de lectura, `opacity` + `pointer-events`, para que siga en el árbol de accesibilidad.
8. SplitText por palabras, con `aria: "auto"`, `autoSplit` y `onSplit`, y sin `balance`.
9. `markers` y GSDevTools solo en desarrollo.

**Scrub 0.4** en toda la lectura (lección v2).

**Cada voz se mueve distinto** (como `defaults` de timeline)
- **Grupo L · se asienta:** opacidad y desplazamiento vertical de 24 px a 0, `power2.out`.
- **Lead semibrutalista · anuncia:** opacidad y desplazamiento horizontal de −16 px a 0.
- **Grupo B · corte:** opacidad en el primer 10 % de su parada, sin desplazamiento. El golpe no flota: aparece.
- **Sello:** escala de 1.06 a 1 y parallax de 40 px como máximo.

**Hero**
- Un `ScrollTrigger.create()` con pin de 1.5 E, cuyos `onEnter`/`onEnterBack` reproducen una timeline autoplay independiente (lección v2).
- Valores: zoom-out 3.7 s (ajustado por el usuario el 2026-09-28; antes 2.2 s) → pausa 0.6 s → disolvencia 0.5 s → texto 0.5 s.

**Interacción**
- Respuesta en `pointerdown`, con resorte crítico interrumpible y sin rebote (apple-design §1, §3, §4).

**Movimiento reducido** (se degrada, no se cancela)
- Sin pin, sin scrub y sin zoom.
- Cada encuadre pasa a ser un bloque en flujo normal que aparece con un fundido de 200 ms.
- Hero estático con fundido de 300 ms.
- Interacción con fundidos de 150 ms.

**Rendimiento**
- Solo `transform` y `opacity`.
- `will-change` mientras el pin está activo.
- `refresh()` después de las fuentes y de decodificar las imágenes; el redimensionado ya lo maneja GSAP.

---

## 8. Decisiones para ti

> **Aprobado el 2026-09-26 con todas las opciones por defecto.**

Por defecto manda el espécimen. Las decisiones 1 y 2 aplican reglas que tú escribiste en las lecciones v2.

1. **Peso del cuerpo:** Inter **500**, según tu lección v2 ("nunca 400 como default"). La muestra de escala del espécimen usa 400. *Por defecto: 500.*
2. **Gris (`muted`) en texto romano pequeño:** tu lección v2 dice que va en `ink`. Afecta a las líneas en gris del espécimen: caption de B01, leads de B03, B04 y B08, caption de B07, y apoyos de L01, L03, L05, L06 y L08. `muted` sigue permitido en itálica (captions de B09 y L08) y en tamaños grandes. *Por defecto: `ink`. Las composiciones conservan su jerarquía por peso y tamaño.*
3. **Índices que no están en el copy** (número fantasma y «sección 05» de L06, «§1» de L07, badge y etiquetas de L08): se omiten y la composición se usa sin ellos. Además, en v2 quitaste los numerales de capítulo. *Por defecto: se omiten.*
4. **Escenario oscuro:** los tokens oscuros del espécimen se usan como pantalla completa **solo en las bisagras** (máximo 5 lapidarios en toda la landing). El modo oscuro del sistema operativo no se sigue. *Por defecto: sí a las bisagras, no al modo del sistema.* La alternativa es no usar oscuro en ningún momento.
5. **Color del acento en los golpes:** siempre `azul-900`, fiel al acento único del espécimen. *Por defecto: azul único.* La alternativa es mi propuesta de la revisión 1: coral en el problema, azul en la solución, violeta en ADA.
6. **Barra superior:** sin barra fija durante los pines, para que el encuadre quede completo. El logo va en el Hero y en el footer, y solo hay una línea de progreso de 3 px encima, sin ocupar alto. *Por defecto: así.* Con una barra fija habría que restar su alto a cada encuadre. *(2026-09-29: se agrega el logo flotante, que sigue sin ser barra; ver §5.)*
7. **Interpretaciones de maquetación:**
   - El «·» entre los CTA es la separación entre los dos botones.
   - «ADA:» y «HIJO:» son las etiquetas de las burbujas.
   - «Escenas tal cual» = no se edita ningún archivo; el encuadre en el layout sí se permite (sin máscara ni viñeta, ajuste del 2026-09-28).
   
   *Por defecto: sí.*
8. **Cuerpo 16 px en móvil**, como en el espécimen. Mi revisión 1 subía a 18. A 16 px caben ~107 palabras por encuadre en el móvil de 360; a 18 px bajaría a unas 85, y habría más paradas. *Por defecto: 16, el del espécimen.*

---

## 9. Auditoría fuente → sistema

| Fuente | Dónde quedó | Excepciones |
|---|---|---|
| `Tipografía esencial.html` | Base del sistema: encuadres (§1.1), escala (§2.2), reglas de composición (§2.3), 17 composiciones (§3), neutros claro y oscuro (§4.1), retícula y espacios internos (§6), breakpoint 860 en `matchMedia` (§7) | Solo las decisiones 1–3 de §8. Los textos de ejemplo del espécimen no se usan como copy. |
| `COPY-PUBLICADO.md` | En la Fase 1 no se coloca copy. Los golpes de §1.5 y los ejemplos se verificaron literales. | Las interpretaciones de §8, decisión 7. |
| `VISION-NARRATIVA.md` | Registros → §2.4 · imágenes que sellan → sello y Hero (§5) · §5 preguntas abiertas → §2.4 · Pin + Scrub → §1.6 y §7 · vocabulario → §7 | Inconsistencia de la fuente para la Fase 2: §4 propone golpes para los caps. 04 y 06, pero §1.1 y §5 dicen que no tienen. Además, §4 cita «Tu instinto no está roto. Éste necesita algo distinto.» sin la frase intermedia del copy. |
| `METAPROMPT.md` §6 | Autoplay del Hero, scrub bidireccional, pines cortos (máximo 6 paradas), movimiento reducido sin pin, peso 500, sin gris en texto pequeño, sin doble numeración, sin eyebrows, viñetas completas, refresh después de las fuentes | Las lecciones 1 y 2 chocan con el espécimen: §8, decisiones 1 y 2. |
| `Scroll Patterns — Especimen Completo.html` | Vocabulario y código de referencia (§7) | Al portarlo, el patrón 11 se reemplaza por `gsap.matchMedia()`. |
| `Skills/gsap/` | Reglas de construcción de §7 | Divergencias documentadas: se degrada en lugar de `duration: 0`, y `opacity` en lugar de `autoAlpha` para el texto. |
| Restricciones de `project.config.md` | Tailwind, copy literal, GSAP, texto protagonista, escenas tal cual, Playfair + Inter, paleta del logo (§4.2) | Ninguna. |

---

## 10. Evaluación — Fase 1, revisión 2

Pesos: Purista 35 % · Arquitecto de Sistemas 45 % · Guardián de Lectura 20 %.

| Lente | Puntaje | Objeciones |
|---|---|---|
| Purista | 4.5/5 | El sistema ya no inventa voces ni escalas: todo sale del espécimen o de una restricción. Queda (1): la paleta del logo tiene cinco roles, contenidos por "un acento por pieza". Y (2): puede que B02 o L05 no tengan copy; si no se usan, deben retirarse. |
| Arquitecto de Sistemas | 4.5/5 | La unidad (encuadre = `100svh`) está medida contra viewports reales. La capacidad y el tamaño de los golpes salen de medir con las fuentes instaladas, y el estacionamiento tiene fórmula. Objeción: la medición usa corte de línea aproximado, sin tracking; se valida con render real en la Fase 2. |
| Guardián de Lectura | 4/5 | La regla de ~100 palabras por encuadre protege la lectura en móvil. Objeción: cuerpo de 16 px con copy largo y tráfico frío es el mínimo aceptable, no lo cómodo (§8, decisión 8). Además, el ritmo de pines en móvil se valida en la Fase 2. |

**Puntaje ponderado:** 0.35 × 4.5 + 0.45 × 4.5 + 0.20 × 4 = **4.4 / 5**
**Resultado:** aprobado internamente.
