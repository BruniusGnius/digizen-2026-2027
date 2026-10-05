# Estado del proyecto Digizen

Actualizado: 2026-10-05. Este archivo dice cuál es la versión vigente de cada landing, dónde se edita, cómo se publica y dónde están las imágenes. Si algo cambia, se corrige aquí.

## Todo está en un solo lugar

- **En GitHub:** la rama `main` tiene la landing A, la landing B, las Skills y este mapa.
- **En local:** la carpeta del proyecto en el disco SACHI, en la rama `main`. Es la única copia de trabajo.

## Versiones vigentes

| Landing | Carpeta | Tecnología | Publicada en |
|---|---|---|---|
| **A** (oficial) | `Projects/digizen-landing/` | Angular (`angular-build/`) | https://bruniusgnius.github.io/digizen-2026-2027/ |
| **B** v04-claude, «una estación por gesto» + «Las reglas de ADA» | `Projects/digizen-landing-b-v04-claude/` | HTML + Tailwind + GSAP (`output-code/`) | https://bruniusgnius.github.io/digizen-2026-2027/b-v04-claude/ |

No hay más landings vigentes. Las B anteriores (`digizen-landing-b`, `-b-v2`, `-b-v3`, `-b-v04-codex`) se descartaron el 2026-10-05 por decisión del usuario; algunos documentos de la B todavía las mencionan como historia. Sus vistas previas publicadas (`b-v2-preview-claude/`, `codex-b-alpha/`) siguen en línea y no se retiran sin que el usuario lo pida.

`https://digizen.gnius.club/` es otro sitio, más antiguo y en otro servidor. Este repositorio no lo actualiza.

## Cómo se publica

- **A:** todo lo que llega a `main` y toca `Projects/digizen-landing/angular-build/**` se despliega solo (GitHub Actions, `.github/workflows/deploy-pages.yml`). **Cuidado:** editar esos archivos directamente en `main` y subirlos es publicar. Los cambios de la A se hacen en una rama corta, se revisan en local y solo entonces pasan a `main`.
- **B:** se publica a mano: se copia `output-code/` a la carpeta `b-v04-claude/` de la rama `gh-pages` (páginas, `dist/`, `js/` y, de `assets/`, lo que haya cambiado, incluidos los `.avif`). Los cambios de la B en `main` no publican nada por sí solos.
- **Orden al publicar las dos:** primero la A; cuando su despliegue termina, la B. El despliegue de la A reescribe `gh-pages` conservando las carpetas `b-*` y `codex-*` tal como las encuentra.
- Nada nuevo se publica sin que el usuario lo haya visto y aprobado.

## Ramas

| Rama | Para qué |
|---|---|
| `main` | Todo lo vigente: A, B, Skills y documentos. |
| `gh-pages` | Lo que está en línea. No se edita a mano salvo la carpeta de la B. |
| `gh-pages-backup-2026-10-01` | Respaldo de lo publicado ese día. Se conserva. |
| `digizen-a-reglas-ada` | Igual a un punto anterior de `main`; la usa la copia de Codex. Se borra cuando esa copia se retire. |

En local quedan además tres ramas viejas que no se usan (`backup-before-attribution-fix`, `digizen/refinamiento-visual` y un `gh-pages` local atrasado). No estorban; se conservan por la regla de no borrar.

## Imágenes: qué se publica y qué es respaldo

Las dos landings sirven cada imagen en **AVIF** con el **WebP** de siempre como respaldo (optimización del 2026-10-05). Cada AVIF se comparó con su original y solo se usa si es al menos tan fiel como el WebP que acompaña.

### Landing A

| Carpeta | Qué es | ¿Se publica? |
|---|---|---|
| `angular-build/public/assets/**/*.avif`, `.webp`, `.svg`, `.mp4`, `assets/og/*.jpg` | Lo que usa el sitio | Sí |
| `angular-build/public/assets/**/*.png` | Originales de trabajo. De ahí salen los WebP (`npm run optimize:images`) y los AVIF (`python3 scripts/make-avif.py`) | No (`angular.json` excluye PNG y PSD) |
| `angular-build/asset-backups/original-images-2026-09-18/` | **Respaldo anterior a la optimización. No se borra.** | No |
| `angular-build/asset-backups/ada-wave-before-secuencia3-2026-09-19/` | Respaldo de la animación de ADA antes de rehacerla | No |
| `imagenes-no-publicadas/` | Opciones que no se publican: el OGP nuevo con su PSD y dos imágenes fuente de las reglas | No |

