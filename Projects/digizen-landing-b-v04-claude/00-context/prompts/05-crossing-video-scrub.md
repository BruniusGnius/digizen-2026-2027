# Prompt · 05 cruzar el feed · video para scrub (desktop)

**Estado:** video recibido (`Rudy_laddaga_Style_Hybrid_photo-illustration_Faces_razor-sharp_photorealis.mp4`, 1908×1084, 5 s) y conectado: `assets/seq/05-crossing/`, 49 cuadros, calidad 50, 4.5 MB.

## Para qué es
- **Parada 05.5, en desktop:** la escena sella la metáfora de cruzar la calle y va justo antes de la tesis «El control caduca. / El criterio no.». Con el scroll, **la calle de pantallas (el feed) se mueve** mientras la mamá le señala al hijo por dónde mirar.
- **En móvil y tablet** va la versión vertical fija (`00-context/scenes/vertical/05-crossing-v.webp`).

## Entrada
- **Cuadro inicial:** `00-context/scenes/05-crossing.webp` (1184 × 672). El video arranca exactamente en esa imagen.

## Especificación del video
| | |
|---|---|
| **Duración** | 4–6 s |
| **Cuadros** | 24 fps |
| **Resolución** | 1920 × 1080 o mayor (16:9). Las de ~850 px se ven blandas en desktop. |
| **Cámara** | Fija, o un avance muy lento hacia la calle. El movimiento lo aporta el scroll. |
| **Personas** | Casi quietas: la mamá sostiene el gesto de señalar y el hijo gira un poco la cabeza hacia donde ella señala. Así se evitan las deformaciones de caras y manos. |
| **Lo que se mueve** | El feed: las fichas del piso avanzan como una corriente hacia el punto de fuga; algunas se encienden, se reemplazan o laten (corazones, play, miniaturas de video). |
| **Final** | Termina en una composición estable y cercana al inicio, porque ahí se estaciona el snap. |
| **Reversible** | Todo debe leerse bien hacia atrás: el scroll hacia arriba lo reproduce al revés. Nada de caídas, salpicaduras ni partículas que se vean raras en reversa. |

## Prompt (en inglés)

```
Dynamic cinematic video from the static initial image. Keep the exact painterly oil style, colors,
characters and composition of the input image. The street is made of glowing social-media tiles (video
thumbnails, hearts, play buttons, profile cards): make this digital street FLOW like a living feed —
tiles glide steadily away from the viewer toward the vanishing point, some tiles light up, pulse or swap
content, a gentle continuous river of screens. The mother keeps pointing forward along the street,
calm and steady; the teenage son slowly turns his head to look where she points. People stay almost
still, natural and undistorted. Camera locked off or a very slow push-in toward the street. Soft
daylight, no flicker, no text, no logos, no new people, no sudden motion. Seamless, smooth, 5 seconds.
```

*(Si tu herramienta tiene un control de intensidad del movimiento, usa bajo o medio: el movimiento fuerte deforma a las personas.)*

## Qué revisar al recibirlo
- El feed se mueve con claridad y las personas **no** se deforman (manos, dedos, caras).
- El estilo pictórico se mantiene durante todo el video y no se vuelve fotográfico.
- Sin texto legible en las fichas.
- Recorrido hacia atrás (en reversa): se ve natural.

## Cuando llegue
Déjalo en `00-context/scenes/` y yo lo convierto en secuencia y lo conecto:

```bash
python3 wireframe-src/make_seq.py "00-context/scenes/<video>.mp4" 05-crossing
```

Salen ~49 cuadros WebP de 1280 px (~3 MB) en `assets/seq/05-crossing/`, como en fastidio.
