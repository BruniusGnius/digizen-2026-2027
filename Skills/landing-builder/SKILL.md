---
name: landing-builder
description: Proceso de 3 fases con gates de aprobación para construir una landing page de conversión (sistema de diseño → wireframe → build). Este archivo es autocontenido -- no asume ningún mecanismo externo de carga de skills, ni memoria de conversaciones previas. Todo lo que necesitas está en esta carpeta y en las rutas de archivo que se referencian explícitamente aquí.
---

# Landing Builder

## Cómo empezar (dado solo el contexto de esta carpeta)

Si estás leyendo este archivo, alguien te apuntó a esta carpeta o te pidió construir/iterar una landing page. No asumas que tienes cargado ningún conocimiento adicional más allá de:
1. Este archivo, completo.
2. Los archivos que este archivo referencia por **ruta relativa explícita** — ábrelos tú mismo cuando corresponda, nadie te los va a inyectar automáticamente.
3. Lo que haya en la carpeta del proyecto (ver estructura abajo).

Antes de actuar, lista el contenido de esta carpeta (`Skills/landing-builder/`) y de la carpeta hermana `../apple-design/` para confirmar qué archivos existen realmente antes de asumir sus rutas.

## Regla no negociable: gates de aprobación

Este proceso tiene **3 fases secuenciales**. Cada fase produce un artefacto de texto/diagrama (nunca código final antes de la Fase 3). **No avances a la siguiente fase sin una confirmación explícita del usuario** con una frase equivalente a "aprobado, sigue" o "sí, continúa a la fase X".

Si el usuario pide un cambio DESPUÉS de haber aprobado una fase y de haber avanzado:
- Si el cambio es menor (un color, un copy suelto) → aplícalo como parche puntual, sin reabrir la fase completa.
- Si el cambio es estructural (cambiar el layout, cambiar la paleta completa) → dilo explícitamente: "esto significa reabrir la Fase X, lo cual invalida lo que se construyó después. ¿Confirmas?" — nunca lo hagas en silencio.

**Por qué existe esta regla:** cada fase es progresivamente más cara de regenerar. Cambiar un token de color en la Fase 1 es gratis; cambiarlo después de tener código Tailwind + animaciones ya escrito no lo es. El gate existe para proteger el presupuesto de tokens/créditos del usuario, no como burocracia.

## Regla no negociable: fidelidad del contenido fuente

El copy, las notas de producción, las restricciones y los datos proporcionados por el usuario son la fuente de verdad. **No se permite omitir, sintetizar, parafrasear, corregir ni inventar contenido** para hacer más breve o más conveniente un artefacto.

- En un wireframe de ocupación real, cada fragmento de copy de producción debe aparecer literal y en el bloque donde se evaluará su espacio. No bastan placeholders ni resúmenes.
- Si un fragmento es una nota interna, una hipótesis o un pendiente y no debe formar parte de la UI pública, consérvalo completo en un anexo o ledger claramente rotulado; no lo conviertas en copy de cara al usuario ni lo descartes.
- Si falta información necesaria para un componente (por ejemplo, FAQ, legal, precio o destino de un CTA), representa el contenedor como pendiente y declara exactamente qué falta. Nunca rellenes el vacío con contenido inventado.
- Antes de cada gate, ejecuta una auditoría fuente → artefacto y entrega cualquier excepción explícita. Una excepción solo es válida si el usuario la aprobó expresamente.

## Estructura de carpetas esperada (por proyecto)

Cada vez que este proceso se usa para un proyecto nuevo, trabaja sobre esta estructura dentro de la misma carpeta raíz donde vive `Skills/` (ej. el vault, o cualquier carpeta que el usuario indique):

```
Projects/<nombre-proyecto>/
  00-context/              ← .md de copy, marca, referencias que el usuario pega/adjunta
  project.config.md        ← este proceso lo crea en la primera ejecución (ver Fase 0)
  01-design-system.md      ← output Fase 1
  02-wireframe.md          ← output Fase 2 (o .html si es un wireframe navegable)
  03-build-notes.md        ← output Fase 3: decisiones, no el código completo
  output-code/             ← el código real vive aquí (o en el repo del proyecto, referenciado)
```

Si la carpeta del proyecto no existe, créala. Si `project.config.md` no existe, es la primera vez que corre este proceso en este proyecto: pregunta lo mínimo necesario (ver Fase 0) y créalo.

## Fase 0 — Setup del proyecto (una sola vez, antes de tocar diseño)

Si no existe `project.config.md` en la carpeta del proyecto, es la primera vez que corre este proceso aquí. Esta fase tiene 3 pasos, en orden, y **no se avanza a la Fase 1 hasta completarlos los tres**:

### 0.1 — Scaffolding (acción, no pregunta)
En cuanto sepas el nombre del proyecto, crea de inmediato la estructura de carpetas completa (ver "Estructura de carpetas esperada" arriba), incluyendo `00-context/` vacía. No esperes a tener contenido para crear las carpetas — es un paso mecánico.

