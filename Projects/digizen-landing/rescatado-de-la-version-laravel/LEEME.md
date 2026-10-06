# Rescatado de la versión en Laravel

La landing A tuvo una primera versión en Laravel (vistas Blade + Vite), compilada el 11 de septiembre de 2026.
Vivía en `Projects/digizen-landing/output-code/`. Dejó de usarse cuando la landing pasó a Angular
(`angular-build/`), y se desechó el 6 de octubre de 2026.

Aquí queda lo único de esa carpeta que no existía en otro lado y puede servir: el boceto de cómo se iba a
conectar con el backend.

| Archivo | Qué es | Venía de |
| --- | --- | --- |
| `digizen.php` | Configuración de frontend: modo, dirección para enviar el formulario y tres destinos de pago (`monthly`, `cycle`, `cash`) | `desarrollo/config/digizen.php` |
| `env.example` | Las variables de entorno que alimentan esa configuración | `desarrollo/.env.example` (se le quitó el punto inicial para que se vea en Finder) |
| `lead.js` | Validación del formulario de ADA, los datos que se iban a enviar (`parent_name`, `channel`, `contact`, `source`) y los mensajes para los errores 419, 422 y 429 | `desarrollo/resources/js/lib/lead.js` |

Es un boceto de septiembre: no refleja la landing actual. Entonces había tres destinos de pago; hoy la
landing A ofrece dos planes (contado y mensualidades).

## Qué no se rescató, y por qué

- **Imágenes:** no tenía propias. Usaba fotos provisionales de Picsum, por internet.
- **Texto:** su `copy-fuente-inmutable.md` era una copia idéntica de `00-context/digizen-copy-ola.md`, que sigue ahí.
- **Canon y prompts de imágenes:** nunca estuvieron en esa carpeta. Siguen en `Projects/digizen-landing/`
  (`05-image-generation-canon-…`, `digizen-v05-mision-clara-image-canon-…` y los archivos `06` a `10`).
- **Tipografías:** las mismas Inter que ya usa la landing actual.
- **Código** (vistas Blade, estilos, pruebas) y seis capturas de pantalla de las pruebas de esa versión.

## Dónde quedó lo desechado

- En la Papelera del disco SACHI: «output-code (landing A en Laravel, desechada 2026-10-06)».
- En el historial de git: la carpeta completa está en el commit `833fbac` y anteriores
  (`git show 833fbac:Projects/digizen-landing/output-code/produccion/LEEME.md`, por ejemplo).
  Fuera de git solo estaban las dependencias instaladas, la compilación y las capturas de las pruebas.
