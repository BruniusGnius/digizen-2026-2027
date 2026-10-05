# Estado del proyecto Digizen

Actualizado: 2026-10-05. Este archivo dice cuál es la versión vigente de cada landing, dónde se edita, cómo se publica y dónde están las imágenes. Si algo cambia, se corrige aquí.

## Versiones vigentes

| Landing | Carpeta | Tecnología | Publicada en |
|---|---|---|---|
| **A** (oficial) | `Projects/digizen-landing/` | Angular (`angular-build/`) | https://bruniusgnius.github.io/digizen-2026-2027/ |
| **B** v04-claude, «una estación por gesto» + «Las reglas de ADA» | `Projects/digizen-landing-b-v04-claude/` | HTML + Tailwind + GSAP (`output-code/`) | https://bruniusgnius.github.io/digizen-2026-2027/b-v04-claude/ |

No hay más landings vigentes. Las B anteriores (`digizen-landing-b`, `-b-v2`, `-b-v3`, `-b-v04-codex`) se descartaron el 2026-10-05 por decisión del usuario; algunos documentos de la B todavía las mencionan como historia.

`https://digizen.gnius.club/` es otro sitio, más antiguo y en otro servidor. Este repositorio no lo actualiza.

## Cómo se publica

- **A:** todo lo que llega a `main` y toca `Projects/digizen-landing/angular-build/**` se despliega solo (GitHub Actions, `.github/workflows/deploy-pages.yml`). Por eso los cambios de la A se hacen en una rama aparte, se revisan en local y solo entonces pasan a `main`.
- **B:** se publica a mano: se copia `output-code/` a la carpeta `b-v04-claude/` de la rama `gh-pages`. El despliegue de la A conserva esa carpeta.
- Nada nuevo se publica sin que el usuario lo haya visto y aprobado en local.

## Ramas

| Rama | Para qué |
|---|---|
| `main` | La A vigente. Publicar la A = llegar aquí. |
| `digizen-b-v04-claude` | Trabajo de la B. Incluye también la A al día y las Skills. |
| `gh-pages` | Lo que está en línea. No se edita a mano salvo la carpeta de la B. |

## Imágenes: qué se publica y qué es respaldo

### Landing A

| Carpeta | Qué es | ¿Se publica? |
|---|---|---|
| `angular-build/public/assets/**/*.webp`, `.svg`, `.mp4`, `assets/og/*.jpg` | Lo que usa el sitio (≈19 MB en línea) | Sí |
| `angular-build/public/assets/**/*.png` | Originales de trabajo. El script `npm run optimize:images` los lee de ahí para generar los WebP | No (`angular.json` excluye los PNG) |
| `angular-build/asset-backups/original-images-2026-09-18/` | **Respaldo anterior a la optimización. No se borra.** | No |
| `angular-build/asset-backups/ada-wave-before-secuencia3-2026-09-19/` | Respaldo de la animación de ADA antes de rehacerla | No |

Los PNG de `public/` y los del respaldo están repetidos a propósito: el respaldo es la copia de seguridad. Pendiente menor: `assets/digizen/seo/digizen-ogp-1200x630.psd` (4.9 MB) sí se publica y no debería.

### Landing B

| Carpeta | Qué es | ¿Se publica? |
|---|---|---|
| `output-code/assets/` (escenas por ancho, `seq/`, `reglas/`, `og/`, `logo/`, `vendor/`) | Lo que usa el sitio (≈19 MB en línea) | Sí |
| `output-code/assets/scenes/*-v.webp` (sin número de ancho) | Originales verticales; el build genera de ahí las versiones de teléfono | No |
| `00-context/scenes/` | Escenas fuente (WebP) y los videos de origen de las animaciones | No |
| `00-context/scenes-originales-png/` | Originales PNG sin pérdida, rescatados de la primera B antes de descartarla | No |
| `assets/seq/`, `assets/avatars/` | Fuentes de las animaciones de cuadros y los avatares | No |
| `asset-backups/publicado-antes-de-optimizar-2026-10-05/` | **Respaldo anterior a la optimización (2026-10-05). No se borra.** | No |
| `imagenes-no-publicadas/` | Opciones que no se publican. Incluye lo recuperado de las B descartadas: 4 escenas en versión web y 30 capturas de revisión de la primera B (ver su `LEEME.md`) | No |

La B se optimizó el 2026-10-05: sirve AVIF con el WebP de siempre como respaldo, 37 % menos peso en desktop sin perder fidelidad. Está en la rama, **sin publicar**. Detalle, garantías y cómo volver atrás: `Projects/digizen-landing-b-v04-claude/03-optimizacion-imagenes.md`.

## Skills del proyecto

`Skills/landing-builder/`, `Skills/apple-design/` y `Skills/gsap/` son parte del proyecto y están en git. Las instrucciones para agentes están en `AGENTS.md`.

## Reglas del usuario (2026-10-05)

- **Nada desaparece.** Lo que se elimine pasa por la Papelera. Las imágenes no publicadas y los PSD se conservan como opciones: en la A, en `Projects/digizen-landing/imagenes-no-publicadas/`.
- **Siempre hay originales** antes de comprimir.
- **Las páginas publicadas en GitHub Pages no cambian** mientras su jefe las revisa, incluidas las vistas previas de las B descartadas (`b-v2-preview-claude/`, `codex-b-alpha/`).
- `Digizen-Cinco-Creencias-Diseno-2026-09-22/` y su `.zip` se quedan: es el ejemplo del jefe que dio origen a la B.

## Listo en ramas, esperando visto bueno para publicar

| Qué | Rama | Estado |
|---|---|---|
| A: la ADA del CTA no aparecía al volver de «Reglas de ADA» | `digizen-a-fix-ada-al-volver` | Corregido y probado en local. Publicar = pasar a `main`. |
| B: optimización de imágenes (AVIF con respaldo WebP) | `digizen-b-v04-claude` | Hecha y probada en local. Publicar = copiar `output-code/` a `gh-pages/b-v04-claude/`, incluidos los `.avif`. |

## Pendientes

- **OGP de la A:** el nuevo (JPG y PSD del 2026-09-30) todavía no está en línea; la página sigue citando `assets/og/digizen-og-control-caduca-criterio-no.jpg`. Los archivos nuevos esperan en `angular-build/public/assets/digizen/seo/` (sin guardar en git) y hay copia en `imagenes-no-publicadas/ogp-2026-09-30/`. Al actualizarlo, sacar el PSD de `public/` para que no se publique.
- **Orden en GitHub** (cuando termine la revisión): llevar la B, las Skills y este mapa a `main`; borrar las ramas ya integradas. Las vistas previas publicadas no se retiran sin que el usuario lo pida.
- Revisión a ojo, en navegador visible y en dispositivos reales, de las dos piezas de la tabla de arriba.
