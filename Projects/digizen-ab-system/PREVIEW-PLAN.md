# Prueba en `digizen-demo.gnius.club`

## Estado actual: dos flujos de prueba

El 2026-10-14 se activó una API PHP real **solo** en el document root de `digizen-demo.gnius.club`, con código y configuración privada en `/home/u502287134/digizen-conversion-api-preview/`. La base existente `u502287134_digizen_conv` estaba vacía y recibió siete tablas. Eventos y leads incluyen `environment=preview`, para poder retirar únicamente datos QA antes del lanzamiento. `health.php` devuelve `database=ready`. El sitio activo `/digizen` no se modificó.

| Flujo | Estado QA | Pendiente |
|---|---|---|
| Conversar con Ada | Solicitudes A y B guardadas en MySQL. A con correo y consentimiento pasó a `synced` en Acumbamail; B con teléfono ficticio y sin consentimiento quedó `not_applicable`. | La URL de ADA sigue simulada; revisar los campos opcionales en Acumbamail. |
| Compra | El evento `checkout_started` de B quedó en MySQL. | El endpoint de checkout devuelve 503 por la pausa de Stripe y de la oferta/precios; no hubo cobro. |

Clarity ya se carga en las landings adultas A y B de la demo con `digizen_environment=preview`, `digizen_variant` y `digizen_landing_id`. Los formularios se marcan `data-clarity-mask=True`. Para probar manualmente el formulario, usar nombre que empiece por `QA ` y correo `bruno+variable@gnius.club` o teléfono ficticio `+52 55 0000 0000`; el backend rechaza otros datos en la demo. El subdominio sigue sin contraseña, como pidió el usuario.

La sincronización de Acumbamail se ejecutó una vez manualmente. **No hay cron configurado aún**: nuevos leads con consentimiento quedarán `pending` hasta ejecutar `php /home/u502287134/digizen-conversion-api-preview/src/retry-acumbamail.php` o instalar un cron restringido a QA. Antes de publicarlo formalmente, revisar los registros `environment=preview` y limpiarlos de forma selectiva.

El 2026-10-14 se corrigió en la demo únicamente `b/reglas-de-ada/index.html`: `<base href="/b/">` estaba después del enlace relativo a `dist/styles.css` y se movió al inicio de `<head>`. Se guardó una copia local anterior en `/private/tmp/digizen-demo-reglas-b-before-20261014.html`; el HTML servido por HTTPS coincide con la huella del archivo corregido y `/b/dist/styles.css` responde 200. La página volvió a mostrar estilos e imágenes en la inspección visual de escritorio y móvil. No se modificó `/digizen` ni otro archivo del hosting.

Consulta de solo lectura de MySQL en la API privada de QA: hay dos leads `environment=preview`. El A tiene nombre de 8 caracteres, variante `A`, `utm_source=qa_ab_2026_10`, consentimiento de marketing y estado Acumbamail `synced` con un intento. El B tiene nombre de 8 caracteres, variante `B`, el mismo UTM, sin consentimiento y estado `not_applicable`. Hay 30 eventos y ningún registro en notas, usuarios del panel, sesiones de checkout o compras. Esto confirma que MySQL conservó los datos que faltan en la lista de Acumbamail; queda revisar el mapeo del webhook de entrada en esa plataforma.

## Historial de la primera demostración simulada

Estado 2026-10-14: el usuario creó el subdominio con document root `/home/u502287134/domains/gnius.club/public_html/digizen-demo`. Se transfirió únicamente `preview-package/public/` a esa ruta tras un `rsync --dry-run` revisado. La carpeta está al mismo nivel que `/digizen`; no se transfirió nada a la versión vigente. El archivo `default.php` que Hostinger creó en la carpeta nueva se dejó intacto y no impide que `/` sirva nuestro `index.html`.

Verificación realizada: SSH autenticado; ruta real distinta de `/digizen` y sin enlace simbólico; 912 archivos públicos transferidos sin `--delete`; PHP 8.2.34 validó la sintaxis de los cinco endpoints; `https://digizen-demo.gnius.club/api/health.php` respondió 200 con `preview_mock`; `/`, `/a/`, `/b/`, ambas reglas y la confirmación respondieron 200. Una solicitud ficticia respondió 201 con `demo_simulated=true`, un origen ajeno recibió 403 y un evento ficticio respondió 202. No se creó base de datos de pruebas ni se guardaron contactos.

