# ADA · Prompts para el asset de saludo (2026-09-17)

Destino: sección "Conoce a ADA", capa frontal del `.dg-ada-composite`.
Sustituye a `public/assets/digizen/ADA-full-body.png` (1200×1600, RGBA, 82.7% transparente).

**Herramienta:** ElevenLabs (ImagineART sin créditos).
**Referencia obligatoria:** subir `public/assets/digizen/ADA-full-body.png` como imagen de referencia.
Sin referencia el personaje se redibuja distinto y se pierde el canon.

---

## Descripción del personaje (bloque fijo — no reescribir entre intentos)

> Reutilizar este bloque textual en todos los intentos. Cambiar solo el bloque de POSE.
> Regla heredada del canon de escenas: reescribir la redacción entre iteraciones es lo que
> rompe la consistencia.

```
CHARACTER (keep identical to the reference image, do not redesign):
Stylized 3D cartoon render of a young girl mentor, Pixar/Disney-like soft matte surfaces,
clean neutral studio lighting, gentle ambient occlusion, no harsh specular highlights.
Chin-length dark navy-black bob haircut with a bright blue lightning-bolt streak sweeping
across her left brow. One thick dark eyebrow visible under the fringe. Large round dark-brown
eyes with soft highlights, small button nose, warm medium-light skin.
Outfit: light cyan-blue long-sleeve turtleneck with orange side panels along the ribs and
red cuff wristbands; red pleated mini skirt; black leggings whose lower legs turn orange with
a black chevron motif; red high-top sneakers with white soles.
Same face, same proportions, same colors, same materials as the reference. Same camera height,
same lens, same lighting setup, same character scale in frame.
```

---

## PROMPT A · Tira de 3 poses en una sola generación (recomendado)

Aspecto: **16:9** · fondo plano uniforme · 1 sola generación.

```
[pegar aquí el bloque CHARACTER de arriba]

LAYOUT: one single image containing the SAME character three times, side by side in a row,
evenly spaced, all three at identical scale, identical camera height and identical lighting,
full body from head to sneakers, feet aligned on the same invisible ground line, generous
empty margin above the head and below the feet, clear empty gap between each figure so they
never overlap or touch.

POSE 1 (left): standing relaxed facing the viewer, both arms down at her sides, calm friendly
closed-mouth smile, looking straight at the viewer.

POSE 2 (center): same standing stance, her right arm raised out to the side at shoulder height,
elbow bent, palm open and facing the viewer with fingers relaxed and slightly spread, warm open
smile showing teeth, head tilted slightly toward the raised hand.

POSE 3 (right): same standing stance, her right arm raised higher beside her head, palm open
and facing the viewer, fingers spread, arm tilted a little further outward as if mid-wave, big
bright open smile, eyes happy, head tilted slightly.

Only the right arm, the head tilt and the mouth change between the three poses. Everything else
— body, legs, feet position, outfit folds, hair silhouette — stays as identical as possible.

BACKGROUND: completely plain flat solid background, one single uniform color, no gradient,
no shadow on the background, no floor, no props, no text, no logos, no watermark, no labels,
no numbers, no panel borders or dividing lines between the figures.
```

**Por qué 3 poses:** con brazo abajo → medio → alto tienes el ciclo de saludo completo.
Alternando las poses 2 y 3 se lee como una mano que se sacude; la 1 sirve de estado de reposo
antes de que entre en cuadro.

---

## PROMPT B · Una sola pose (si A sale mal o prefieres gastar menos)

Aspecto: **3:4** · fondo plano uniforme.

```
[pegar aquí el bloque CHARACTER de arriba]

POSE: standing full body facing the viewer, weight on one leg, her right arm raised beside her
head with the palm fully open toward the viewer, fingers relaxed and slightly spread, in a
friendly hello wave. Left arm relaxed at her side, not touching the body. Warm open smile
showing teeth, eyes looking directly at the viewer, head tilted slightly toward the raised hand.
Full body visible from the top of the hair to the soles of the sneakers, with empty margin all
around — nothing cropped at any edge.

BACKGROUND: completely plain flat solid background, one single uniform color, no gradient,
no shadow, no floor, no props, no text, no logos, no watermark.
```

