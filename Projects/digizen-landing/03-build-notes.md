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
