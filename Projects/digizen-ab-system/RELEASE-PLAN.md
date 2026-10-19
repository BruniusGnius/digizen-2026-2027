# Promoción de la demo a DIGIZEN

## Fuente única

Los dos paquetes salen del mismo código local: `stage.py` lee los builds existentes de `digizen-landing` y `digizen-landing-b-v04-claude` sin escribir en esas carpetas; las correcciones y adaptaciones del experimento viven en `digizen-ab-system/`. `preview.py --real-api` agrega al paquete la banda de prueba, `noindex`, URLs de la demo y el cargador de API privada de QA. Para cambios futuros de copy o diseño se preparará una copia de trabajo dentro de `digizen-ab-system/`, sin editar los proyectos origen. No editar las páginas directamente en Hostinger salvo una reparación urgente que después se incorpore al generador.

## Pruebas en la demo

Verificar en `digizen-demo.gnius.club` las rutas `/`, `/a/`, `/b/`, las dos Reglas de ADA, recursos CSS e imágenes, persistencia de variante y UTM, eventos, formularios, consentimiento, MySQL, Acumbamail y Clarity. El flujo de compra se limita a eventos mientras Stripe, oferta y precios estén pausados. La URL de ADA sigue simulada.

## Activación única

1. Congelar una versión del código y generar el paquete de producción desde esa versión. Su dominio, canonical y configuración privada deben ser de `digizen.gnius.club`; `allow_mock_demo=false` y URL ADA real verificada.
2. Respaldar la carpeta actual `/home/u502287134/domains/gnius.club/public_html/digizen` y su manifiesto. Revisar el `rsync --dry-run` del paquete de producción. No usar `--delete` durante la activación inicial.
3. Subir `/a/`, `/b/`, `/api/`, Reglas y confirmación a esa carpeta, con la lógica privada en `/home/u502287134/digizen-conversion-api/`. Mantener el `index.html` anterior mientras se comprueban rutas y salud.
4. Sustituir solo `index.html` por el router A/B al final. Hacer pruebas de humo de ambos flujos en el dominio final. Si falla, restaurar el `index.html` anterior y los archivos respaldados.
5. Antes de abrir captación formal, revisar y retirar solo los registros `environment='preview'` de MySQL. Verificar primero los conteos y las relaciones con notas; no borrar otras filas. Confirmar por separado la limpieza de alias QA en Acumbamail.

No redirigir públicamente `digizen.gnius.club` a `digizen-demo.gnius.club`: cambiaría la URL visible y mezclaría métricas, canonical y configuración de API. Tampoco se necesita rehacer las pruebas completas: la demo valida la versión y el dominio final recibe una comprobación breve de rutas, API y dos flujos tras el cambio.

Hostinger documenta que el home directory de Web/WordPress/Cloud hosting no se puede cambiar desde hPanel; ofrece una regla `.htaccess` para servir un subdirectorio. En esta implementación hay rutas absolutas `/a/`, `/b/` y `/api/`, por lo que esa regla añadiría una capa de mapeo que habría que validar completa. Se prefiere la activación de `index.html` descrita arriba.
