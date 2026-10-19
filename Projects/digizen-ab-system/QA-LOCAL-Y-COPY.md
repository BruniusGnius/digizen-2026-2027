# DIGIZEN — QA local y auditoría de copy

Fecha: 2026-10-14. Alcance: variantes A y B, Reglas de ADA, flujo de compra, flujo «Conversar con ADA» y textos añadidos para la integración. Es un diagnóstico y un borrador editorial; **no cambia el copy fuente aprobado**.

## Estado funcional comprobado

| Área | Evidencia | Estado |
|---|---|---|
| Builds | `ng build --base-href /a/` y `npm run build` de B terminaron correctamente. B conserva 151 segmentos literales y las Reglas de ADA 798/798 palabras. | Pasa |
| Recursos | `stage.py` y `audit-assets.py`: 7 HTML, 166 referencias locales, 0 faltantes. `<base href="/b/">` quedó antes del CSS en Reglas B de la demo y se comprobó por HTTPS e inspección visual. | Pasa en local y demo |
| Asignación A/B | `router.test.mjs`: persistencia, QA, UTM y cookie correctos. | Pasa |
| Formularios y eventos | La API QA ya guardó solicitudes A/B y eventos en MySQL en la demo; el correo A con consentimiento pasó a `synced` en Acumbamail y el teléfono B sin consentimiento no se envió. | Pasa en la demo; falta recorrido visual completo en navegador |
| Clarity | El JS de A/B de la demo contiene el tag, variante, landing y `digizen_environment=preview`, con formularios enmascarados. | Instalado; falta confirmar sesiones en el panel de Clarity |
| Compra | El clic puede emitir `checkout_started`. Los botones de pago no abren un checkout; `/api/checkout.php` responde 503 porque Stripe y la oferta están pausados. | Parcial por decisión comercial |
| ADA | El formulario devuelve confirmación y código; `demo_url` sigue siendo ficticia. | Parcial hasta contar con la URL real |
| Panel, CSV y cron | Código local preparado; panel no publicado y cron no programado. | Pendiente |

### Reglas de ADA B en tableta (revisión 2026-10-15)

La referencia válida para esta revisión es el resultado final de `Projects/digizen-landing-b-v04-claude/output-code/`, por indicación del usuario. El CSS de la demo es idéntico a su `dist/styles.css` (SHA-256 `f9b1d245c62aa7b22453c58a81fc307fabe1628c8ea55fae48301ff488ebcf38`); también coinciden `dz-rules.js` y `dz-main.js`. El HTML público de la demo contiene las mismas dos listas cortas y dos índices completos de la página final B. En 600–859 px se muestra la lista corta de tres ideas con la imagen a la derecha; desde 860 px, incluida una tableta de 1024 px en horizontal, el CSS final B muestra el índice completo de 13 reglas. La demo reproduce esa decisión del resultado final. No se modificaron las carpetas origen ni el servidor durante esta revisión.

### Casillas del formulario ADA A (corrección 2026-10-15)

En el diálogo modal de A, la expresión Angular de clic del contenedor devuelve `false` para clics interiores y cancela la acción por defecto de las casillas. Se reprodujo en la demo: ambas permanecían sin marcar después de hacer clic. La capa de integración `frontend/digizen-ab.js` detiene la propagación al llegar al interior del diálogo; la captura de eventos se ejecuta en fase de captura para conservar telemetría. Solo se actualizaron `digizen-demo/a/digizen-ab.js` y `digizen-demo/a/index.html` (URL versionada por caché de siete días), tras un respaldo local y un `rsync --dry-run`. Verificado en navegador: privacidad y marketing cambian de 0 a 1 al hacer clic; captura en `/private/tmp/digizen-ada-checkboxes-fixed-20261015.png`. La carpeta origen A y DIGIZEN público permanecen intactos.

Riesgo de degradación: los formularios dependen de `digizen-ab.js` para enviar JSON. Si ese script no carga, el envío HTML nativo usa `application/x-www-form-urlencoded` y la API responde 415. Antes de producción, mostrar un error recuperable cuando JavaScript no esté disponible o admitir una ruta de fallback controlada.