---

## Requisitos técnicos del entregable

- **Fondo plano de un solo color** (no degradado, no sombra de piso). Si ElevenLabs no entrega
  alpha, el recorte se hace después; un fondo uniforme es lo que lo hace limpio.
- **Nada tocando los bordes.** Si un dedo o un zapato se corta, el recorte queda inservible.
- **La mano abierta y el brazo separado del torso son el requisito crítico.** Si el brazo sale
  pegado al cuerpo o la mano cerrada (como el puño del asset actual), no se puede separar la
  capa del brazo y hay que regenerar.
- Entregar en PNG con alpha, ~1200×1600 por pose, mismo encuadre que `ADA-full-body.png`
  (personaje centrado, pies cerca del borde inferior).

## Nombres de archivo al entregar

- Tira de 3: `ada-wave-sheet-v01.png` (yo recorto las poses).
- Poses ya recortadas: `ada-wave-01.png`, `ada-wave-02.png`, `ada-wave-03.png`.
- Pose única: `ada-wave-full-body.png`.

---

# Metaprompt · Video del saludo (image-to-video)

Entrada: PNG fijo de ADA saludando, **con fondo verde croma plano**.
Salida esperada: MP4 de 3–4 s, cámara fija, verde intacto.
Post: llave de croma + conversión a WebP animado con alpha (no hace falta video con alpha).

## Prompt principal

```
Locked-off static camera, no camera movement whatsoever.

A stylized 3D cartoon girl stands facing the viewer against a flat chroma green
background. She waves hello at the camera: her already-raised right forearm rotates
from the elbow, the open palm sweeping smoothly left and right, three relaxed waves
across the clip, fingers open and softly spread, with a gentle follow-through in the
wrist at the end of each sweep.

Her face stays warm and alive: a wide open smile held throughout that brightens a
little as she waves, cheeks lifting, eyes narrowing slightly with the smile, and one
soft natural blink midway through the clip. Her shoulders rise and fall once with a
quiet breath.

Everything else stays still: her feet planted in exactly the same spot, legs and hips
locked, torso upright and unmoving, left arm hanging relaxed at her side, hair keeping
its silhouette. The green background stays perfectly flat, uniform and static for the
whole clip.

The first and last frames match so the action loops seamlessly.
```

## Prompt negativo

```
camera movement, zoom in, zoom out, pan, tilt, dolly, handheld shake, parallax,
walking, stepping, turning, leaning, body sway, weight shift, hip movement, change of
pose, reframing, crop change, background gradient, cast shadow on the background,
moving shadow, light flicker, added floor, props, text, watermark, logo, character
redesign, different face, different outfit, different colors, motion blur, depth of
field change, film grain
```

## Ajustes

- Duración: **3–4 s**. Más largo sólo agrega peso y cuadros que se descartan.
- Si el modelo ofrece preset de cámara: **fixed / static / no motion**.
- Si ofrece "fidelidad a la imagen de referencia": al máximo.

## Si el resultado falla

No rescatar; regenerar. Los tres fallos que lo invalidan:

1. **Deriva de cámara** (zoom lento "cinematográfico"). Es lo que más se desobedece.
   Se nota muchísimo con ADA recortada sobre el panel.
2. **Cuerpo que se balancea o cambia de apoyo.** Al recortarla parece que flota.
3. **Verde sucio** — degradado, sombra proyectada o parpadeo de luz. Rompe la llave
   de croma y deja bordes verdes.

Si insiste en mover la cámara, reforzar al inicio del prompt:
`Absolutely static locked-off tripod shot. The frame never changes.`

---

# Metaprompt v2 · 16:9, tras el fallo de Kling 3.0 Pro (2026-09-17)

