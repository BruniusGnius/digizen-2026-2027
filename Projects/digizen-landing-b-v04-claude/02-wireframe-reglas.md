---
project: digizen-landing-b-v04-claude
pieza: página «Las reglas de ADA»
fase: 2 - wireframe
estado: aprobado (2026-10-02)
fecha: 2026-10-02
fuente: 00-context/REGLAS-DE-ADA-fuente-A.html (el `<main>` de /reglas-de-ada de la landing A, versión final, pegado por el usuario)
artefacto: 02-wireframe-reglas.html (grises, copy literal; se genera con `python3 -B wireframe-src/build_reglas.py`)
contenido: wireframe-src/reglas.py (fuente única: de aquí salen el wireframe y, después del gate, la página)
---

# Wireframe · página «Las reglas de ADA»

## Decisiones del usuario (2026-10-02)

1. **Página aparte**, para no afectar la narrativa de la landing.
2. **Scroll libre**, manteniendo las constantes de diseño de la landing B.
3. **Botones con los textos de la A.**
4. **Las 3 imágenes de la A.**

La fuente real es el HTML final de la A que pegó el usuario; coincide palabra por palabra con la rama `digizen-a-reglas-ada` (commit d859d88).

## Orden de bloques

El orden del copy es el de la fuente. Lo que cambia entre tamaños es solo la posición de la imagen y cuál de las dos listas se ve (igual que en la A).

| # | Bloque | Contenido (literal) | Nota de intención |
|---|---|---|---|
| R0 | Encabezado | Logo flotante y botón de menú | Igual que en la landing. El logo lleva a la landing; el menú es el mismo y sus opciones llevan a las secciones de la landing. Sin riel ni barra de progreso: aquí no hay estaciones. |
| R1 | Entrada | «Marco de seguridad» · **Las reglas de ADA** · 3 párrafos · imagen de ADA con su tableta · lista · botones «Inscribir a mi hijo» y «Volver a Digizen» | Dice qué es la página y por qué importa antes de pedir que se lea la lista. Se lee en 3 segundos: el título y las dos frases en negritas. |
| R2 | Las reglas | «Seguridad por diseño» · **ADA no improvisa: responde dentro de estas reglas** · 13 tarjetas | Contenido de consulta: todo abierto, nada en acordeón. Cada tarjeta se entiende con su rótulo y su título; el subtítulo y el cuerpo son la profundidad. La primera ocupa todo el ancho y lleva la imagen de ADA con el adolescente. |
| R3 | Cierre | «¿Ya viste suficiente?» · **Tu hijo puede empezar hoy mismo.** · línea de apoyo · retrato de papá e hijo · botones «Inscribir a mi hijo · EMPIEZA HOY» y «Tengo dudas · CONVERSAR CON ADA» | Las dos acciones con el mismo peso, después de leer. |
| R4 | Pie | El pie de la landing | Componente compartido, sin cambios. |

### Diferencias por tamaño

| | Teléfono (< 600 px) | Tablet (600–859 px) | Desktop (≥ 860 px) |
|---|---|---|---|
| R1 | Texto → imagen → lista corta (3) → botones. La imagen no pasa del 40 % del alto de la pantalla. | Texto, lista corta y botones a la izquierda; imagen a la derecha. | Imagen · texto y botones · lista completa (13), en una sola pantalla. La lista completa es también el índice: cada punto lleva a su tarjeta. |
| R2 | 1 columna. | 2 columnas. | 2 columnas hasta 1099 px; 3 columnas desde 1100 px (4 filas de 3). En la primera tarjeta, el texto a la izquierda y la imagen a la derecha. |
| R3 | Retrato → texto → botones. | Igual que teléfono. | Retrato a la izquierda; texto y botones a la derecha. |

Medidas del wireframe con el copy real: en desktop de 1280 × 800 la entrada mide 647 px (cabe en una pantalla) y la página completa, unas 6 pantallas. En teléfono de 390 × 844 la entrada mide 1,110 px (1.3 pantallas) y la página completa, unas 10.5 pantallas.

## Decisiones de legibilidad aplicadas

- **Constantes de la landing B:** retícula de 1180 px y 12 columnas, márgenes de 24 / 48 px, escala tipográfica de la landing (título de entrada y de cierre en semimonumental, título de sección en encabezado, cuerpo de 16 / 18 px), tarjeta blanca de radio 16 con barra corta de acento, botones de 56 px de alto con radio 16.
- **Jerarquía de escaneo** (barra negra en el wireframe): título de la página, título de la sección, los 13 títulos de tarjeta y el título del cierre.
- **Renglón de las tarjetas:** a 3 columnas solo desde 1100 px (≈ 295 px de texto); antes de eso, 2 columnas para que el renglón no quede angosto.
- **Primer botón temprano:** en R1, antes de las 13 tarjetas. En el cierre se repiten las dos acciones.
- **Las listas:** la corta (3 puntos) resume; la completa (13) es el índice en desktop.

## Intención de interacción

