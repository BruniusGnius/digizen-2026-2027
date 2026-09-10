---
project: DIGIZEN
fase: 3 - plan previo al build
estado: pendiente de aprobación del usuario
fecha: 2026-09-10
codigo_escrito: ninguno
---

# Plan de implementación

La Fase 2 queda aprobada por instrucción explícita del usuario. Este documento propone la implementación para su aprobación previa; no autoriza por sí mismo resolver diferencias de copy, modificar responsive ni activar servicios externos.

## Referencias y precedencia

- Composición vigente: `Digizen Landing Refinado.dc.html`, identificado expresamente como artefacto actual en el handoff. Se conservan sus 16 secciones, navegación, agrupaciones y posiciones de CTA.
- Sistema visual: `01-design-system.md`. Paleta, materiales, tipografía, iconografía y estados se traducen a CSS propio.
- Intenciones funcionales: `02-wireframe.md`, incluyendo formulario ADA, feedback inmediato, progreso, acordeones y CTA móvil. Las tablas históricas que contradicen la composición vigente no reemplazan el HTML.
- Contenido fuente inmutable: `00-context/digizen-copy-ola.md`. Las diferencias con el HTML se registran abajo; no se corrigen ni se declaran excepciones aprobadas de manera implícita.
- Tokens localizados: `../../creador de landings/insumos/sistema-diseno-refinado/tokens.css`. El enlace relativo `tokens.css` del documento de diseño no existe dentro del proyecto. Este CSS se usa como insumo, no se importa su layout de demostración.
- Los archivos de referencia permanecen como fuente. Solo se han actualizado los metadatos de aprobación y avance de fase.

## Componentes y orden de render

| Orden | Parcial Blade propuesto | Responsabilidad |
| --- | --- | --- |
| Navegación | `navigation.blade.php` | Marca, cuatro anclas, Inscribir y progreso; flotante, centrada y de ancho intrínseco. |
| 01 | `hero.blade.php` | Hook, subheadline, cita y visual familiar. |
| 02 | `beat-1.blade.php` | Alivio, cuerpo íntegro, remate y visual humano. |
| 03 | `beat-2.blade.php` | Reframe, citas, dos imágenes desktop, remate y mini-panel local. |
| 04 | `decision-early.blade.php` | Banda de decisión tras Beat 2. |
| 05 | `beat-3.blade.php` | Cuatro pruebas, analogía, remate y card sticky de precio existente. |
| 06 | `beat-4.blade.php` | Visual conceptual, criterio y puente hacia ADA. |
| 07 | `beat-5.blade.php` | Explicación, preview de producto y formulario; agrupación del HTML vigente. |
| 08 | `safety.blade.php` | Gate íntegro, cuatro guardas, invitación y diagrama. |
| 09 | `decision-trust.blade.php` | Banda con ADA como acción primaria. |
| 10 | `beat-6.blade.php` | Presencia y visual de acuerdo. |
| 11 | `founders.blade.php` | Generación Fundadora y sus tres beneficios. |
| 12 | `offer.blade.php` | Ciclo e inclusiones: cinco elementos, como en el HTML actual. |
| 13 | `payment-options.blade.php` | Mensual → ciclo 12 MSI → contado; garantía posterior. |
| 14 | `closure.blade.php` | Garantía, decisión y cierre de la metáfora. |
| 15 | `decision-final.blade.php` | Banda final de inscripción y ADA. |
| 16 | `faq-legal.blade.php` | Tres contenedores reservados, sin inventar sus cuerpos. |

Primitivas en `resources/views/components/digizen/`: `button`, `section`, `quote`, `cta-panel`, `decision-band`, `accordion`, `price-card`, `icon`, `responsive-picture`, `ada-form`, `ada-dialog` y `mobile-cta`.

El copy queda literal en las vistas de sección; los componentes reciben slots para conservar palabras, énfasis y puntuación sin reconstruir frases mediante concatenaciones.

## Archivos propuestos

Todo el código vivirá en `output-code/`:

