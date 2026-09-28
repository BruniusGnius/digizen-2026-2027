---
project: digizen-landing-b-v04-claude
fase: 2 - wireframe
estado: propuesto
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
- **Primer CTA:** el salto que ya trae el copy en 09.3, «Si ya viste suficiente, la inscripción está al final de esta página ↓», que lleva a 11.1. Los botones aparecen donde los pone el copy: 11.6 y 12.5.
- **CTA flotante en móvil:** no se agrega por defecto, porque repetiría las etiquetas del copy en lugares donde el copy no las puso (decisión 2).
- **Progreso:** la línea de 3 px del sistema (decisión 6 de la Fase 1). En el wireframe, la regla lateral hace ese papel y además muestra la escala.
- **Anclas:** solo `#inscripcion`, la que trae el copy.
- **Escaneo de 3 s (★):** golpes, títulos, citas-eco del cap. 02, la lista 01–05, el diálogo, el dato, los precios, el par de CTA y el FAQ.

## 4. Responsive (cambios de agrupamiento, no solo de tamaño)

| Bloque | Desktop | Móvil |
|---|---|---|
| Reglas de ADA (08.5) | 1 parada, 3 columnas | 2 paradas (08.5a, 08.5b) |
| Inscripción fundadora (11.3) | 2 paradas (4 + 3 viñetas) | 3 paradas (2 + 3 + 2) |
| Citas-eco del cap. 02 (L05) | Cita a la izquierda (5 col), prosa a la derecha (7 col) | Apiladas, con separador arriba |
| Par de CTA | Lado a lado, mismo ancho | Apilados a todo el ancho, en el orden del copy |
| Precio | Dos piezas lado a lado | Apiladas |
| Escena | Cubre el encuadre | A sangre en ancho, centrada |

## 5. Intención de interacción (apple-design §1, §2, §3, §7)

| Componente | Feedback inmediato | Interrumpible | Entra / sale |
|---|---|---|---|
| Par de CTA | Sí, `scale(.97)` en `pointerdown` | — (un toque) | — (destinos pendientes) |
| Enlace a la inscripción (09.3) | Sí, al tocar | Sí: el scroll animado se corta si el usuario hace scroll | Baja a 11.1; se regresa con scroll normal |
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

