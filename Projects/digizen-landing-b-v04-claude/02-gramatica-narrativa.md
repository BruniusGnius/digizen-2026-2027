---
project: digizen-landing-b-v04-claude
fase: 2 - wireframe
estado: propuesto
base: versión 1 (commit 5be8569). La iteración 2 se descartó y está guardada en git stash.
---

# Gramática narrativa del recorrido

## Principio

**Cada función narrativa tiene un layout, y se repite siempre igual.** El lector aprende la gramática: cuando ve ese layout, sabe qué tipo de momento es. La variación del ritmo la pone la historia (qué función aparece), no el cambio de composición.
- No se usan las 17 composiciones: se usan las que la narrativa necesita, y se repiten.
- Una columna de lectura repetida es consistencia, no monotonía.

La versión 1 ya seguía esta gramática sin haberla escrito. Este documento la nombra y corrige solo los puntos donde la v1 rompe su propia regla o lee mal el impacto de una frase.

## 1. La gramática: función → layout

| Función narrativa | Cómo se reconoce en el copy | Layout | Tamaño | Eje | Paradas (v1) |
|---|---|---|---|---|---|
| **Apertura de capítulo** | Título que presenta el tema | L06: título Playfair 700 + apoyo | heading | lectura | 02.1, 03.1, 04.1, 05.1, 06.1, 07.1, 09.1, 11.1, 11.2 |
| **Título que golpea** | Título que ya es sentencia (confirmado por ti) | B01 | semimonumental (N2) | centro | 01.1, 08.1, 12.1 |
| **Golpe** | Se sostiene sola y reencuadra | B01; si le sigue un anuncio, este va como remate chico debajo | semimonumental (N2) | centro | 01.4, 05.4 |
| **Lapidario** | El golpe principal del capítulo (uno) | B01 o B03 | monumental (N1). Es el único con acento; va en oscuro si es bisagra | centro | H.2, 01.3, 03.5, 05.7, 07.5, 10.5, 12.2, 12.7 |
| **Puente → golpe** | Una frase anuncia y la siguiente remata | B03 (entrada → cierre) | entrada en subhead; cierre del nivel del golpe | centro | 01.3, 03.3, 03.5, 05.7, 10.1, 10.5, 12.2 |
| **Puente solo** | Anuncia, pregunta o conecta («Ahora…», «Y…») | Línea lead: Inter 500 | subhead | centro | H.3, 05.6, 06.5, 08.4, 10.4, 12.3 |
| **Puente + lectura** | Un puente que abre un párrafo | Encabezado en subhead del espécimen (Playfair 500 romana) + L07 | subhead + body | lectura | 03.2 |
| **Lectura** | Narración, argumento | L07: columna de 38 caracteres | body | lectura | Todas las de lectura |
| **Golpe dentro de párrafo** | Frase de impacto que abre un párrafo que continúa | La frase en semimonumental, **centrada**; el resto del párrafo en la columna de lectura, 32/48 px debajo, en el mismo encuadre (ajuste del usuario, 2026-09-28) | semi + body | centro + lectura | 03.7, 05.3, 08.4, 12.4 |
| **Golpe en dos alturas** | Una parte del golpe solo señala y la otra revela («La cinco.» / «No te escucha.») | La parte que señala en semimonumental y la que revela en monumental, en dos tiempos: primero señala, luego revela (patrón del usuario, 2026-09-28) | semi → mon | centro | 01.3, 05.4 |
| **Voz citada** | Habla otro: el niño, la mamá, las creencias y objeciones del lector entre «» | Playfair itálica | según su nivel | — | 10.3 |
| **Presentación de ADA** | El momento en que aparece ADA («Esto se llama ADA.») | Texto a la izquierda (7 col) + ADA a la derecha (5 col). ADA es el personaje de la versión A (130 cuadros con transparencia, copiados sin modificar A): scrub del saludo en desktop, primer cuadro fijo en móvil | heading + body | lectura + figura | 07.1 |
| **Lista** | Creencias numeradas / elementos paralelos | L03 / L08 | — | — | 01.2 / 08.5, 11.3 |
| **Dato** | La cifra | B09 | monumental-xl | centro | 08.3 |
| **Antítesis** | Dos mitades con la misma estructura, en tensión | B06: dos líneas iguales, con acento en la segunda | monumental | centro | 12.7 |
| **Escena** | Sella un concepto ya argumentado | Pantalla completa | — | — | 02.6, 03.4, 03.8, 05.5, 08.6, 10.7, 12.6 |
| **Interfaz** | Diálogo, precio, CTA, FAQ | Los componentes de la Fase 1 | — | — | 07.4, 11.5, 11.6, 12.5, FAQ |

**Reglas que la sostienen:**
- **Dos tamaños de golpe:** N1 (lapidario) en monumental y N2 (golpe) en semimonumental. Solo se baja un paso si no cabe (5 líneas o menos, 60 % o menos del alto en el móvil de 360).
- **Dos ejes y nada más:**
  - el **centro**: golpes, puentes, citas;
  - el **eje de lectura**: el borde izquierdo de la columna de L07, que comparten las aperturas y los golpes dentro de párrafo.