- `routes/web.php`: ruta de la landing y, cuando se defina el servicio receptor, acceso ADA.
- `resources/views/layouts/landing.blade.php`: documento semántico, idioma español y entradas Vite.
- `resources/views/landing.blade.php`: composición explícita de las secciones en el orden anterior.
- `resources/views/landing/sections/`: los parciales de contenido.
- `resources/views/components/digizen/`: componentes reutilizables.
- `resources/css/app.css`, `tokens.css`, `base.css`, `layout.css`, `components.css`: entrada, tokens, tipografía, composición responsive y estados. Los valores visuales se centralizan, con origen documentado.
- `resources/js/app.js` y `modules/{navigation,accordions,ada-form,mobile-cta,spring,narrative-motion}.js`: inicializadores pequeños y separados por comportamiento.
- `config/digizen.php`: destinos de checkout por modalidad, integración ADA y manifiesto de assets; secretos únicamente en configuración de entorno.
- `public/assets/digizen/`: imágenes locales de producción y variantes responsive independientes.
- `vite.config.js`, `package.json`, `composer.json` y archivos de bloqueo de dependencias.
- `tests/Feature/`: render, orden, integridad de contenido y rutas, según lo efectivamente implementado.

Documentación fuera del código: `03-build-notes.md`, `03-content-audit.md` y `03-asset-manifest.md`. El ledger de contenido conservará completas las notas internas y la matriz de headlines, separadas de la UI pública.

Se usará render de servidor con Blade y CSS propio. Las versiones de Laravel, PHP, Vite y GSAP se verificarán contra el entorno y documentación oficial al iniciar el build.

## Interacciones

- Navegación: anclas operables sin JavaScript; mejora de foco al encabezado destino y margen para la barra fija. Progreso mediante `transform: scaleX`, actualizado con scroll pasivo y trabajo agrupado por frame.
- CTA: feedback visual al presionar, activación mediante eventos nativos accesibles y restauración en liberación/cancelación. Las etiquetas actuales permanecen en su ubicación.
- Pruebas: `details/summary` independientes. Propuesta para aprobación: primera prueba abierta y las otras tres cerradas, siguiendo la intención final escrita en C06; el HTML actual deja las cuatro cerradas. Apertura de contenido inmediata; solo el indicador recibe motion.
- ADA: formulario reutilizado en Beat 5 y en el contenedor de acceso. Desktop se origina visualmente en el disparador; móvil entra como sheet desde abajo. Cierre con Escape, foco contenido y retorno al disparador; restauración de posición de lectura.
- Canal de entrega: selección instantánea correo/WhatsApp. La implementación funcional necesita el dato de contacto correspondiente, ausente en el formulario del HTML; su campo, mensajes de validación y resultado se deben concretar antes de activar el envío.
- CTA móvil C12: implementar la intención ya documentada, ausente en el HTML: aparece después de la decisión temprana, permite cerrar, prioriza ADA y cambia a inscripción al entrar a oferta conservando ADA como alternativa.
- Checkout: cada modalidad conserva su propia acción y destino configurable. La conexión depende de URLs o contrato real; no se presentará un envío o compra como exitoso sin confirmación del servicio.

## Motion propuesto

| Elemento | Tratamiento | Justificación / tecnología |
| --- | --- | --- |
| Botones, diálogo ADA y barra móvil | Spring pequeño, amortiguación crítica, reversible desde valor y velocidad actuales. | Feedback y continuidad espacial; módulo JavaScript mínimo, sin una segunda librería de animación. |
| Acordeones y selector | Estado inmediato; indicador mediante transform, sin animar altura. | La respuesta conserva lectura y control. |
| Visual de Beat 4 | Secuencia local `feed → pausa → criterio`, una vez al entrar en viewport, dentro del espacio aprobado. | Único uso inicial propuesto de GSAP/ScrollTrigger: explicar el paso de impulso a decisión. Requiere visual por capas; si el asset es plano, quedará estático. |
| Fotografías, copy, precios y guardas | Presentación estable y legible desde el inicio. | La narración y la comparación no requieren coreografía adicional. |

Las animaciones usan transform y opacidad. Con movimiento reducido se conserva el estado final y feedback estático o un cambio breve de opacidad. GSAP se carga solo cuando el visual narrativo existe y la preferencia de movimiento lo permite. El plan no necesita drag, carruseles, pinning, scroll controlado ni animaciones repetidas de todas las secciones.

## Responsive y assets

Se reproducen las reglas efectivas del HTML vigente: cambio narrativo hasta 1023 px y reglas móviles hasta 767 px. Beats 1, 2 y 4 usan visual horizontal 16:9 antes del contenido en tablet/móvil; Beat 2 usa dos archivos desktop independientes (1:1 y 4:5) y un tercer archivo horizontal independiente para tablet/móvil.

Se conserva la barra intrínseca, las anclas móviles con scroll horizontal, la card de precio de Beat 3 y el orden mensual → ciclo → contado, con el ciclo central oscuro. El documento histórico incluye otros ratios y una ilustración de cruce en Beat 3 que no está en el HTML vigente: no se agregan ni se sustituyen automáticamente.