### 0.2 — Solicitud explícita de archivos
Pide al usuario, como dos cosas separadas (no las mezcles en una sola pregunta):
- **Contenido/copy ya escrito** — obligatorio. Sin esto no se puede avanzar: este proceso construye sobre copy ya escrito, no lo genera. Pídele que lo coloque en `00-context/`.
- **Sistema de diseño previo a refinar, si existe** — opcional (ej. un HTML de otra pieza, un brand book, capturas). Si existe, también va a `00-context/`, y la Fase 1 lo va a tomar como punto de partida de tokens (nunca copiarlo 1:1 sin evaluarlo — eso ya está definido en `phases/01-design-system.md`). Si el usuario dice que no hay nada previo, anótalo así y sigue — no insistas.

No sigas al cuestionario (0.3) hasta que al menos el copy esté efectivamente en la carpeta — pedirlo y seguir sin confirmarlo es el error más común aquí.

### 0.3 — Cuestionario de contexto
Antes de tocar cualquier decisión de diseño, pregunta:
- Público objetivo (quién lee esto, y qué tan frío/tibio llega).
- ¿El contenido es largo/denso? (si sí, esto sube el peso de "legibilidad" en la rúbrica de la Fase 2 — ver `phases/_evaluation-rubric.md`).
- Tono/personalidad de marca en 2-3 adjetivos (ej. "cálido y editorial" vs. "técnico y directo") — esto es insumo real de la Fase 1, no relleno.
- Objetivo de conversión de la landing (¿una sola acción? ¿dos CTAs distintos? ¿solo informar?).
- ¿Hay restricciones de marca ya fijas e innegociables (un color de logo, una tipografía obligatoria)? Si las hay, quedan congeladas desde ya — la Fase 1 refina alrededor de ellas, no las reemplaza.

No preguntes todavía por stack técnico — eso es Fase 3, cuando ya hay diseño aprobado y tiene sentido decidirlo.

Guarda las respuestas en `project.config.md` con este formato:
```markdown
---
project: <nombre>
created: <fecha>
fase_actual: 1
---
- contenido_fuente: 00-context/<archivo(s)>.md
- sistema_previo: 00-context/<archivo>.html | ninguno
- publico: <descripción corta>
- reto_legibilidad: <sí/no + por qué>
- tono_marca: <2-3 adjetivos>
- objetivo_conversion: <descripción corta>
- restricciones_fijas: <lista o "ninguna">
---
```

Actualiza el campo `fase_actual` cada vez que una fase se apruebe y se avance.

## Dependencia de contenido: principios de interacción física

Antes de ejecutar la Fase 1, busca y lee **completo** el archivo en la ruta relativa `../apple-design/SKILL.md` (relativa a esta carpeta `Skills/landing-builder/`). Contiene los principios de tipografía dependiente del tamaño, materiales/translucidez, manipulación directa, feedback y motion que las 3 fases usan — no son un tema aparte de "animación", informan decisiones desde el sistema de diseño.

**Si ese archivo no existe en esa ruta:** dile al usuario explícitamente — "no encontré `../apple-design/SKILL.md`, ¿existe en otra ruta o seguimos sin esos principios?" — y espera su respuesta antes de continuar. No sigas asumiendo un contenido que no leíste.

Cada archivo de fase (abajo) indica en qué punto exacto de esa lectura debes apoyarte.

## Fases

Cada fase tiene su propio archivo de instrucciones detalladas, en esta misma carpeta bajo `phases/`. Ábrelo y léelo completo **antes** de ejecutar esa fase — no operes de memoria de una lectura anterior si la conversación se reinició:

1. **Fase 1 — Sistema de diseño** → lee `phases/01-design-system.md`
2. **Fase 2 — Wireframe / arquitectura de información** → lee `phases/02-wireframe.md`
3. **Fase 3 — Build final** → lee `phases/03-build.md`

## Evaluación interna antes de cada gate

Ninguna de las 3 fases llega al usuario "en crudo". Antes de cada gate de aprobación, lee `phases/_evaluation-rubric.md` y corre ese loop de evaluación y refinamiento (rúbrica de 3 lentes de calidad + máximo 2 rondas de refinamiento automático) sobre el artefacto de la fase. Este loop **nunca modifica el copy/contenido fuente** — solo refina el artefacto de diseño/estructura/código de esa fase. Cada archivo de fase define los pesos de la rúbrica que le corresponden.

## Reutilización entre proyectos

Esta carpeta (`Skills/landing-builder/`) es markdown portátil — no depende de que ninguna herramienta la "instale" ni la autocargue. Se reutiliza simplemente reabriendo este mismo archivo desde cualquier sesión/herramienta/IA y apuntándolo a una carpeta de proyecto distinta en `Projects/<nombre>/`. Lo único que cambia entre proyectos es esa carpeta de contenido — nunca hardcodees referencias a un proyecto específico (ej. "DIGIZEN", "ADA") dentro de este archivo ni de los archivos de `phases/`; esos nombres solo deben vivir dentro de los archivos de output de cada proyecto.
