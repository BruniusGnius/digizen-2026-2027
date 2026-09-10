---
project: DIGIZEN
fase: 2 - wireframe / arquitectura de información
estado: propuesto
input_copy: 00-context/digizen-copy-ola.md
input_system: 01-design-system.md
---

# Wireframe · Landing Generación Fundadora

El orden conserva todos los beats del copy fuente. El diagrama asociado (`02-wireframe.html`) mantiene el recorrido narrativo. `02-wireframe-components.html` es la referencia de componentes, retícula y responsive. `02-wireframe-full.html` es la referencia de ocupación real: coloca el copy de producción completo dentro de los componentes para revisar densidad, scroll y proporciones antes del build.

La versión de ocupación real deja los cuatro acordiones de prueba abiertos de manera deliberada. La versión final conserva la interacción definida para C06, pero aquí no se oculta información que afecte la evaluación espacial.

## Retícula y reglas de diagramación

| Contexto | Retícula | Contenedor | Gutter | Regla de lectura |
| --- | --- | --- | --- | --- |
| Desktop ≥ 1120 px | 12 columnas | máximo 1240 px | 24 px | Copy nunca supera 7 columnas ni 68 caracteres. |
| Tablet 768–1119 px | 8 columnas | ancho fluido − 48 px | 20 px | Media y formularios pasan bajo el copy si la línea baja de 48 caracteres. |
| Móvil < 768 px | 4 columnas | 10 px exterior + 18 px por sección | 12 px | Visual → título → argumento → prueba → acción; sin mínimos que provoquen overflow. |

El wireframe usa los tamaños aprobados del sistema: display 36–60 px, H2 30–44 px, lead 16–18 px, cuerpo 15–16 px a peso 500, labels 11–12 px. Los componentes están en grises para que la revisión evalúe tamaño, agrupación y orden, no estética final.

## Inventario de componentes

| ID | Componente | Anatomía | Desktop | Móvil | Estado / intención |
| --- | --- | --- | --- | --- | --- |
| C01 | Navegación flotante | marca, 4 anclas, CTA de inscripción y progreso de lectura | flotante, ancho máximo 1120 px | flotante, anclas con scroll horizontal y CTA compacto | Siempre visible; anclas con respuesta inmediata y destino espacial claro. |
| C02 | Hero split | eyebrow, H1, deck, ancla, media editorial | copy 1–6, media 8–12 | copy completo → media | La imagen acompaña el hook; no recibe CTA de compra. |
| C03 | Intro editorial | label, H2, lead, cuerpo, cita lateral | copy 2–8, cita 9–11 | todo apilado; cita después de primer párrafo | Sin card: pausa y jerarquía tipográfica. |
| C04 | Quote pair | dos pull quotes y remate | quotes 1–4 / 5–8, remate 1–8 | citas apiladas, remate después | Prueba emocional visible, no acordeón. |
| C05 | Mini-panel CTA | microcopy de decisión y los dos CTA | dentro de beat 2 y oferta; ancho de lectura | botones apilados a ancho completo | Da contexto antes del clic sin competir con el bloque narrativo; feedback en `pointerdown`. |
| C05a | Banda CTA de decisión | contexto, promesa, soporte y dos CTA jerarquizados | 12 columnas, bloque propio oscuro | copy → primario → secundario | Aparece tras beat 2, tras el gate 5.5 y al cierre; la acción principal cambia a ADA en el gate de confianza. |
| C06 | Evidence stack | introducción, 4 acordeones y card sticky de precio | evidencia 1–8; card 9–12 | evidencia → card | 1 abierto por default; cada panel crece hacia abajo desde su trigger. La card se conserva por instrucción explícita. |
| C07 | Statement bridge | declaración grande + cuerpo | 2–10, sin media | 4 columnas | Transición entre problema y mecanismo; no se convierte en card. |
| C08 | ADA proof composite | copy, media ADA, form card | 1–5 / 6–8 / 9–12 | copy → media → form | Selector correo/WhatsApp cambia instantáneamente; form conserva posición del lector. |
| C09 | Safety guard grid | título, texto, 4 guardas, CTA, diagrama | copy 1–7, guardas 8–12 (2×2), diagrama integrado | texto → 4 guardas en una columna → diagrama → CTA | Todo abierto: no es FAQ ni contenido colapsable. |
| C10 | Founder value strip | declaración, media acuerdo, 3 beneficios | copy 1–7, media 9–12; beneficios 1–12 en 3 columnas | copy → media → beneficios apilados | Cada beneficio es fila/divisor, no card promocional. |
| C11 | Offer card | kicker, grid de inclusiones | contenedor 2–11; inclusiones 2×2 | todo apilado; inclusiones 2×2 | Prepara el valor antes de comparar modalidad de pago. |
| C14 | Comparativo de pago | mensual, ciclo 12 MSI destacado, contado, ventaja, consideración factual, garantía y CTA por tarjeta | 3 columnas; ciclo al centro, elevado y oscuro | 1 columna; ciclo sigue al centro en el orden | No añade descuentos: compara únicamente montos y condiciones aprobadas. |
| C12 | Mobile sticky CTA | texto contextual + CTA + cerrar | oculto | 4 columnas, borde inferior fijo | Aparece tras CTA temprano; al entrar a oferta cambia de prioridad ADA → inscripción. |
| C13 | FAQ / reglas | lista de acordeones | 2–10 | 4 columnas | Solo contenido aprobado; apertura y cierre reversibles. |

