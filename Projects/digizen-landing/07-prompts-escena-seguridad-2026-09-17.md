# Escena "Seguridad por diseño" · prompts de reemplazo (2026-09-17)

Sustituye `scenes/dg-scene-a06-ai-rules-family.png`.
Formato: **3:4 vertical** (`.dg-safety-image { aspect-ratio: 3/4 }`).
Solo se muestra en escritorio; en tablet y móvil está en `display: none`.

> **Importante:** la imagen se renderiza con `.dg-media--flip`, que la **espejea
> horizontalmente** por CSS. Si la escena nueva tiene una lateralidad deliberada (quién
> está a la izquierda y quién a la derecha), hay que quitar esa clase del `<figure>` o
> pedir la escena invertida. Decidir al colocarla.

## Por qué se reemplaza la actual

| Canon | Imagen actual |
|---|---|
| Halo impasto multicolor (coral/naranja, teal, mostaza) | Monocroma azul, sin halo |
| Escena entre personas | Un panel de interfaz falso flotando al centro |
| Padre presente, no vigilante | Padre de brazos cruzados, con una barrera entre ambos |

El fallo de fondo es de narrativa: el copy dice *"sin espiar sus conversaciones, porque
un hijo espiado deja de hablar"*, y la imagen muestra supervisión con una divisoria.
La ilustración contradice al texto que acompaña.

## Bloque de estilo (copiar sin modificar)

> Regla del canon: reutilizar este bloque verbatim y cambiar **solo** la parte de "Scene:".
> Reescribir la redacción entre intentos es lo que rompe la consistencia entre escenas.
>
> **Excepción deliberada en esta escena: la paleta del halo.** El canon fija
> `coral/orange, teal, mustard/gold`, que es cálida y terrosa. Aquí se sustituye por
> **violeta, azul eléctrico y cian**, con coral sólo como acento puntual, por dos razones:
> el H2 de esta sección usa `dg-emphasis--violet`, así que el acento ya es violeta; y una
> escena sobre seguridad y tecnología no se sostiene en mostaza y ocre. El resto del
> bloque —tratamiento del rostro, pincelada, composición, negativos— va intacto.
>
> Si esta paleta funciona, conviene anotarla en `05-image-generation-canon` como variante
> por sección, para que el canon no se contradiga en la siguiente ronda.

```
Style: modern photo-illustration — faces and skin read with real photographic quality and
detail (sharp, lifelike, believable human likeness, natural skin texture and lighting),
intervened with visible painterly brush strokes: thick directional strokes in the hair,
visible loose brush marks and texture breaks in the clothing fabric, crisp dark contour
accents. Background: plain white canvas with a bold multicolor impasto paint-block halo
behind the figures — thick rectangular and rounded brush blocks in violet, electric blue
and cyan, with coral appearing only as a small sharp accent, plus a few scattered accent
dots and thin circular brush-line arcs in matching colors, high-contrast and vivid, cool
and technological rather than warm and earthy, no mustard, no gold, no ochre, no olive,
not monochrome, not just white texture.
Composition: both figures fit completely within the frame with comfortable margin on all
sides — no cropped limbs, nothing bleeding off any edge. Scene: [AQUI VA LA ESCENA].
No readable text, no logos, no locks, no surveillance icons, no melodrama, no 3D render,
no stock photo look, no smooth vector look, no ADA, no second mentor figure, no ghost or
spirit presence.
```

---

## El problema de decir "seguridad" en esta marca

El vocabulario visual estándar de ciberseguridad —candado, escudo, huella, ojo— está
**prohibido por el canon** (`no locks, no surveillance icons`). Y no es capricho: el beat 3
de esta misma landing se titula *"Por qué el candado no funciona"*. Un candado en la
sección de seguridad contradiría el argumento central de la página.

Lo que sí es vocabulario canónico: **cuadros redondeados con íconos de línea y sombra
suave**, que ya aparecen en la escena canon y en el árbol de decisión (a05). Ahí vive la
palomita de aprobación, sin necesidad de cerraduras.

**Los íconos deben leerse tecnológicos, no artesanales.** El repertorio del árbol de
decisión (planta, libro, corazón) sale rústico. Aquí el trazo va fino, parejo y geométrico,
en el lenguaje de una app moderna, con brillo suave y sombra sutil — aunque el *cuadro* que
los contiene siga pintado con textura de pincel, que es lo que los mantiene dentro del
canon y fuera del territorio "captura de pantalla".

Y conviene que cada ícono corresponda a una de las cuatro tarjetas del bloque:

| Tarjeta | Ícono |
|---|---|
| Privacidad, no secretos | burbuja de conversación |
| En familia, no a escondidas | dos nodos enlazados |
| Salud digital | anillo de temporizador de sesión |
| IA diseñada para menores | insignia de verificado |

Y "aprobación" tiene dos lecturas que llevan a imágenes opuestas. Las separo.

---

## Estado (actualizado 2026-09-18)

La generación con la OPCIÓN A salió muy bien, **pero se reasigna a la sección
"Presencia, no vigilancia"** (`dg-scene-a07`), donde la imagen actual son dos meñiques con
un listón y el copy habla de *"volver a mirarlo a los ojos"* — una sección sobre miradas
ilustrada sin una sola cara. El usuario le quita los cuatro íconos en Photoshop y compone
para **4:5**, que es el hueco de esa sección (`.dg-media--portrait`).

