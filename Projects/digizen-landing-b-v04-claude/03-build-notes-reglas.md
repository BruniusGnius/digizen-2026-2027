---
project: digizen-landing-b-v04-claude
pieza: página «Las reglas de ADA»
fase: 3 - build
estado: construida (2026-10-02)
plan: 03-build-plan-reglas.md (aprobado por el usuario el 2026-10-02)
wireframe: 02-wireframe-reglas.md (aprobado el 2026-10-02)
---

# Notas de build · página «Las reglas de ADA»

## Qué se construyó

`output-code/reglas-de-ada.html`, generada por `output-code/scripts/build.py` desde `wireframe-src/reglas.py` (la misma fuente del wireframe). Es una página aparte, de lectura con scroll libre, hecha con las piezas de la landing B.

## Qué se tradujo de cada fase

| De | Qué | Cómo quedó |
|---|---|---|
| Sistema de diseño (Fase 1) | Colores, Inter, escala, márgenes, retícula de 1180 px | Los mismos tokens de `src/tokens.css`; ningún color ni tamaño nuevo. |
| Sistema de diseño | Tarjeta L08 | `.card.r-ada`: blanca, borde, radio 16, barra corta en cian (ADA), título Inter 700 en subhead. Un solo color en las 13, sin iconos (decisión del usuario). |
| Sistema de diseño | Botones | `.btn` azul (inscribir), `.btn.alt` cian (conversar con ADA), `.btn.sec` (Volver a Digizen); 56 px, radio 16, flecha en círculo. |
| Sistema de diseño | Reglas de texto | Antetítulos y rótulos en pequeño, Inter 700, en tinta (no gris); cuerpo en peso 500; «ADA» en violeta en el título; cian solo como relleno (palomitas). |
| Wireframe (Fase 2) | Orden de bloques y diferencias por tamaño | Entrada, reglas, cierre y pie, en ese orden. Lista corta en teléfono y tablet, completa en desktop. 1, 2 y 3 columnas (3 desde 1100 px). |
| Wireframe | Intención de interacción | Respuesta inmediata al tocar; el formulario nace del botón y se puede cerrar a medio camino; el índice se interrumpe si el lector hace scroll; «Volver a Digizen» sale por donde se entró. |

## Archivos

| Archivo | Qué hace |
|---|---|
| `wireframe-src/reglas.py` | Contenido literal (fuente única). |
| `output-code/scripts/build.py` | `rules_assets()`, `rules_page()` y `rules_audit()`; el botón de la landing «Conocer las reglas de ADA ↗» ahora abre la página. |
| `output-code/src/components.css` | Bloque `rg-`: solo la maqueta (entrada en 3 áreas, palomitas, retícula, tarjeta ancha, cierre). |
| `output-code/js/dz-rules.js` | «Volver a Digizen», enlaces a secciones de la landing y el índice. |
| `output-code/js/dz-pager.js` | La landing abre en una estación cuando llega con `#P-…`, `#FAQ` o `#precio`, y reacciona si se lo piden desde otra pestaña. |
| `00-context/reglas/` y `output-code/assets/reglas/` | Las 3 imágenes de la A (5 archivos) y sus versiones optimizadas en dos anchos, con su transparencia. |

Librerías: ninguna nueva. La página de reglas no carga GSAP (no hay recorrido).

## Decisiones tomadas en el build (no estaban en las fases)

1. **Flecha de los botones:** el copy de la A no trae flecha escrita; el icono del círculo va por CSS (→ en inscribir y conversar, ← en «Volver a Digizen»), como en los botones de la landing que no traen flecha en el copy.
2. **Logo:** en esta página se queda arriba y no flota al hacer scroll, para que no pase encima del texto en una lectura libre. El botón de menú sí queda fijo.
3. **La entrada en desktop ocupa una pantalla** (alto mínimo de la ventana), como una estación de la landing.
4. **Cómo sabe la página que vino de la landing:** el botón de la landing abre la pestaña con `rel="opener"` (mismo sitio). Si vino de la landing, «Volver a Digizen» cierra la pestaña; si alguien abrió la página directo, el botón lo lleva a la landing en la estación 08.5 en vez de cerrarle la pestaña.
5. **Botones de inscripción:** si la landing sigue abierta en su pestaña, la mueven a las tarjetas de precio y cierran la pestaña de reglas; si no, navegan ahí mismo.
6. **Descripción para buscadores:** el primer párrafo de la página, literal. Mientras la B sea preview, la página no se indexa.

## Verificación

- **Auditoría del copy (automática, en cada build):** 798 palabras de la fuente, las mismas y en el mismo orden; 2 textos alternativos iguales; 13 tarjetas. Si algo difiere, el build falla.
- **En el navegador:** desktop (1280 × 800), teléfono (390 × 844). Sin desbordes ni errores de consola. Tarjeta, botones y tipografía miden lo mismo que en la landing (tarjeta blanca, radio 16, relleno 26/24/24, barra cian; título 24 px / 700; botón de 56 px).
- **Comportamientos probados:** el formulario abre y cierra; el menú abre con los nombres de la landing; el índice lleva a su tarjeta sin cambiar la dirección; «Volver a Digizen» sin landing abierta llega a la estación 08.5 (08.5m en teléfono); los botones de inscripción llegan a las tarjetas de precio (11.4 en desktop, 11.5m en teléfono); la landing reacciona a `#P-10a`, `#FAQ` y `#precio`.
- **No verificado:** el caso de dos pestañas reales (abrir desde la landing y que «Volver a Digizen» cierre la pestaña). El navegador integrado abre todo en la misma pestaña, así que solo pude probar el camino alterno. Hay que probarlo en Chrome o Safari.