## Composición por bloque

| Bloque | Componentes | Desktop · columnas | Móvil · orden |
| --- | --- | --- | --- |
| Header | C01 | 1–12 | logo → menú → CTA |
| Hook | C02 | copy 1–6; media 8–12 | copy → media |
| Beat 1 | C03 | copy 2–8; cita 9–11 | título → cuerpo → cita |
| Beat 2 + decisión temprana | C03, C04, C05, C05a | intro 1–7; media 9–12; quotes 1–8; mini-panel en lectura; banda 1–12 | título → cuerpo → quotes → visual → remate → mini-panel → banda CTA |
| Beat 3 | C06 | visual 1–4; evidence 6–12 | intro → prueba 1 → visual → pruebas 2–4 → remate |
| Beat 4 | C07 | 2–10 | título → statement → cuerpo |
| Beat 5 | C08 | copy 1–5; ADA 6–8; form 9–12 | copy → ADA → form |
| Beat 5.5 + decisión de confianza | C09, C05a | copy 1–7; guardas/diagrama 8–12; banda 1–12 | título → contexto → 4 guardas en una columna → diagrama → banda CTA |
| Beat 6 | C10 | copy 1–7; acuerdo 9–12; strip 1–12 | copy → acuerdo → beneficios |
| Oferta | C11 | card 2–11 | card apilada |
| Comparativo de pago | C14 | 3 cards 2–11; ciclo destacado al centro; garantía debajo | mensual → ciclo destacado → contado → garantía |
| Cierre | C07 + C05a | texto / comparación 2–10; banda 1–12 | statement → banda CTA |
| FAQ / footer | C13 | 2–10 | acordeones → footer |

## Orden de bloques

1. **Navegación flotante y anclas**
   - Visible en todo momento y con progreso de lectura integrado; no tapa el hero porque el contenido inicia debajo de su altura.
   - Anclas: problema, ADA, seguridad IA y oferta. En móvil se desplazan horizontalmente dentro de la barra; no sustituyen copy.
   - CTA de navegación: `Inscribir`, con destino a la oferta; no desplaza los CTA de compra del cierre.

2. **Hero · Hook**
   - Lectura de 3 segundos: headline `Le quitaste el celular… con el tuyo en la mano.` y su subheadline.
   - Desktop: copy en 6 columnas y visual editorial en 6 columnas. Móvil: visual primero y copy debajo.
   - Visual: mesa familiar nocturna, adulto e hijo físicamente cerca pero absorbidos por pantallas; el encuadre comunica distancia, no culpa. El copy domina la primera mirada.
   - La primera acción no se adelanta al reframe: una ancla discreta permite continuar al argumento.

3. **Beat 1 · Alivio de culpa**
   - Título, respiración editorial y cuerpo completo abierto por default.
   - El pasaje `No eres mal papá` y `Suéltate la culpa` recibe jerarquía de cita, no una card nueva.
   - Intención: bajar defensas antes de presentar mecanismo o prueba.

