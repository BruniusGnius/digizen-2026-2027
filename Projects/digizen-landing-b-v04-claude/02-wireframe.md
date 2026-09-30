---
project: digizen-landing-b-v04-claude
fase: 2 - wireframe
estado: aprobado
aprobado: 2026-09-29 — «ya completamos la fase del wireframe; me gusta mucho como está». En la construcción se refina lo que está, sin cambios drásticos salvo que sea un error.
formato: wireframe de recorrido (HTML) + esta partitura
---

# Wireframe de recorrido — Digizen Landing B v04

## 0. Qué es y cómo verlo

Esta landing se estructura por el scroll, así que el wireframe no son cajas estáticas: es el **recorrido real**, en escala de grises, con los pines, el estacionamiento de cada parada (E), el snap y el copy literal adentro.

- **Ver:** abre [`02-wireframe.html`](02-wireframe.html) en el navegador (necesita internet para cargar GSAP; sin conexión se muestra el modo reducido, sin pines).
- **Regla de la derecha:** la escala completa del recorrido, a proporción.
  - gris claro = lectura;
  - gris medio = golpe;
  - negro = escenario oscuro;
  - rayado = escena;
  - blanco = tránsito entre pines.
  
  Cada raya es un punto de snap; clic para saltar ahí.
- **Panel inferior (HUD):** parada actual, composición, E, pin, posición en E y la nota de intención. Botones: ocultar notas, ver modo reducido, leyenda.
- **Etiqueta de cada parada:** id · composición · E · ★ (escaneo de 3 s) · **% de ocupación del encuadre medido a tu tamaño de pantalla** (negro = desborda).
- **Móvil:** angosta la ventana por debajo de 860 px y cambia a la escala y el encuadre móvil.
- **Regenerar** (si cambia algo): `python3 wireframe-src/build.py`. El script contiene el copy una sola vez y audita el resultado contra `00-context/COPY-PUBLICADO.md`.

Reglas de esta fase que se respetan:
- Solo grises; los acentos se marcan con subrayado punteado.
- Las escenas se ven en gris.
- Sin animación final: solo cortes y fundidos de trabajo.
- La tipografía es la real (Playfair + Inter con la escala del espécimen), porque la ocupación depende de ella.

## Refinamiento con gramática narrativa (2026-09-28)

Se parte de la versión 1. La iteración 2 (variedad de composiciones) se descartó y quedó en git stash. El criterio está en [`02-gramatica-narrativa.md`](02-gramatica-narrativa.md): cada función narrativa tiene un layout, y se repite.

**Aplicado:**
- **A1:** 03.2 «¿Qué sentiste?» pasa a la voz de puente de todos (Inter 500, subhead).
- **A2:** las aperturas (L06, incluidos 02.1 y 11.2) y los golpes dentro de párrafo comparten el borde izquierdo de la columna de lectura (el eje de lectura).
- **B3:** 01.4 como «golpe + remate»: «Pero no por lo que crees.» en grande, «Y ahí es donde se pone interesante.» chico.
- **B4:** 03.7 y 08.4 como «golpe dentro de párrafo», el mismo layout de 12.4.
- **C5:** voz citada en itálica: las citas-eco del cap. 02, el título de 08.1 y la cita del niño en 10.5 (10.3 ya lo estaba).
- **C6:** la tesis (05.7) con la forma del cierre de marca (B06), como 12.7.
- **C7:** «Eres tú.» (10.1) y «Ya lo tienes.» (12.2) en monumental-xl, como rima.
- **Escenas:** se cargan desde `00-context/scenes/` (ruta relativa). Si alguna no carga, el wireframe muestra un aviso con la ruta.

**Imágenes (ajustes por estación):**
- Sin viñeta en ninguna escena.
- 02.6: zoom-in largo hacia el celular.
- 03.4: scrub de video en desktop (`assets/seq/03-fastidio/`, 49 frames) e imagen fija provisional en móvil.
- 03.8 (escudos): completa, sin recortar, y solo disolvencia.
- **Versiones verticales para móvil y tablet:** faltan las 8 (lista y especificación en `00-context/scenes/vertical/LEEME.md`). El wireframe muestra un aviso en móvil donde falta alguna.

**Pendiente, se decide al llegar a su estación:**
- 8: en 12.4, ¿una frase en grande o las dos?
- 9: ¿remate en negrita dentro de los párrafos?

**Pendiente para la versión final de la página (usuario, 2026-09-28):**
- **Indicador de recorrido / navegación por capítulos.** La regla derecha del wireframe es solo instrumento. Para la final se propusieron tres opciones: 1) riel de capítulos (recomendado; en móvil, solo barra fina arriba), 2) barra de progreso fina, 3) píldora con capítulo actual + índice. Se decide en la versión final. Sería un componente nuevo que hay que agregar al sistema de diseño.
- **Nombres de capítulo:** lo más sintéticos posible y con títulos atractivos. Es **copy nuevo**: requiere propuesta y aprobación del usuario; no se toma ni se inventa sin aprobación.
- **Escenas en desktop:** exportarlas en 16:8.6 (2560×1376) para que las bandas sean mínimas; 07-together-mother-daughter está hoy en 2:1 (1412×706). 12.6: ¿solo disolvencia en vez del zoom de entrada de 106 %?

