---
project: digizen-landing-b-v04-claude
fase: 3 - build
documento: auditoría de distancias de scroll (antes de cambiar nada)
fecha: 2026-09-30
método: mismas fórmulas del motor (dz-pins.js, dz-carousel.js, dz-hero.js); 1 E = alto de la pantalla; entre pines hay 1 E de tránsito
---

# Auditoría de scroll · landing B v04

**Qué se mide:** la distancia de scroll entre cada punto de snap y el siguiente (lo que el lector tiene que recorrer para pasar de un tiempo al otro) y en cuánto scroll aparece cada línea dentro de una parada. En píxeles para un iPhone (663 px de alto) y una laptop (774 px).

## Resumen

1. **Dentro de una misma parada, cuando las líneas aparecen de a poco, los puntos de snap quedan muy juntos:** entre 139 y 380 px en el teléfono. La peor es la evolución de 07.6 (139, 179 y 239 px); después 01.3 «La cinco. / No te escucha.» (325 y 307 px), 07.5, 09.1 y los mazos de tarjetas de 11.3 (226 a 325 px).
2. **Cada línea de esas paradas aparece con solo 50–68 px de scroll.** Un movimiento mínimo del dedo o del trackpad la prende o la apaga: esa es la sensación de «muy sensible».
3. **Entre paradas, la distancia es de 1 a 2.5 E** (660 a 1650 px en el teléfono). Scrolleando con calma está bien; pero un deslizamiento normal con el dedo lleva inercia y recorre 1500–3000 px, así que cruza 2–4 paradas de una vez. Eso es lo que pasa al inicio (del Hero a «Las cuatro falsas»): las distancias ahí son de 1000–1650 px, pero un gesto con inercia se las salta.
4. **En desktop pasa lo mismo en proporción** (163 a 406 px dentro de las paradas con varios tiempos); el trackpad de la Mac también tiene inercia.


## Móvil (iPhone, 663 px) · 99 puntos de snap · recorrido total 107.3 E

### Distancias entre puntos de snap, de la más corta a la más larga (las 20 primeras)

| Desde | Hasta | E | px |
|---|---|---:|---:|
| 07.6 paso 2 | 07.6 paso 3 | 0.21 | 139 |
| 07.6 paso 1 | 07.6 paso 2 | 0.27 | 179 |
| 11.3m tarjeta 3 | 11.3m | 0.34 | 226 |
| 07.6 paso 3 | 07.6 | 0.36 | 239 |
| 11.3m tarjeta 2 | 11.3m tarjeta 3 | 0.42 | 278 |
| 11.3bm tarjeta 1 | 11.3bm tarjeta 2 | 0.42 | 278 |
| 11.3m | 11.3bm tarjeta 1 | 0.45 | 301 |
| 01.3 paso 1 | 01.3 | 0.46 | 307 |
| 11.3bm tarjeta 2 | 11.3bm | 0.47 | 313 |
| 01.3 puente | 01.3 paso 1 | 0.49 | 325 |
| 11.3m tarjeta 1 | 11.3m tarjeta 2 | 0.49 | 325 |
| 07.5 paso 2 | 07.5 | 0.52 | 348 |
| 09.1 paso 2 | 09.1 | 0.53 | 348 |
| 08.5m tarjeta 2 | 08.5m | 0.55 | 365 |
| 03.3 puente | 03.3 | 0.64 | 423 |
| 05.8 puente | 05.8 | 0.64 | 423 |
| 10.4 puente | 10.4 | 0.64 | 423 |
| 12.2 puente | 12.2 | 0.64 | 423 |
| 05.4 paso 1 | 05.4 | 0.68 | 448 |
| 07.4 mensaje 1 | 07.4 mensaje 2 | 0.72 | 477 |

### Tramo del Hero a «Las cuatro falsas» (02.1)