## Qué falló en la v1 (clip `ElevenLabs_video_kling-3-0-pro_..._20_45_19.mp4`)

| Fallo | Detalle medido |
|---|---|
| Se da la vuelta | A los ~2.0 s gira y queda de espaldas, ojos cerrados. Otra vez a partir de 5.6 s |
| Cambia de mano | De 0 a 1.5 s saluda con la mano a la derecha del cuadro (como el fijo). Tras el giro se queda a la izquierda **el resto del clip**, cruzando frente a su cara y tapándole el mechón azul |
| Brazo cortado | En 9:16 el brazo levantado toca el borde derecho del cuadro en 2 de 21 cuadros de la ventana buena |
| No cierra el ciclo | Primer cuadro con brazo arriba, último con brazo abajo |
| Saludo flojo | La mano barre ~4% del ancho del cuadro. Se lee como temblor, no como saludo |

**Única ventana aprovechable: 0.08 s → 1.42 s.**

## Correcciones para la v2

1. **16:9 horizontal.** El 9:16 no deja aire lateral para el arco del brazo. El reencuadre
   final lo hace el usuario en Premiere.
2. La instrucción de **ciclo va al principio**, no al final — al final la ignora.
3. Prohibir el giro y el cambio de mano **explícitamente**, no sólo en el negativo.
4. Pedir **amplitud** del saludo con una medida concreta (el ancho de su cabeza).

## Prompt principal v2

```
A seamless loop: the clip begins and ends on the exact same pose and the exact same
hand position, so it can repeat forever without a visible cut.

Locked-off static camera on a tripod. No camera movement whatsoever — no pan, tilt,
zoom, dolly or drift. The frame never changes.

Medium shot, waist up, the character centred with clear empty space on both sides of
the frame. A stylized 3D cartoon girl faces the camera against a flat chroma green
background.

She waves hello. The arm that is already raised on the RIGHT side of the frame is the
only arm that moves, and it stays the waving arm for the entire clip. Her forearm
rotates from the elbow and the open palm sweeps in a generous arc from side to side —
the hand travelling a distance about as wide as her own head on each sweep — three
unhurried waves across the clip, fingers open and relaxed, with a soft follow-through
in the wrist at the end of each sweep. The raised arm never touches or crosses in
front of her face or hair, and never leaves the frame.

Her face stays warm and alive: a wide open smile held throughout, cheeks lifted, eyes
narrowing slightly with the smile, and one soft natural blink. Her shoulders rise and
fall once with a quiet breath.

She faces the camera directly from the first frame to the last. She NEVER turns, never
rotates, never shows her back or her side. Her other arm stays hanging relaxed at her
side and never rises. Her feet stay planted, her legs, hips and torso do not shift.

The green background stays perfectly flat, uniform and static throughout.
```

## Prompt negativo v2

```
turning, turning away, showing her back, back view, rear view, side view, profile,
switching hands, waving with the other hand, raising the other arm, lowering the arm,
arm out of frame, hand crossing the face, camera movement, zoom, pan, tilt, dolly,
handheld shake, parallax, walking, stepping, leaning, body sway, weight shift, change
of pose, reframing, crop change, background gradient, cast shadow on background,
moving shadow, light flicker, floor, props, text, watermark, character redesign,
different face, different outfit, different colors, motion blur, film grain
```

## Notas de post

- **Despill: suave.** Con `mix=0.5` la playera cian `(77,192,218)` se volvió azul violeta
  `(80,119,227)` — el filtro se come el canal verde, que en un cian es medio color.
  `mix=0.12` conserva el cian. En After Effects, mismo cuidado con el Advanced Spill
  Suppressor.
- El ciclo se cierra con **ping-pong** (ida + vuelta sin repetir los extremos), lo que
  hace innecesario que el modelo acierte el loop perfecto.
- Entrega final a web: **WebP animado con alpha**, no video con alpha (evita tener que
  servir WebM/VP9 y HEVC por separado).