## 1. Escala del recorrido

| Concepto | Desktop | Móvil |
|---|---:|---:|
| Paradas (suma de E) | 83.5 E | 85.5 E |
| Tránsitos entre pines (1 E cada uno, 21 pines) | 20 E | 20 E |
| FAQ + footer (flujo normal) | ~2–3 E | ~3–4 E |
| **Total aproximado** | **~106 E** | **~109 E** |

1 E = una pantalla de scroll. Hay unos 80 puntos de snap: cada gesto de scroll lleva a la siguiente parada.

**Decisión 1 (abajo):** con los E iniciales del sistema, el recorrido dura ~106 pantallas. Con E más cortos bajaría a ~87 pantallas:
- golpe 1.0;
- dos tiempos 1.25;
- lectura, puente, escena y panel 0.8;
- diálogo 3.

## 2. Decisiones de estructura aplicadas

- **Orden:** el del copy, sin reordenar nada. La auditoría lo confirma en desktop y en móvil.
- **Una parada = un encuadre.** Ninguna parada pasa de ~100 palabras y ningún párrafo se parte entre paradas. La ocupación estimada en móvil de 360 × 612 queda por debajo del 85 % en todas, salvo la conversación de ejemplo (07.4, ~91 %). La página mide el valor real.
- **Golpes:** tamaño según el encuadre (regla de Fase 1). Hay un lapidario por capítulo; los secundarios bajan un paso. Única excepción: 12.4, 6 líneas en móvil 360, anotada.
- **Escenario oscuro:** 5 bisagras exactas:
  - 01.3–01.4 «La cinco. No te escucha.»;
  - 03.5 «Alguien les dijo…»;
  - 05.7 «El control caduca. / El criterio no.»;
  - 10.5 la cita del niño;
  - 12.7 «Presencia, no vigilancia. / Criterio, no candado.».
- **Imágenes:** solo donde sellan un concepto ya argumentado (VISION §1.1). El Hero es la excepción.

  | Capítulo | Escena elegida | Alternativa |
  |---|---|---|
  | Hero | 01-dinner | — |
  | 02 | 02-facial-recognition (candado + reloj en pantalla) | 02-facial-recognition-alt |
  | 03 (mitad) | 03-eyes | 03-eyes-wide |
  | 03 (final) | 04-shield | — |
  | 05 | 05-crossing | 05-crossing-alt |
  | 08 | 06-rules | 06-rules-alt |
  | 10 | 07-together-mother-daughter | 07-together-father-son |
  | 12 | 08-autonomy-father | 08-autonomy-mother |

  Los caps. 01, 04, 06, 07, 09 y 11 no llevan imagen.
- **Capítulos de respiro** (04, 06, 09; 11 transaccional): solo composiciones L, sin acento, sin oscuro y sin imagen.
- **Contradicción de VISION, resuelta con §1.1/§5:** los caps. 04 y 06 no llevan golpe. Las candidatas de §4 («Tu instinto no está roto…», «El criterio se construye con preguntas…») quedan dentro de su párrafo, completas.
- **«El control caduca. El criterio no.»** se compone como B03 en dos tiempos (lead «El control caduca.» → cierre «El criterio no.»). Es la misma línea, en el mismo orden: el B03 del espécimen hace exactamente esto con esta frase.

## 3. Estrategia contra la densidad

- **Acordeón:** solo el FAQ, con las 7 preguntas cerradas para que se escaneen de un vistazo.
- **Primer CTA:** el salto que ya trae el copy en 09.3 (misma lámina que la lectura), «Si ya viste suficiente, la inscripción está al final de esta página ↓», que lleva a 11.1. Los botones aparecen donde los pone el copy: 11.6 y 12.4 (en la misma lámina que su texto).
- **CTA flotante en móvil:** no se agrega por defecto, porque repetiría las etiquetas del copy en lugares donde el copy no las puso (decisión 2).
- **Progreso:** la línea de 3 px del sistema (decisión 6 de la Fase 1). En el wireframe, la regla lateral hace ese papel y además muestra la escala.
- **Anclas:** solo `#inscripcion`, la que trae el copy.
- **Escaneo de 3 s (★):** golpes, títulos, citas-eco del cap. 02, la lista 01–05, el diálogo, el dato, los precios, el par de CTA y el FAQ.

## 4. Responsive (cambios de agrupamiento, no solo de tamaño)