- **Cada paso de la escala lleva la familia del espécimen:** body, small y micro en Inter; subhead y heading en Playfair romana (500 y 700); del semimonumental para arriba, Playfair 800–900. Las excepciones son solo las que trae una composición del espécimen (la entrada de B03 en Inter, los dos pesos de B08).
- **Una sola voz de puente** dentro de B03 (su entrada en Inter 500, subhead).
- **Acento y oscuro, solo en lapidarios.** Hay 5 bisagras.
- **En una composición de dos partes, lo grande es siempre lo de más impacto** (prueba de §2).

## 1b. Énfasis dentro de la lectura (criterio del usuario, 2026-09-28)

Sale de las marcas que hizo el usuario en el cap. 02. La lectura no debe quedar plana: se destacan las palabras clave del discurso, en su lugar y sin cambiar el texto.

| Qué se destaca | Cómo | Ejemplos (cap. 02) |
|---|---|---|
| **Las palabras de otros citadas dentro de un párrafo** (la evidencia) | Negrita (Inter 700), con sus comillas | «una hora y ya» · «falsa sensación de control» · «en dos días encontró cómo saltárselo» |
| **La acción del lector que se está desmontando** | Negrita | «Negociaste «una hora y ya».» |
| **El remate que cierra el argumento** | Negrita | «No es mala suerte. Es aritmética.» |
| **Un motivo que vuelve a lo largo de la pieza** | Negrita cada vez que aparece, para que el lector lo reconozca | «deja el cel» (03.3, 03.6, 06.3) |
| **El testimonio que un párrafo presenta con dos puntos** | **Cita aparte:** el párrafo se abre después de los «:»; la cita va en su propia línea, en voz citada (Playfair itálica), y el texto sigue en la línea siguiente | «Ni siquiera me mira a los ojos.» |


**Densidad (ajustada con el usuario, 2026-09-28):** se marcan fragmentos, no párrafos completos, y normalmente 2 o 3 por párrafo. En las viñetas ya va en negrita la etiqueta; solo se agrega un remate donde hace falta. No se marcan títulos, citas aparte ni el diálogo.

## 2. Prueba de impacto

Una frase pega si:
1. se sostiene sola;
2. concluye, en vez de anunciar;
3. contradice o reencuadra lo que el lector creía;
4. es la que el lector repetiría.

Si solo anuncia, pregunta o conecta, es un puente, y nunca va en grande.

## 3. Qué cambia respecto a la versión 1

Todo lo demás de la v1 se queda igual.

**A · La v1 rompe su propia gramática (correcciones)**
1. **03.2 «¿Qué sentiste?»** es el único puente en otra voz (Playfair 600, heading). Pasa a la voz de puente de todos los demás: Inter 500, subhead.
2. **Aperturas y lectura en el mismo eje.** Hoy las aperturas (L06) van pegadas al borde del contenedor y la lectura (L07) centrada: son dos ejes distintos. Las aperturas se alinean al borde izquierdo de la columna de lectura. 02.1 y 11.2 (solo título) estaban centradas y pasan al mismo eje.

**B · Impacto mal leído (correcciones)**

3. **01.4.** Hoy las dos frases van juntas en grande. Pasa a B01, igual que H.2: «Pero no por lo que crees.» en grande y «Y ahí es donde se pone interesante.» como remate chico.
4. **03.7 y 08.4.** «Por eso «no me escucha» era la única verdadera.» y «No es que vaya a pasar. Ya está pasando.» son golpes que hoy quedan enterrados. Pasan al layout que ya usa 12.4 (golpe dentro de párrafo). Se reutiliza, no se inventa nada.

**C · Rimas: el mismo layout donde la historia se repite (propuestas)**

5. **Voz citada en itálica**, como ya está 10.3: las creencias del lector (02.2–02.5), su objeción (08.1) y el niño (10.5). Cuando habla otro, se ve igual en toda la pieza.
6. **La tesis con la forma del cierre.** 05.7 pasa a B06, como 12.7: «El control caduca. / El criterio no.» ↔ «Presencia, no vigilancia. / Criterio, no candado.». Al final, el lector reconoce en el cierre de marca la tesis que leyó en el cap. 05.
7. **«Eres tú.» (10.1) y «Ya lo tienes.» (12.2) en monumental-xl, las dos.** Son los dos momentos en que la pieza le devuelve el protagonismo al papá: misma forma, misma rima. Es la única excepción de tamaño, y tiene una razón narrativa.

**D · Decisiones tuyas**

8. **12.4:** ¿las dos frases en grande, como hoy, o solo «La diferencia es que ésa no tiene botón de cancelar.»?
9. **Remate en párrafo** (Inter 700 en su lugar, máximo uno por parada, ~18 frases): ¿sí o no? Si es sí, va en todas las paradas de lectura por igual. Si es no, la lectura queda limpia, como en la v1.

## Anexo · Negritas aplicadas (por parada)

Generado desde `wireframe-src/content.py`. Para quitar una, dímelo por ID.

