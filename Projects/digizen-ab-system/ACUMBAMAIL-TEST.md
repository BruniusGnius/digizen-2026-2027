# Prueba controlada de Acumbamail

Estado 2026-10-14: el webhook de entrada está guardado de forma privada en `.env`. Los alias QA `bruno+acumbamail_webhook_qa`, `bruno+acumbamail_webhook_qa2` y `bruno+acumbamail_webhook_qa3` (todos en `@gnius.club`) se enviaron directamente desde pruebas locales al webhook; no proceden de una visita a la demo. `bruno+ada_a_qa@gnius.club` se envió mediante una prueba automatizada de la API en `digizen-demo.gnius.club`, se guardó en MySQL y luego se sincronizó con Acumbamail. Acumbamail confirmó que el alias `qa2` ya existía al repetirlo. El lead ADA A quedó `synced` tras el envío desde MySQL; el lead B sin correo/consentimiento quedó `not_applicable`.

La captura de suscriptores del 2026-10-14 muestra `UTM_SOURCE` poblado (`qa_webhook` y `qa_ab_2026_10`), pero `NOMBRE` y `VARIANTE_AB` vacíos en estos cuatro registros. Las capturas del mapeo revelaron la causa: Acumbamail esperaba los nodos `nombre` y `variante_ab`, mientras el backend enviaba `name` y `variant_ab`. El código local de integración y la prueba directa ahora usan las claves del mapeo. No asumir que corregir el envío rellenará contactos ya creados, pues `update_subscriber` se envía en 0.

Una consulta de solo lectura a la base de Hostinger confirmó que el lead A inicial de QA conserva nombre, variante `A` y `utm_source=qa_ab_2026_10`, con estado `synced` y un intento de envío. El lead B conserva nombre y variante `B`, pero no tiene consentimiento de marketing y correctamente no se envió. Las capturas posteriores confirmaron que el mapeo del webhook de entrada usaba `nombre → nombre`, `variante_ab → variante_ab` y `utm_source → utm_source`. La respuesta del webhook solo acredita el alta de email; no acredita los campos personalizados.

Después, el usuario observó un webhook marcado como desactivado. Una captura posterior del listado de **webhooks de entrada** muestra `DIGIZEN | Alta interesados ADA` con endpoint `Add subscriber`, estado `Active`, 4 llamadas exitosas y 2 erróneas. Las 4 exitosas son coherentes con los cuatro alias QA iniciales visibles en la lista. Una petición HTTPS de diagnóstico con JSON vacío `{}` a la URL privada configurada devolvió HTTP 400 sin crear suscriptores y probablemente figura entre las llamadas erróneas. El webhook de entrada estaba activo en esa captura; el estado anterior de desactivación no explica los campos faltantes.

Corrección 2026-10-14: se cambió solo `Acumbamail.php` de la API privada de QA para enviar `nombre` y `variante_ab`, conservando `utm_source`. El archivo anterior se respaldó localmente en `/private/tmp/digizen-demo-Acumbamail-before-20261014.php`; la versión publicada pasó `php -l` y su huella SHA-256 coincide con la local. La prueba integrada creó el lead QA `bruno+ada_campos_qa@gnius.club` (id 3) en `digizen-demo`, y el único pendiente pasó a `synced` tras un intento. El usuario confirmó en la ficha de Acumbamail de ese contacto que aparecen `NOMBRE=QA ADA campos`, `VARIANTE_AB=A` y `UTM_SOURCE=qa_campos_2026_10`; por tanto, el mapeo del contacto nuevo quedó verificado.

Relleno de QA 2026-10-14: el usuario añadió `update_subscriber` al JSON de ejemplo del webhook y lo mapeó en la fila correspondiente. `backfill-acumbamail-qa.py --send` actualizó los cuatro alias iniciales con `update_subscriber=1`, sin confirmación ni bienvenida: `bruno+ada_a_qa@gnius.club` con `QA ADA A`, `A`, `qa_ab_2026_10`; los tres `bruno+acumbamail_webhook_qa*` con `DIGIZEN QA`, `A`, `qa_webhook`. Las cuatro respuestas fueron HTTP 200 y devolvieron el mismo email y un id. El usuario revisó después las cuatro fichas en Acumbamail y confirmó `NOMBRE`, `VARIANTE_AB` y `UTM_SOURCE` con los valores esperados en todas. El backend normal sigue enviando `update_subscriber=0`.

## Mapeo que debe verse en Acumbamail

Operación: **Añadir suscriptor a una lista**. Lista seleccionada: `DIGIZEN | Interesados en ADA` (`1544280`). El JSON esperado por el backend y por `test-acumbamail.py` tiene esta forma, con un correo controlado real durante la prueba:

```json
{
  "email": "correo-controlado@example.com",
  "nombre": "DIGIZEN QA",
  "variante_ab": "A",
  "utm_source": "qa_webhook",
  "list_id": "1544280",
  "double_optin": 0,
  "welcome_email": 0,
  "update_subscriber": 0
}
```

En **Mapeo de campos**, comprobar estas correspondencias:

| Campo de Acumbamail | Nodo del JSON |
|---|---|
| `email` | `email` |
| `NOMBRE` | `nombre` |
| `VARIANTE_AB` | `variante_ab` |
| `UTM_SOURCE` | `utm_source` |

`double_optin`, `welcome_email` y `update_subscriber` se dejan en 0 para esta prueba, sin correo automático de bienvenida ni actualización de un contacto existente. La lista se elige al configurar el webhook; el `list_id` adicional del JSON no reemplaza esa selección. No usar una dirección previamente dada de baja para la prueba.

## Ejecución

`python3 Projects/digizen-ab-system/test-acumbamail.py` revisa la presencia del webhook y los nombres de campos sin enviar nada. Con un correo de prueba que el usuario controle, `--email CORREO --send` realiza **un POST**. El script no muestra la URL secreta, el contacto ni la respuesta completa. El éxito se confirma solo si Acumbamail devuelve `id` y el mismo `email` con HTTP 200 o 201. Este webhook concreto devolvió HTTP 200 con el objeto JSON serializado dentro de una cadena JSON; el backend acepta ese formato real y el 201 documentado.

Después de la prueba, revisar en Acumbamail la lista y los valores `NOMBRE`, `VARIANTE_AB`, `UTM_SOURCE`; el HTTP 201 por sí solo no demuestra que esos campos hayan quedado mapeados. Si devuelve 400, revisar el mapeo; 403 puede indicar webhook desactivado o plan; 404 puede indicar URL inválida o lista inexistente. La documentación de Acumbamail describe estos estados y la respuesta de alta: https://soporte.acumbamail.com/article/224-webhooks-de-entrada.

La prueba integrada inicial API de formulario → MySQL → webhook pasó con `bruno+ada_a_qa@gnius.club` para el alta del correo, pero no para `NOMBRE` ni `VARIANTE_AB`: ambos aparecen vacíos en la lista. Tras corregir las claves del payload se usó un alias QA nuevo; la API informó `synced` y el usuario confirmó los tres campos en su ficha de Acumbamail. El envío a Acumbamail solo procede si hay correo y consentimiento de marketing; una solicitud sin ese consentimiento nunca debe activar el webhook.