### Rechazo de solicitud con datos normales en la demo (2026-10-15)

La API de `digizen-demo` respondió HTTP 403 con `preview_qa_only` a una solicitud que no seguía el formato QA. El frontend traducía cualquier error a «No pudimos registrar tu solicitud. Inténtalo de nuevo.»; ese mensaje ocultaba la causa. La demo está limitada a un nombre que empiece por `QA ` y a un correo `bruno+...@gnius.club` o el teléfono ficticio `+52 55 0000 0000`.

La petición controlada `QA UTM ADA` / `bruno+ada_utm_qa_20261015@gnius.club` devolvió HTTP 201 y creó el lead 4. La consulta de solo lectura a MySQL confirmó variante A, `utm_source=prueba_fase2`, `utm_medium=enlace`, `utm_campaign=ada_octubre`, `utm_content=boton_a`, `marketing_consent=0` y `acumbamail_status=not_applicable` (el consentimiento comercial estaba desmarcado). Esto confirma que el guardado y la atribución UTM funcionan para datos QA.

Prueba adicional de canal único: en B se eligió WhatsApp, se introdujo `QA WhatsApp solo` y el número ficticio `+52 55 0000 0000`, sin correo y sin consentimiento comercial. El navegador llegó a la confirmación con código `15077926E317`. El correo no es obligatorio para solicitar ADA.

Por aclaración del usuario, una solicitud debe usar **correo o WhatsApp, no ambos**. La integración A/B ahora detiene el envío cuando están llenos los dos campos, y la API devuelve `choose_one_contact_method` (HTTP 422) antes de escribir en MySQL. Se desplegaron solo los JS e índices A/B (cambio de versión del script en los índices) y `/api/leads.php` de `digizen-demo`. El PHP remoto pasó `php -l`; una petición sintética con los dos canales recibió HTTP 422. La prueba anterior de B confirma el recorrido completo con solo WhatsApp.

La integración A/B ahora explica el formato de prueba antes de enviar y muestra mensajes específicos para `preview_qa_only` y `demo_not_configured`. Se actualizaron solo los JS de A/B y los dos `index.html` de `digizen-demo` para versionar la URL del script. En B se partió del HTML que ya estaba en el servidor y solo cambió la URL del script, para preservar su diseño. No se tocó DIGIZEN público, los orígenes A/B ni la base de datos salvo el registro QA anterior.

El servidor local HTTP no pudo abrir un puerto en este entorno (`PermissionError`); por eso esta revisión no afirma haber completado una inspección visual en navegador local. Las comprobaciones de API en la demo son de una ejecución anterior del mismo día. La revisión automática bloqueó nuevas conexiones SSH por falta de créditos del workspace.

## Problemas de copy añadidos por la integración

