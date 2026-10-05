# Auditorías de Lighthouse

Aquí se guardan las mediciones de Lighthouse que sirven de referencia. Cada carpeta es una fecha.

**Cómo medir para que valga:** en una **ventana de incógnito** (las extensiones de Chrome falsean el resultado), una vez para desktop y otra para móvil, y guardar el reporte como JSON. El JSON se puede abrir en https://googlechrome.github.io/lighthouse/viewer/.

## 2026-10-05 · línea base

Lighthouse 13.4.1, incógnito, sobre lo publicado ese día en GitHub Pages: la A y la B con la optimización de imágenes (AVIF), **antes** de las mejoras de la rama `mejoras-lighthouse`.

| Página | Rendimiento | Accesibilidad | Buenas prácticas | SEO | Primer pintado | Imagen o texto principal | Bloqueo | Salto de diseño | Peso |
|---|---|---|---|---|---|---|---|---|---|
| A · desktop | 99 | 96 | 100 | 100 | 0.4 s | 0.8 s | 0 ms | 0.002 | 7,389 KiB |
| A · móvil | 88 | 96 | 100 | 100 | 1.7 s | 3.8 s | 70 ms | 0 | 7,594 KiB |
| B · desktop | 97 | 100 | 100 | 66 | 0.8 s | 1.2 s | 0 ms | 0 | 8,750 KiB |
| B · móvil | 93 | 100 | 100 | 66 | 1.7 s | 3.0 s | 0 ms | 0 | 760 KiB |

Lo que dejó esta medición:

- El SEO de 66 en la B es a propósito: está marcada como vista previa (`noindex`) mientras la A es la oficial.
- Con las extensiones del navegador del usuario, la A bajaba a 75 (desktop) y 48 (móvil) por un salto de diseño de 0.85–1.0, y aparecían 1.9 MB de «JavaScript sin usar» y errores de consola que eran de las extensiones. Esos reportes no se conservaron.
- Correcciones hechas a partir de aquí: ver `Projects/digizen-landing/03-build-notes.md` («Mejoras tras la auditoría de Lighthouse») y `Projects/digizen-landing-b-v04-claude/03-optimizacion-imagenes.md`.
- La caché marcada por Lighthouse depende del servidor: GitHub Pages la fija en 10 minutos.
