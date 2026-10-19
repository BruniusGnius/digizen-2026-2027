---
project: digizen legal layer
phase: 2 - legal interaction and information architecture
status: proposed
scope: digizen-landing, digizen-landing-b-v04-claude, and the future digizen-ab-system replication
date: 2026-10-19
---

# Capa legal propuesta

Este documento define la arquitectura que debe aprobarse antes de construir la capa legal. No sustituye la revisión final de una persona abogada en México. No modifica el copy de producción de las landing pages.

## 1. Documentos públicos y versiones

| Documento | URL pública propuesta | Estado requerido antes de publicar | Versión que se registra |
|---|---|---|---|
| Aviso de privacidad | `https://gnius.club/aviso-de-privacidad.html` | Ya existe; verificar que cumpla el artículo 15 de la LFPDPPP vigente | identificador y hash del HTML publicado |
| Términos y condiciones DIGIZEN | `https://digizen.gnius.club/terminos-y-condiciones-digizen.html` | Vista previa local construida; falta el contenido legal aprobado | identificador, fecha de vigencia y hash del HTML publicado |
| Política de cookies DIGIZEN | `https://digizen.gnius.club/politica-de-cookies-digizen.html` | Vista previa local construida; falta el contenido legal aprobado | identificador, fecha de vigencia y hash del HTML publicado |
| Centro de preferencias de cookies | disparador persistente `Preferencias de cookies` en el footer | Falta construir | versión de la política y elecciones por categoría |

No se publicará una página de términos ni de cookies con datos inventados. Para redactar y aprobar sus textos hacen falta, como mínimo: razón social o nombre de la persona responsable, RFC si corresponde, domicilio, correo y canal de reclamaciones, descripción contractual precisa del programa, precio y modalidades vigentes, reglas de cancelación/reembolso, duración del acceso, edad y rol de quien contrata, proveedores que tratan datos, plazo de conservación, y los scripts/cookies realmente desplegados.

## 2. Bloques de interfaz

### Footer de ambas landing pages

Agregar enlaces visibles y consecutivos:

`Aviso de privacidad` · `Términos y condiciones` · `Política de cookies` · `Preferencias de cookies`

Los documentos abren en pestaña nueva. El centro de preferencias se abre en la misma página desde el enlace que lo invoca, devuelve el foco a ese enlace al cerrarse y conserva las elecciones.

### Formularios «Conversa con ADA»

Se aplica a todos los formularios de cada versión, incluidos los diálogos. Antes del botón de envío, en este orden:

1. Checkbox obligatorio, vacío por defecto: `Acepto los Términos y condiciones.` El texto `Términos y condiciones` enlaza al documento versionado.
2. Checkbox obligatorio, vacío por defecto: `He leído el Aviso de privacidad.` El texto `Aviso de privacidad` enlaza al documento versionado.
3. Checkbox opcional y separado: `Acepto recibir comunicaciones de DIGIZEN por correo.` No se preselecciona.

Cada control tiene una etiqueta completa, foco visible, área táctil suficiente y validación nativa y del servidor. Abrir un enlace no equivale a aceptación; la evidencia se genera solo al enviar el formulario con ambos checkboxes marcados.

### Inscripción y Stripe Checkout

Todo CTA de pago abre primero un diálogo de confirmación de compra, sin capturar tarjeta. Muestra el plan, precio, periodicidad y cualquier renovación aplicable tal como estén definidos en la oferta vigente. El diálogo contiene los mismos dos checkboxes obligatorios de términos y aviso de privacidad. Solo con ambos aceptados se crea la sesión de Stripe.

La sesión de Stripe recibe únicamente referencias internas y versiones de los documentos como metadatos; no recibe el texto de los documentos ni datos que no necesite. El servidor crea la sesión y vuelve a validar las dos aceptaciones. El webhook vincula la evidencia con la compra pagada.

### Cookies y tecnologías similares

En la primera visita se muestra un panel que no bloquea la lectura de la landing. Tiene tres acciones con el mismo peso visual: `Aceptar todas`, `Rechazar opcionales` y `Configurar`.

El panel de configuración ofrece categorías con propósito, proveedor y duración:

| Categoría | Estado inicial | Decisión propuesta |
|---|---|---|
| Necesarias | Siempre activa | seguridad, sesión y conservación de la propia preferencia |
| Funcionalidad | Desactivada | personalización que no sea indispensable |
| Medición y rendimiento | Desactivada | analítica, experimentos A/B y medición de conversiones identificables |
| Marketing | Desactivada | píxeles, audiencias y publicidad comportamental |

No se inicializa ninguna etiqueta, píxel, cookie o `localStorage` de categorías opcionales antes de aceptar esa categoría. La asignación A/B persistente actual y el identificador de visitante pasan a `Medición y rendimiento`; si se rechaza, se usa una variante estable solo para la sesión, sin persistencia ni envío de analítica. La elección puede retirarse desde el footer y el retiro impide nuevas cargas, borra los identificadores opcionales propios y registra la revocación.

