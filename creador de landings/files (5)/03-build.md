# Fase 3 — Build final

**Requisito previo:** `01-design-system.md` y `02-wireframe.md` ambos con `estado: aprobado`. Si falta alguno, detente y dilo.

**Input:** design system aprobado + wireframe aprobado + el stack técnico que el usuario defina para este proyecto (puede variar entre proyectos — pregúntalo aquí si `project.config.md` no lo especifica ya).
**Output:** código real en `/output-code/` (o en el repo del proyecto), + `03-build-notes.md` con las decisiones tomadas.

## En esta fase NO se reabren la Fase 1 ni la Fase 2

Si durante el build notas que un token de color falta o un bloque del wireframe no tenía suficiente detalle, resuélvelo con el criterio ya definido en esas fases (son la fuente de verdad), o pide un ajuste puntual — pero no vuelvas a diseñar el sistema de color ni el layout desde cero aquí. Si el usuario pide un cambio estructural en esta fase, avísale explícitamente que eso reabre una fase anterior y tiene costo de reconstrucción.

## Qué preguntar si no está definido en `project.config.md`

- Stack de backend/templating (ej. Laravel+Blade, Astro, HTML estático, Next.js).
- Sistema de CSS (ej. Tailwind) y si hay que traducir los tokens de la Fase 1 a su config.
- Librería de interactividad ligera (ej. Alpine.js) si el wireframe requiere acordeones, toggles, CTA flotante, etc.
- Si hay un formulario/lead capture: qué backend lo recibe (ruta+controller+tabla, o un servicio externo).

## Motion y animación

Si no lo has hecho ya en esta sesión, lee `../../apple-design/SKILL.md` (ruta relativa desde esta carpeta) completo — es la fuente de verdad de comportamiento para todo lo implementado aquí (puntos 4, 5, 6, 10 y 11: springs vs. keyframes, interrumpibilidad, traspaso de velocidad, rubber-banding, reduced motion, rendimiento). No reinventes esas reglas en esta fase — impléméntalas. Verifica en particular que las anotaciones de intención de interacción que se dejaron en `02-wireframe.md` (punto 6 de esa fase) se traduzcan fielmente: si un componente se marcó como interrumpible/con feedback inmediato, el código debe cumplirlo, no solo animar bonito.

**Si `../../apple-design/SKILL.md` no existe en esa ruta:** detente y díselo al usuario antes de escribir motion — no continúes con un fallback silencioso ni con reglas inventadas de memoria.

## Construcción

1. Traduce los tokens de `01-design-system.md` a la configuración real del CSS (ej. `tailwind.config.js`) — no dejes valores sueltos hardcodeados en las clases.
2. Construye un componente/sección por bloque del wireframe aprobado, en el mismo orden.
3. Implementa las tácticas de legibilidad marcadas en la Fase 2 (acordeones, CTA temprano, barra de progreso, etc.) tal como se anotaron — no las reinterpretes.
4. Antes de escribir todo el código, entrega primero un resumen del plan de componentes/archivos y espera aprobación — esto sigue siendo más barato que escribir todo y corregir después.
5. Al terminar, entrega `03-build-notes.md`: qué se tradujo de cada fase anterior, qué librerías se usaron, y cualquier decisión tomada que no estuviera ya definida en las fases previas.

## Evaluación antes del gate

Antes de dar por cerrada la fase, corre el loop de `_evaluation-rubric.md` con estos pesos (aquí Sistema pesa más porque el riesgo principal es implementación infiel a los tokens/wireframe aprobados; Lectura sigue pesando porque ahora sí hay producto real que se puede medir):

- Purista: 20%
- Arquitecto de Sistemas: 40%
- Guardián de Lectura: 40%

Para esta fase, además de las objeciones cualitativas de cada lente, verifica explícitamente (esto alimenta el puntaje del Arquitecto de Sistemas y del Guardián de Lectura, no es un lente aparte):
- Fidelidad a los tokens de la Fase 1 (nada hardcodeado fuera de la config).
- Fidelidad al orden y las anotaciones de la Fase 2 (nada reordenado sin decirlo).
- Cumplimiento de las reglas de motion leídas en `../../apple-design/SKILL.md`.
- Accesibilidad básica (contraste, `prefers-reduced-motion`, semántica HTML).

Muestra siempre la tabla de evaluación junto con `03-build-notes.md` antes de considerar el proyecto cerrado.

## Cierre del proyecto

Actualiza `project.config.md` con `fase_actual: completado`. Este proyecto queda como referencia — si el usuario quiere iterar después, es un ajuste puntual sobre el output existente, no una nueva corrida completa de las 3 fases salvo que él lo pida explícitamente.
