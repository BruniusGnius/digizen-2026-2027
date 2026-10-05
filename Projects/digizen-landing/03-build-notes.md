---
project: DIGIZEN
fase: 3 - build final
estado: implementado; integraciones externas pendientes
fecha: 2026-09-10
codigo: angular-build/
---

# Build final · DIGIZEN

## Resultado

Landing implementada como aplicación Angular standalone con Tailwind, CSS propio basado en tokens y GSAP/ScrollTrigger limitado al visual narrativo de Beat 4. La composición conserva el orden del wireframe aprobado, su copy público, CTAs, pricing y comportamiento responsive.

El tema claro evita masas navy: las bandas de decisión, la card sticky y el plan destacado usan superficies claras, borde cromático, elevación y acentos. El tema oscuro aplica la paleta Faro completa mediante superficies profundas escalonadas, no inversión automática.

## Traducción del sistema visual

- Paleta Faro completa con roles para orientación, ADA, reflexión, cuidado, pacto y confirmación.
- Retícula tenue, halos ambientales, placas circulares, cards con regla inferior, notas editoriales y gradiente de acción azul → cyan.
- Tipografía dependiente del tamaño, ancho de lectura, escala de espacios, radios y elevaciones centralizados.
- `data-theme="light|dark"`, preferencia del sistema como valor inicial, persistencia local y aplicación antes del arranque de Angular.
- Logo horizontal con slots separados para tema claro y oscuro, ambos reemplazables sin cambiar markup.

## Stack

- Angular 21 standalone, fijado por compatibilidad con Node 24.8 del entorno.
- Tailwind CSS 4 + PostCSS para utilidades, responsive y composición.
- CSS custom properties como fuente de verdad de los dos temas.
- Angular Signals para tema, canal ADA, progreso, navegación activa y CTA móvil.
- GSAP + ScrollTrigger para una sola secuencia `feed → pausa → criterio`.
- Elementos nativos `details`, `dialog`, inputs y botones para semántica y teclado.

## Interacciones

- Navegación flotante intrínseca con anclas, indicador activo y progreso de lectura por `transform: scaleX`.
- Feedback inmediato de botones mediante `:active`, reversible al soltar.
- Primer acordeón de evidencia abierto y los tres siguientes cerrados; todos independientes.
- Selector correo/WhatsApp instantáneo.
- Diálogo ADA en desktop y sheet inferior en móvil, con Escape y retorno de foco nativos.
- CTA móvil descartable después de la decisión temprana; cambia de ADA a inscripción al entrar en oferta.
- `prefers-reduced-motion` elimina la secuencia narrativa y conserva el estado final.
- `prefers-reduced-transparency` sustituye materiales translúcidos por superficies sólidas.

## Responsive

- Breakpoint narrativo en 1023 px y móvil en 767 px, como en el artefacto vigente.
- Beats 1, 2 y 4 muestran su visual horizontal antes del argumento en tablet/móvil.
- Beat 2 usa dos fuentes desktop y una fuente horizontal independiente para tablet/móvil.
- Pricing pasa a una columna sin perder el orden mensual → ciclo 12 MSI → contado.
- Navegación conserva ancho intrínseco; sus anclas tienen scroll horizontal en móvil.

## Estado de integración

Los CTAs de compra emiten el evento `digizen:checkout` con la modalidad seleccionada. El formulario conserva su UX y datos, pero no transmite información. Faltan los destinos reales de checkout y el endpoint/receptor de ADA; no se simula una compra ni un envío exitoso.

FAQ, Reglas de ADA y legales permanecen como contenedores pendientes porque el contenido aprobado aún no existe. Por estos pendientes externos, `fase_actual` permanece en 3 y no se marca el proyecto como completado.

## Verificación

- Build de producción exitoso.
- Bundle inicial: 300.09 kB sin comprimir; estimado 93.15 kB transferido.
- Pruebas Angular: 2/2 aprobadas.
- Respuesta local HTTP 200.
- Auditoría de headings, precios, garantías, orden narrativo y ausencia de superficies navy extensas en tema claro.

### Evaluación — Fase 3, ronda 1

| Lente | Puntaje | Objeciones |
|---|---:|---|
| Purista | 4.7/5 | Picsum y el logo son placeholders deliberados; deben sustituirse antes de publicación final. |
| Arquitecto de Sistemas | 4.6/5 | Tokens, temas y estados están centralizados; checkout y receptor ADA siguen sin contrato técnico. |
| Guardián de Lectura | 4.7/5 | Jerarquía, acordeones y CTA móvil reducen fricción; faltan validar las imágenes definitivas con el copy real. |

**Puntaje ponderado:** 4.7 / 5  
**Resultado:** aprobado internamente; build implementado con pendientes externos explícitos.

---

## Revisión visual v2 — 2026-09-11

La revisión se aplicó exclusivamente en `angular-build/src/styles.css`. No se modificaron `app.html`, `app.ts`, copy, diagramación, estructura, CTAs, pricing, responsive ni interacciones.

