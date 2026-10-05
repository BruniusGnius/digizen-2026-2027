# Imágenes no publicadas de la landing B

Aquí se conservan, como opciones, las imágenes que no se publican. Nada de esta carpeta sale al sitio.

Regla del proyecto (usuario, 2026-10-05): nada se borra. Lo que deja de usarse se guarda; lo que se elimina pasa por la Papelera.

## `de-las-b-descartadas/`

Recuperado el 2026-10-05 de las cuatro landings B descartadas (`digizen-landing-b`, `-b-v2`, `-b-v3` y `-b-v04-codex`), que están en la Papelera del disco SACHI.

Esas carpetas tenían 181 imágenes y videos (67 MB). Se comparó cada archivo, byte a byte, contra lo que ya está guardado en git:

- **139 ya estaban en el proyecto**, idénticas (no se copiaron otra vez):
  - los PNG originales sin pérdida de las escenas y sus versiones de trabajo → `../00-context/scenes-originales-png/` (rescatados antes de descartar las carpetas);
  - las escenas WebP y los tres videos de origen de las animaciones → `../00-context/scenes/`;
  - logos y favicon → en la landing A (`Projects/digizen-landing/angular-build/public/`).
- **8 estaban repetidas** dentro de las mismas carpetas descartadas.
- **34 solo existían ahí** y son las que se guardaron aquí:

| Carpeta | Qué hay |
|---|---|
| `escenas-version-web-primera-b/` | 4 escenas de la primera B en su versión WebP para web: `02-time`, `04-distance`, `07-together` y `08-autonomy`. Sus originales PNG están en `../00-context/scenes-originales-png/`. |
| `capturas-de-revision-primera-b/` | 30 capturas de pantalla de la primera B (Hero, historia, chat, formulario y «antes de decidir») en seis tamaños: ancho, desktop, tablet, horizontal, móvil y pequeño. Sirven como registro de cómo se veía. |

Con esto, ninguna imagen de las B descartadas queda solo en la Papelera. Lo que sí queda solo ahí no son imágenes: código, documentos de diseño y wireframes, tipografías y un zip de entrega (`digizen-landing-b/delivery/digizen-b-previa-autocontenida-2026-09-24.zip`).