| Pin | Parada | Composición | E | Marcas | Intención |
|---|---|---|---:|---|---|
| P-H0 | H.1 | Hero | 1.5 | ★ | Secuencia autoplay (no scrub): zoom-out extremo de 01-dinner → pausa → velo → aparece la frase. Se repite si regresas a este punto (onEnterBack). Sin texto de 'scroll'. |
| P-H | H.2 | B01 | 1.25 | ★ | Golpe lapidario del Hero. Composición B01 literal del espécimen (mismas dos frases). El caption va en ink (decisión 2). |
| P-H | H.3 | Puente (lead) | 1 |  | Puente solo, en la línea lead de B03. Empuja hacia el cap. 01. |
| P-01 | 01.1 | B01 (secundario) | 1.25 | ★ | Título = golpe (confirmado). Secundario → baja un paso: semimonumental. |
| P-01 | 01.2 | L03 | 1 | ★ | L03 = la lista 01–05. La fila 05 recibe el acento del espécimen recién al salir de la parada (anticipa la revelación, no la delata antes). |
| P-01 | 01.3 | B03 | 1.5 | ★ oscuro | Bisagra 1 (oscuro). Dos tiempos: puente → golpe lapidario por corte. |
| P-01 | 01.4 | B01 (secundario) | 1.25 | oscuro | Sigue en oscuro. Golpe secundario (semimonumental, 4 líneas en móvil 360). Al salir vuelve la luz. |
| P-01 | 02.1 | L06 (solo título) | 1 | ★ | Título A. Parada corta que abre el carrusel. |
| P-02b | 02.2 | L05 (cita-eco + prosa) | 1 | ★ | Patrón 3+5: pin + desplazamiento horizontal (ease none), snap por panel. Panel 1/4. La cita-eco es micro-golpe de apertura del bloque. |
| P-02b | 02.3 | L05 | 1 | ★ | Panel 2/4. Entra desde la derecha; si regresas, sale por la derecha. |
| P-02b | 02.4 | L05 | 1 | ★ | Panel 3/4. |
| P-02b | 02.5 | L05 | 1 | ★ | Panel 4/4. «Aguanta. Ahorita llegamos ahí.» es el puente de cierre, pero vive dentro del párrafo: no se separa. |
| P-03a | 02.6 | Sello | 1 |  | Sella el capítulo completo. La referencia usa «candados»; aquí la pantalla del celular muestra candado y reloj de arena (tiempo + contraseña). Alternativa: 02-facial-recognition-alt. |
| P-03a | 03.1 | L06 | 1 | ★ | Título-puente («Ahora…») + primera línea. |
| P-03a | 03.2 | L06 (título en voz de puente) | 1 |  | La pregunta va en la línea lead de B05 (Playfair 600, heading). Dos párrafos de lectura debajo. |
| P-03a | 03.3 | B03 (cierre secundario) | 1.5 | ★ | Puente → golpe secundario (semimonumental). La escena lo sella en la siguiente parada. |
| P-03a | 03.4 | Sello | 1 |  | Sella el beat de «los ojos al techo» (primera de las dos imágenes del capítulo). Alternativa: 03-eyes-wide. |
| P-03b | 03.5 | B03 | 1.5 | ★ oscuro | Bisagra 2 (oscuro). Lapidario del capítulo (confirmado). El lead termina en dos puntos: anuncia el corte. |
| P-03b | 03.6 | L07 | 1 |  | Vuelve la luz. Lectura. |
| P-03b | 03.7 | L07 | 1 |  | Lectura. Va aparte de 03.6: juntos pasan de ~100 palabras. |
| P-03b | 03.8 | Sello | 1 |  | Sella el capítulo: mamá e hija, cada una con su escudo, separadas. |
| P-04 | 04.1 | L06 | 1 | ★ | Capítulo de respiro: solo composiciones L, sin acento, sin oscuro, sin imagen. |
| P-04 | 04.2 | L07 | 1 |  | Lectura. |
| P-04 | 04.3 | L07 | 1 |  | Lectura. VISION §4 proponía un golpe aquí; se respeta §1.1/§5 (sin golpe) — ver decisión en 02-wireframe.md. |
| P-05a | 05.1 | L06 | 1 | ★ | Título-puente («Ahora sí:»). |
| P-05a | 05.2 | L07 | 1 |  | Lectura: la metáfora de cruzar la calle. |
| P-05a | 05.3 | L06 (título en voz de puente) | 1 |  | Puente (línea lead de B03) + lectura. |
| P-05a | 05.4 | B01 (secundario) | 1.25 | ★ | Golpe intermedio, secundario (semimonumental). |
| P-05a | 05.5 | Sello | 1 |  | Sella la metáfora a mitad del capítulo. El lapidario viene después, sin imagen propia. Alternativa: 05-crossing-alt. |
| P-05b | 05.6 | Puente (lead) | 1 |  | Puente solo que prepara la tesis. |
| P-05b | 05.7 | B03 | 1.5 | ★ oscuro | Bisagra 3 (oscuro). Tesis de la pieza. B03 del espécimen: lead «El control caduca.» → cierre «El criterio no.» (misma línea del copy, en dos tiempos). |
| P-05b | 05.8 | L07 | 1 |  | Vuelve la luz. Una sola frase de lectura cierra el capítulo. |
| P-06 | 06.1 | L06 | 1 | ★ | Respiro: solo L. |
| P-06 | 06.2 | L07 | 1 |  | Lectura. |
| P-06 | 06.3 | L07 | 1 |  | Lectura. VISION §4 proponía golpe con la primera frase; está dentro del párrafo y el capítulo es de respiro — ver decisión. |
| P-06 | 06.4 | L07 | 1 |  | Lectura. |
| P-06 | 06.5 | Puente (lead) | 1 |  | Puente de cierre hacia ADA. |
| P-07a | 07.1 | L06 | 1 | ★ | Título A + primer párrafo. |
| P-07a | 07.2 | L07 | 1 |  | Lectura. |
| P-07a | 07.3 | L07 | 1 |  | Lectura. |
| P-07a | 07.4 | Diálogo | 4 | ★ | Un mensaje por paso de scroll (4 snaps). ADA entra por la izquierda, HIJO por la derecha; al regresar salen por el mismo lado. Burbujas: tinte violeta (ADA) / cian (HIJO) en el build. |
| P-07c | 07.5 | B01 | 1.25 | ★ | Lapidario del capítulo: staccato de tres tiempos (candidato a SplitText por frase, patrón 9). |
| P-07c | 07.6 | L07 | 1 |  | Lectura. |
| P-07c | 07.7 | L07 | 1 |  | Lectura. Sin pausa de cierre: fluye directo al cap. 08 (como en la referencia). |
| P-08a | 08.1 | B01 (secundario) | 1.25 | ★ | Título = golpe (confirmado). Secundario: semimonumental. |
| P-08a | 08.2 | L07 | 1 |  | Lectura (~88 palabras: al límite de un encuadre móvil). |
| P-08a | 08.3 | B09 | 1.25 | ★ | Dato = Registro B (confirmado). B09: el numeral en su lugar dentro de la frase, sin duplicarlo ni reordenar. Lapidario del capítulo. Candidato a patrón 10 (contador). |
| P-08a | 08.4 | Puente (lead) | 1 |  | El puente («No es que vaya a pasar. Ya está pasando.») abre un párrafo que no se parte: todo el párrafo va en voz lead. |
| P-08b | 08.5 | L08 | 1 | ★ solo desktop | Desktop: una parada, tres columnas. Viñetas completas; la primera frase en 700 como etiqueta. |
| P-08b | 08.5a | L08 | 1 | ★ solo móvil | Móvil: la lista se reparte en dos paradas (juntas pasan de la capacidad del encuadre). Ninguna viñeta se corta. |
| P-08b | 08.5b | L08 (cont.) | 1 | solo móvil | Móvil, segunda parada de la lista. |
| P-08b | 08.6 | Sello | 1 |  | Sella la tranquilización: papá revisando las reglas. Alternativa: 06-rules-alt. |
| P-09 | 09.1 | L06 | 1 | ★ | Respiro instruccional: solo L. |
| P-09 | 09.2 | L07 | 1 |  | Lectura. |
| P-09 | 09.3 | Enlace + puente | 1 | ★ | PRIMER CTA del recorrido: el salto a la inscripción que ya trae el copy. Toque → feedback inmediato; el scroll animado se interrumpe si el usuario hace scroll. El puente empalma con el título del cap. 10. |
| P-10a | 10.1 | B03 | 1.5 | ★ | Título + primera línea = un solo golpe (confirmado). Dos tiempos. Secundario (el lapidario del capítulo es la cita del niño): cierre en monumental. |
| P-10a | 10.2 | L07 | 1 |  | Lectura. |
| P-10a | 10.3 | L04 (cita + remate) | 1 | ★ | L04: la cita en Playfair itálica; el remate debajo en lectura (no se inventa fuente). |
| P-10a | 10.4 | Puente (lead) | 1 |  | Párrafo completo en voz lead: arranca con el puente «Y aquí pasa algo que no te esperas.» |
| P-10b | 10.5 | B03 | 1.5 | ★ oscuro | Bisagra 4 (oscuro). Lapidario (confirmado). Semimonumental porque en monumental serían 6 líneas en móvil 360. Sin acento: la cita ya pesa sola. |
| P-10b | 10.6 | L07 | 1 |  | Vuelve la luz. Lectura. |
| P-10b | 10.7 | Sello | 1 |  | Sella el capítulo más emocional: mamá e hija juntas, celulares boca abajo. Alternativa: 07-together-father-son. |
| P-11a | 11.1 | L06 | 1 | ★ | Destino del ancla #inscripcion. Sin golpe B: capítulo transaccional. |
| P-11a | 11.2 | L06 (solo título) | 1 | ★ | Copy de venta punchy: NO entra en B (decisión Fase 1). Va como título Playfair 700. |
| P-11a | 11.3 | L08 | 1 | ★ solo desktop | Desktop: la lista de 7 se reparte en dos paradas (4 + 3). Viñetas completas. |
| P-11a | 11.3b | L08 (cont.) | 1 | solo desktop | Desktop, segunda parada de la lista. |
| P-11a | 11.3m1 | L08 | 1 | ★ solo móvil | Móvil: la lista de 7 se reparte en tres paradas. |
| P-11a | 11.3m2 | L08 (cont.) | 1 | solo móvil | Móvil, 2/3. |
| P-11a | 11.3m3 | L08 (cont.) | 1 | solo móvil | Móvil, 3/3. |
| P-11b | 11.4 | L07 + título | 1 | ★ | Lectura con subtítulo del copy. |
| P-11b | 11.5 | Bloque de precio | 1 | ★ | Dos piezas iguales (el párrafo que sigue pasa a 11.6 para no llenar el encuadre). Monto en su lugar (Inter 800), nunca duplicado. El marcador gris = ámbar de valor en el build. |
| P-11b | 11.6 | Cierre de pago + garantía + par de CTA | 1 | ★ | Cierre del pago + garantía pegada al par de CTA. Los dos botones pesan igual (en el build: azul / violeta). Feedback en pointerdown. Destinos pendientes. |
| P-12a | 12.1 | B01 (secundario) | 1.25 | ★ | Título = golpe y puente a la vez (confirmado). |
| P-12a | 12.2 | B03 | 1.5 | ★ | Lapidario del capítulo, en paralelo con «Eres tú.» (cap. 10). |
| P-12a | 12.3 | Puente (lead) | 1 |  | Puente («Ahora…»). |
| P-12a | 12.4 | B01 (secundario, a la izquierda) | 1.25 | ★ | El golpe son las dos primeras frases del párrafo; la tercera sigue en lectura dentro del MISMO encuadre (el párrafo no se parte entre paradas). Semimonumental: 6 líneas en móvil 360 (excepción a la regla de ≤5, anotada). |
| P-12b | 12.5 | Par de CTA | 1 | ★ | Parada de decisión: solo los dos botones, mismo peso. |
| P-12b | 12.6 | Sello | 1 |  | Pago visual de la metáfora: el hijo cruza solo, el papá observa sin celular. Alternativa: 08-autonomy-mother. |
| P-12b | 12.7 | B06 | 1.25 | ★ oscuro | Bisagra 5 (oscuro). B06: dos líneas, la segunda en acento itálico. Resumen de marca. |
| FAQ | — | Acordeón | flujo | ★ | Flujo normal (no pineado). Todas cerradas por defecto: las 7 preguntas se escanean de un vistazo. Toda la fila es el botón; feedback inmediato; abre hacia abajo y cierra por el mismo camino; se puede interrumpir. |
| FOOT | — | Footer | flujo | ★ | Flujo normal. «digizen» = logo (00-context/logo/digizen-logo-light.svg). Enlaces del copy: gnius.club y aviso de privacidad. |