Los PNG de `public/` y los del respaldo están repetidos a propósito: el respaldo es la copia de seguridad. Detalle de la optimización: `Projects/digizen-landing/03-build-notes.md` y `angular-build/scripts/avif-report.json`.

### Landing B

| Carpeta | Qué es | ¿Se publica? |
|---|---|---|
| `output-code/assets/` (escenas por ancho en AVIF y WebP, `seq/`, `reglas/`, `og/`, `logo/`, `vendor/`) | Lo que usa el sitio | Sí |
| `output-code/assets/scenes/*-v.webp` (sin número de ancho) | Originales verticales; el build genera de ahí las versiones de teléfono | No |
| `00-context/scenes/` | Escenas fuente (WebP) y los videos de origen de las animaciones. Los tres videos no están en git (`.gitignore`): viven solo en este disco | No |
| `00-context/scenes-originales-png/` | Originales PNG sin pérdida, incluidas las versiones no elegidas (por ejemplo, papá e hijo en la escena 07 y mamá en la 08) | No |
| `assets/seq/`, `assets/avatars/` | Fuentes de las animaciones de cuadros y los avatares | No |
| `asset-backups/publicado-antes-de-optimizar-2026-10-05/` | **Respaldo anterior a la optimización. No se borra.** | No |
| `imagenes-no-publicadas/` | Opciones que no se publican, incluido lo recuperado de las B descartadas (ver su `LEEME.md`) | No |

Detalle, garantías y cómo volver atrás: `Projects/digizen-landing-b-v04-claude/03-optimizacion-imagenes.md`.

## Skills del proyecto

`Skills/landing-builder/`, `Skills/apple-design/` y `Skills/gsap/` son parte del proyecto y están en git. Las instrucciones para agentes están en `AGENTS.md`.

## Reglas del usuario

- **Nada desaparece.** Lo que se elimine pasa por la Papelera. Las imágenes no publicadas y los PSD se conservan como opciones en las carpetas `imagenes-no-publicadas/`.
- **Siempre hay originales** antes de comprimir.
- **Lo publicado se cuida:** su jefe revisa las direcciones de GitHub Pages; no se retira ni se cambia nada publicado sin que el usuario lo pida.
- `Digizen-Cinco-Creencias-Diseno-2026-09-22/` y su `.zip` se quedan: es el ejemplo del jefe que dio origen a la B.

## Publicado el 2026-10-05

- **A:** botones principales con el degradado del logo; corrección de la ADA del CTA, que no aparecía al volver de «Reglas de ADA»; optimización de imágenes (escenas y los 130 cuadros de ADA en AVIF); el PSD del OGP deja de publicarse.
- **B:** optimización de imágenes (escenas y animaciones de cuadros en AVIF con respaldo WebP).

## Pendientes

- **Copia de Codex de la A** (`~/.codex/worktrees/digizen-a-content/`): ya no hace falta; todo su contenido está en `main`. No se retiró porque otro chat tenía una vista previa corriendo desde ahí. Al cerrarla, la carpeta va a la Papelera y se borra la rama `digizen-a-reglas-ada`.
- **OGP de la A:** el nuevo (JPG y PSD del 2026-09-30) todavía no está en línea; la página sigue citando `assets/og/digizen-og-control-caduca-criterio-no.jpg`. Los archivos nuevos esperan en `angular-build/public/assets/digizen/seo/` (sin guardar en git) y hay copia en `imagenes-no-publicadas/ogp-2026-09-30/`.
- **Revisión a ojo** de lo publicado, en un navegador normal y en dispositivos reales: las pruebas automáticas se hicieron con el panel oculto, que pausa las animaciones.
- **Optimización que sí cambia cómo se ve** (requiere decisión): tope de 1920 px en pantallas retina y menos cuadros en las secuencias de la B; las 17 imágenes sueltas y el video del reloj de la A.
