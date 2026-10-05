---
project: digizen-landing-b-v04-claude
documento: optimización de imágenes
fecha: 2026-10-05
estado: publicada el 2026-10-05 por indicación del usuario (gh-pages, carpeta b-v04-claude)
---

# Optimización de imágenes de la landing B

Pedido del usuario (2026-10-05): optimizar las imágenes de la B antes de ordenar GitHub, conservando siempre los originales: «a veces se nos pasa la compresión y siempre debemos tener disponibles las originales».

## Qué se hizo

Las mismas imágenes se sirven ahora también en **AVIF**, un formato más eficiente. El WebP que ya estaba publicado no se tocó y queda de respaldo: el navegador que no entiende AVIF recibe exactamente lo mismo que antes.

- **Escenas:** cada `<picture>` ofrece primero el AVIF y después el WebP. La primera imagen (Hero) se precarga en el formato que el navegador va a usar, sin descargar los dos.
- **Secuencias de cuadros** («fastidio», «crossing» y la ADA que saluda): el script de las secuencias (`js/dz-seq.js`) averigua una vez si el navegador decodifica AVIF y pide esos cuadros; si no, los WebP.
- No se bajó la resolución, no se quitaron cuadros y no cambió ninguna composición.

## La garantía de calidad

Ningún AVIF se eligió «a ojo». El build compara cada uno con su referencia y solo lo usa si es **al menos tan fiel como el WebP que reemplaza** (medida SSIM, de 0 a 1) y pesa menos:

- Escenas: la referencia es la imagen fuente reducida a ese ancho. Se prueba de menor a mayor calidad y gana la primera que iguala al WebP.
- «fastidio» y «crossing»: los cuadros AVIF se generan desde el **video original** (no desde el WebP ya comprimido) y deben igualar la fidelidad de los cuadros WebP actuales. Se identificaron los 49 cuadros de cada una en su video.
- ADA que saluda: solo existe en WebP, así que su AVIF debe ser casi idéntico a ese cuadro (SSIM ≥ 0.995).
- Si un AVIF no mejora al WebP, no se genera. Pasó en 4 de 28 variantes de escena (las verticales del Hero, del fastidio y una de «crossing»): esas siguen en WebP.

El detalle por imagen (peso, calidad elegida y fidelidad) queda en `output-code/scripts/avif-report.json`. Además se compararon a ojo recortes al 100 % de los casos de mayor ahorro: sin manchas, sin bandas y con los bordes de ADA limpios.

## Resultado por visitante

| | Antes | Ahora | Ahorro |
|---|---|---|---|
| Escenas, desktop con pantalla retina | 2.38 MB | 1.23 MB | 48 % |
| Escenas, laptop | 1.77 MB | 1.04 MB | 41 % |
| Escenas, teléfono | 0.97 MB | 0.70 MB | 28 % |
| Secuencias (solo desktop) | 11.63 MB | 7.62 MB | 34 % |
| **Total, desktop con pantalla retina** | **14.00 MB** | **8.85 MB** | **37 %** |

La ADA que saluda es la que más baja: de 4.15 MB a 1.78 MB (57 %).

## Dónde están los originales

Nada se sobrescribió. Las fuentes siguen en su lugar y de ellas se derivan las versiones optimizadas:

| Carpeta | Qué guarda |
|---|---|
| `asset-backups/publicado-antes-de-optimizar-2026-10-05/` | **Respaldo anterior a la optimización:** copia exacta de lo publicado ese día (escenas, secuencias, reglas, avatares y OGP; 281 archivos, 23.9 MB, verificada byte a byte). No se toca. |
| `00-context/scenes/` | Escenas fuente y los tres videos de origen de las secuencias. |
| `00-context/scenes-originales-png/` | PNG sin pérdida rescatados de la primera B. |
| `assets/seq/` | Cuadros WebP de las secuencias (los que se publican como respaldo). |
| `output-code/assets/scenes/*-v.webp` | Originales verticales para teléfono. |

**Dos escenas no tienen fuente en `00-context`:** las versiones publicadas de `04-shield` y `08-autonomy-father` son encuadres ampliados (1370 × 796 y 1374 × 798) que se colocaron a mano en `output-code/assets/scenes/`; la carpeta de fuentes guarda el encuadre anterior, más cerrado. El build lo detecta (la imagen publicada no se parece a su fuente) y genera el AVIF desde la imagen publicada, que es la buena. Su única copia de seguridad es el respaldo de arriba.

## Cómo volver atrás

Los WebP publicados no cambiaron, así que basta con quitar los AVIF: en `output-code/scripts/build.py`, dejar `AVIF_QS = ()` y `SEQ_AVIF_QS = ()`, borrar `scripts/avif-report.json` y volver a correr el build. Para una imagen sola: borrar su `.avif` y poner `"avif": null` en su entrada del reporte.

## Verificado

- Build completo: copy sin cambios (151 segmentos, 0 problemas; reglas 798 palabras, mismo orden).
- Ningún WebP ya publicado cambió (comprobado con git).
- En el navegador, con AVIF: el Hero y las tres secuencias piden solo AVIF y las secuencias quedan pintadas; sin errores de consola.
- Simulando un navegador sin AVIF: el Hero y las tres secuencias piden solo WebP; cero AVIF pedidos; sin errores.

## No verificado

- A ojo en un navegador visible y en dispositivos reales: el panel de pruebas estaba oculto y pausa las animaciones, así que las secuencias se probaron con sustitutos de temporizador y decodificación.
- Safari anterior a 16.4, que no decodifica AVIF: debe recibir WebP por el mismo camino del respaldo, pero no se probó en ese navegador.

## Lo que no se hizo (requiere decisión, porque sí cambia cómo se ve)

1. Tope de 1920 px para pantallas retina (hoy bajan la de 2560): ahorraría otro 40 % en la primera imagen, con algo menos de nitidez.
2. Menos cuadros o cuadros más chicos en las secuencias.
3. Imágenes de la página de reglas (0.8 MB en total) y la vertical del fastidio: siguen solo en WebP.
4. Caché larga con nombres versionados: depende del hosting final; GitHub Pages la fija en 10 minutos.

## Observación

La página entra en «modo ligero» cuando el navegador reporta ahorro de datos o conexión 2G/3G: en ese modo las secuencias no se descargan y queda la imagen fija. Es por diseño, pero explica por qué en una conexión lenta las animaciones pueden no aparecer.
