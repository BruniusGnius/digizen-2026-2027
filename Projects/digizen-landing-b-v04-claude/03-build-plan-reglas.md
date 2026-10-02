---
project: digizen-landing-b-v04-claude
pieza: página «Las reglas de ADA»
fase: 3 - build
documento: plan de componentes y archivos (se entrega antes de escribir el código)
estado: propuesto, en espera de aprobación
fecha: 2026-10-02
wireframe: 02-wireframe-reglas.md (aprobado el 2026-10-02)
---

# Plan de build · página «Las reglas de ADA»

**Criterio principal (usuario):** que se vea de la landing B. No se crea ningún estilo nuevo si ya existe uno en la landing; solo se agrega la maqueta de los bloques que la landing no tiene.

## 1. Qué se reutiliza tal cual de la landing

| Pieza | De dónde sale | Uso en la página de reglas |
|---|---|---|
| Colores, tipografía (Inter), escala de tamaños, márgenes, retícula de 1180 px y 12 columnas | `src/tokens.css` | Todo. Ningún valor suelto. |
| Logo flotante | `BRAND` + `dz-brand.js` | Arriba a la izquierda; lleva a la landing. |
| Menú de hamburguesa | `menu_html` + `dz-menu.js` | El mismo panel, con los mismos nombres; cada opción lleva a su sección de la landing. |
| Tarjeta (blanca, borde, radio 16, barra corta de acento, título Inter 700) | `.card` + `.card.r-ada` (cian) | Las 13 reglas, todas con el acento cian de ADA. Sin iconos. |
| Botones (56 px, radio 16, flecha en círculo) | `.btn`, `.btn.alt`, `.btn.sec` | Azul para inscribir, cian para conversar con ADA, secundario para «Volver a Digizen». |
| Respuesta al tocar | `dz-actions.js` | Todos los botones, igual que en la landing. |
| Formulario «Conversar con ADA primero» | `DIALOG` + `dz-actions.js` | Lo abre «Tengo dudas · CONVERSAR CON ADA»; nace del botón y regresa a él. |
| Pie | el pie de la landing | Sin cambios. |
| Texto pequeño en tinta, no en gris; peso 500 de cuerpo; antetítulos solo los del copy | `01-design-system.md` | Se respetan. |

## 2. Qué se agrega

| Archivo | Qué hace |
|---|---|
| `wireframe-src/reglas.py` | Ya existe: el contenido literal. Fuente única. |
| `output-code/scripts/build.py` | Nueva función que genera `output-code/reglas-de-ada.html` con las piezas de arriba, optimiza las 3 imágenes y **audita el copy contra la fuente** (las mismas palabras, en el mismo orden); si algo difiere, el build falla. |
| `output-code/src/components.css` | Un bloque nuevo, solo de maqueta: la entrada en 3 áreas, la lista con palomitas, la retícula de reglas (1, 2 y 3 columnas), la primera tarjeta ancha con imagen y el cierre con retrato. Todo con los tokens de la landing. |
| `output-code/js/dz-rules.js` | Pequeño: «Volver a Digizen» (cierra la pestaña o regresa a la estación 08.5), los botones de inscripción (llevan a las tarjetas de precio de la landing) y el índice de la lista completa (lleva a cada tarjeta; se interrumpe si el lector hace scroll). |
| `output-code/assets/reglas/` | Las 3 imágenes de la A, copiadas y optimizadas (5 archivos: ADA con tableta para desktop y para teléfono, ADA con el adolescente para desktop y para teléfono, y el retrato). No se toca la A. |
| `03-build-notes-reglas.md` | Al terminar: qué se tradujo, decisiones y evaluación. |

## 3. Qué cambia en la landing (mínimo)

1. El botón **«Conocer las reglas de ADA ↗»** (estación 08.5) deja de estar pendiente: abre `reglas-de-ada.html` en una pestaña nueva. La landing no se mueve de su estación.
2. La landing aprende a **abrir en una estación** cuando llega con una dirección como `…/#P-08b` o `…/#precio`. Lo usan «Volver a Digizen» (cuando no se puede cerrar la pestaña), los botones de inscripción de la página de reglas y las opciones del menú de esa página.

Nada más cambia: mismas 78 estaciones, mismo copy, mismo recorrido.

## 4. Decisiones de detalle que tomo con el sistema de la landing

- **«ADA» en el título:** en violeta, como en «Habla tú con ADA primero.» (en la landing, ADA en texto va en violeta; el cian es solo relleno).
- **Antetítulos** («Marco de seguridad», «Seguridad por diseño», «¿Ya viste suficiente?») y **rótulos** («La regla más importante», «Regla 01»…): tamaño pequeño, Inter 700, en tinta.
- **Palomitas de la lista:** cuadro en tinte cian con la palomita en tinta.
- **Imágenes:** sobre el fondo de la página, sin marco, como las escenas de la landing.
- **SEO:** igual que la landing mientras sea preview (no se indexa). Título «Las reglas de ADA · DIGIZEN» (aprobado). Descripción: el primer párrafo de la página, literal.
- **Movimiento:** casi ninguno; es una página de lectura. Solo la respuesta al tocar, el formulario y el desplazamiento del índice. Con movimiento reducido, el índice salta sin animación.

## 5. Cómo lo verifico

- Auditoría automática del copy contra la fuente (798 palabras, mismo orden) y de los textos alternativos.
- En el navegador: desktop, tablet y teléfono; botones, formulario, pestaña nueva, regreso a la estación 08.5 y llegada a las tarjetas de precio.
- Comparación lado a lado con la landing: tarjetas, botones, tipografía y márgenes deben medir lo mismo.
