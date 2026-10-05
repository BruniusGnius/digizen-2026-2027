# Digizen · Cinco creencias

Paquete de la variante B revisada hasta el 21 de septiembre, entregado el 22 de septiembre de 2026.

## Dirección visual

Una historia vertical en una columna. Azul marino `#172b41`, turquesa `#48d2d0`, fondo blanco. Texto principal Arial/Helvetica; énfasis en Georgia; etiquetas en monoespaciada. No requiere descargar fuentes. Conservar legibilidad, blancos y adaptación móvil definidos en `sitio/dist/style.css`.

## Decisiones vigentes de lectura

- Trece secciones, ocho PNG y una conversación de ejemplo construida en HTML.
- Doce flechas centradas con animación continua; respetan la preferencia de movimiento reducido.
- «Ahora te digo cuál es la verdad» sigue a «No me escucha», con separación breve de dos saltos y la flecha debajo. Se conserva una pausa larga antes de «La cinco».
- Se eliminó la explicación que definía «candado».
- «Ahora acuérdate de la cara de tu hijo» sigue como párrafo normal a «Quédate con eso un segundo».
- «Alguien les dijo “no”, y nadie les dijo “cómo”» sigue inmediatamente a «los dos están parados en el mismo lugar».
- «El control caduca. El criterio no» y «Ese día, lo único que va a cruzar…» se leen juntos. La flecha va después del segundo párrafo.
- «Pero sí hay alguien que puede estar ahí…» sigue a «Y ahí está el problema práctico…». La flecha cierra ambos párrafos.
- «Espera. ¿Una IA hablando con mi hijo?» y «Una última cosa, y ya te dejo» tienen transiciones compactas con el bloque anterior.
- Los botones de inscripción y acceso a ADA aparecen al final; las preguntas frecuentes están en el pie.

Las notas de producción históricas del Markdown hablan de ocho viñetas y tres pausas largas: quedaron superadas por estos ajustes y por el HTML final. No reintroducir esas pausas al maquetar.

## Ilustraciones

Todos los originales finales incluidos son PNG de 1536 × 1024, generados/editados con ImageGen. Son imágenes rasterizadas: no son vectores ni archivos con capas.

| Archivo en sitio/dist/assets | Uso |
|---|---|
| 01-cena-absorto.png | Portada: mamá y papá cenan; hijo absorto en el celular, sin tristeza. |
| 02-candados.png | Cuatro candados abiertos y un oído. |
| 08-fastidio-cejas.png | Ojos al techo con fastidio; el celular tapa la parte inferior del rostro. |
| 03-escudos-mama.png | Mamá e hijo con escudos iguales. |
| 04-calle-mama.png | Mamá enseña al hijo a mirar antes de cruzar la calle digital. |
| 05-reglas.png | Hoja en el refrigerador. |
| 06-mesa.png | Papá e hijo conversan; teléfonos boca abajo. |
| 07-cruzar-mochila.png | Niño con mochila, mirando hacia adelante; papá observa desde atrás. |

Conservar el equilibrio entre mamá y papá. La conversación con ADA es HTML editable, no una imagen.

## Integraciones pendientes

Configurar únicamente destinos reales en `sitio/dist/config.js`: checkout.contado, checkout.mensualidades, adaAccessFormUrl, rulesUrl y analyticsEndpoint. Nunca poner claves privadas en ese archivo: se descarga al navegador.

Mientras estén vacíos, se muestran diálogos de revisión. El formulario de ADA no envía ni guarda datos y el checkout no cobra. Los enlaces de WhatsApp y correo sí abren contacto con Gnius Club.

La página emite eventos de profundidad de lectura, tiempo activo e intención de compra/acceso a ADA. Falta conectar el destino de medición; no se generan conversiones Lead/Purchase sin confirmación real.

Oferta actualmente maquetada: ciclo de 12 meses, $5,990 MXN total; $4,990 de contado como precio fundador hasta el 31 de octubre de 2026, o diez pagos de $599. Garantía de 30 días desde la primera conversación del hijo con ADA. Consultar el copy vigente para los términos completos.