4. **Beat 2 · Reframe de la distancia**
   - Título, cuerpo completo y dos citas destacadas en columna editorial.
   - Visual de apoyo en desktop: retrato/escena de distancia cotidiana, no una foto de stock de conflicto. En móvil abre el bloque antes del título.
   - La conclusión `No estás perdiendo tiempo de pantalla. Lo estás perdiendo a él.` queda como remate visible.
   - Un mini-panel contextualiza los dos destinos con `¿Listo? Tu hijo empieza hoy mismo.`; después, una banda CTA oscura repite la decisión sin confundirse con el cuerpo narrativo.
   - En esta primera banda, `INSCRIBIR A MI HIJO — EMPIEZA HOY` es primario y `CONVERSA CON ADA` permanece como ruta secundaria visible para el lector que aún quiere prueba.
   - Justificación: cumple la nota de producción para el lector ya convencido sin interrumpir la cadena de creencias para los demás.

5. **Beat 3 · Por qué el candado falla**
   - Encabezado y analogía de cruzar la calle permanecen abiertos.
   - La cascada de cuatro pruebas aparece como acordeón progresivo: el bloque 1 está abierto al entrar; 2–4 conservan sus textos completos detrás de su propio disparador.
   - En móvil, cada prueba abre hacia abajo desde su título; no hay carrusel ni paginación.
   - La card sticky de precio se conserva en desktop y se apila tras la evidencia en móvil, según instrucción explícita del usuario.

6. **Beat 4 · Criterio como alternativa**
   - Bloque de esperanza abierto, con `El control caduca. El criterio no.` como cita de alto contraste tipográfico.
   - El párrafo de IA y el puente de reconexión se mantienen inmediatamente después: son la transición necesaria hacia ADA.

7. **Beat 5 · ADA como mecanismo**
   - Explicación completa de Gnius Space / ADA en columna de lectura.
   - Entre copy y módulo de prueba en desktop: escena vertical de ADA. En móvil: escena de producto → copy → formulario. Fuente prevista: `ADA-full-body.png` del sistema original.
   - A un costado en desktop y después del copy en móvil: módulo de prueba con el CTA `CONVERSA CON ADA`.
   - El CTA abre el flujo de datos del adulto, no WhatsApp directo: selección de correo o WhatsApp → envío de liga → acceso a ADA.

8. **Beat 5.5 · Seguridad de IA, gate obligatorio**
   - Sección visualmente separada pero abierta en su totalidad por default; nunca se oculta detrás de una FAQ porque resuelve una objeción crítica antes de precio.
   - La admisión de la preocupación, la comparación de categorías, los cuatro principios de ADA y la invitación a auditarla permanecen en este orden.
   - Al terminar el gate, una banda CTA propia separa la decisión de la explicación: `CONVERSA CON ADA` pasa a ser el primario y conserva `INSCRIBIR A MI HIJO — EMPIEZA HOY` como alternativa. El microcopy literal conserva la entrega por correo o WhatsApp.
   - Visual: diagrama de límites de ADA o perfil ADA con cuatro guardas; es informativo, no una foto decorativa.

9. **Beat 6 · Presencia + Generación Fundadora**
   - Reconexión familiar, beneficios de fundador y garantía. El mensaje `Presencia, no vigilancia. Criterio, no candado.` se trata como remate.
   - No se mezcla todavía con precio: prepara el valor y la urgencia antes del bloque de oferta.
   - Visual: acuerdo/pinky promise del sistema original. Reafirma vínculo antes de la oferta.

10. **Oferta v3 · Inscripción · Ciclo Digizen**
    - Título y lista de inclusión; todo visible por default.
    - No hay A/B de precio. El plan mensual funciona como comparación dentro del mismo bloque, según copy fuente.
11. **Comparativo de pago · una sola oferta, tres modalidades**
    - Mensual: `$599` + inscripción de `$900`; ciclo 12 MSI destacado: `$5,990` y `$499/mes efectivo`; contado: `$5,990`.
    - La tarjeta central es la única elevada y oscura: hace visible el ahorro de `$2,098` sin inventar una promoción nueva.
    - CTA principal: `INSCRIBIR A MI HIJO — EMPIEZA HOY`. Secundario: `Tengo dudas — quiero conversar con ADA primero`.