| Bloque | Desktop | Móvil |
|---|---|---|
| Reglas de ADA (08.5) | 1 parada, 3 columnas | 1 parada (08.5m): en tablet, las tres una debajo de otra; en móvil < 600 px, mazo apilado (cada tarjeta sube y deja asomada la anterior por su subtítulo) |
| Inscripción fundadora (11.3) | 2 paradas de tarjetas (4 + 3), cada grupo en una fila | 2 paradas (11.3m con el título + 4 tarjetas; 11.3bm, 3 tarjetas). Tablet: una debajo de otra; móvil < 600 px: mazo apilado |
| Lectura + precio (11.4) | 1 lámina: lectura en la columna ancha y las dos piezas de precio debajo | 2 paradas (11.4m, 11.5m): juntas no caben en el teléfono |
| Citas-eco del cap. 02 (L05) | Cita a la izquierda (5 col), prosa a la derecha (7 col) | Apiladas, con separador arriba |
| Par de CTA | Lado a lado, mismo ancho | Apilados a todo el ancho, en el orden del copy |
| Precio | Dos piezas lado a lado | Apiladas |
| Escena | Cubre el encuadre | A sangre en ancho, centrada |

## 5. Intención de interacción (apple-design §1, §2, §3, §7)

| Componente | Feedback inmediato | Interrumpible | Entra / sale |
|---|---|---|---|
| Par de CTA | Sí, `scale(.97)` en `pointerdown` | — (un toque) | — (destinos pendientes) |
| Botón a la inscripción (09.3) | Sí, al tocar | Sí: el scroll animado se corta si el usuario hace scroll | Baja a 11.1; se regresa con scroll normal |
| Acordeón FAQ | Sí, el indicador se encoge en `pointerdown` | Sí, apertura y cierre a medio camino | Abre hacia abajo, cierra por el mismo camino |
| Carrusel del cap. 02 | — (lo mueve el scroll, no se arrastra) | Sí, scrub reversible y snap por panel | Entra por la derecha; al regresar sale por la derecha |
| Diálogo ADA / HIJO | — | Sí (scrub) | ADA por la izquierda, HIJO por la derecha; al regresar salen por su mismo lado |
| Snap de paradas | — | Sí: el usuario puede seguir de largo | — |
| Hero | — | Se repite al volver (onEnterBack) | Zoom-out → velo → texto |

## 6. Decisiones para ti

1. **Largo del recorrido:** ~106 E con los valores iniciales, o ~87 E con E más cortos (§1). *Por defecto: los iniciales, y se calibra en el prototipo de la Fase 3.* Recorrerlo en el wireframe es la mejor forma de decidirlo.
2. **CTA flotante en móvil:** *por defecto no* (duplicaría copy). La alternativa es que aparezca después del cap. 07, con las dos etiquetas del copy.
3. **Escenas:** las elegidas de la tabla de §2, o cualquiera de sus alternativas.
4. **12.4 en 6 líneas** en móvil 360: se acepta la excepción, o se baja ese golpe a `heading`, lo que lo sacaría del grupo B.
5. **Pines de máximo 6 paradas** (regla de v2): generan 20 tránsitos de 1 E. Subir el máximo a 8 quitaría unos 5 tránsitos, a cambio de pines más largos y frágiles. *Por defecto: 6.*

## 7. Partitura completa (pin → parada)

La genera `wireframe-src/build.py` desde `content.py`; no la edites a mano.