| Desde | Hasta | E | px |
|---|---|---:|---:|
| H.1 | H.2 | 2.50 | 1658 |
| H.2 | H.3 | 1.75 | 1160 |
| H.3 | 01.1 | 1.50 | 994 |
| 01.1 | 01.2 | 1.75 | 1160 |
| 01.2 | 01.3 puente | 0.81 | 540 |
| 01.3 puente | 01.3 paso 1 | 0.49 | 325 |
| 01.3 paso 1 | 01.3 | 0.46 | 307 |
| 01.3 | 01.4 | 1.07 | 713 |
| 01.4 | 02.1 | 1.13 | 750 |

### Líneas que aparecen con menos scroll

| Qué aparece | E | px |
|---|---:|---:|
| 05.4 paso 2 | 0.075 | 50 |
| 07.6 paso 2 | 0.075 | 50 |
| 07.6 paso 3 | 0.075 | 50 |
| 07.6 paso 4 | 0.075 | 50 |
| 01.3 paso 1 | 0.088 | 58 |
| 01.3 paso 2 | 0.088 | 58 |
| 07.5 paso 2 | 0.088 | 58 |
| 07.5 paso 3 | 0.088 | 58 |
| 09.1 paso 2 | 0.088 | 58 |
| 09.1 paso 3 | 0.088 | 58 |
| 02.1 entra | 0.100 | 66 |
| 01.4 entra | 0.125 | 83 |

## Desktop (laptop, 774 px) · 91 puntos de snap · recorrido total 105.6 E

### Distancias entre puntos de snap, de la más corta a la más larga (las 20 primeras)

| Desde | Hasta | E | px |
|---|---|---:|---:|
| 07.6 paso 2 | 07.6 paso 3 | 0.21 | 163 |
| 07.6 paso 1 | 07.6 paso 2 | 0.27 | 209 |
| 07.6 paso 3 | 07.6 | 0.36 | 279 |
| 01.3 paso 1 | 01.3 | 0.46 | 359 |
| 01.3 puente | 01.3 paso 1 | 0.49 | 379 |
| 07.5 paso 2 | 07.5 | 0.52 | 406 |
| 09.1 paso 2 | 09.1 | 0.53 | 406 |
| 03.3 puente | 03.3 | 0.64 | 493 |
| 05.8 puente | 05.8 | 0.64 | 493 |
| 10.4 puente | 10.4 | 0.64 | 493 |
| 12.2 puente | 12.2 | 0.64 | 493 |
| 05.4 paso 1 | 05.4 | 0.68 | 522 |
| 07.4 mensaje 1 | 07.4 mensaje 2 | 0.72 | 557 |
| 07.4 mensaje 2 | 07.4 mensaje 3 | 0.72 | 557 |
| 07.4 mensaje 3 | 07.4 mensaje 4 | 0.72 | 557 |
| 07.5 | 07.6 paso 1 | 0.75 | 584 |
| 09.1 paso 1 | 09.1 paso 2 | 0.77 | 596 |
| 07.5 paso 1 | 07.5 paso 2 | 0.77 | 596 |
| 10.3 | 10.4 puente | 0.80 | 619 |
| 03.2 | 03.3 puente | 0.80 | 619 |

### Tramo del Hero a «Las cuatro falsas» (02.1)

| Desde | Hasta | E | px |
|---|---|---:|---:|
| H.1 | H.2 | 2.50 | 1935 |
| H.2 | H.3 | 1.75 | 1354 |
| H.3 | 01.1 | 1.50 | 1161 |
| 01.1 | 01.2 | 1.75 | 1354 |
| 01.2 | 01.3 puente | 0.81 | 631 |
| 01.3 puente | 01.3 paso 1 | 0.49 | 379 |
| 01.3 paso 1 | 01.3 | 0.46 | 359 |
| 01.3 | 01.4 | 1.07 | 832 |
| 01.4 | 02.1 | 1.13 | 876 |

### Líneas que aparecen con menos scroll