12. **Cierre · Garantía, decisión y postscript**
   - Riesgo invertido, comparación de decisiones y el cierre de la metáfora de cruzar la calle.
   - Una banda CTA oscura e independiente repite ambos CTA después de la conclusión; esta es la última oportunidad de prueba para quien aún no está listo para checkout.

12. **FAQ y reglas públicas · contenedor reservado**
    - Acordeones para objeciones de precio y Las Reglas de ADA. No se inventa contenido: se alimentan cuando exista copy aprobado.
    - La oferta y el bloque 5.5 no se delegan a esta sección.

13. **Footer legal y soporte · contenedor reservado**
    - Privacidad, términos, contacto y referencia a Las Reglas de ADA; contenido legal pendiente de fuente aprobada.

14. **Matriz de headlines · registro de experimentación, fuera de la landing**
    - H1 es el hook de producción para esta arquitectura. H2–H7 permanecen en el copy fuente como variantes para pauta, con H1 vs H2 como test de anuncios.
    - No se agregan como secciones ni se duplican en la página: se preservan como configuración de adquisición.

## Plan de imágenes y bloques visuales

| Bloque | Función | Desktop | Móvil | Fuente / estado |
| --- | --- | --- | --- | --- |
| Hero | Hacer visible la distancia sin convertirla en culpa. | 6 columnas a la derecha; altura aproximada de hero. | Debajo de headline y subheadline. | Brief nuevo: escena familiar cotidiana, pendiente de producción. |
| Beat 2 | Sostener las citas y el reframe emocional. | 4 columnas a la derecha; se alinea al cuerpo, no al título. | Después de las dos citas. | Brief nuevo, pendiente. |
| Beat 3 | Anclar la metáfora de cruzar la calle. | 4 columnas, alterna a la izquierda para dar ritmo. | Después de la primera prueba, antes del acordeón restante. | Ilustración editorial nueva, pendiente. |
| Beat 5 | Presentar ADA como acompañante visible. | 3 columnas entre explicación y formulario. | Después de explicación, antes de formulario. | `assets/shared/ADA-full-body.png`; binario aún no está disponible en `insumos`. |
| Beat 5.5 | Hacer comprensibles los límites de seguridad. | 4 columnas a la derecha, con cuatro guardas rotuladas. | Después de principios de ADA, antes del CTA. | Perfil ADA + diagrama, pendiente de composición. |
| Beat 6 | Materializar el acuerdo familiar. | 4 columnas a la derecha. | Tras la promesa de presencia, antes de beneficios fundadores. | `digizen-acuerdo-pinky-promise-gpt-image-2-v01.png`; binario pendiente de restaurar. |
| Oferta | Ayudar a escanear inclusiones, no contar otra historia. | Franja de 4 iconos funcionales; no fotografía. | Grilla 2 × 2 antes de garantía. | Iconografía del sistema aprobado. |

Todos los slots del diagrama son grises y rotulados. Las imágenes finales se definen durante Fase 3 a partir de estos briefs y de los assets restaurados; no se improvisan ni sustituyen el copy.

## Replanteamiento visual aprobado para revisión

Esta sección prevalece sobre las descripciones visuales anteriores del inventario. No altera ni recorta el copy: cambia únicamente dónde y con qué proporción se mide cada visual.

