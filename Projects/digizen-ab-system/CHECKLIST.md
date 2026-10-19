# Fase 2: verificación y pendientes

## Preparado y comprobado localmente

- [x] Rutas públicas y privada de Hostinger informadas por el usuario; PHP 8.2.34 y `rsync` disponibles. El usuario creó `digizen-demo.gnius.club`; se activó allí la API real de QA, sin tocar `/digizen`.
- [x] Fuentes A y B separadas; builds locales y paquete `staging/` con `/`, `/a/`, `/b/`, reglas por variante, API pública, confirmación y panel.
- [x] Router 50/50 con persistencia, TTL, UTM y QA; test automatizado correcto.
- [x] Eventos anónimos y formularios ADA conectados a `/api/`; Clarity restringido a las landings adultas y sin PII en tags.
- [x] SQL, API PHP y panel protegidos preparados localmente; Stripe permanece pausado con endpoints 503.
- [x] El usuario confirmó que las cuatro variables de MySQL en `.env` son reales; la conexión desde Hostinger pasó sin imprimir valores.
- [x] Simulación local de ADA con `https://ada-demo.example/`; rutas y respuesta HTTP comprobadas. El simulador no forma parte de `staging/`.
- [x] Formularios enlazados al aviso de privacidad de Gnius Club, conforme a la elección del usuario.
- [x] Demostración en Hostinger verificada por HTTPS: router, A, B, reglas y confirmación 200; API real conectada a MySQL, formularios A/B y eventos 201, origen ajeno 403. Lead A con consentimiento sincronizado con Acumbamail; B sin consentimiento no se envió. Clarity habilitado en A/B de la demo con etiqueta `preview`.

## Obligatorio antes de publicar la nueva DIGIZEN

- [ ] Recibir y probar la URL real de ADA. Reemplazar la URL ficticia en la configuración privada antes de la publicación de producción; la URL ficticia solo se admite en la demostración identificada como simulación.
- [ ] Verificar el contenido vigente del aviso de Gnius Club, su cobertura de DIGIZEN y registrar una versión o huella verificable en `privacy_notice_version`.
- [ ] Revisar oferta, precios y promesas comerciales en A y B al cerrar la nueva versión. Stripe, checkout y compras siguen pausados.
- [x] Probar sintaxis PHP, conexión a MySQL real y aplicar `schema.sql` en la base exclusiva de conversiones, en un entorno autorizado.
- [ ] Completar pruebas de panel, CSV y cron programado. La captación de leads, consentimiento, eventos y alta del correo en Acumbamail ya pasaron. Se corrigieron las claves para enviar `nombre` y `variante_ab`; el usuario confirmó los tres campos del alias nuevo y de los cuatro contactos QA anteriores tras actualizarlos.
- [ ] Definir cuentas individuales del panel y validar login, permisos, CSRF y expiración de sesión.
- [ ] Inventariar y respaldar el sitio público actual; revisar manifiestos `rsync --dry-run` y plan de rollback antes de transferir archivos.
- [ ] Publicar únicamente cuando la nueva DIGIZEN esté completa y el usuario autorice la activación.

## Límite de las pruebas actuales

La API de `digizen-demo.gnius.club` ejecuta MySQL y Acumbamail para datos QA. El destino de ADA sigue simulado y el flujo de compra permanece pausado: `checkout_started` se registra, pero `/api/checkout.php` devuelve 503 y no cobra. Los registros QA llevan `environment=preview` para su limpieza antes del lanzamiento; el `.env` y sus secretos no se publicaron.