| Parada | Fragmentos en negrita |
|---|---|
| H.2 | «te va a doler.» |
| 02.2 | «Negociaste «una hora y ya».» |
| 02.3 | «falsa sensación de control» |
| 02.4 | «en dos días encontró cómo saltárselo» · «No es mala suerte. Es aritmética.» |
| 03.2 | «ya lo sé… ¿y entonces qué hago?» · «Porque te acabo de hacer exactamente lo que tú le haces a él.» |
| 03.3 | «ya deja el cel» |
| 03.5 | «Tú sientes angustia. Él ya está harto de oírlo.» |
| 03.6 | «el candado no sirve» · «deja el cel» · «no» no se construye nada · «Solo un hijo que busca el «cómo»» |
| 03.7 | «un «no» sin «cómo» no le deja nada que hacer» · «un candado abierto en dos días» |
| 04.1 | «como papá que también trae el celular en la mano» |
| 04.2 | «Nadie te dio el manual.» · «lo hiciste por amor» |
| 04.3 | «Tu instinto no está roto.» · «Suéltate la culpa.» |
| 05.2 | «cruzar la calle» · «Miras a los dos lados.» · «Lo haces para que un día cruce sin ti.» |
| 05.3 | «se para en la banqueta sin saber mirar» · «Solo le dijeron que no.» |
| 05.6 | «el día en que cruce solo va a llegar» |
| 05.8 | «lo que le hayas enseñado antes» |
| 06.1 | «más lenta que un candado» |
| 06.2 | «no» sin «cómo» · «alguien te hizo una pregunta» |
| 06.3 | «El criterio se construye con preguntas.» · «deja el cel» |
| 06.4 | «Salen en una conversación.» · «tú no puedes estar ahí en cada momento» |
| 06.5 | «sí hay alguien que puede estar ahí» |
| 07.1 | «un mentor de inteligencia artificial que le habla en su idioma, uno a uno» · «Sin nadie que lo juzgue por lo que pregunta.» |
| 07.2 | «no es un vigilante» · «Eso rompería su confianza, y la tuya.» |
| 07.3 | «Es un lugar al que va a entrenar el criterio.» · «en vez de decirle qué hacer, le hace la pregunta» |
| 07.6 | «lo que veo en redes me dice quién soy» · «yo decido qué me sirve y qué quiero compartir» |
| 07.7 | «ADA está viva y está creciendo.» · «cómo hablar tú con ADA antes de pagar un peso» |
| 08.2 | «tienes razón en desconfiar» · «Por eso ADA existe.» · «riesgos inaceptables para menores» · «ADA tiene un propósito educativo» |
| 08.4 | «una hecha para tu hijo, con reglas y con tu participación» |
| 08.5 | «Cero rol romántico.» · «Tú también participas.» · «Un hijo espiado deja de hablar.» · «Con un tiempo definido para cada conversación.» · «Quiere su criterio.» |
| 08.5a | «Cero rol romántico.» |
| 08.5b | «Tú también participas.» · «Un hijo espiado deja de hablar.» · «Con un tiempo definido para cada conversación.» · «Quiere su criterio.» |
| 09.2 | «conversar tú con ADA antes de inscribir a tu hijo» · «Te va a contestar sin rodeos.» · «antes de pagar» |
| 10.2 | «Los incluye a los dos.» · «Quedas adentro, del lado de tu hijo» · «un tema real para la cena» |
| 10.3 | «la puerta queda abierta» |
| 10.4 | «se vuelven ustedes dos, del mismo lado» · «El criterio que lo cuida es el mismo puente que te lo regresa.» |
| 10.6 | «tú también vas entrenando el tuyo» · «Él aprende a mirar a los dos lados. Tú aprendes a caminar a su lado.» |
| 11.1 | «Pagas hoy y ADA se presenta con tu hijo hoy mismo.» · «el día que ustedes deciden» |
| 11.3 | «ADA, su mentor personal, todo el ciclo.» · «Cada semana pasa algo.» · «Y entre semana, para lo que traiga.» · «Un resumen de su avance.» |
| 11.3b | «SAFE gratis todo el ciclo.» · «Código de descuento en Alquimistas de I.A.» · «Precio fundador congelado cuando lo reinscribas al siguiente nivel.» |
| 11.3m1 | «ADA, su mentor personal, todo el ciclo.» · «Cada semana pasa algo.» |
| 11.3m2 | «Y entre semana, para lo que traiga.» · «Un resumen de su avance.» · «SAFE gratis todo el ciclo.» |
| 11.3m3 | «Código de descuento en Alquimistas de I.A.» · «Precio fundador congelado cuando lo reinscribas al siguiente nivel.» |
| 11.4 | «de tercero de primaria a tercero de prepa» · «Es un solo precio.» |
| 11.6 | «No es una suscripción» · «pruébalo un mes» · «cancelas en un clic y no pagas» |
| 12.3 | «Ahora te toca dárselo a él.» |
| 12.4 | «el día en que cruce solo va a llegar» · «si llega sabiendo mirar» |