| Bloque | Desktop / tablet | Móvil | Componente y regla |
| --- | --- | --- | --- |
| Beat 1 · alivio de culpa | Copy en 7 columnas + imagen narrativa **4:5** a la derecha. La imagen ilustra acompañamiento y humanidad, sin repetir la distancia/pantalla del bloque siguiente. | Después del copy, **3:2**. | C03 `Relief visual`; gesto humano cotidiano, sin añadir un nuevo argumento ni CTA. |
| Beat 2 · distancia | Copy en 7 columnas + díptico a la derecha: una toma **1:1** y una toma **4:5**. Las dos forman una misma escena de distancia; no son dos fotos genéricas. | Tras el cuerpo y las citas, en dos columnas. | C04 `Editorial image pair`; cuadrada = detalle, vertical = separación/espacio emocional. |
| Beat 3 · candado | Imagen/ilustración vertical dominante **4:5**, 5 columnas a la izquierda, mínimo 720 px de alto; evidencia completa en 7 columnas a la derecha. En tablet: 3 + 4 columnas con mínimo 610 px. | La visual pasa a 1:1 antes de la evidencia para no alargar artificialmente la página. | C06 `Vertical evidence composition`; la imagen no se recorta y los cuatro acordeones quedan abiertos en esta revisión de ocupación. |
| Beat 4 · criterio | Visual conceptual **4:5** a la izquierda y argumento a la derecha: `feed → pausa → criterio`. | 1:1 antes del argumento. | C07 deja de ser solo texto: diagrama/ilustración editorial, no foto decorativa. |
| Beat 5 · ADA | Explicación 5 columnas + monitor/chat ADA 4 columnas + formulario 3 columnas. | Copy → monitor/chat → formulario. | C08 `Product preview`: pantalla 16:10; ADA puede aparecer como avatar/personaje dentro de la interfaz. El preview usa líneas neutras, sin inventar una conversación ni promesas nuevas. |
| Beat 5.5 · seguridad IA | Copy 7 columnas + 4 cards 2×2, cada una con icono, índice y borde inferior de componente. | Copy → cuatro guardas, una por fila → diagrama ADA → CTA. | C09 no usa viñetas planas: las cuatro guardas conservan su copy completo dentro de cards con iconografía del sistema. |
| FAQ / legal | Después del cierre, tres contenedores acordeón. | Igual, una columna. | C13 usa acordeones, pero no se escribe ni se supone el contenido pendiente: precio, reglas y legal permanecen explícitamente pendientes de fuente aprobada. |

### Auditoría de fidelidad fuente → wireframe

- El plano de ocupación real (`02-wireframe-full.html`) contiene el copy de producción íntegro: hook, beats 1–6, las cuatro pruebas, gate de IA, beneficios fundadores, oferta v3, garantía, CTAs y cierre.
- La información que no corresponde a la UI pública se preserva literalmente en su anexo: origen, restricciones de oferta/precio, mecánica del lead, nota de producción, ancla de objeción de precio y matriz de headlines.
- Los únicos contenedores sin cuerpo real son FAQ, reglas públicas, privacidad, términos y soporte. El documento fuente no aporta esos textos; por ello están rotulados como pendientes, sin contenido inventado.

## Proporciones, crop y tratamiento de imágenes

| Visual | Ratio desktop | Ratio móvil | Tratamiento | Foco / regla de crop |
| --- | --- | --- | --- | --- |
| Hero familiar | 4:5, máximo 448 × 560 px | 3:2 | `cover` | Adulto y menor en tercios opuestos; no cortar ojos, manos ni pantalla. Requiere variante horizontal móvil, no un recorte automático del master vertical. |
| Distancia · beat 2 | 4:3 | 3:2 | `cover` | Rostro o gesto queda en tercio superior; el vacío entre personas es parte de la lectura. |
| Cruce · beat 3 | 1:1 | 1:1 | Ilustración / `contain` | Composición completa siempre visible; no es fotografía y no se corta. |
| ADA full body · beat 5 | 2:3 | 4:5 | `contain`, alineado abajo | ADA conserva cuerpo completo y espacio de respiración arriba. Nunca usar `cover` ni cortar cabeza o manos. |
| Guardas ADA · beat 5.5 | 1:1 | 1:1 | Diagrama vectorial / `contain` | ADA al centro, cuatro guardas en los cuadrantes. No requiere crop. |
| Acuerdo / pinky promise · beat 6 | 1:1 | 1:1 | `contain` | Manos completas, listón y gesto central visibles. Se preserva el asset en su composición original. |
| Iconos de oferta | 1:1 por tile | 1:1 por tile | Icono / `contain` | No son imágenes hero: 48 px de icono dentro de tile, con etiqueta debajo. |

Regla de escala: un visual narrativo solo ocupa 4–5 columnas y nunca debe ser más alto que 1.25× el bloque de copy que acompaña. ADA es la única excepción vertical, porque su cuerpo completo es parte del mecanismo de confianza. En móvil, cada imagen abre la sección antes del texto que contextualiza; el único caso compuesto es ADA: escena → explicación → formulario.

## Jerarquía de escaneo

| Prioridad | Elementos visibles sin leer cuerpo |
| --- | --- |
| 1 · 3 segundos | Hook, subheadline, reframe de beat 2, `El control caduca. El criterio no.`, ADA, precio y garantía. |
| 2 · Decisión | Citas, pruebas de candado, principios de seguridad IA, beneficios fundadores, CTA temprano y CTA de oferta. |
| 3 · Profundidad opcional | Pruebas 2–4 del candado, guía de conversación, objeciones futuras en FAQ y legales. |