- Fondo migrado a una base gris-azulada fría; se eliminaron retícula, formas y degradados usados como placeholders cuando no hay imagen.
- Cards, formularios, precios, citas y controles usan superficie opaca, borde fino, radio compacto y sombra contenida.
- Inter ajustada a pesos variables legibles: cuerpo `450`, lead `520`, `strong` `700`, H2 principal `760` y H2 secundario gris `560`.
- La estrategia de titulares gris/negro se conserva mediante `.dg-h2-muted` y `.dg-h2`.
- El violeta actual se preserva como acento de CTA, decisiones y progreso; cyan, coral, verde y dorado quedan reservados para sus estados semánticos.
- Iconos y números ahora usan placas compactas con fondo de color semántico; se conservan los iconos, cantidad y orden existentes.
- El build de producción finalizó correctamente: 307.62 kB sin comprimir, 94.84 kB estimado de transferencia.

### Evaluación — Fase 3, revisión visual v2

| Lente | Puntaje | Objeciones |
|---|---:|---|
| Purista | 4.8/5 | Los placeholders fotográficos externos siguen pendientes de assets definitivos. |
| Arquitecto de Sistemas | 4.8/5 | Los cambios se concentran en tokens y selectores visuales; no hay cambios de markup. |
| Guardián de Lectura | 4.7/5 | Conviene una revisión final con imágenes definitivas antes de publicar. |

**Puntaje ponderado:** 4.8 / 5
**Resultado:** aprobado internamente; la revisión preserva el wireframe y el copy.

---

## Botones principales con el degradado del logo — 2026-10-05

Pedido del usuario: relleno de degradado en los botones, muy similar al del círculo del logo de Digizen (el que va detrás del joven con la mochila).

- El cambio está solo en `angular-build/src/styles.css`. No se modificaron `app.html`, `app.ts`, copy, estructura ni interacciones.
- Token nuevo `--dg-btn-fill: linear-gradient(230deg, #1a75ea 0%, #2c1ddb 100%)`: los mismos dos colores y la misma dirección del círculo del logo (`logo-SVG/digizen-logo-*.svg`: `#1a75ea` arriba a la derecha → `#2c1ddb` abajo a la izquierda).
- Lo usan los botones principales (`.dg-btn`) y el enlace «Inscribir a mi hijo» del menú móvil (`.dg-nav-links-cta`), en tema claro y oscuro. `background-origin: border-box` evita que el degradado se repita bajo el borde de 1 px.
- No cambian: los botones secundarios (`.dg-btn--secondary`), ni los demás usos de `--dg-btn-bg` (barra de progreso, marca de los antetítulos, sombras, enlaces del pie).
- Contraste del texto blanco: 4.96:1 en el peor punto bajo el texto de los botones medidos (extremo claro del degradado 4.40, extremo oscuro 9.11; el azul sólido anterior daba 5.05).
- Verificado en local: tema claro y oscuro, desktop y teléfono (menú abierto); build de producción correcto.
- Aprobado por el usuario y publicado el 2026-10-05 (pasó a `main` desde la rama `digizen-a-botones-degradado`).

---

## ADA no aparecía en el CTA al volver de «Reglas de ADA» — 2026-10-05

Reporte del usuario: en GitHub, al pasar de «Reglas de ADA» a Digizen, la ADA que saluda en el CTA no se desplegaba.

- **Causa.** La portada vive dentro de un `@if`: al entrar a las reglas Angular la desmonta y, al volver, crea nodos nuevos. Las animaciones de la portada se preparaban una sola vez, en `ngAfterViewInit`, así que el lienzo nuevo de ADA nunca recibía su clase `is-ready` (se quedaba con opacidad 0) ni sus cuadros. Lo mismo le pasaba al chat animado y al video del reloj. También fallaba al entrar directo por `/reglas-de-ada` y pasar después a la portada.
- **Corrección.** Solo en `angular-build/src/app/app.ts`: `setupLandingMotion()` prepara las tres animaciones cada vez que la portada vuelve a existir (al cargar, al volver de las reglas y con el botón Atrás) y `teardownLandingMotion()` suelta los disparadores anteriores. Una preparación que quedó a medias al cambiar de página se descarta. No cambian el marcado, los estilos, el copy ni el comportamiento al cargar la portada.
- **Verificado.** En la versión publicada se reprodujo el fallo (al volver: lienzo vacío, sin `is-ready`). En local, con la corrección: al volver con «Volver a Digizen», con el botón Atrás y entrando directo por las reglas, el lienzo queda preparado y pintado, se cargan los 130 cuadros y el video del reloj queda listo; sin errores de consola; build de producción correcto.
- **No verificado.** El recorrido de la animación con el scroll en un navegador visible: el panel de pruebas estaba oculto y pausa las animaciones. Falta una revisión a ojo.
- Aprobado por el usuario y publicado el 2026-10-05 (pasó a `main` desde la rama `digizen-a-fix-ada-al-volver`).

