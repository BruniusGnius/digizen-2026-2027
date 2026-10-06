# Sistema de diseño Digizen (landing A)

Guía y librería de componentes del diseño de la landing A, en una sola página HTML.
Sirve para llevar ese diseño a otro proyecto: explica por qué se ve así, con qué se construye,
cómo se comporta y trae cada componente ya diseñado con su marcado.

**Esta carpeta no modifica la landing.** El generador solo la lee. Todo lo que hay aquí es nuevo.

## Cómo verla

Abre `index.html` en el navegador (doble clic). No necesita servidor ni conexión.

Si se prefiere con servidor local, desde la raíz del proyecto:

```bash
python3 -m http.server 4306 --bind 127.0.0.1 --directory Projects/digizen-sistema-de-diseno
```

y entrar a `http://localhost:4306/`.

## Cómo está organizada

| Parte | Qué contiene |
| --- | --- |
| 1 · Filosofía | Intención, los 7 principios y las decisiones vigentes con su fecha |
| 2 · Fundamentos | Color (con tabla de contraste calculada), tipografía, espacio y retícula, forma y elevación, iconos, imágenes, movimiento, temas claro y oscuro |
| 3 · Experiencia | Una decisión por momento, navegación, lectura por capas, formularios y diálogo, accesibilidad, rendimiento, contenido |
| 4 · Guía de componentes | 18 fichas: para qué sirve, partes, medidas, estados, variantes y reglas de uso |
| 5 · Librería | 28 ejemplos pintados con el CSS real y su marcado («Ver el marcado») |

El botón de arriba a la derecha cambia entre tema claro y oscuro; todos los ejemplos cambian con él.

## Para usarla en otro proyecto

La carpeta es autosuficiente. Lo que se lleva:

- `css/digizen-a.css` y `css/media/` — el CSS de la landing ya compilado, con la tipografía Inter. Trae los tokens `--dg-*` y todas las clases `dg-*`.
- `css/digizen-ajustes.css` — la regla del sistema que la landing todavía no aplica. Se carga después de `digizen-a.css`.
- `assets/` — logos, escenas y avatares que usan los ejemplos.
- El marcado de cada componente se copia de «Ver el marcado» en la librería.

`css/guia.css` y `js/guia.js` son solo el marco de esta guía (clases `ds-*`); no hacen falta en otro proyecto.

El tema oscuro se activa con `data-theme="dark"` en la etiqueta `<html>`.

## Archivos

| Archivo | Qué es |
| --- | --- |
| `index.html` | La guía. **Se genera**: no editarla a mano |
| `plantilla.html` | El texto de la guía, con marcas `<!--@…-->` donde entra lo generado. Aquí se edita la redacción |
| `construir.py` | El generador |
| `fuente/landing.html`, `fuente/reglas.html` | Instantáneas de la landing ya renderizada (portada y Reglas de ADA). De ahí sale el marcado de los ejemplos |
| `css/digizen-a.css`, `css/media/` | Copia del CSS compilado de la landing y sus fuentes |
| `css/digizen-ajustes.css` | Regla del sistema que la landing aún no aplica. Se escribe a mano y no se pisa al recopiar el CSS |
| `css/guia.css`, `js/guia.js` | Marco de la guía: índice, recuadros de ejemplo, cambio de tema |
| `assets/` | Imágenes de los ejemplos, copiadas de la landing por el generador |

## Cómo regenerarla

```bash
cd Projects/digizen-sistema-de-diseno
```

```bash
python3 construir.py
```

Al terminar avisa cuántos ejemplos colocó (deben ser 28 de 28) y si hay identificadores repetidos
o enlaces sin destino.

El generador lee en vivo los tokens y las reglas tipográficas de
`../digizen-landing/angular-build/src/styles.css`, así que las tablas de color, contraste y
tipografía se actualizan solas al regenerar.

## Cómo actualizarla cuando cambie la landing A

Tres cosas son copias y hay que volver a tomarlas. Solo las que correspondan al cambio:

1. **Cambió el CSS** (colores, medidas, un componente): compilar la landing y copiar el resultado.

   ```bash
   npm run build --prefix Projects/digizen-landing/angular-build
   ```

   Copiar `dist/angular-build/browser/styles-*.css` a `css/digizen-a.css` y la carpeta
   `dist/angular-build/browser/media/` a `css/media/`.
   (Compilar no publica nada; solo escribe en `dist/`.)

2. **Cambió el contenido o el marcado de un componente**: volver a tomar la instantánea.
   Con la landing abierta en local, a ancho de escritorio y recorrida hasta el final, en la consola del navegador:

   ```js
   copy(document.querySelector('.dg-shell').outerHTML)
   ```

   Pegar en `fuente/landing.html`. Repetir en `/reglas-de-ada` y pegar en `fuente/reglas.html`.

3. **Cambió una imagen**: nada que hacer; el generador vuelve a copiar las que sean más recientes.

Después, `python3 construir.py`.

Si un componente cambió de nombre de clase, el generador se detiene al no encontrarlo: se ajusta
su línea en la función `libreria()` de `construir.py`.

## Ajuste respecto a la landing publicada

El sistema va un paso adelante de la landing en una regla (5 de octubre de 2026): **las tarjetas de un
mismo grupo miden lo mismo de alto, también entre filas**. En la landing cada fila toma su propia altura
(en Reglas de ADA, 305 y 328 px a 1280 px de ancho). Está en `css/digizen-ajustes.css` y explicada en la
guía, en Filosofía → «Ajuste respecto a la landing publicada».

La tarjeta de precio destacada es más grande que la otra a propósito: es la única excepción y no se toca.

Si un día la regla se lleva a la landing A, se borra de ese archivo y de la tabla de la guía.

## Qué no cubre

- **La landing B** (scroll, GSAP). Su sistema es otro: «Tipografía esencial» y «Scroll Patterns».
- Los textos de la guía (filosofía, experiencia, fichas) están escritos a mano en `plantilla.html`:
  si una decisión de diseño cambia, hay que actualizar ahí su explicación.

Estado: 5 de octubre de 2026, sobre la landing A publicada ese día.