<!-- PARTITURA:INICIO -->
| Pin | Parada | Composición | E | Marcas | Intención |
|---|---|---|---:|---|---|
| P-H0 | H.1 | Hero | 1.5 | ★ | Autoplay (no scrub): zoom-out extremo de 01-dinner en 3.7 s → pausa → velo → aparece la frase en semimonumental. Desktop con su propia configuración: texto abajo a la izquierda (7 columnas, 3 líneas, 24 % del encuadre) y velo solo en el tercio inferior, para no tapar las caras. Móvil: centrado, 4 líneas. Se repite al regresar (onEnterBack). Al final aparece el indicador de continuar. |
| P-H | H.2 | B01 | 1.25 | ★ | Golpe lapidario del Hero. Composición B01 literal del espécimen (mismas dos frases). El caption va en ink (decisión 2). |
| P-H | H.3 | Puente (lead) | 1 |  | Puente solo, en la línea lead de B03. Empuja hacia el cap. 01. |
| P-01 | 01.1 | B01 (secundario) | 1.25 | ★ | Título = golpe (confirmado). Secundario → baja un paso: semimonumental. |
| P-01 | 01.2 | L03 | 1 | ★ | L03 = la lista 01–05. La fila 05 recibe el acento del espécimen recién al salir de la parada (anticipa la revelación, no la delata antes). |
| P-01 | 01.3 | B03 (revelación en tres tiempos) | 1.75 | ★ oscuro | Bisagra 1 (oscuro). Tres tiempos (pedido del usuario): 1) el puente solo; 2) el puente se desvanece y aparece «La cinco.» (semimonumental, solo señala); 3) cae «No te escucha.» (monumental, revela, con acento). Puente y revelación ocupan el mismo lugar: nunca hay más de dos tamaños en pantalla. |
| P-01 | 01.4 | B01 (golpe + remate) | 1.25 | oscuro | Sigue en oscuro. Gramática «golpe + remate», como H.2: «Pero no por lo que crees.» es el giro (grande); «Y ahí es donde se pone interesante.» solo anuncia (remate). Al salir vuelve la luz. |
| P-01 | 02.1 | B01 (título en display) | 1 | ★ | Título en semimonumental con la gramática de los títulos que golpean (B01, centrado). Camino de triángulos centrado abajo, fuera del bloque del título (así no hereda su transform ni choca con el texto). |
| P-02b | 02.2 | L05 (cita-eco + prosa) | 1 | ★ | Patrón 3+5: pin + desplazamiento horizontal. Cada panel llega y se estaciona el 70 % de su E; el paso al siguiente ocurre en el 30 % restante. Snap a la mitad de cada estacionamiento, sin inercia (corrección del usuario: antes cambiaba casi en automático). Panel 1/4. La cita-eco es micro-golpe de apertura del bloque. |
| P-02b | 02.3 | L05 | 1 | ★ | Panel 2/4. Entra desde la derecha; si regresas, sale por la derecha. |
| P-02b | 02.4 | L05 | 1 | ★ | Panel 3/4. |
| P-02b | 02.5 | L05 | 1 | ★ | Panel 4/4. «Aguanta. Ahorita llegamos ahí.» es el puente de cierre, pero vive dentro del párrafo: no se separa. |
| P-03a | 02.6 | Sello (zoom-in largo) | 1.5 |  | Sella el capítulo completo. Zoom-in largo con scroll (pedido del usuario): de 1× a 1.5× en 1.5 E, hacia el celular con el candado y el reloj; en el encuadre final siguen la cara del chico, el celular y parte de la laptop. El snap se detiene al terminar el zoom. La referencia usa «candados»; aquí la pantalla del celular muestra candado y reloj de arena (tiempo + contraseña). Alternativa: 02-facial-recognition-alt. |
| P-03a | 03.1 | L06 | 1 | ★ | Título-puente («Ahora…») + primera línea. |
| P-03a | 03.2 | L06 (título en voz de puente) | 1 |  | Gramática «puente + lectura»: el encabezado en el subhead del espécimen (Playfair 500 romana, 24/19; corrección del usuario); los párrafos en body (Inter), con negritas según el criterio editorial: la voz citada «ya lo sé… ¿y entonces qué hago?» y el remate que gira el argumento. |
| P-03a | 03.3 | B03 (cierre secundario) | 1.5 | ★ | Puente → golpe secundario (semimonumental). La escena lo sella en la siguiente parada. |
| P-03a | 03.4 | Secuencia con scrub (desktop) | 1.5 | solo desktop | Desktop: video con scrub (decisión del usuario). 49 cuadros WebP de 1280 px (3.0 MB) sacados de «initial_image»; el scroll recorre el gesto completo (mira el celular → ojos al techo → cabeza atrás) en 1.5 E y se estaciona al final. Póster = cuadro 64 (modo reducido y mientras carga). |
| P-03a | 03.4m | Sello (imagen fija) | 1 | solo móvil | Móvil y tablet: imagen fija (decisión del usuario: ahí el scrub de video es más frágil). PROVISIONAL: el cuadro más expresivo del video, hasta generar la imagen fija nueva. |
| P-03b | 03.5 | B03 | 1.5 | ★ oscuro | Bisagra 2 (oscuro). Lapidario del capítulo (confirmado). El lead termina en dos puntos: anuncia el corte. «no» y «cómo» en acento como antítesis (pedido del usuario, 2026-09-29): en el build, «no» en coral (la prohibición) y «cómo» en azul (el método). |
| P-03b | 03.6 | L07 | 1 |  | Vuelve la luz. Lectura. |
| P-03b | 03.7 | B01 (golpe dentro de párrafo) | 1.25 | ★ | Gramática «golpe dentro de párrafo» (layout de 03.7, 08.4 y 12.4): la primera frase paga la revelación del cap. 01 y va en grande y centrada (ajuste del usuario); el resto del párrafo sigue en la columna de lectura, 32/48 px debajo, en el mismo encuadre. |
| P-03b | 03.8 | Sello | 1 |  | Sella el capítulo: mamá e hija, cada una con su escudo, separadas. Cubre todo el contenedor en desktop, como las demás escenas (pedido del usuario, 2026-09-29; antes se mostraba completa con franjas). Movimiento: solo disolvencia de entrada, sin zoom (pedido del usuario). |
| P-04 | 04.1 | L06 | 1 | ★ | Capítulo de respiro: solo composiciones L, sin acento, sin oscuro, sin imagen. |
| P-04 | 04.2 | L07 | 1 |  | Lectura. |
| P-04 | 04.3 | L07 | 1 |  | Lectura. VISION §4 proponía un golpe aquí; se respeta §1.1/§5 (sin golpe) — ver decisión en 02-wireframe.md. |
| P-05a | 05.1 | L06 | 1 | ★ | Título-puente («Ahora sí:»). |
| P-05a | 05.2 | L07 | 1 |  | Lectura: la metáfora de cruzar la calle. |
| P-05a | 05.3 | B01 (golpe dentro de párrafo) | 1.25 | ★ | Mismo layout que 03.7 (pedido del usuario): la frase en semimonumental y centrada; el párrafo en la columna de lectura, 32/48 px debajo, en el mismo encuadre. |
| P-05a | 05.4 | B01 (golpe en dos alturas) | 1.5 | ★ | Golpe en dos alturas (pedido del usuario, mismo patrón que 01.3): «Bloquearle el celular es» señala → semimonumental; «no cruces». revela → monumental. Dos tiempos: primero lo que señala, al seguir scrolleando lo que revela. |
| P-05a | 05.5 | Secuencia con scrub (desktop) | 1.5 | solo desktop | Desktop: video con scrub (pedido del usuario), REPRODUCIDO AL REVÉS (pedido del usuario, 2026-09-29; se estaciona en el cuadro inicial del video, que es la escena fija): el feed de la calle fluye mientras la mamá señala. 49 cuadros WebP de 1280 px, calidad 50 (4.5 MB; el detalle de las fichas pesa más que en fastidio), sacados del video «Style_Hybrid…» (1908×1084, 5 s). Se estaciona al final. Sella la metáfora a mitad del capítulo; el lapidario viene después, sin imagen propia. |
| P-05a | 05.5m | Sello (imagen fija) | 1 | solo móvil | Móvil y tablet: imagen fija. Falta su versión vertical (00-context/scenes/vertical/05-crossing-v.webp). Alternativa: 05-crossing-alt. |
| P-05b | 05.6 | Puente (lead) | 1 |  | Puente solo que prepara la tesis. |
| P-05b | 05.7 | B06 (antítesis) | 1.25 | ★ oscuro | Bisagra 3 (oscuro). Tesis de la pieza. Gramática «antítesis»: la misma forma que el cierre de marca (12.7), dos líneas iguales con acento en la segunda, para que al final el lector reconozca la tesis en «Presencia, no vigilancia. / Criterio, no candado.». |
| P-05b | 05.8 | B03 (entrada → revelación) | 1.5 | ★ | Vuelve la luz. La frase se parte en entrada y revelación (pedido del usuario): «lo que le hayas enseñado antes.» en semimonumental, un paso abajo de la tesis (05.7, monumental) para no competir con ella. |
| P-06 | 06.1 | L06 | 1 | ★ | Respiro: solo L. |
| P-06 | 06.2 | L07 | 1 |  | Lectura. |
| P-06 | 06.3 | L07 | 1 |  | Lectura. VISION §4 proponía golpe con la primera frase; está dentro del párrafo y el capítulo es de respiro — ver decisión. |
| P-06 | 06.4 | L07 | 1 |  | Lectura. |
| P-06 | 06.5 | Puente (lead) | 1 |  | Puente de cierre hacia ADA. |
| P-07a | 07.1 | Presentación de ADA (texto 7 col + ADA 5 col) | 1 | ★ | ADA de la versión A (copiada sin modificar A; sin su animación de chat). Texto a la izquierda y ADA a la derecha (pedido del usuario). Desktop: el saludo se reproduce SOLO, en tiempo real (130 cuadros a 24 fps ≈ 5.4 s), cuando la parada entra en pantalla, y se repite al regresar. No va atado al scroll: con scrub era demasiado sensible (ajuste del usuario); es un gesto de un solo uso, como el Hero. Móvil y tablet: primer cuadro fijo, abajo del párrafo, sin descargar el resto. |
| P-07a | 07.2 | L07 | 1 |  | Lectura. |
| P-07a | 07.3 | L07 | 1 |  | Lectura. |
| P-07a | 07.4 | Diálogo | 4 | ★ | Un mensaje por paso de scroll (4 snaps). ADA entra por la izquierda, HIJO por la derecha; al regresar salen por el mismo lado. Avatares como en la versión A (pedido del usuario): cuadrados de 34 px con radio 10, ADA a la izquierda y el hijo a la derecha; imágenes de A copiadas sin modificar A. Burbujas: tinte violeta (ADA) / cian (HIJO) en el build. |
| P-07c | 07.5 | B01 (golpe en dos alturas, tres tiempos) | 1.75 | ★ | Lapidario del capítulo (ajuste del usuario): «Una pausa.» y «Una consecuencia.» en semimonumental, una por línea; «Una idea propia.» completa en monumental, con el acento subrayado en «idea propia.». Patrón «golpe en dos alturas» en tres tiempos: cada frase aparece al seguir scrolleando y «idea propia.» cae al final. |
| P-07c | 07.6 | Evolución (de → a, dos columnas) | 1.5 | ★ | Evolución en dos columnas (pedido del usuario): el antes en Playfair 400 y el después en Playfair 800; en medio, el «a» del copy con una flecha que se dibuja (→ en desktop, ↓ en móvil). Entra en tiempos: frase → antes → flecha → después. Mismas palabras, mismo orden. |
| P-07c | 07.7 | L07 | 1 |  | Lectura. Sin pausa de cierre: fluye directo al cap. 08 (como en la referencia). |
| P-08a | 08.1 | B01 (secundario) | 1.25 | ★ | Título = golpe (confirmado), semimonumental. Es la objeción del lector entre «»: va en voz citada (itálica), como las creencias del cap. 02. |
| P-08a | 08.2 | L07 | 1 |  | Lectura con columna ancha (~60 caracteres por línea; pedido del usuario: con ~88 palabras la columna estándar quedaba angosta y muy alta). En móvil, igual que las demás. |
| P-08a | 08.3 | B09 | 1.25 | ★ | Dato = Registro B (confirmado). B09: el numeral en su lugar dentro de la frase, sin duplicarlo ni reordenar. Lapidario del capítulo. Candidato a patrón 10 (contador). |
| P-08a | 08.4 | B01 (golpe dentro de párrafo) | 1.25 | ★ | Gramática «golpe dentro de párrafo» (layout de 12.4): «No es que vaya a pasar. Ya está pasando.» en grande; el resto del párrafo en lectura, mismo encuadre. |
| P-08b | 08.5 | L08 | 1 | ★ solo desktop | Tres tarjetas separadas (pedido del usuario): subtítulo (subhead Playfair) + párrafo; «Conocer las reglas de ADA ↗» como botón secundario; la tercera lleva el título «Práctica y breve», adición de copy aprobada por el usuario. Desktop: tres columnas. |
| P-08b | 08.5m | L08 (mazo apilado) | 1.75 | ★ solo móvil | Móvil y tablet: las tres tarjetas en la MISMA parada (pedido del usuario). Tablet (600–859 px): caben juntas; aparecen una debajo de otra con el scroll. Móvil (< 600 px): no caben (~150 % a 360 px), así que van en mazo apilado (decisión del usuario; patrón 3 + 8 del catálogo): el título se queda, cada tarjeta sube desde abajo y se apila sobre la anterior, que queda asomada por su subtítulo. Snap por tarjeta. Al volver hacia arriba reaparece el botón «Conocer las reglas de ADA ↗» de la primera tarjeta. |
| P-09 | 09.1 | B01 (golpe en dos alturas) | 1.5 | ★ | Golpe en dos alturas (pedido del usuario, mismo patrón que 01.3 y 05.4): «Y la prueba no te la pido por fe.» señala → semimonumental; «Habla tú con ADA primero.» revela → monumental. Dos tiempos. |
| P-09 | 09.2 | Sello | 1 |  | El papá con la tableta, después de «Habla tú con ADA primero.» (pedido del usuario, 2026-09-29; antes sellaba las reglas en 08.6). Sin zoom, solo disolvencia de entrada (pedido del usuario). Alternativa: 06-rules-alt. |
| P-09 | 09.3 | L07 + botón + puente | 1.25 | ★ | UNA sola lámina (pedido del usuario): lectura en la columna ancha (como 08.2), y debajo, centrados a lo ancho (pedido del usuario), el botón secundario (mismo estilo que «Conocer las reglas de ADA ↗») y el texto debajo. PRIMER CTA del recorrido: el salto a la inscripción que ya trae el copy. Toque → feedback inmediato; el scroll animado se interrumpe si el usuario hace scroll. El puente empalma con el título del cap. 10. |
| P-10a | 10.1 | B03 | 1.5 | ★ | Título + primera línea = un solo golpe (confirmado). Rima con «Ya lo tienes.» (12.2): los dos momentos en que la pieza le devuelve el protagonismo al papá van en monumental-xl. |
| P-10a | 10.2 | L07 | 1 |  | Lectura en la columna ancha (pedido del usuario, como 08.2 y 09.2). «Los incluye a los dos.» sigue corrido, en negrita (se probó aparte y se revirtió: se leía como subtítulo). |
| P-10a | 10.3 | L04 (cita + remate) | 1 | ★ | L04: la cita en voz citada a semimonumental (Playfair 700 itálica, como las citas-eco del cap. 02; pedido del usuario); el remate debajo en lectura, con aire amplio de 32/48 px (pedido del usuario). No se inventa fuente. |
| P-10a | 10.4 | B03 (puente → golpe) | 1.5 |  | Puente → golpe (pedido del usuario, mismo layout que 05.8): el puente en voz lead; «El criterio que lo cuida es el mismo puente que te lo regresa.» cae después en semimonumental. |
| P-10b | 10.5 | B03 | 1.5 | ★ oscuro | Bisagra 4 (oscuro). Lapidario (confirmado). Semimonumental porque en monumental serían 6 líneas en móvil 360. Habla el niño: voz citada (itálica). En el build va en coral, «para que se sienta» (pedido del usuario, 2026-09-29; antes: sin acento). |
| P-10b | 10.6 | L07 | 1 |  | Vuelve la luz. Lectura en la columna ancha (pedido del usuario, como 08.2, 09.2 y 10.2). |
| P-10b | 10.7 | Sello | 1 |  | Sella el capítulo más emocional: mamá e hija juntas, celulares boca abajo. Sin zoom, solo disolvencia de entrada (pedido del usuario). Alternativa: 07-together-father-son. |
| P-11a | 11.1 | L06 | 1 | ★ | Destino del ancla #inscripcion. Sin golpe B: capítulo transaccional. Columna ancha (pedido del usuario; regla por largo, párrafo de 240 caracteres). |
| P-11a | 11.2 | L06 (solo título) | 1 | ★ | Copy de venta punchy: NO entra en B (decisión Fase 1). Va como título Playfair 700. |
| P-11a | 11.3 | L08 (tarjetas) | 1 | ★ solo desktop | Tarjetas con título (pedido del usuario; mismo estilo que 08.5). El título de cada tarjeta es la primera frase de su viñeta, literal; el párrafo es el resto. Desktop: 4 tarjetas en una fila. |
| P-11a | 11.3b | L08 (tarjetas, cont.) | 1 | solo desktop | Desktop: las otras 3 tarjetas en una fila. |
| P-11a | 11.3m | L08 (mazo apilado) | 1.75 | ★ solo móvil | Móvil y tablet: las 4 tarjetas en una parada. Tablet: una debajo de otra. Móvil < 600 px: mazo apilado, como 08.5m. |
| P-11a | 11.3bm | L08 (mazo apilado, cont.) | 1.5 | solo móvil | Móvil y tablet: las otras 3 tarjetas, mismo comportamiento. |
| P-11b | 11.4 | L07 + título + bloque de precio | 1.25 | ★ solo desktop | UNA lámina (pedido del usuario): lectura con subtítulo del copy en la columna ancha y, debajo, las dos piezas de precio al ancho de esa columna. Monto en su lugar (Inter 800), nunca duplicado. El marcador gris = ámbar de valor en el build. |
| P-11b | 11.4m | L07 + título | 1 | ★ solo móvil | Móvil y tablet: juntas no caben en el teléfono (~125 % a 360 px), así que la lectura y el precio van en paradas seguidas. |
| P-11b | 11.5m | Bloque de precio | 1 | ★ solo móvil | Móvil y tablet: las dos piezas apiladas. |
| P-11b | 11.6 | Cierre de pago + garantía + par de CTA | 1 | ★ | Cierre del pago + garantía pegada al par de CTA, en la columna ancha; el par de botones mide lo mismo que la columna (pedido del usuario). Los dos botones pesan igual (en el build: azul / violeta). Feedback en pointerdown. Destinos pendientes. |
| P-12a | 12.1 | B01 (secundario) | 1.25 | ★ | Título = golpe y puente a la vez (confirmado). |
| P-12a | 12.2 | B03 | 1.5 | ★ | Lapidario del capítulo. Rima con «Eres tú.» (10.1): monumental-xl. |
| P-12a | 12.3 | Puente (lead) | 1 |  | Puente («Ahora…»). |
| P-12a | 12.4 | B01 (golpe dentro de párrafo) | 1.25 | ★ | El golpe son las dos primeras frases del párrafo; la tercera sigue en lectura dentro del MISMO encuadre (el párrafo no se parte entre paradas). Debajo, el par de CTA al ancho de la columna (pedido del usuario; antes era la parada 12.5). Semimonumental: 6 líneas en móvil 360 (excepción a la regla de ≤5, anotada). |
| P-12b | 12.6 | Sello | 1 |  | Pago visual de la metáfora: el hijo cruza solo, el papá observa sin celular. Alternativa: 08-autonomy-mother. |
| P-12b | 12.7 | B06 | 1.25 | ★ oscuro | Bisagra 5 (oscuro). B06: dos líneas, la segunda en acento itálico. Resumen de marca. |
| FAQ | — | Acordeón | flujo | ★ | Flujo normal (no pineado). Todas cerradas por defecto: las 7 preguntas se escanean de un vistazo. Toda la fila es el botón; feedback inmediato; abre hacia abajo y cierra por el mismo camino; se puede interrumpir. |
| FOOT | — | Footer | flujo | ★ | Flujo normal. «digizen» = logo oficial (00-context/logo/digizen-logo-light.svg; la auditoría lo lee de su alt). En gris en el wireframe; a color en la versión avanzada. Enlaces del copy: gnius.club y aviso de privacidad. |