| Componente | Respuesta al tocar | Interrumpible | De dónde entra y por dónde sale |
|---|---|---|---|
| Botones | Inmediata: se hunden, como todos los de la landing. | — | — |
| «Volver a Digizen» | Inmediata. | — | Sale por donde se entró: cierra la pestaña de reglas y deja al lector en la landing, en la estación 08.5 donde estaba. Si el navegador no permite cerrarla, lleva a la landing en esa estación. |
| «Inscribir a mi hijo» y «… · EMPIEZA HOY» | Inmediata. | — | Llevan a las tarjetas de precio de la landing (11.4 en desktop, 11.5m en teléfono), como el botón del menú. |
| «Tengo dudas · CONVERSAR CON ADA» | Inmediata. | Sí: el formulario se puede cerrar a medio camino. | Nace del botón y regresa al botón (el mismo formulario de la landing). |
| Puntos de la lista completa (desktop) | Inmediata. | Sí: el desplazamiento se interrumpe si el lector hace scroll. | Llevan a su tarjeta dentro de la misma página. |
| Menú | Igual que en la landing. | Sí. | Entra y sale por la derecha. |

## Auditoría fuente → artefacto

`python3 -B wireframe-src/build_reglas.py` compara el wireframe con la fuente:

- Copy de la fuente: **798 palabras**; en el wireframe: **798 palabras**, las mismas y en el mismo orden.
- Textos alternativos de imagen: 2 en la fuente, 2 en el wireframe, iguales. El retrato del cierre es decorativo en la A (sin texto alternativo) y así se conserva.
- 13 tarjetas; lista completa de 13 puntos; lista corta de 3.
- Excepciones: ninguna.

### Notas internas (no son UI; se conservan completas)

1. En la lista completa, cuatro nombres no coinciden con el título de su tarjeta: «Adultos presentes» / «Los adultos no se reemplazan»; «Sin diagnósticos» / «Sin etiquetas»; «Privacidad con cuidado» / «Privacidad, no abandono»; «Límites claros» / «Sin promesas vacías». Así está en la fuente; no se corrige sin que lo decida el usuario.
2. En A cada tarjeta lleva un icono y un color de acento que rota (violeta, cian, verde, azul). No son copy. En la B las tarjetas no llevan iconos y el color va por función: ADA = cian.

### Contenido que falta o que es nuevo (no se suple)

- **Título de la pestaña** de la página (`<title>`): en la A es el mismo de la landing porque es una sola aplicación. Para una página aparte hace falta uno; propuesta con palabras que ya existen: «Las reglas de ADA · DIGIZEN». Requiere aprobación.
- **Destino del pago** y **envío del formulario de ADA:** siguen pendientes, igual que en la landing.

## Decisiones del gate (usuario, 2026-10-02)

1. **Un solo color, lo más parecido a la landing B:** tarjetas sin iconos y con el acento de ADA (cian) en todas, como las de «ADA es lo segundo, por diseño:».
2. **Pestaña nueva:** «Conocer las reglas de ADA ↗» abre la página en una pestaña nueva, para no romper la narrativa; la landing se queda en su pestaña, en la estación donde estaba. «Volver a Digizen» cierra la pestaña de reglas; si el navegador no permite cerrarla, lleva a la landing en esa misma estación (08.5).
3. **Título de la pestaña:** «Las reglas de ADA · DIGIZEN» (aprobado).
4. **Lo que más importa:** que la página se vea de la landing B; mismas constantes y mismo sistema de diseño.

## Puntos que se llevaron al gate

1. **Iconos y colores de las tarjetas:** en la B, sin iconos y con el acento de ADA (cian) en todas, como las tarjetas de «ADA es lo segundo, por diseño:»; o con los iconos de la A.
2. **Cómo abre desde la landing:** el botón «Conocer las reglas de ADA ↗» abre la página en la misma pestaña y «Volver a Digizen» regresa a la estación 08.5; o en una pestaña nueva.
3. **Título de la pestaña:** «Las reglas de ADA · DIGIZEN».

### Evaluación — Fase 2, ronda 1

| Lente | Puntaje | Objeciones |
|---|---|---|
| Purista (25 %) | 4/5 | La lista completa repite los títulos de las tarjetas; se defiende porque en desktop funciona como índice. Los iconos de la A se dejan fuera: no cumplen función en el sistema de la B. |
| Arquitecto de Sistemas (20 %) | 4/5 | Reutiliza los componentes de la landing (encabezado, tarjeta, botones, formulario, pie) y una fuente única de contenido con auditoría automática. Objeción: el corte de 1100 px para las 3 columnas es nuevo; la landing solo usa 600 y 860. |
| Guardián de Lectura (55 %) | 4/5 | En desktop la entrada cabe en una pantalla y el escaneo es claro. Objeciones: en teléfono la entrada mide 1.3 pantallas y el primer botón queda después de un scroll; las 13 tarjetas abiertas son unas 5 pantallas de teléfono, aceptable por ser contenido de consulta con scroll libre. |

**Puntaje ponderado:** 4.0 / 5
**Resultado:** aprobado internamente (sin rondas de refinamiento adicionales; quedan las objeciones menores anotadas).

## Gate de salida

¿Apruebas este layout y arquitectura de información para construir la página, o ajustamos el orden o la estructura primero?
