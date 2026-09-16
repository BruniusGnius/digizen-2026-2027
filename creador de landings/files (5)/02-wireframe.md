# Fase 2 — Wireframe / arquitectura de información

**Requisito previo:** `01-design-system.md` con `estado: aprobado`. Si no está aprobado, detente y dile al usuario que hay que cerrar la Fase 1 primero.

**Input:** el copy completo de `00-context/` + `01-design-system.md` aprobado.
**Output:** `02-wireframe.md` (y opcionalmente un HTML de baja fidelidad si ayuda a visualizar).

## Regla central: esto debe verse feo a propósito

El wireframe usa **solo escala de grises y cajas** — nada de la paleta de color aprobada en Fase 1. Si se ve bonito aquí, el usuario va a empezar a opinar de estética en el momento equivocado, y vas a mezclar decisiones de layout con decisiones de color/tipografía que ya se cerraron.

## Qué resolver en esta fase

1. **Mapeo contenido → sección.** Cada bloque de copy (hook, cada "beat"/sección temática, oferta, FAQ) se convierte en un bloque del wireframe, en el orden del copy original — nunca reordenes el copy sin decírselo al usuario explícitamente.
2. **Jerarquía de escaneo.** Marca en el wireframe qué es lo que se lee en un escaneo de 3 segundos (subtítulos, quotes destacados, CTA) vs. qué es profundidad opcional.
3. **Estrategia contra la densidad** (si el proyecto la necesita, según `project.config.md`):
   - ¿Qué bloques van en acordeón/expandible vs. abiertos por default?
   - ¿Dónde va el primer CTA (no solo al final)?
   - ¿Hay barra de progreso de scroll, CTA flotante móvil, anclas de navegación?
4. **Responsive.** Anota diferencias relevantes mobile vs. desktop si cambian el orden o el agrupamiento (no solo el tamaño).
5. **Anotaciones, no solo cajas.** Cada bloque lleva una nota corta de intención: "acordeón — 4 puntos, abierto solo el primero", "CTA temprano — repite el del hero", "cita destacada — mayor tamaño que el cuerpo".
6. **Intención de interacción.** Si no lo has hecho ya en esta sesión, lee `../../apple-design/SKILL.md` (ruta relativa desde esta carpeta) — los puntos 1, 2, 3 y 7 aplican aquí. Para cada componente interactivo del wireframe (acordeón, CTA flotante, barra de progreso, cualquier cosa arrastrable o con estado abierto/cerrado), anota explícitamente: qué necesita feedback inmediato al tocarlo, si debe poder interrumpirse/revertirse a medio gesto, y de qué dirección entra/sale (para que salga por el mismo camino por el que entró). Esto no es detalle de animación — es información de diseño que cambia cómo se construye el componente en la Fase 3, así que se decide aquí, no se improvisa después.

## Formato de salida

Puede ser:
- **Texto estructurado** (`02-wireframe.md`) con una lista ordenada de bloques + anotaciones — el mínimo viable, siempre entregarlo.
- **Diagrama/HTML de cajas grises** además del texto, si el proyecto se beneficia de verlo (usar el Visualizer o un HTML mínimo sin color real) — opcional, no obligatorio.

```markdown
---
project: <nombre>
fase: 2 - wireframe
estado: propuesto | aprobado
---

## Orden de bloques (desktop / mobile si difiere)
1. Hero — [nota de intención]
2. Beat 1 — [nota]
3. CTA temprano — [nota: por qué aquí]
...

## Decisiones de legibilidad aplicadas
- ...
```

## Evaluación antes del gate

Antes de mostrarle el wireframe al usuario, corre el loop de `_evaluation-rubric.md` con estos pesos (aquí el Guardián de Lectura pesa más — es literalmente el problema que esta fase existe para resolver):

- Purista: 25%
- Arquitecto de Sistemas: 20%
- Guardián de Lectura: 55%

Recordatorio explícito para el Guardián de Lectura en esta fase: debe evaluar puntualmente si el orden y las anotaciones (acordeones, CTA temprano, jerarquía de escaneo) resuelven el reto de densidad marcado en `project.config.md` — no evalúa estética, porque el wireframe no debe tenerla todavía.

Muestra siempre la tabla de evaluación junto con el `02-wireframe.md` propuesto.

## Gate de salida

Pregunta explícitamente: *"¿Apruebas este layout y arquitectura de información para pasar a la Fase 3 (build), o ajustamos el orden/estructura primero?"* Actualiza `estado: aprobado` y `fase_actual: 3` solo tras confirmación.
