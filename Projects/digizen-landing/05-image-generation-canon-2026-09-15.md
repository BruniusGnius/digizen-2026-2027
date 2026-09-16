# DIGIZEN · Canon y proceso de generación de imágenes (sesión 2026-09-15)

> Este documento existe para que la generación de imágenes de Digizen no se "rompa" otra vez —
> perder el estilo, reintroducir a ADA, o repetir errores de flujo ya resueltos. Léelo antes de
> generar o pedir que se generen nuevas escenas.

## 1. Referencia visual — de dónde sale el estilo

Dos fuentes, en este orden de autoridad:

1. **`Projects/digizen-landing/angular-build/public/assets/digizen/generated/references/digizen-preset-avatar-set-mx-v03-white-0X.png`**
   (5 archivos). Esta es LA referencia de fondo: bloques de pincelada gruesa **multicolor** (coral/naranja,
   teal, mostaza/dorado) formando un halo detrás de la cabeza, con puntitos y arcos delgados de acento,
   sobre lienzo blanco. Rostro con calidad fotográfica intervenida con pincelada (no plano/vector, no
   pintura desde cero sin base realista).
2. **`digizen-v05-mision-clara-image-canon-2026-09-15.md`** (mismo folder que este archivo). Canon
   escrito de la tesis visual, semiótica prohibida y reglas de composición. **Nota:** la sección de ADA
   en ese documento quedó anulada por la decisión de abajo — no generar figuras de ADA.
3. Imagen fuente original (fuera de este repo, en el vault Obsidian):
   `operations/digizen/product-design/generated-assets/digizen-v05-mision-clara-asset-gpt-image-2-v01.png`
   dentro de `Gnius-Copywriting-Factory-FA`. Cópiala a un scratchpad si necesitas volver a verla (está
   fuera del working directory de este proyecto).

**Antes de generar cualquier imagen nueva, mirar las 5 referencias del punto 1.** No confiar en la
descripción acumulada en una conversación — el estilo se degrada rápido si se describe de memoria.

## 2. Decisión firme: ADA no aparece en las ilustraciones

Las primeras generaciones (ronda v01) mostraban a ADA como una figura femenina azul, translúcida y
gigante, con lectura no deseada de "diosa"/aparición religiosa (manos abiertas, halo de luz). Se
descartó por completo.

- **Ninguna escena de landing lleva a ADA como personaje.** Solo adolescente/familia + celular +
  iconografía abstracta si acaso.
- ADA como personaje visual (chat/UI real del producto) se define aparte, fuera de estas ilustraciones.
- Las imágenes descartadas por este motivo están archivadas en
  `generated/archive-with-ada/` — no reciclar ese estilo de figura.

## 3. Estilo de prompt que funciona (esqueleto a reutilizar)

No reescribir la redacción desde cero en cada iteración — cambiar solo la parte de "Scene:", dejar
"Style:" intacto. Esqueleto validado:

```
Style: modern photo-illustration — faces and skin read with real photographic quality and detail
(sharp, lifelike, believable human likeness, natural skin texture and lighting), intervened with
visible painterly brush strokes: thick directional strokes in the hair, visible loose brush marks and
texture breaks in the clothing fabric, crisp dark contour accents. Background: plain white canvas with
a bold multicolor impasto paint-block halo behind the figures — thick rectangular and rounded brush
blocks in coral/orange, teal, and mustard/gold, with a few small scattered accent dots and thin
circular brush-line arcs in matching colors, high-contrast and vivid, not monochrome, not just white
texture. Composition: both figures fit completely within the frame with comfortable margin on all
sides — no cropped limbs, nothing bleeding off any edge unless the format specifically calls for a
bleed (ver sección 5). Scene: [describir aquí la escena específica]. No readable text, no logos, no
locks, no surveillance icons, no melodrama, no 3D render, no stock photo look, no smooth vector look,
no ADA, no second mentor figure, no ghost or spirit presence.
```

### Errores de redacción que rompen el estilo (evitar)

- **NUNCA usar "over a photographic base"** ni frases similares — empujan el resultado hacia lo
  fotorrealista puro y alejan del canon pictórico.
- **NUNCA describir el fondo como "flat white" o "plain white, no texture"** — el canon lleva el halo
  de color de la sección 1, no un blanco liso ni textura monocromática pálida.
- Vigilar que la ropa no salga toda del mismo tono de azul en ambos personajes — variar la paleta
  (coral/terracota, verde) dejando azul/cian solo como acento.

## 4. Herramienta: ImagineART (MCP)