### Evaluación — Fase 3, ronda 1

| Lente | Puntaje | Objeciones |
|---|---|---|
| Purista (20 %) | 4/5 | Nada decorativo: sin iconos, un solo acento. La lista completa repite títulos, pero funciona como índice. |
| Arquitecto de Sistemas (40 %) | 4/5 | Fiel a los tokens y a los componentes de la landing; contenido en una fuente única con auditoría. Objeciones: el corte de 1100 px es nuevo en el sistema, y algunos espacios de la maqueta (64, 96, 104 px) van escritos directo, como en la landing, y no como token. |
| Guardián de Lectura (40 %) | 4/5 | En desktop la entrada es una pantalla y el escaneo es claro. Objeción: en teléfono la entrada mide 1.4 pantallas y el primer botón queda después de un scroll. Accesibilidad: h1, h2 y h3 en orden, textos alternativos, foco visible, y el índice salta sin animación con movimiento reducido. |

**Puntaje ponderado:** 4.0 / 5
**Resultado:** aprobado internamente; quedan las objeciones menores anotadas y el caso de dos pestañas por verificar.

## Pendientes

- Probar en Chrome y Safari, en computadora y en teléfono, que «Volver a Digizen» cierra la pestaña y deja la landing en su estación.
- Destino del pago y envío del formulario de ADA: siguen pendientes, igual que en la landing.
- Para producción: canonical e indexación de esta página junto con la landing (`PREVIEW = False`).

## Refinamiento de la entrada (pedido del usuario, 2026-10-02)

El usuario comparó la entrada con la de la A: la de la A se veía mejor distribuida. Se reconfiguró en desktop con las piezas de la B:

- **Imagen de ADA más grande** (350 px de ancho en vez de 270), a la izquierda, centrada con el bloque.
- **Título en una línea**, con la barra corta del sistema (la de las tarjetas, en cian) y el antetítulo arriba. Ocupa el ancho del texto y de la lista.
- **Texto de entrada en el paso «lead»** de la landing (24 px) cuando la pantalla tiene 780 px de alto o más; en pantallas bajas se queda en cuerpo para que todo quepa.
- **Lista de 13 puntos compacta** a la derecha: pequeña, en negritas, con la palomita sobre cian sólido y una flecha ↓ que indica que cada punto lleva a su tarjeta.
- **Botones compactos en fila**, al ancho de su texto, en vez de dos bloques apilados a todo el ancho.
- **Flecha de scroll** de la landing al pie de la entrada (pedido del usuario).
- De 860 a 1099 px: imagen a la izquierda, título, texto y botones a la derecha, y la lista debajo en 3 columnas.
- Teléfono y tablet: sin cambios de orden.

Además, adición de copy aprobada por el usuario: botón secundario **«Regresar a Digizen»** al final de la página, bajo los dos botones del cierre; se comporta igual que «Volver a Digizen». La auditoría lo lista como adición (no está en la fuente de la A).

**No se publicó en GitHub Pages:** el usuario pidió ver y refinar antes de publicar. La versión que está en línea es la anterior a este refinamiento.

**Pendiente de decisión:** el usuario quiere que la página tenga estaciones de scroll con GSAP, como la landing. Eso cambia el modo de lectura aprobado en el wireframe (scroll libre) y pide rearmar la página por estaciones; se propone el mapa de estaciones antes de construirlo.

## Estaciones con el motor de la landing y ajustes de la entrada (usuario, 2026-10-02)

- **Estaciones:** la página usa el mismo motor de la landing (`dz-core.js`, `dz-pager.js`, `dz-main.js`, GSAP): una estación por gesto. 7 estaciones en desktop (reglas de 3 en 3), 9 en tablet (de 2 en 2) y 8 en teléfono (tarjetas apiladas, una por gesto; la entrada en dos estaciones, como prueba). El motor reconoce tres cortes nuevos para esta página (`w`, `t`, `s`, `n` en `DZ.visible`); la landing no cambia.
- **Entrada, desktop:** el texto vuelve al tamaño de cuerpo (el tamaño grande hacía la entrada muy alta; corrección del usuario). Los botones quedan bajo el texto y la lista, al lado, ocupa el alto del texto más los botones, como en la A.
- **Entrada, tablet:** los dos botones en una sola fila a todo el ancho, fuera de la columna del texto; uno queda debajo de ADA (pedido del usuario).
- **Teléfono:** en el mazo, la tarjeta anterior asoma con su rótulo y su título. El índice (desktop) lleva a la estación de la tarjeta.
- **Auditoría:** por tamaño (desktop, tablet, teléfono): 798 palabras, las mismas y en el mismo orden, y los textos alternativos.
- **Verificado en el navegador:** 1380 × 865, 1280 × 720, 1024 × 768, 768 × 1024 y 390 × 844: todas las estaciones miden una pantalla y ninguna necesita scroll interno; gestos de rueda, teclado y dedo avanzan una estación (o una tarjeta en el mazo). Sin errores de consola. La landing sigue igual.
- **Sigue sin publicarse en GitHub Pages**, a la espera de la revisión del usuario. La entrada en dos estaciones del teléfono es una prueba: falta su decisión.

