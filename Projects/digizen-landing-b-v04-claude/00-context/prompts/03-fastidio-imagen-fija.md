# Prompt · 03 fastidio · imagen fija (móvil y tablet)

**Estado:** propuesto, pendiente de tu aprobación. No se ha generado nada.

## Para qué es
- **Parada 03.4, en móvil y tablet** (menos de 860 px). En desktop esa parada usa el scrub de video (`assets/seq/03-fastidio/`).
- Sella la frase «Los ojos al techo. En señal de fastidio.», que responde a «…la quinta vez que le dijiste «ya deja el cel».».
- Reemplaza a `03-eyes.webp` (no convenció la expresión: el celular tapa media cara y los ojos en blanco se ven exagerados). También reemplaza a la imagen provisional `fastidio-f064.webp`.

## Entradas de referencia
1. `assets/seq/03-fastidio/fastidio-f064.webp`: identidad del chico, ropa, pose y dirección de la expresión (el cuadro más expresivo del video).
2. `00-context/scenes/01-dinner.webp`: el estilo pictórico de la serie (óleo empastado, muro blanco texturizado, pinceladas azul/cian/violeta).

## Formato
- **Vertical 3:4, 1200 × 1600.** En tablet vertical llena el encuadre; en móvil (9:15.3) se recorta solo por los lados.
- El chico va centrado y ocupa el 70 % central del ancho, para que el recorte móvil no lo toque.

## Prompt (en inglés, como los originales)

```
Use case: illustration-story. Create ONE new vertical painted illustration, 3:4 portrait, 1200x1600.
Input image 1 is the identity, wardrobe and pose reference; input image 2 is the style reference.
STYLE: match input image 2 exactly — expressive semi-realistic oil painting with visible impasto
brushstrokes, off-white textured plaster wall background with loose abstract strokes of cobalt blue,
cyan/teal and violet, soft natural daylight, warm realistic skin, painterly edges. Same art direction as
the rest of the series. Not photorealistic, not 3D, not cartoon, no imitation of a specific artist.
SUBJECT: the same Mexican teenage boy (about 14) from input image 1: dark curly tousled hair, dark teal
hoodie with drawstrings and the orange paint-stroke graphic on the right chest, white t-shirt collar.
Chest-up framing, centered, generous headroom above the hair (about 12% of the height), the boy within
the central 70% of the width.
POSE: he holds his smartphone at chest height with both hands, screen turned toward himself (screen not
visible to viewer, NO glow or light coming from the phone). He is not looking at the camera and not
looking at the phone.
CRITICAL EXPRESSION: an unmistakable exasperated eye-roll, reacting because a parent told him to put the
phone down for the fifth time. Both eyes rolled UP toward the ceiling with pupils high in the eyes;
eyebrows slightly lowered and knitted in annoyance (NOT raised, NOT worried, NOT sad, NOT surprised);
mouth slightly open in an audible bored sigh; head tilted back a few degrees. His WHOLE face is
visible and readable — nothing covers the mouth or nose. Natural, human, not exaggerated: no blank
white "zombie" eyes, no caricature.
No text, no lettering, no emoji, no speech bubbles, no logos, no brands, no watermark, no other people.
Generate exactly one image.
```

## Qué revisar al recibirla
- La expresión es **fastidio**, no tristeza, preocupación ni sorpresa. Las cejas **no** suben por dentro.
- La cara se ve completa; el celular no tapa nada.
- El celular no brilla (el video trae un resplandor que no queremos repetir).
- La identidad y la ropa coinciden con el video, y el estilo con el resto de la serie.
- En el recorte móvil (9:15.3) el chico queda completo.

## Cuándo se integra
Se guarda como `00-context/scenes/vertical/03-fastidio-v.webp` (convención de versiones verticales, ver `00-context/scenes/vertical/LEEME.md`). El wireframe la toma solo y reemplaza a la provisional en la parada `03.4m`.