**Totales:** paradas 86.00 E (desktop) / 87.75 E (móvil) · 21 pines → 20 E de tránsito · total aprox. 108 E desktop / 111 E móvil (con FAQ y footer).
<!-- PARTITURA:FIN -->

## 8. Auditoría fuente → wireframe

- **Copy de producción:** 151 segmentos de `COPY-PUBLICADO.md`, todos presentes literalmente y en orden, tanto en el recorrido desktop como en el móvil (auditoría automática de `wireframe-src/build.py`: **0 faltantes, 0 fuera de orden**).
- **Interpretaciones de maquetación** (aprobadas en la Fase 1, decisión 7):
  - El «·» entre los CTA es el espacio entre los dos botones.
  - `ADA` / `HIJO` son etiquetas de burbuja sin los dos puntos (así aparecen en el sitio de referencia).
  - Las escenas se encuadran sin editar los archivos, con bordes limpios (sin viñeta).
  - «digizen» del footer es el logo oficial (`00-context/logo/digizen-logo-light.svg`, `alt="digizen"`); la auditoría lo lee de su `alt`. El logo del Hero es decorativo (`alt=""`), no agrega texto. En el wireframe los logos van en gris; a color en la versión avanzada.
- **Notas internas conservadas fuera de la UI** (no son copy de página):
  - Etiqueta de sección «## Footer» (no aparece en el sitio de referencia).
  - Etiqueta «(FAQ)» del encabezado «Por si te quedó una duda. (FAQ)» (no aparece en el sitio de referencia).
  - Nota de procedencia al final del archivo: **Nota de procedencia:** este copy se extrajo del sitio renderizado en `Digizen-Cinco-Creencias-Diseno-2026-09-22/sitio/dist/index.html` (el usuario lo señaló como la versión más completa/adecuada — incluye el FAQ con respuestas completas, que `COPY-PUBLICADO.md` de iteraciones anteriores no tenía). Tratar como fuente de verdad literal: no omitir, resumir, parafrasear ni inventar contenido, por la regla de fidelidad de `Skills/landing-builder/SKILL.md`.