## Sistema de decisión CTA

- **Mini-panel local (C05):** fondo `#F6F8FB`, borde `#E8EDF3`, microcopy previo y botones cercanos. Se usa donde la sección ya contiene una decisión: beat 2 y oferta.
- **Banda de decisión (C05a):** fondo `#152033`, padding generoso y bloque propio entre beats. El primario blanco se reconoce antes que el secundario delineado; en móvil ambos ocupan el ancho completo.
- **Repetición con intención:** después del beat 2 resuelve al lector ya convencido; después del beat 5.5 ofrece primero auditar ADA, justo tras la objeción de seguridad; el cierre recupera la inscripción con la garantía presente.
- **Interacción:** todos los CTA responden en `pointerdown`; ADA abre el flujo de datos del adulto y conserva su retorno al punto de lectura. Ninguno abre WhatsApp directo.

## Densidad y responsive

- **Desktop:** ancho de lectura de 62–68 caracteres; comparaciones de privacidad / conversación en dos columnas solo cuando no rompan el orden narrativo.
- **Móvil:** una sola columna y gutters de 10 px exteriores + 18 px internos. Las dos citas del beat 2 se apilan; imágenes y previews abren sus secciones; los CTA se expanden al ancho del contenedor; las cuatro guardas de ADA se muestran una por fila; las pruebas del beat 3 y FAQ conservan acordeones independientes.
- **CTA flotante móvil:** aparece al rebasar el CTA temprano y permanece hasta la oferta. Primario `CONVERSA CON ADA`; al acercarse a oferta cambia a `INSCRIBIR A MI HIJO` sin ocultar la alternativa ADA.
- **Progreso:** marcador de scroll sin porcentaje numérico, que muestra posición narrativa pero no convierte la landing en un formulario largo.

## Intención de interacción

| Elemento | Feedback inmediato | Dirección / reversibilidad |
| --- | --- | --- |
| Anclas | Estado activo al tocar y desplazamiento inmediato al bloque. | El foco se mueve al encabezado destino; la navegación puede interrumpirse con scroll manual. |
| CTA ADA | En `pointerdown`, compresión mínima y confirmación visual del destino. | Desktop: formulario se expande desde el CTA; móvil: sheet entra desde abajo y vuelve abajo al cerrar. El usuario puede cancelarlo sin perder posición de lectura. |
| Selector correo / WhatsApp | Cambio instantáneo del estado seleccionado y del texto de entrega. | Sin transición bloqueante; cambiar de canal revierte el estado anterior al instante. |
| Acordeón de pruebas / FAQ | Indicador cambia en el toque inicial y la profundidad se revela inmediatamente. | El contenido crece hacia abajo desde su propio encabezado y se colapsa hacia arriba por el mismo camino. |
| Barra CTA móvil | Respuesta inmediata al cruzar el CTA temprano u oferta. | Entra y sale por el borde inferior; no debe capturar el scroll ni bloquear la lectura. |

## Contenido pendiente, sin inventar

- Copy aprobado de FAQ de precio, reglas y legales.
- Destino técnico de checkout y del formulario de acceso a ADA.
- Confirmación final del nombre público de la plataforma: `Gnius Space` o `la plataforma Digizen`.

### Evaluación — Fase 2, ronda 3 · refinamiento solicitado

| Lente | Puntaje | Objeciones |
| --- | --- | --- |
| Purista | 4.8/5 | La card de beat 3 se conserva por decisión explícita; el comparativo detalla cada pago con hechos aprobados, sin promociones inventadas. |
| Arquitecto de Sistemas | 4.8/5 | Navegación, C05/C05a y C14 tienen reglas reutilizables por viewport. Siguen pendientes los destinos técnicos externos. |
| Guardián de Lectura | 4.8/5 | Las anclas reducen fricción de scroll y el comparativo muestra mensual, 12 MSI y contado sin obligar a calcular. |

**Puntaje ponderado:** 4.8 / 5
**Resultado:** aprobado internamente.

¿Apruebas este layout y arquitectura de información para pasar a la Fase 3 (build), o ajustamos el orden/estructura primero?
