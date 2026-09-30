# Versiones verticales de las escenas (móvil y tablet)

Cada escena tiene **dos versiones**:
- **Horizontal** (la actual en `00-context/scenes/`): para desktop y tablet horizontal, desde 860 px.
- **Vertical 2:3**: **un solo archivo para teléfono y tablet vertical**, por debajo de 860 px (decisión del usuario, 2026-09-29). Así no se ve chica ni mal recortada.

Las verticales las haces tú en Photoshop **a partir de la misma imagen base**: reencuadre y extensión del fondo, para que sea la misma escena y no una generación distinta. Cuando pongas el archivo con el nombre de la tabla (junto a la original o en esta carpeta), el wireframe lo usa solo en móvil y tablet. Mientras falte, en móvil aparece un aviso con el nombre del archivo, y `python3 wireframe-src/build.py` lista cuáles faltan.

## Especificación

| | |
|---|---|
| **Proporción** | 2:3 vertical: queda a medio camino entre el teléfono (≈ 9:15.3) y la tablet vertical (≈ 3:4) |
| **Tamaño** | 1200 × 1800 px (mínimo 1080 × 1620) |
| **Formato** | WebP, calidad ~75 (o PNG, que convierto yo) |
| **Nombre y lugar** | El mismo nombre de la original + el sufijo `-v` (ej.: `05-crossing.webp` → `05-crossing-v.webp`), **sin carpeta aparte**: junto a la original en `00-context/scenes/` o junto a las imágenes del sitio en `output-code/assets/scenes/`. Para la imagen fija del fastidio vale el nombre del cuadro (`fastidio-f017-v.webp`). Esta carpeta solo guarda esta ficha. |
| **Cómo se ve** | Llena la pantalla en teléfono y en tablet. En teléfono se recorta ~6 % de cada lado; en tablet, entre 5 y 9 % arriba y abajo (según la barra del navegador). |
| **Zona segura** | Lo importante (caras, manos, celular, objetos clave) dentro del **rectángulo central de 80 % × 80 %**: deja un margen de 10 % en cada borde con fondo o elementos que se pueden perder. |
| **Sin** | Texto, captions, viñeta ni bordes difuminados |

## Escenas y cómo componer cada vertical

| Parada | Horizontal actual | Vertical a hacer | Qué debe quedar en cuadro | Movimiento en el recorrido |
|---|---|---|---|---|
| H.1 Hero | `01-dinner.webp` | `01-dinner-v.webp` | El hijo al centro, absorto en el celular, y los papás a los lados (pueden quedar parciales). El centro de la escena, a ~45 % de la altura. | Zoom-out extremo de 3.7 s que arranca cerrado sobre el hijo; encima aparece la frase del Hero. |
| 02.6 | `02-facial-recognition.webp` | `02-facial-recognition-v.webp` | La cara del chico en el tercio superior; el celular (candado y reloj) cerca del centro, ~55 % de la altura; la laptop puede quedar parcial. | Zoom-in largo hacia el celular (1× → 1.5×). |
| 03.4 | *(desktop: scrub del video)* | `03-fastidio-v.webp` | Imagen fija nueva: el chico con los ojos al techo y la cara completa. Prompt en `00-context/prompts/03-fastidio-imagen-fija.md`. | Fija (el scrub es solo para desktop). |
| 03.8 | `04-shield.webp` | `04-shield-v.webp` | Mamá e hija, cada una con su escudo, **separadas**: que se lea la distancia entre las dos. Sugerencia: una más adelante y abajo, la otra más atrás y arriba. | Zoom suave. |
| 05.5 | `05-crossing.webp` | `05-crossing-v.webp` | Mamá señalando y el hijo en la banqueta, en la mitad inferior; la calle de pantallas fugándose hacia arriba (la perspectiva funciona bien en vertical). | Zoom suave. |
| 09.2 | `06-rules.webp` | `06-rules-v.webp` | El papá centrado, con la tablet y el escudo con palomita visibles. | Zoom suave. |
| 10.7 | `07-together-mother-daughter.webp` | `07-together-mother-daughter-v.webp` | Mamá e hija mirándose, en plano más cerrado; los dos celulares boca abajo visibles abajo. | Zoom suave. |
| 12.6 | `08-autonomy-father.webp` | `08-autonomy-father-v.webp` | El hijo cruzando solo, en primer plano a media altura; el papá atrás, en la banqueta, sin celular; la calle fugándose hacia arriba. | Zoom suave. |

"Zoom suave" es el tratamiento actual (6 %). El zoom de cada escena se define al llegar a su estación.