El manifiesto de assets registrará slot, fuente, ratio, variante, tratamiento y estado. No se encontraron imágenes de producción en el inventario del workspace. ADA y el acuerdo requieren recuperar sus originales; las imágenes narrativas nuevas requieren producción. El preview de chat conservará el esquema neutral aprobado, sin inventar diálogos.

## Auditoría fuente → plan / referencia vigente

Auditoría documental previa al código; no equivale todavía a una prueba automatizada del render final.

| Fuente / requisito | Destino previsto | Resultado y excepción pendiente |
| --- | --- | --- |
| Hook, Beats 1–6 y gate 5.5 | Secciones 01–10 | Cobertura narrativa localizada en el HTML; conservar los cuerpos completos. |
| Fundadores, oferta v3, garantías y cierre | Secciones 11–15 y card de Beat 3 | Contenido localizado; oferta y ahorro tienen diferencias de presentación literal indicadas abajo. |
| CTA secundario fuente | Mini-panel y bandas existentes | Fuente: `Tengo dudas — quiero conversar con ADA primero`. El HTML usa, entre otras variantes, `Tengo dudas — conversar con ADA`. Diferencia literal pendiente; no se corrige durante el build sin indicación. |
| Inclusiones de oferta | Sección 12 | El HTML separa títulos y cuerpos y omite los guiones largos que los conectan en varias inclusiones de la fuente. Diferencia de puntuación pendiente. |
| Frase de ahorro | Sección 13 | La fuente integra el cálculo entre paréntesis en la frase; el HTML sitúa `12×$599 + inscripción = $8,088` en la card mensual y usa dos puntos en la frase de ahorro de la card central. Los datos están presentes, pero no hay equivalencia literal completa. |
| Notas internas, historial v3/v4 y matriz H1–H7 | Fuente intacta y ledger interno del build | El HTML vigente no incluye el anexo que describen las notas del wireframe. Preservarlo íntegro en documentación, identificado como no público. |
| Formulario, card sticky, C12 y primer acordeón abierto | Componentes funcionales propuestos | Card presente; formulario esquemático; C12 ausente y primer acordeón cerrado en HTML. Las propuestas de implementación están explicitadas arriba para aprobación. |
| FAQ, reglas, privacidad, términos y soporte | Sección 16 | Contenedores presentes; cuerpos pendientes de fuente aprobada. |

La aprobación general de Fase 2 se registra como tal. Esta auditoría no la convierte en autorización específica para cambiar copy ni en una afirmación de fidelidad literal al 100%.

Pendientes para completar las conexiones y la publicación: destinos de checkout por modalidad; receptor de datos y entrega de acceso ADA; campo de contacto y copy de estados; textos de FAQ/reglas/legal; originales de ADA/acuerdo y nuevos assets. `Gnius Space` se conserva como aparece en el HTML, con la nota de naming fuente aún documentada.

## Verificación y entrega

Después de aprobar el plan: scaffolding, traducción del sistema visual, secciones, interacciones y conexión de servicios cuando estén definidos. Verificación de render y compilación Vite, navegación por teclado, foco, preferencias de movimiento, estados reales del formulario y ausencia de overflow. Comparación visual en móvil, tablet y desktop, incluyendo ambos lados de los breakpoints actuales.

La auditoría final cotejará copy, énfasis, orden, CTA, pricing, notas internas y assets. Se entregará el build con `03-build-notes.md` y evaluación de Fase 3. Los pendientes externos permanecerán declarados y no se marcará el proyecto completado mientras falte trabajo necesario.

## Evaluación del plan — ronda 1

Evaluación cualitativa del plan, no del producto todavía inexistente. Pesos de Fase 3: 20% / 40% / 40%.

| Lente | Puntaje | Objeciones |
| --- | --- | --- |
| Purista | 4.5/5 | La secuencia narrativa depende de disponer de un asset por capas que justifique GSAP. |
| Arquitecto de Sistemas | 4/5 | Integraciones y diferencias entre fuentes siguen declaradas; deben resolverse antes de cerrar el build. |
| Guardián de Lectura | 4/5 | La fidelidad responsive se podrá validar visualmente al renderizar; falta completar contenido funcional y legal. |

Puntaje ponderado: 4.1/5. Resultado: plan apto para revisión del usuario, con pendientes explícitos. No es el gate de cierre de Fase 3.