| Prioridad | Variante y ubicación | Texto actual | Problema | Propuesta de trabajo |
|---|---|---|---|---|
| Alta | A, formulario y diálogo | «Formulario de datos del adulto.» | Suena a trámite; interrumpe la invitación directa a probar ADA. | A: «Antes de decidir, habla tú con ADA. Déjanos un medio de contacto para mostrarte el siguiente paso.» |
| Alta | A, invitación previa | «Déjanos tus datos y consulta el acceso a ADA al terminar tu solicitud.» | La frase enfría el impulso de «Interrógala» y no dice con claridad qué sucede hoy. | Cuando la URL real esté lista: «Déjanos cómo contactarte. Al terminar, podrás abrir ADA y hacerle tus propias preguntas.» Mientras siga simulada, mostrar una nota de prueba separada. |
| Alta | B, diálogo | «Canal de entrega» | Sugiere que el acceso llegará por correo o WhatsApp, pero no existe ese envío. | B: «¿Dónde podemos localizarte?»; conservar Correo y WhatsApp como opciones de contacto. |
| Alta | B, nota del formulario | «El acceso se muestra al terminar la solicitud, cuando esté disponible.» | Es una condición técnica y ambigua en una página que habla con voz personal. | Con ADA real: «Primero vas tú. Al terminar, podrás abrir ADA y preguntarle lo que quieras.» En QA: «Esta es una prueba del recorrido; ADA todavía no abre desde aquí.» |
| Alta | A/B, botón del formulario | «Conversa con ADA» | En la demo el botón registra un lead, pero ADA no abre. | En QA: «Probar solicitud de acceso». En producción, usar el CTA vigente solo cuando el destino real funcione. |
| Media | A/B, confirmación | «Recibimos tu solicitud para conversar con ADA» y «Estamos preparando tu acceso.» | Es una pantalla genérica, sin continuidad visual ni verbal con A o B; «preparando» sugiere una entrega activa inexistente. | Redactar dos variantes de confirmación y dos estados: QA sin acceso y producción con enlace real. A puede ser más directa; B debe retomar «primero vas tú». Mostrar el código como dato secundario. |
| Media | A/B, error del formulario | `alert('No pudimos registrar tu solicitud. Inténtalo de nuevo.')` | Mensaje genérico que no distingue validación, red o servidor; rompe la experiencia. | Mensajes visibles junto al formulario y acción de reintento, sin exponer detalles técnicos. |
| Media | A/B, consentimiento | «Acepto recibir comunicaciones de DIGIZEN por correo.» | Correcto como base legal, pero debe aclararse que es opcional y separado del acceso ADA. | Mantener lenguaje explícito y añadir «Opcional» en la UI; revisar el aviso de Gnius Club antes del lanzamiento. |

Estas frases son **borradores**, no reemplazos autorizados del copy fuente. La redacción final debe depender de la disponibilidad real de ADA y de qué ocurre tras dejar correo o WhatsApp. No prometer envíos automáticos que no existan.

## Copy comercial y promesas que impiden cerrar el flujo de compra

1. **Oferta y precio:** A y B aún muestran $4,990, $5,990, 10 pagos de $599, «un solo precio» y ahorro de $1,000. La estrategia de uno o dos productos y la modalidad de pago siguen sin aprobarse. La nueva oferta debe ser idéntica en A y B para que el experimento mida la página, no condiciones comerciales distintas.
2. **Activación inmediata:** «Empieza hoy» y «ADA se presenta hoy mismo» requieren onboarding y acceso real comprobados. Hoy la demo solo confirma solicitudes.
3. **Garantía:** «cancelas en un clic», «no pagas» y «te devolvemos tu dinero» necesitan política y operación de devolución verificadas para el método de pago elegido.
4. **Beneficios:** SAFE, descuento de Alquimistas, reporte familiar y precio fundador congelado necesitan condiciones, disponibilidad y alcance final antes de conservarlos como promesas de venta.
5. **Afirmaciones externas:** «7 de cada 10 adolescentes» y la posición de México en adopción juvenil de IA requieren fuente vigente y formulación precisa antes de publicación.

El documento `Projects/digizen-ab-testing/decision-precios-y-planes-digizen.md` describe la tensión comercial, pero es una propuesta para decidir, no una oferta aprobada. `COPY-PUBLICADO.md` de B sigue siendo fuente literal de referencia. Los cambios aprobados se harán en una copia de trabajo dentro de `digizen-ab-system/` y se propagarán allí de forma consistente a wireframe, HTML, FAQ y datos estructurados; las carpetas origen se mantienen intactas.

## Orden de cierre

1. Revisar visualmente ambas páginas y Reglas B en un navegador con servidor local; confirmar formulario, diálogo, respuesta móvil y ausencia de errores de consola.
2. Decidir qué sucede realmente tras solicitar ADA (apertura inmediata, lista de espera o contacto manual) y redactar los cuatro estados: formulario, éxito, error y acceso no disponible para A y B.
3. Resolver oferta, pago y garantía. Después actualizar en una sola pasada el copy comercial, FAQ, CTA y JSON-LD de A y B.
4. Probar end to end en la demo: acceso ADA real, Acumbamail y panel; después Stripe en modo test cuando se reactive el flujo de compra.
5. Promover esa versión al dominio definitivo y hacer solo pruebas de humo allí.
