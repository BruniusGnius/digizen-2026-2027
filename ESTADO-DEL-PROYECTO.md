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
| `00-context/scenes-originales-png/` | Originales PNG sin pérdida, rescatados de la primera B antes de descartarla. Todavía no están en git | No |
| `assets/seq/`, `assets/avatars/` | Fuentes de las animaciones de cuadros y los avatares | No |

La B no tiene todavía un respaldo «antes de optimizar» porque su optimización está pendiente (ver `Projects/digizen-landing-b-v04-claude/03-build-notes-reglas.md`, sección de optimización de imágenes).

## Skills del proyecto

`Skills/landing-builder/`, `Skills/apple-design/` y `Skills/gsap/` son parte del proyecto y están en git. Las instrucciones para agentes están en `AGENTS.md`.

## Pendientes de orden

- Archivos de la A que siguen solo en este disco, sin guardar en git: un OGP nuevo (`seo/digizen-ogp-1200x630.jpg` y `.psd`, modificados el 2026-09-30), dos imágenes fuente de las reglas, tres documentos y dos imágenes borradas en local. Falta decidir cuáles se guardan y si el OGP nuevo se publica.
- `Digizen-Cinco-Creencias-Diseno-2026-09-22/` y su `.zip`, en la raíz: sin guardar en git; falta decidir su lugar.
- Orden en GitHub: llevar la B y las Skills a `main`, retirar las vistas previas de las B descartadas (`b-v2-preview-claude/`, `codex-b-alpha/`) y borrar las ramas que ya no se usan.
- Optimización de imágenes de la B.