---

## Optimización de imágenes: AVIF con respaldo WebP — 2026-10-05

Pedido del usuario: publicar las correcciones con optimización de imágenes en A y B, conservando siempre los originales.

- **Qué cambia.** Las imágenes se sirven también en AVIF; el WebP que ya estaba publicado no se tocó y queda de respaldo para el navegador que no entienda AVIF. No se bajó resolución ni cambió ninguna composición.
  - Escenas: los 9 `<picture>` de `app.html` ofrecen primero su AVIF (18 imágenes: Hero, escenas con versión móvil y las de la página de reglas). La precarga del Hero en `index.html` pasó a AVIF para no descargar los dos formatos.
  - ADA que saluda: los 130 cuadros existen en AVIF. `app.ts` averigua una vez si el navegador lo decodifica (`supportsAvif()`) y pide esos cuadros; si no, los WebP.
  - `angular.json` excluye `**/*.psd`: el PSD del OGP (4.9 MB) se publicaba por accidente. El archivo sigue en su carpeta.
- **Garantía de calidad.** `scripts/make-avif.py` compara cada AVIF con su referencia y solo lo conserva si es al menos tan fiel (SSIM) como el WebP y pesa menos. Para las escenas la referencia es su **PNG original** de `public/`; para ADA, su cuadro WebP (SSIM ≥ 0.995). El detalle por imagen queda en `scripts/avif-report.json`.
- **Resultado.** Escenas con AVIF: 2.80 MB → 2.11 MB (25 % menos; cada una entre 14 % y 38 %). ADA: 4.15 MB → 1.78 MB (57 % menos). Lo publicado baja además 4.9 MB por el PSD.
- **Originales.** Nada se sobrescribió: los PNG siguen en `public/` y el respaldo `asset-backups/original-images-2026-09-18/` no se tocó.
- **Lo que no se hizo.** Las 17 imágenes sueltas (fuera de `<picture>`, 0.9 MB en total) siguen en WebP: envolverlas cambia el marcado y pide revisión visual. El video del reloj (6.1 MB) tampoco se tocó.
- **Verificado en local.** Build de producción correcto (148 AVIF en la salida, ningún PSD). En el navegador: el Hero y la imagen de reglas toman el AVIF; al volver de las reglas ADA queda preparada y pintada con sus 130 cuadros AVIF; sin errores de consola.
- **No verificado.** A ojo en un navegador visible (el panel de pruebas estaba oculto y pausa las animaciones) ni en un navegador sin AVIF.

---

## Mejoras tras la auditoría de Lighthouse — 2026-10-05

El usuario corrió Lighthouse 13 sobre la versión publicada, con y sin extensiones de Chrome. En incógnito (medición limpia): desktop 99 / 96 / 100 / 100 y móvil 88 / 96 / 100 / 100 (rendimiento, accesibilidad, buenas prácticas, SEO). Con sus extensiones el rendimiento bajaba a 75 y 48 por un salto de diseño de 0.85–1.0, y aparecían 1.9 MB de «JavaScript sin usar» y errores de consola que eran de las extensiones.

Cambios (rama `mejoras-lighthouse`; ninguno cambia cómo se ve la página):

- **Hoja de estilos sin carrera** (`angular.json`, `inlineCritical: false`). Angular ponía en línea los «estilos críticos» y cargaba el resto en diferido; como el HTML llega vacío, esos estilos críticos no incluían ninguna regla de la portada. Si el JavaScript pintaba antes de que llegara la hoja (pasa con extensiones que ocupan el navegador), la página se veía un instante sin estilos y luego saltaba entera. Ahora la hoja es un enlace normal: no hay nada que pintar antes de tenerla.
- **El video del reloj no se descarga en móvil** (`app.html`, `preload="none"`). Pesa 6.2 MB y solo se usa en desktop, pero el marcado lo precargaba en todos los dispositivos (7.6 MB de página en móvil). En desktop lo sigue pidiendo el script, como antes.
- **Enlace de WhatsApp del pie:** su nombre accesible ahora incluye el número visible («(+52) 221 848 1116, enviar WhatsApp a Gnius Club»).

Verificado en local: build de producción con la hoja como enlace normal; en móvil el video no se pide y en desktop queda listo (8 s); sin errores de consola.

Pendiente, requiere decisión porque cambia colores o es un cambio mayor:
- **Contraste** (accesibilidad 96): `.dg-emphasis--green` (#188958 sobre blanco, 4.41; pide 4.5), los `.dg-caption` de la comparación de precios (#8b98aa, 2.9 y 2.6, texto de 10 px) y el texto «Escribe aquí...» del chat de ejemplo (#8b98aa, 2.85).
- **Imágenes más grandes de lo que se muestran** (hasta 418 KiB en móvil): la del reloj, la cena y el apego en móvil, y las dos del CTA. Se resuelve con varios anchos por imagen.
- **Prerenderizado:** en móvil el título principal tarda 3.8 s porque la página se arma con JavaScript.