- **Adiciones de copy aprobadas por el usuario** (no están en `COPY-PUBLICADO.md`; en el wireframe llevan la etiqueta «copy agregado · aprobado» y la auditoría las lista aparte):
  - 08.5 / 08.5m · subtítulo **«Práctica y breve»** sobre «Con un tiempo definido para cada conversación. ADA no quiere sus horas. Quiere su criterio.». Pedido del 2026-09-28: «Agregar un titulo similar a 'Práctica y breve'». Redacción por confirmar.
- **Contenidos que faltan (contenedor marcado, sin inventar nada):**
  - Destino de «Inscribir a mi hijo ↗» (pago).
  - Destino de «Conversar con ADA primero»: el copy y los campos de la solicitud de acceso no están en la fuente. El FAQ lo menciona («para ver la solicitud de acceso»).
  - Documento enlazado en «Conocer las reglas de ADA ↗».
  - Texto `alt` de las escenas: se dejan decorativas (`alt=""`), como en el sistema de diseño, para no inventar texto.

## 9. Evaluación — Fase 2, ronda 1

Pesos: Purista 25 % · Arquitecto de Sistemas 20 % · Guardián de Lectura 55 %.

| Lente | Puntaje | Objeciones |
|---|---|---|
| Purista | 4.5/5 | Cada parada sale del catálogo del espécimen y cada imagen sella algo. Algunas paradas tienen muy poca ocupación a propósito (un puente solo, 9–18 %; la parada de solo título 02.1). Hay que confirmar en el recorrido que se sienten como pausa y no como vacío. |
| Arquitecto de Sistemas | 4.5/5 | Una sola fuente de datos, auditoría automática, E por parada y pines calculados con fórmula. Objeciones: (1) todavía no verifiqué el comportamiento en un navegador; (2) el tope de 6 paradas por pin fuerza 20 tránsitos. |
| Guardián de Lectura | 4/5 | Densidad resuelta: una idea por encuadre, ~100 palabras como máximo, escaneo marcado y todas las paradas caben. Objeciones: (1) el recorrido es largo (~106 E, ~80 gestos) para tráfico frío (decisión 1); (2) el primer CTA llega en 09.3, a ~60 % del recorrido, porque así lo decide el copy (decisión 2); (3) la conversación queda justa en móvil de 360 (~91 %). |

**Puntaje ponderado:** 0.25 × 4.5 + 0.20 × 4.5 + 0.55 × 4 = **4.2 / 5**
**Resultado:** aprobado internamente.

---

¿Apruebas este layout y arquitectura de información para pasar a la Fase 3 (build), o ajustamos el orden/estructura primero?