## 8. Auditoría fuente → wireframe

- **Copy de producción:** 151 segmentos de `COPY-PUBLICADO.md`, todos presentes literalmente y en orden, tanto en el recorrido desktop como en el móvil (auditoría automática de `wireframe-src/build.py`: **0 faltantes, 0 fuera de orden**).
- **Interpretaciones de maquetación** (aprobadas en la Fase 1, decisión 7):
  - El «·» entre los CTA es el espacio entre los dos botones.
  - `ADA` / `HIJO` son etiquetas de burbuja sin los dos puntos (así aparecen en el sitio de referencia).
  - Las escenas se encuadran y se funden con máscara, sin editar los archivos.
- **Notas internas conservadas fuera de la UI** (no son copy de página):
  - Etiqueta de sección «## Footer» (no aparece en el sitio de referencia).
  - Etiqueta «(FAQ)» del encabezado «Por si te quedó una duda. (FAQ)» (no aparece en el sitio de referencia).
  - Nota de procedencia al final del archivo: **Nota de procedencia:** este copy se extrajo del sitio renderizado en `Digizen-Cinco-Creencias-Diseno-2026-09-22/sitio/dist/index.html` (el usuario lo señaló como la versión más completa/adecuada — incluye el FAQ con respuestas completas, que `COPY-PUBLICADO.md` de iteraciones anteriores no tenía). Tratar como fuente de verdad literal: no omitir, resumir, parafrasear ni inventar contenido, por la regla de fidelidad de `Skills/landing-builder/SKILL.md`.
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
