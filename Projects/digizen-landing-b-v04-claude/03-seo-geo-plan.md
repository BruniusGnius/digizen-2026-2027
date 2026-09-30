---
project: digizen-landing-b-v04-claude
fase: 3 - build
documento: plan de SEO y búsqueda generativa (propuesta; no se aplica nada sin aprobación)
estado: aplicado en modo preview (2026-09-30)
fecha: 2026-09-29
referencia: capa de la propuesta A (Projects/digizen-landing/angular-build/src/index.html, public/robots.txt, sitemap.xml, llms.txt, ai-context/) y su documento Projects/digizen-landing/digizen-seo-ai-ogp-metadata-proposal-2026-09-18.md (solo lectura)
---

# Plan de SEO y búsqueda generativa · landing B v04

## 0. El punto de partida

- La **A está en producción** en `https://digizen.gnius.club/`, con su capa completa: metadatos, Open Graph, JSON-LD (Organization, WebSite, WebPage, Course, FAQPage), `robots.txt` abierto a buscadores y bots de IA, `sitemap.xml`, `llms.txt` y `/ai-context`.
- La **B v04 es una preview** en `https://bruniusgnius.github.io/digizen-2026-2027/b-v04-claude/`.
- Si la B se indexa mientras la A está en producción, las dos compiten por lo mismo (mismo producto, mismo mensaje) y se reparten el posicionamiento.

**Ventaja de la B:** es HTML estático; todo el copy está en el HTML, no lo genera JavaScript. Buscadores y asistentes de IA la leen completa sin ejecutar nada (la A es una SPA de Angular).

## 1. Ahora, mientras es preview (recomendado aplicarlo ya)

- `robots` en `noindex, nofollow`, para no competir con la A.
- `canonical` hacia la A (`https://digizen.gnius.club/`), que es la página oficial hoy.
- Aun así, título, descripción y tarjeta para compartir completos: si mandas el enlace por WhatsApp o redes, se ve bien.

## 2. Cuando la B pase a producción (se deja listo, se activa con un cambio)

### 2.1 Metadatos del `<head>`
- `title`, `description`, `robots: index,follow,max-image-preview:large`, `canonical` a su URL final, `lang="es-MX"`, `theme-color`, favicon.
- Open Graph y Twitter: `og:title`, `og:description`, `og:image` 1200 × 630 con su `alt`, `og:locale es_MX`, `twitter:card summary_large_image`.

### 2.2 Datos estructurados (JSON-LD)
- **Organization** (Digizen, `parentOrganization` Gnius Club) y **WebSite**: los mismos de la A, para que buscadores y asistentes vean una sola entidad.
- **WebPage** de la B.
- **Course** con **Offer**, con datos literales del copy de la B: $5,990 MXN el ciclo de 12 meses, $4,990 de contado (precio fundador, vigente hasta el 31 de octubre), 10 pagos de $599, de tercero de primaria a tercero de prepa.
- **FAQPage** con las 7 preguntas y respuestas **literales** del FAQ de la B. Es la pieza que más usan los buscadores y los asistentes para contestar preguntas directas.

### 2.3 Búsqueda generativa (asistentes de IA)
- `robots.txt`, `sitemap.xml`, `llms.txt` y `/ai-context` viven en la **raíz del dominio**: son del sitio, no de una página. Si la B reemplaza a la A en el mismo dominio, se conservan los de la A y se actualizan con los datos de la B (precio, ciclo de 12 meses, garantía de 30 días desde la primera conversación, niveles, reglas de ADA, que la familia no lee las conversaciones completas), manteniendo la lista de lo que **no** se debe afirmar.
- La página enlaza `llms.txt` y `/ai-context` con `<link rel="alternate">`, como la A.

### 2.4 Estructura y rendimiento (ya casi listo)
- Un solo `h1` (la frase del Hero) y títulos de capítulo en `h2`: revisar que el orden de encabezados no salte niveles.
- Las escenas siguen con `alt=""` (decorativas, decisión del sistema); la imagen para compartir sí lleva `alt`.
- LCP: el Hero ya se precarga con prioridad y en su tamaño justo. Fuentes con `display=swap`.

## 3. Textos: de dónde salen (regla de copy literal)

| Campo | Propuesta | Origen |
|---|---|---|
| `og:title` / `twitter:title` | «El control caduca. El criterio no.» | Copy de la B (05.7) y el mismo de la A |
| `title` | «DIGIZEN \| Ciudadanía digital para hijos: criterio, no control» | Texto aprobado de la A (a confirmar) |
| `description` | «Tu hijo no necesita más vigilancia. Necesita criterio. DIGIZEN lo acompaña con ADA para pensar, decidir y construir una relación más sana con el mundo digital.» | Texto aprobado de la A (a confirmar) |
| `og:description` | «DIGIZEN ayuda a tu hijo a construir criterio digital con ADA, sin convertirte en policía de su celular.» | Texto aprobado de la A (a confirmar) |
| JSON-LD FAQPage, Course, Offer | Literales del copy de la B | Copy de la B |
| `llms.txt` / `/ai-context` | Los de la A + datos de la B | A + copy de la B |

## 4. Imagen para compartir

- Opción 1: reusar la de la A (`digizen-og-control-caduca-criterio-no.jpg`, 1200 × 630), que ya dice «El control caduca. El criterio no.».
- Opción 2: una propia de la B, hecha con su Hero y la frase en Inter (la hago con las piezas de la página).

## Estado (2026-09-30)

Aplicado en modo preview (decisión del usuario: «publica con SEO aunque las repliques»; recomendación: no indexar mientras la A esté en producción): metadatos, Open Graph y Twitter con la imagen de la A, JSON-LD (Organization, WebSite, WebPage, Course con 2 ofertas literales, FAQPage con las 7 preguntas literales), `noindex,nofollow` y `canonical` a `https://digizen.gnius.club/`. Para producción: `PREVIEW = False` y `PUBLIC_URL` con la dirección final en `output-code/scripts/build.py`. Pendiente para producción: `robots.txt`, `sitemap.xml`, `llms.txt` y `/ai-context` de la raíz del dominio (§2.3).

## 5. Decisiones que necesito

1. ¿Aplico ya el modo preview (`noindex` + `canonical` a la A)?
2. ¿Cuál será la URL final de la B? ¿Reemplaza a la A en `digizen.gnius.club`, o va en otra dirección? Define el `canonical` y si se reutilizan `robots.txt`, `sitemap.xml`, `llms.txt` y `/ai-context`.
3. ¿Reuso los textos de SEO aprobados de la A (tabla §3)?
4. Imagen para compartir: ¿la de la A o una propia?
