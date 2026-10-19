# DIGIZEN: fase 2 local de A/B, captación y medición

Estado: **demostración QA con API PHP real publicada en `digizen-demo.gnius.club` el 2026-10-14**; la versión activa de DIGIZEN permanece intacta. Stripe, precios y cobros siguen pausados. La URL de ADA sigue simulada.

Restricción vigente: `Projects/digizen-landing/` y `Projects/digizen-landing-b-v04-claude/` se usan solo como fuentes de lectura. Las nuevas correcciones se preparan dentro de `Projects/digizen-ab-system/`; el lanzador local no reconstruye ni escribe en los proyectos origen.

Para la demostración en el subdominio independiente, ver [PREVIEW-PLAN.md](PREVIEW-PLAN.md) y regenerar `preview-package/` con `python3 preview.py --real-api` si cambia el código. El usuario indicó que el subdominio no lleve contraseña hasta nuevo aviso.

Para validar el alta real en Acumbamail y los campos de la lista, ver [ACUMBAMAIL-TEST.md](ACUMBAMAIL-TEST.md). El script `test-acumbamail.py` no envía nada sin `--send` y un correo controlado.

La promoción de la demo al dominio final se describe en [RELEASE-PLAN.md](RELEASE-PLAN.md): mismo código fuente, paquete de producción, respaldo y cambio del router al final.

La revisión local de funciones y los textos a resolver antes de publicar están en [QA-LOCAL-Y-COPY.md](QA-LOCAL-Y-COPY.md).

El usuario creó `digizen-demo.gnius.club` con document root `/home/u502287134/domains/gnius.club/public_html/digizen-demo`. La primera entrega tuvo una API simulada; después se activó la API real con código privado en `/home/u502287134/digizen-conversion-api-preview/` y la base DIGIZEN existente, según decisión del usuario. Eventos y leads llevan `environment=preview`; el panel sigue sin publicarse.

## Qué contiene

- `router/index.html`: asignación A/B 50/50, persistencia 90 días en cookie y `localStorage`, QA con `?variant=A|B`, conservación de UTM y `ab_variant` diagnóstico.
- `frontend/digizen-ab.js`: telemetría anónima hacia `/api/events.php`, Clarity con tags anónimos en las landings adultas de producción y demo, captura de formulario ADA hacia `/api/leads.php`.
- `frontend/demo-ada-confirmado.html`: confirmación de solicitud; muestra la `demo_url` devuelta por la API. No muestra un enlace `.example` en dominio público.
- `api/schema.sql`: tablas propias de eventos, leads, seguimiento comercial, cuentas del panel y reserva de esquema para pagos pausados.
- `api/public/`: endpoints PHP públicos. `checkout.php` y `stripe-webhook.php` devuelven 503 mientras pagos estén pausados.
- `api/src/`: código privado de conexión, validación, reintentos de Acumbamail y administración.
- `api/admin/`: panel PHP con login, leads, filtros, notas, seguimiento y CSV.
- `stage.py`: genera **solo archivos locales** en `staging/`; no se conecta a Hostinger.
- `simulate.py`: sirve `staging/` únicamente en `127.0.0.1` y simula en memoria la respuesta de eventos y solicitudes ADA. No usa `.env`, MySQL ni Acumbamail.

Las fuentes de A y B permanecen en sus proyectos separados. A se compila con base `/a/`. B sigue siendo HTML/CSS/JS generado por Python. El paquete excluye páginas de prueba, fuentes, `.env`, `secrets.php`, `node_modules` y código privado.

## Vista local sin modificar los proyectos origen

Para abrir el sistema en tu Mac, haz doble clic en `ver-local.command` (o ejecútalo desde Terminal). Lee los builds existentes de A y B, prepara `staging/` **solo dentro de `digizen-ab-system/`**, verifica recursos y router, inicia `http://127.0.0.1:8765/` y abre el navegador. Deja la ventana de Terminal abierta; `Control+C` detiene el servidor. `ver-local.command --check` hace la revisión sin abrir servidor. El lanzador no reconstruye ni escribe en `digizen-landing` o `digizen-landing-b-v04-claude`.

Para ejecutar solo la revisión desde la raíz del vault:

```sh
Projects/digizen-ab-system/ver-local.command --check
```

Para probar el recorrido de ADA, ejecutar `python3 Projects/digizen-ab-system/simulate.py` después de `stage.py` y abrir `http://127.0.0.1:8765/`. La API simulada devuelve internamente `https://ada-demo.example/`, pero la confirmación lo identifica como simulación y no muestra un enlace hacia esa dirección. No guarda nombres, correos ni teléfonos. Detener con `Ctrl+C`.

`staging/` contiene los destinos relativos al directorio público DIGIZEN: `index.html`, `a/`, `b/`, `api/`, `demo-ada-confirmado/` y `conversion-admin/`. **El `index.html` de `staging/` no debe copiarse a producción hasta la activación explícita del experimento**, ya que reemplazaría la versión vigente.

## Configuración privada pendiente

La ruta privada `/home/u502287134/digizen-conversion-api/` fue creada y validada por el usuario el 2026-10-14. Antes de publicar la API, colocar ahí `src/` y `config/secrets.php`, tomando `api/config/secrets.example.php` como plantilla. El usuario confirmó que `DB_HOST`, `DB_NAME`, `DB_USER` y `DB_PASSWORD` del `.env` local son datos reales. La plantilla deja esos valores vacíos deliberadamente; no usar sus ejemplos históricos como credenciales. El `.env` también contiene el webhook de Acumbamail; nunca se incluye en `staging/` ni se imprime. El 2026-10-14 se corrigió únicamente `DB_NAME` del nombre provisional al nombre confirmado por phpMyAdmin (`u502287134_digizen_conv`); se preservaron la contraseña y las demás variables. `check-env.py` confirma presencia y coherencia sin mostrar valores privados. La API requiere además:

1. La URL **real y probada** del demo ADA para `demo_url`. `https://ada-demo.example/` solo sirve para simulaciones locales y para `digizen-demo.gnius.club`; la API de producción la rechaza.
2. El usuario eligió el aviso de privacidad de Gnius Club, enlazado desde ambos formularios en `https://gnius.club/aviso-de-privacidad.html`. Falta comprobar que el texto vigente cubre la captación DIGIZEN y registrar su versión o una huella del contenido en `privacy_notice_version`. La fecha de esta implementación no debe confundirse con la fecha de revisión legal del aviso.
3. Comprobar en un entorno controlado que el webhook de entrada de Acumbamail acepta el JSON `email`, `name`, `list_id` y añade el contacto a la lista 1544280. El token API no se usa.
4. Crear cuentas individuales con `php src/create-admin.php NOMBRE` desde la carpeta privada. El comando pide la contraseña sin mostrarla y exige al menos 12 caracteres.
5. Programar cada cinco minutos `php /home/u502287134/digizen-conversion-api/src/retry-acumbamail.php`. El registro del lead responde sin esperar a Acumbamail.

La nueva DIGIZEN de producción no debe publicarse mientras `demo_url` o el aviso de privacidad estén pendientes. La demostración del subdominio usa solo datos ficticios. La base exclusiva `u502287134_digizen_conv` debe recibir `api/schema.sql` y comprobarse con `health.php` después de publicar la API real, en una activación autorizada. No usar la base de WordPress.

## Publicación futura y rollback

**No ejecutar ahora.** Antes de cualquier transferencia:

1. Confirmar que la nueva DIGIZEN y su oferta/copy comercial están completos; validar la URL real de ADA, el panel y el flujo de leads.
2. Inventariar y respaldar los archivos actuales dentro de `/home/u502287134/domains/gnius.club/public_html/digizen/`, en especial `index.html`, `api/` y cualquier ruta `a/`, `b/`, `demo-ada-confirmado/` o `conversion-admin/` ya ocupada. Conservar el respaldo fuera de la carpeta servida.
3. Mostrar un `rsync --dry-run` por **cada destino exacto** y revisar el manifiesto. No usar `--delete`. Transferir primero carpetas privadas y rutas nuevas; probarlas sin tocar `/`.
4. Probar conexión MySQL, migración SQL, `health.php`, eventos, lead con correo y con WhatsApp, consentimiento, reintentos de Acumbamail, reglas de A y B, login y CSV. Verificar que Clarity solo tenga tags anónimos.
5. Activar el router de `/` únicamente tras aprobación explícita y prueba de rollback. Para revertir, restaurar el `index.html` original respaldado; conservar la base de conversiones para no perder leads.

No tocar `public_html/.htaccess` del dominio padre, WordPress, `gnius.club`, DNS ni otros subdominios. La ruta raíz aquí siempre es la de `digizen.gnius.club`.

## Pruebas realizadas localmente

- Build de Angular A con `--base-href /a/`: correcto.
- Build Python/JS de B: correcto; auditoría de 151 segmentos de copy desktop y móvil y reglas de 798 palabras en las tres vistas, sin problemas.
- Test del router: persistencia, QA, UTM y cookie correctos.
- Paquete local: rutas requeridas presentes; `.env`, secretos y páginas de prueba excluidos.
- Simulador HTTP local: `/`, `/a/`, `/b/`, ambas reglas y confirmación respondieron 200; una solicitud ADA ficticia respondió 201 con `demo_url` de `.example`.
- `.env` local: MySQL y webhook presentes; contraseña y URL privada no mostradas.
- Sintaxis JS y Python: correcta.

No hay intérprete PHP local. En el subdominio de pruebas, PHP 8.2.34 validó la sintaxis de la API real; MySQL, formularios A/B, eventos y sincronización de un lead QA con Acumbamail pasaron. El destino real de ADA, el panel y el flujo de compra con Stripe siguen pendientes antes de la publicación formal.

## Cambios de copy necesarios para el flujo ADA

La versión anterior de A prometía que el acceso llegaría por correo en un minuto; se cambió en las dos formas y en el texto de presentación a que el acceso se mostrará tras la solicitud cuando esté disponible. El diálogo de B dejó de prometer envío de la liga y explica que el acceso se muestra al terminar. Estos cambios corrigen una promesa que no puede cumplirse sin servicio transaccional ni URL de ADA. El resto del copy de B pasó su auditoría literal del generador. Las reglas de ADA de A y B no cambiaron.

## Riesgos y pendientes

- La URL real de ADA no existe en la configuración privada de producción y la API real responde `demo_not_configured` hasta definirla. La demostración publicada devuelve una confirmación ficticia y no habilita captación funcional.
- Los precios y las afirmaciones comerciales de ambas landings siguen presentes en su copy y datos estructurados, aunque Stripe está pausado. Revisarlos al cerrar la nueva oferta antes de publicar.
- El número de WhatsApp visible en A aún es candidato sin confirmar; no se añadió CTA nuevo con ese número.
- La API QA y el alta de Acumbamail se probaron con PHP/MySQL reales. Falta confirmar visualmente los campos opcionales de Acumbamail y probar el panel.
- El panel limita la vista a 200 leads y el CSV a 10 000 filas por solicitud. Si el volumen lo supera, agregar paginación/exportación por lotes.
- Las métricas de compras del panel quedan para cuando se reactive y defina Stripe.