- Modelo: `gpt-image-2` (a menos que el usuario pida otro).
- Organización: `c886ec80-ab4b-432c-bb37-9e24aece8745` (rudyladdaga's personal).
- **Carpeta de trabajo: "digizen 2026-2027"** — `folder_id: 797d5e89-98fc-43fc-bc38-73e8399da5bb`.
  Pasar siempre este `folder_id` en `generate_image` para que todo quede organizado ahí.
- Aspect ratios soportados por `gpt-image-2`: `1:1, 4:3, 3:4, 3:2, 16:9, 9:16, 2:3, 21:9`. No soporta
  `4:5` ni `16:10` — si el diseño pide esas proporciones, generar en el más cercano soportado
  (`3:4` o `2:3`) y dejar que el recorte final se haga en Photoshop (ver sección 5).
- Para referencia por imagen (img2img) hay que subir el archivo primero — un `image_url` con ruta local
  del sistema de archivos **falla silenciosamente** (error de generación). Si se necesita, usar
  `request_image_upload` (widget) o `user_upload` con base64, no pasar una ruta de archivo directo.

## 5. Reglas de flujo de trabajo (con el usuario)

- **Una sola imagen por escena, en formato vertical/base**, no generar variantes mobile/desktop por
  separado — el usuario las recorta él mismo en Photoshop a partir de esa única imagen. Cuando entregue
  su recorte, el nombre de archivo lleva el sufijo `-mobile` (tablet/móvil) o `-16-9`/`-1-1` (variantes
  de proporción), y solo hay que conectarlo al `<picture><source>` correspondiente.
- **Nunca usar el atributo `data-label` en `.dg-media`** al insertar una imagen final — ese atributo se
  renderiza como caption visible (`::after { content: attr(data-label) }` en `styles.css`). Solo se usa
  en placeholders temporales de desarrollo.
- **Ir imagen por imagen, con aprobación antes de seguir con la siguiente.** No generar el set completo
  de una vez — así fue como se coló el error de ADA y las escenas que no calzaban con el copy real de
  su sección.
- **Antes de reemplazar un placeholder, confirmar que no es un componente interactivo.** Ejemplo real:
  el placeholder "reloj que reacciona con el scroll" en el beat 3 (`dg-placeholder-scene`,
  `dg-evidence-visual`) y el diagrama `[data-criteria-visual]` en `app.ts:288` tienen lógica JS propia —
  no son huecos de imagen a sustituir sin más.
- **El bleed "más alto que el cuadro" en los CTA (`.dg-decision-portrait`) se logra por CSS, no por
  lienzo extra pintado.** El contenedor es un cuadrado (`aspect-ratio: 1`); la imagen adentro se
  muestra a su proporción nativa escalada (`width: X%; height: auto`, ancla `bottom:0`). Si la imagen
  nueva llena el cuadro de borde a borde (sin margen alrededor de las figuras) en vez de tener espacio
  vacío como el placeholder viejo, hay que **bajar el porcentaje de escala en CSS**
  (`styles.css` → `.dg-decision-portrait img`, valor actual `width: 115%; left: -30%`) — no volver a
  generar la imagen con más "aire" pintado alrededor.

## 6. Estado de escenas al cierre de esta sesión (2026-09-15)

| Escena / sección | Archivo final | Estado |
|---|---|---|
| Hero ("Le quitaste el celular…") | `scenes/dg-scene-a01-hero-phone-hypocrisy.png` (+ `-mobile`) | ✅ Resuelto — papá absorto en su propio celular, hijo con fastidio genuino, tensión sin pelea |
| Beat 1 "Nadie te enseñó esto" | `scenes/dg-scene-a02-parent-phone-attachment.png` (+ `-mobile`) | ✅ Resuelto — mamá con atención total en su celular (el adulto también tiene apego al dispositivo) |
| Beat 2 "Lo que de verdad duele" | `scenes/dg-scene-a03-mother-son-dinner.png` (+ `-mobile`) | ✅ Resuelto (v11) — mamá e hijo cerca en cuerpo, lejos en conexión por el celular |
| Beat 3 "Bloquear no te lo devuelve" | placeholder "reloj reactivo al scroll" (`dg-placeholder-scene`) | ⏸️ No es un slot de imagen — es un componente JS pendiente de implementar, no tocar con IA |
| Beat 4 "Otro camino" | diagrama CSS `dg-criteria-visual` (`app.ts:288`) | ❌ Pendiente — el diagrama no funciona, hay que sustituirlo por una imagen (decidir si se conserva la interactividad) |
| "Seguridad por diseño" (ADA) | `scenes/dg-scene-a06-ai-rules-family.png` (con `.dg-media--flip` en CSS) | ✅ Resuelto |
| "Antes de decidir" (ADA + guardas) | `scenes/dg-scene-a05-criterion-mission.png` | ✅ Colocado, sin feedback explícito de aprobación aún |
| Beat 6 "Presencia, no vigilancia" | `scenes/dg-scene-a07-pinky-promise.png` | ✅ Colocado, sin feedback explícito de aprobación aún |
| Generación Fundadora | `scenes/dg-scene-a08-founder-start.png` | ❌ Pendiente — concepto correcto, ejecución con error (el respaldo del laptop se ve transparente) |
| CTA "¿Ya viste suficiente?" (2 apariciones) | `scenes/dg-scene-cta-father-son-team-1-1.png` | ✅ Resuelto — papá e hijo en equipo, celular sostenido de cabeza a la altura del pecho, fondo con halo de color |
| CTA final (última aparición) | `scenes/dg-scene-cta-mother-daughter-laptop-1-1.png` | ✅ Resuelto — mamá e hija de primaria revisando una laptop juntas, mismo tratamiento de fondo |

### Pendientes para la siguiente sesión

1. **Beat 4 "Otro camino":** reemplazar `dg-criteria-visual` por una imagen (o decidir si se mantiene
   como diagrama interactivo y solo se rediseña visualmente).
2. **Generación Fundadora:** regenerar `dg-scene-a08-founder-start.png` corrigiendo el error de la
   laptop (el respaldo se ve transparente, como si se viera la pantalla a través de él).
3. Confirmar con el usuario si "Antes de decidir" y "Presencia, no vigilancia" (a05, a07) quedan
   aprobadas tal cual, o necesitan la misma ronda de ajustes que tuvieron hero/beat1/beat2.
4. Evaluar si vale la pena regenerar hero/beat1/beat2 con el halo de color multicolor de la sección 1
   (se resolvieron antes de encontrar esa referencia — actualmente llevan fondo blanco con textura
   sutil, no el halo vívido).