Queda pendiente generar la escena de **seguridad**, que es la de abajo.

## Quién aparece: papá con su hija adolescente

Recuento del set tras mover mamá+hijo a presencia:

| Escena | Pareja |
|---|---|
| Hero, CTA "¿Ya viste suficiente?" | papá + hijo |
| Beat 1 | mamá sola |
| Beat 2 (cena), Presencia | mamá + hijo |
| CTA final | mamá + hija |

**Papá + hija no aparece en ninguna.** Va aquí: llena el hueco del set y evita repetir la
misma pareja que la sección de presencia, que queda cerca.

**Diversidad dentro de la escena:** familia mexicana, tonos de piel distintos entre padre e
hija, rasgos reales y no idealizados.

---

## Advertencia: las laptops ya fallaron una vez

El canon registra que `dg-scene-a08-founder-start` se descartó porque **el respaldo de la
laptop salió transparente**, como si se viera la pantalla a través de él. Las dos escenas
de abajo llevan una laptop, así que ambas incluyen un negativo explícito contra eso.

Segundo riesgo: una pantalla de laptop en cuadro invita al modelo a dibujar una interfaz,
que es exactamente como falló la imagen actual de esta sección. Por eso los prompts piden
brillo y reflejo, nunca contenido legible.

---

## ESCENA A GENERAR · Opción 1: la confianza del padre (recomendada)

```
Scene: a Mexican teenage girl sits at the dining table working on an open laptop, absorbed
and comfortable, her posture relaxed. Her father stands a few steps away in the kitchen
doorway with a mug in his hand, pausing for a moment on his way past, looking over at her
with a calm, proud half-smile — the expression of someone who is glad about what he sees
and has no need to walk over. He is clearly not checking on her and not approaching: his
body is already turned to continue on his way. She has not noticed him and is not hiding
anything. Four rounded-square cards float lightly in the air in the upper part of the
frame, each carrying one crisp, precise, geometric line icon in the visual language of a
modern app: a speech bubble, a session timer ring, two circles connected by a short line,
and a verified check badge. The icon strokes are thin, clean and of even weight,
technological rather than hand-drawn or craft-like, with a soft glow and a subtle drop
shadow — but the cards themselves are painted into the artwork with visible brush texture,
not rendered as a screen interface. The laptop is solid and opaque, its lid and back
completely non-transparent, its screen showing only soft glow and reflection with nothing
readable on it. Warm afternoon light, an ordinary lived-in Mexican home. Father and
daughter have visibly different skin tones within the same family.
```

**Por qué funciona:** la distancia es el mensaje. Él mira, aprueba y sigue su camino — eso
es confianza, y es lo contrario del padre de brazos cruzados de la versión actual. Que ella
ni se entere de que la miró es lo que separa la confianza de la vigilancia.

---

## ESCENA A GENERAR · Opción 2: los dos frente a la laptop

```
Scene: a Mexican father and his teenage daughter sit side by side at the dining table,
both leaning slightly toward an open laptop they are looking at together. Seen from behind
and a little to one side, over their shoulders, so their backs and the turn of their heads
read first — but the father's face is visible in three-quarter profile, attentive and
pleased, and a part of the daughter's cheek and smile can be seen as she turns toward him.
She has one hand on the trackpad; he is not reaching for it. Four rounded-square cards
float lightly in the air above the laptop, each carrying one crisp, precise, geometric
line icon in the visual language of a modern app: a speech bubble, a session timer ring,
two circles connected by a short line, and a verified check badge. The icon strokes are
thin, clean and of even weight, technological rather than hand-drawn or craft-like, with a
soft glow and a subtle drop shadow — but the cards themselves are painted into the artwork
with visible brush texture, not rendered as a screen interface. The laptop is solid and
opaque, its lid and back completely non-transparent, its screen showing only soft glow and
reflection with nothing readable on it. Warm afternoon light. Father and daughter have
visibly different skin tones within the same family.
```

**Por qué funciona:** el plano sobre el hombro mete al espectador en el lugar del padre, y
"los dos viendo la misma pantalla" es literalmente *tú estás en el circuito*. Además rompe
la frontalidad que tienen todas las demás escenas del set.

**Su riesgo:** de espaldas se pierden los rostros, y el canon pide calidad fotográfica en
las caras precisamente porque es lo que sostiene el estilo. El prompt fuerza que el padre
quede en tres cuartos para no caer en el error de la imagen de los meñiques, que ilustraba
una sección sobre miradas sin una sola cara.

---

## Recomendación

**La 1.** Dice confianza con una decisión de puesta en escena —la distancia y que él siga
de largo— en vez de decirlo con un gesto. Y conserva los dos rostros, que es donde vive el
estilo de la marca.

La 2 es más original de encuadre y vale la pena si quieres romper la frontalidad del set,
pero apuesta más: si el modelo no acierta el tres cuartos del padre, quedan dos nucas.

## Reglas de entrega

- **Una sola imagen**, en 3:4. Los recortes para otros formatos los hace el usuario en
  Photoshop; no pedir variantes generadas.
- Al colocarla: `<figure class="dg-media dg-safety-image">` **sin** `data-label` (se
  renderiza como caption visible) y revisando si conserva o no `dg-media--flip`.
- Nombre sugerido: `dg-scene-a06-ai-rules-family-v02.png`.