## 3. Trazabilidad de consentimiento

La base de datos necesita un ledger de solo inserción, separado de la tabla `leads`, para conservar una prueba por acción y por documento. La fila del lead conserva el estado operativo actual; el ledger conserva el historial demostrable.

Campos mínimos por recibo:

| Campo | Uso |
|---|---|
| `id`, `created_at_utc` | identificador y fecha-hora del servidor en UTC |
| `subject_type`, `lead_id`, `checkout_session_id`, `visitor_id` | vincular el recibo con una persona conocida, una compra o un visitante seudónimo |
| `document_type`, `document_version`, `document_url`, `document_sha256` | probar exactamente qué documento fue aceptado |
| `action` | `accepted` o `revoked`; nunca se actualiza una aceptación existente |
| `categories_json` | elecciones de cookies por categoría, cuando aplique |
| `source`, `landing_id`, `variant`, `entry_url` | origen de la evidencia |
| `ip_proof_encrypted`, `user_agent_hash` | señal de auditoría; IP cifrada con llave gestionada y acceso restringido, nunca expuesta en analítica |
| `receipt_hmac` | sello de integridad calculado en servidor con llave fuera de la base de datos |

Se agregan índices para `lead_id`, `checkout_session_id`, `visitor_id`, `document_type + created_at_utc`. Ninguna ruta pública puede editar o borrar recibos. Las consultas administrativas se limitan por rol y quedan auditadas. El aviso de privacidad debe explicar esta finalidad, los destinatarios, la conservación y el canal ARCO.

## 4. Reglas de servidor

1. `POST /api/leads.php` rechaza la solicitud si no recibe aceptación booleana de términos y aviso de privacidad, sus versiones y sus hashes esperados en servidor. Inserta los dos recibos y el lead en una sola transacción.
2. `POST /api/checkout.php` permanece inaccesible hasta que se configure Stripe, precios y documentos. Al activarse, rechaza la creación de sesión sin las dos aceptaciones válidas e inserta recibos antes de llamar a Stripe.
3. El webhook de Stripe registra el vínculo entre sesión, compra y recibos; no considera pagada una compra por datos del navegador.
4. El endpoint de preferencias inserta un recibo al aceptar, cambiar o revocar categorías. No recibe nombres, correos ni teléfonos para ese fin.
5. Las versiones de documentos viven en configuración del servidor; el navegador no puede decidir qué versión se guarda.

## 5. Cobertura de fuentes → artefacto

| Fuente | Tratamiento |
|---|---|
| Copy publicado de `digizen-landing` | No se modifica ni se omite. Los nuevos controles son contenido legal pendiente de aprobación y quedan fuera de su fuente de copy. |
| `COPY-PUBLICADO.md` de `digizen-landing-b-v04-claude` | No se modifica ni se omite. Los nuevos controles son contenido legal pendiente de aprobación y quedan fuera de su fuente de copy. |
| Aviso de privacidad existente | Se conserva como destino actual; su contenido debe auditarse contra LFPDPPP antes de usarlo como documento versionado. |
| Términos y política de cookies | No fueron proporcionados. Se requieren antes de publicar los enlaces o exigir aceptación. |

## 6. Evaluación — Fase 2, ronda 1

| Lente | Puntaje | Objeciones |
|---|---:|---|
| Purista | 4.5/5 | El centro de cookies y dos casillas obligatorias responden a finalidades distintas; no se añade una casilla de marketing obligatoria. |
| Arquitecto de Sistemas | 4.7/5 | El ledger, las versiones y las reglas son reutilizables para A, B y AB. Falta concretar las URLs y versiones finales de los documentos. |
| Guardián de Lectura | 4.3/5 | La fricción se concentra justo antes de enviar datos o pagar; falta validar el copy legal final para asegurar lectura clara en móvil. |

**Puntaje ponderado:** 4.4 / 5
**Resultado:** aprobado internamente.

## 7. Base normativa revisada