## Primera demostración: A/B y ADA simulado

La primera versión se generó con `python3 Projects/digizen-ab-system/preview.py`. Para regenerar la versión **actual** con API real, usar `python3 Projects/digizen-ab-system/preview.py --real-api`; ese comando rehace `preview-package/`, así que se debe volver a generar su `private/config/secrets.php` local antes de cualquier despliegue privado. El ZIP público no incluye `.env`, credenciales, código privado ni la carpeta `private/`.

Esta primera versión usa una API PHP de simulación en `/api/`: no conecta MySQL, no guarda nombres, correos o teléfonos y no llama a Acumbamail. Devuelve un código ficticio y una confirmación que indica que ADA aún no está activo. Los endpoints de pago responden 503. Clarity solo se carga en `digizen.gnius.club`, por lo que queda apagado aquí. No habrá panel interno en esta primera demostración.

Las páginas muestran una banda de **sitio de prueba**, llevan `noindex,nofollow,noarchive` y un `robots.txt` con `Disallow: /`. Por instrucción del usuario, **el subdominio no lleva contraseña hasta nuevo aviso**. Cualquiera con la URL podrá abrirlo; usar únicamente datos ficticios.

## Subir el ZIP en hPanel

1. Confirmar que `https://digizen-demo.gnius.club/` resuelve con HTTPS. **Hecho el 2026-10-14** con `curl`, validando el certificado. Una prueba inicial con el almacén de certificados de Python falló localmente, mientras `curl` validó la conexión; no fue un fallo del certificado del subdominio.
2. Abrir el Administrador de archivos de Hostinger en **la ruta exacta** `/home/u502287134/domains/gnius.club/public_html/digizen-demo`. Verificar que la ruta no es `/digizen`.
3. Subir `preview-package/digizen-demo-public.zip` y extraerlo **dentro de esa carpeta**, o usar el script SSH de abajo. **Hecho por SSH el 2026-10-14**: `index.html`, `a/`, `b/`, `api/`, `demo-ada-confirmado/` y `robots.txt` quedaron directamente dentro de `digizen-demo`.
4. Probar `/api/health.php`: debe responder `{"ok":true,"mode":"preview_mock","database":"not_connected"}`. Probar `/?variant=A`, `/?variant=B`, ambas reglas y una solicitud con contacto ficticio. **Verificado por HTTP y API el 2026-10-14**; queda una revisión visual en navegador por parte del usuario.
5. Compartir el enlace para revisar copy y funcionamiento. Mantener la versión de `/digizen` intacta.

La clave SSH ED25519 exclusiva está en `.ssh/digizen_demo_ed25519`; el usuario registró su parte pública en hPanel con el nombre `digizen-ab-test-demo` (huella `SHA256:PhmWsRQCrxXYgQnq8hMaSLpZSiFcROhiaPQRw0C8N5M`). La privada está excluida de Git y del ZIP. `python3 Projects/digizen-ab-system/upload-preview.py` ejecuta `rsync --dry-run` y `--apply` transfiere solo al destino exacto, sin `--delete`. La clave puede revocarse en hPanel cuando termine el trabajo de pruebas. No introducir contraseñas ni la clave privada en este chat.

## Segunda etapa: API con datos de prueba

`preview-package/private/` prepara el código para una futura prueba real de PHP/MySQL, pero **no se sube en la primera demostración**. Para activarla habrá que crear una base MySQL y usuario exclusivos de pruebas, instalar la carpeta privada fuera de `public_html`, verificar el aviso de privacidad y reemplazar la API simulada de forma controlada. Las credenciales reales del `.env` de DIGIZEN no deben copiarse a esa base de pruebas.

## Deshacer la primera demostración

Retirar solo los archivos de `/home/u502287134/domains/gnius.club/public_html/digizen-demo` después de verificar la ruta exacta. No hay datos ni base de pruebas que migrar en esta etapa. No tocar `/home/u502287134/domains/gnius.club/public_html/digizen`.