| Qué aparece | E | px |
|---|---:|---:|
| 05.4 paso 2 | 0.075 | 58 |
| 07.6 paso 2 | 0.075 | 58 |
| 07.6 paso 3 | 0.075 | 58 |
| 07.6 paso 4 | 0.075 | 58 |
| 01.3 paso 1 | 0.088 | 68 |
| 01.3 paso 2 | 0.088 | 68 |
| 07.5 paso 2 | 0.088 | 68 |
| 07.5 paso 3 | 0.088 | 68 |
| 09.1 paso 2 | 0.088 | 68 |
| 09.1 paso 3 | 0.088 | 68 |
| 02.1 entra | 0.100 | 77 |
| 01.4 entra | 0.125 | 97 |

## Qué propongo (no se aplica nada sin aprobación)

1. **Más rango dentro de las paradas con varios tiempos** (lo que detectaste): sin agregar paradas, darles más E a 07.6, 01.3, 07.5, 09.1 y a los mazos (11.3m, 11.3bm, 08.5m), de modo que entre un tiempo y el siguiente haya al menos ~0.5 E (≈330 px en el teléfono), y que cada línea aparezca en ~0.15 E (≈100–150 px) en vez de 50–68 px. Se ajusta en la fuente compartida: el wireframe y la página cambian igual.
2. **Distancia mínima por encuadre (900 px)** para pantallas bajas, en teléfono y en laptop: las paradas cortas ganan recorrido en proporción.
3. **Solo si después sigue saltándose paradas con un gesto fuerte:** limitar la inercia del dedo en pantallas táctiles.

Se prueba primero en una carpeta aparte de GitHub Pages para comparar con la versión actual.

## Pruebas publicadas (2026-09-30)

- **Prueba 1** (`prueba-scroll-1.html`): puntos 1 y 2.
- **Prueba 2** (`prueba-scroll-2.html`): puntos 1, 2 y 3.
- **Prueba 3** (`prueba-scroll-3.html`) · **una estación por gesto** (`js/dz-pager.js`). El problema que señaló el jefe del usuario: «cuando yo le doy scroll para continuar con lo que sigue, se salta tres pasos y la gente no sabe que hay texto antes».
  - Cada gesto (rueda, trackpad, dedo o teclado) mueve exactamente una estación. La inercia se ignora; cuenta un gesto nuevo después de una pausa o de un empujón nuevo.
  - Las estaciones son las mismas 78 del wireframe y llegan compuestas: sin animaciones internas ni la entrada del Hero.
  - Cada escena ocupa exactamente una pantalla, con la composición de la versión animada; la imagen y su zoom no se salen de su estación.
  - Desktop: solo las escenas con efecto visible (02.6 con zoom, y los videos 03.4 y 05.5) tienen dos paradas (primer cuadro y final); el gesto entre las dos corre la escena con el mismo scrub: los videos a velocidad constante, como video (~20 cuadros por segundo, 49 cuadros ≈ 2.5 s), y el zoom en 1.6 s. Antes el video se comprimía en 1.6 s y se veía acelerado (corrección del usuario). Las que no tienen efecto (zoom 1 o casi: 03.8, 09.2, 10.7, 12.6) son estaciones normales. El saludo de ADA corre por tiempo al llegar.
  - Teléfono y tablet: todas las imágenes son estaciones ancladas, sin animación (pedido del usuario).
  - Tarjetas del teléfono (08.5m «ADA es lo segundo, por diseño:», 11.3m y 11.3bm «Tu inscripción fundadora incluye:»): apiladas como en la versión animada; cada gesto sube una tarjeta sobre la anterior y, con la última en su lugar, el siguiente pasa de estación (pedido del usuario; se probó un tramo fluido y se veía raro).
  - Otras estaciones más altas que la pantalla: se llega anclado a su inicio, adentro el scroll es fluido y se detiene en su final; el gesto siguiente ancla en la estación que sigue.
  - Del FAQ hacia abajo, el scroll es libre; al subir, se detiene en el FAQ. El menú, el riel, el logo y los botones saltan a su estación.