- La [LFPDPPP vigente](https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf), artículos 14 a 16, exige poner a disposición el aviso antes del tratamiento e indica su contenido mínimo; sus artículos sobre consentimiento, medidas de seguridad y derechos ARCO deben reflejarse en el aviso y en el tratamiento real.
- La [LFPC vigente](https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPC.pdf), artículo 76 Bis, exige que la venta electrónica informe condiciones aplicables, permita verificar y aceptar la transacción, conserve prueba, proteja la transacción y ofrezca reclamaciones, identidad, pago y entrega. Para cobros recurrentes exige información clara, consentimiento expreso e informado y mecanismo de cancelación.
- El [Código de Comercio](https://www.diputados.gob.mx/LeyesBiblio/pdf/CCom.pdf), artículo 89, reconoce la equivalencia funcional de los mensajes de datos y el uso de medios electrónicos en actos de comercio. El ledger propuesto conserva evidencia verificable de esa aceptación.

La legislación mexicana no impone literalmente el mismo banner de cookies europeo por el mero uso de cookies. Aun así, la identificación persistente, analítica, publicidad y su combinación con formularios pueden constituir tratamiento de datos personales. Por los principios de información, finalidad, consentimiento, proporcionalidad y responsabilidad de la LFPDPPP, esta propuesta usa consentimiento previo, granular y revocable para tecnologías no necesarias. Es la postura más segura para esta implementación; debe confirmarse frente a los proveedores y scripts definitivos durante la revisión legal.

## 8. Implementación local — 2026-10-19

### Alcance construido

| Elemento | Landing A | Landing B |
|---|---|---|
| Banner inicial de cookies | Construido | Construido |
| Configurador de preferencias | Construido | Construido |
| Categorías y switches | Necesarias bloqueadas; Rendimiento y medición; Marketing | Necesarias bloqueadas; Rendimiento y medición; Marketing |
| Restablecer elección local | Construido | Construido |
| Casilla de aviso de privacidad en formulario ADA | Obligatoria | Obligatoria |
| Casilla de términos en formulario ADA | Obligatoria | Obligatoria |
| Casillas antes del evento de checkout | Obligatoria | Obligatoria |
| Enlaces legales subrayados dentro de casillas | Construido | Construido |
| Vista previa de Términos | Ruta Angular local | Archivo HTML local con componentes de B |
| Vista previa de Política de cookies | Ruta Angular local | Archivo HTML local con acordeones de B |

### Constantes de diseño B usadas en los documentos

- `--w-wide` mantiene la medida máxima de lectura.
- `--pad-x` y `--air` fijan la posición y el ritmo vertical según dispositivo.
- `.faq details`, `.ind` y `dz-faq.js` proveen los acordeones, sus bordes, el indicador circular y el movimiento crítico interrumpible ya usados por B.
- `t-small`, `t-body`, `t-head`, la paleta de neutros y los bordes `--color-line` mantienen la jerarquía visual de la landing.

### Archivos modificados

- `Projects/digizen-landing/angular-build/src/app/app.html`
- `Projects/digizen-landing/angular-build/src/app/app.ts`
- `Projects/digizen-landing/angular-build/src/styles.css`
- `Projects/digizen-landing-b-v04-claude/output-code/index.html`
- `Projects/digizen-landing-b-v04-claude/output-code/terminos-y-condiciones-digizen.html`
- `Projects/digizen-landing-b-v04-claude/output-code/politica-de-cookies-digizen.html`
- `Projects/digizen-landing-b-v04-claude/output-code/js/dz-actions.js`
- `Projects/digizen-landing-b-v04-claude/output-code/src/components.css`
- `Projects/digizen-landing-b-v04-claude/output-code/scripts/build.py`

### Verificación local

- Landing A: `npm run build` completó correctamente.
- Landing B: `npm run css` y `node --check js/dz-actions.js` completaron correctamente.
- Previsualización A: `http://127.0.0.1:4200/`.
- Previsualización B: `http://127.0.0.1:8080/`.

### Pendiente antes de publicar

1. Reemplazar los textos de vista previa por términos y política de cookies aprobados, con datos de la persona responsable, servicio, pagos, cancelación, conservación y proveedores reales.
2. Publicar ambos documentos bajo `digizen.gnius.club`.
3. Configurar en cada entorno las versiones, URLs, hashes SHA-256 y llave de recibos; ejecutar `api/schema.sql` en la base exclusiva antes de activar la captura real.

### Registro en DIGIZEN AB System

El sistema A/B ya incorpora el soporte de servidor para esta capa:

- `consent_receipts` es un ledger de solo inserción, con evidencia de términos, privacidad y decisiones o revocaciones de cookies.
- `POST /api/leads.php` exige las dos casillas, toma las versiones y hashes desde configuración privada y guarda el lead y los dos recibos en una misma transacción.
- `POST /api/consents.php` registra preferencias de cookies con el visitante seudónimo, variante, landing, fecha UTC, prueba HMAC de IP, hash de user agent y sello HMAC de integridad.
- `frontend/digizen-ab.js` envía los consentimientos sin incluir nombre, correo ni teléfono en la telemetría de cookies.
- La clave de sellado, hashes y versiones solo viven en `config/secrets.php`, fuera del repositorio y de `public_html`.

La creación de Stripe continúa pausada. Al habilitarla, deberá reutilizar el mismo ledger para guardar recibos de términos y privacidad antes de crear la sesión y vincularlos desde el webhook.
