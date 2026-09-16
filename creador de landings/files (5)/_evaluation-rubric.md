# Evaluación y loop de refinamiento (compartido por las 3 fases)

Este archivo define **cómo** se evalúa el artefacto de cada fase antes de presentarlo al usuario para el gate de aprobación. Se invoca desde `01-design-system.md`, `02-wireframe.md` y `03-build.md` — cada uno trae su propia rúbrica de criterios (abajo se explica cómo se combinan), pero el mecanismo del loop es el mismo en las tres.

## Regla no negociable: el contenido es intocable

Este loop evalúa y refina **el artefacto de diseño/estructura de esa fase** (tokens, jerarquía tipográfica, layout, anotaciones de wireframe, código). **Nunca reescribe, resume, recorta ni "mejora" el copy fuente.** Si un evaluador señala que "el texto es muy largo para el bloque", la corrección válida es de **diseño** (acordeón, jerarquía visual, espaciado) — nunca tocar las palabras del copy. Si genuinamente crees que el copy necesita cambiar, eso se reporta al usuario como una nota aparte, fuera del loop, nunca se ejecuta solo.

## Los 3 lentes de evaluación

En vez de nombrar a una persona real, usa estos tres arquetipos — cada uno representa un estándar de calidad reconocible en la industria, sin atribuirle opiniones inventadas a alguien específico:

1. **El Purista** — el lente de la reducción radical. Pregunta: *¿cada elemento de esto se puede defender, o sobra?* Penaliza decoración sin función, inconsistencia de intención, cualquier cosa que exista "porque se veía bien" en vez de porque resuelve algo. Tolerancia cero a la ambigüedad de propósito.
2. **El Arquitecto de Sistemas** — el lente de la escalabilidad y consistencia, con el rigor de un design system profesional (piensa en cómo se documentan y versionan los sistemas de diseño de producto serios). Pregunta: *¿esto es un sistema con reglas reutilizables, o son decisiones sueltas que se van a desalinear en la siguiente sección?* Penaliza valores hardcodeados, falta de nomenclatura clara, tokens no documentados.
3. **El Guardián de Lectura** — el lente centrado en el usuario final que escanea en frío, en un celular, con poca paciencia. Pregunta: *¿alguien que no está comprometido a leer todo, entiende lo esencial en segundos?* Penaliza densidad sin jerarquía, ambigüedad de a dónde mirar primero, fricción de scroll/tap.

## Rúbrica (1–5 por lente, cada fase define sus pesos)

Cada lente puntúa 1–5:
- **5** — ejemplar, sin objeciones.
- **4** — sólido, con 1-2 ajustes menores.
- **3** — funcional pero con problemas claros que afectan el resultado.
- **2** — insuficiente, requiere rediseño de esa dimensión.
- **1** — no cumple el criterio en absoluto.

**Puntaje final = promedio ponderado** según los pesos que define cada fase (ver sus archivos). **Umbral de aprobación interna: ≥ 4.0.**

## Mecánica del loop (con tope de costo)

1. Genera el artefacto de la fase (v1).
2. Evalúa con los 3 lentes → puntaje + lista concreta de objeciones por lente.
3. Si puntaje ≥ 4.0 → detente aquí, pasa el artefacto al usuario con el resumen de evaluación adjunto (transparencia: muéstrale el puntaje y las objeciones menores que quedaron, no las escondas).
4. Si puntaje < 4.0 → aplica **una sola ronda de refinamiento** dirigida específicamente a las objeciones señaladas (no regeneres todo desde cero) → vuelve a evaluar (v2).
5. **Máximo 2 rondas de refinamiento internas** (v1→v2→v3). Si tras la v3 sigue sin llegar a 4.0, **detente igual** y entrégale al usuario el artefacto junto con las objeciones abiertas, explícitas: "esto quedó en X puntaje; los lentes señalan estos problemas sin resolver; se detuvo el refinamiento automático para no seguir gastando iteraciones — decide tú si seguimos ajustando o si estos problemas son aceptables."

Este tope existe por lo mismo que los gates entre fases: cada ronda de refinamiento cuesta, y un loop sin límite puede gastar presupuesto sin que el usuario lo esté decidiendo activamente.

## Formato de salida de la evaluación (siempre visible al usuario, no oculto)

```markdown
### Evaluación — Fase <N>, ronda <n>
| Lente | Puntaje | Objeciones |
|---|---|---|
| Purista | X/5 | ... |
| Arquitecto de Sistemas | X/5 | ... |
| Guardián de Lectura | X/5 | ... |

**Puntaje ponderado:** X.X / 5
**Resultado:** aprobado internamente | refinado (ronda n+1) | detenido por tope de rondas
```

Esta tabla se muestra **siempre** junto al artefacto de la fase, antes de pedir el gate de aprobación al usuario — el usuario aprueba viendo la evaluación, no a ciegas.
