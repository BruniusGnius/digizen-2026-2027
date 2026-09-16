#!/usr/bin/env bash
set -e

echo "Instalando landing-builder + apple-design en: $(pwd)"

mkdir -p "Skills/landing-builder"
cat > "Skills/landing-builder/SKILL.md" << 'LB_EOF_000'
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
LB_EOF_000

mkdir -p "Skills/landing-builder"
cat > "Skills/landing-builder/README.md" << 'LB_EOF_001'
# landing-builder — qué es esto y cómo usarlo

## Qué problema resuelve

Construir una landing page completa en un solo prompt es barato al inicio y carísimo después: cada corrección de color, de orden de secciones o de tono obliga a regenerar código completo. Este skill separa el trabajo en **3 fases con costo de iteración creciente**, y no deja avanzar a la siguiente fase sin tu aprobación explícita — así los cambios baratos (un token de color, el orden de un bloque) se resuelven antes de llegar a la fase cara (código real con animaciones).

Además, cada fase se autoevalúa contra una rúbrica antes de llegar a ti — no apruebas a ciegas, apruebas viendo un puntaje y las objeciones que quedaron.

## Las 3 fases, en una frase cada una

1. **Sistema de diseño** — tipografía, paleta, componentes clave. Sin layout de página todavía.
2. **Wireframe** — en qué orden va cada bloque de contenido y qué necesita cada uno (acordeón, CTA temprano, feedback al tocar). A propósito feo, sin color real.
3. **Build** — el código final, con el stack técnico que definas y las animaciones.

Entre cada fase hay un **gate**: el skill se detiene y te pregunta explícitamente si aprueba para seguir. Si dices que sí a algo, quedó congelado — un cambio estructural después de eso es una excepción cara, no la norma.

## Qué es `apple-design` y por qué está aquí

Es otro archivo, en la carpeta hermana `Skills/apple-design/SKILL.md`, con principios de cómo debe *sentirse* una interfaz al tocarla — springs en vez de animaciones de duración fija, feedback inmediato, materiales translúcidos con jerarquía, tipografía que cambia de tracking/leading según el tamaño. No hay ningún mecanismo mágico que lo "cargue" solo: el archivo de `landing-builder` le indica a la IA, en cada fase, la ruta exacta donde leerlo (`../apple-design/SKILL.md` o `../../apple-design/SKILL.md` según desde dónde se referencie) y qué puntos aplican ahí. Si mueves esa carpeta o la renombras, tienes que actualizar esas rutas. Es reutilizable fuera de este proceso también — cualquier interfaz que construyas después puede apuntarle a ese mismo archivo.

## Qué necesitas tener listo antes de empezar

- El **copy ya escrito** de la landing (este skill no lo redacta ni lo edita — construye sobre contenido aprobado).
- Claridad de si el contenido es largo/denso (afecta cómo se pesa la rúbrica de legibilidad en la Fase 2).
- El stack técnico que quieres usar, o estar dispuesto a decidirlo cuando el skill lo pregunte en la Fase 3 (puede cambiar entre proyectos).

## Estructura de carpetas por proyecto

```
Projects/<nombre-del-proyecto>/
  00-context/            ← pega aquí tus .md de copy y referencias
  project.config.md       ← lo crea el skill la primera vez
  01-design-system.md
  02-wireframe.md
  03-build-notes.md
  output-code/            ← el código real
```

`Skills/landing-builder/` nunca contiene datos de un proyecto — solo la lógica reutilizable. Así no tienes que reinstalar ni duplicar nada para el siguiente proyecto: apuntas a una carpeta nueva en `Projects/` y ya.

## Cómo se invoca (no depende de una sola herramienta)

Este skill es texto plano — no está atado a Claude Code ni a ninguna IA específica:

- **En un chat normal:** pega `SKILL.md` como primer mensaje del proyecto, y luego el archivo de la fase en la que estés (`phases/01-design-system.md`, etc.).
- **En una herramienta con contexto de proyecto persistente** (Claude Projects, GPTs, Gemini con archivos, Cursor/Windsurf): adjunta toda la carpeta `Skills/landing-builder/` como conocimiento del proyecto.
- **Por CLI, sobre el vault de Obsidian** (ej. `claude` desde la terminal, parado en la carpeta del vault): le pides directamente "ejecuta la Fase 1 del skill en `Skills/landing-builder/` para el proyecto en `Projects/<nombre>/`" y el agente lee y escribe esos mismos archivos que luego ves renderizados en Obsidian.

## Qué esperar de la evaluación en cada fase

Antes de pedirte el gate, cada fase se autoevalúa con 3 lentes de calidad (rigor/reducción, consistencia de sistema, legibilidad para el usuario final) y hace como máximo 2 rondas de auto-refinamiento si el puntaje no alcanza el umbral — con un límite explícito para no gastar iteraciones sin que tú lo decidas. Esa evaluación **nunca toca el copy fuente**, solo el diseño/estructura/código de esa fase. Si después de las 2 rondas sigue sin pasar el umbral, el skill te lo entrega igual, con las objeciones abiertas a la vista, y decides tú si vale la pena seguir ajustando.

## Qué NO hace este skill

- No escribe ni edita el copy de venta.
- No decide el stack técnico por ti de forma silenciosa — lo pregunta si no está definido.
- No reabre una fase ya aprobada por su cuenta — un cambio estructural post-aprobación se te avisa explícitamente antes de aplicarse.
LB_EOF_001

mkdir -p "Skills/landing-builder/phases"
cat > "Skills/landing-builder/phases/01-design-system.md" << 'LB_EOF_002'
# Fase 1 — Sistema de diseño

**Input:** todo lo que haya en `00-context/` (copy, referencias de marca, HTMLs/imágenes de diseño previos que el usuario haya pegado o adjuntado).
**Output:** `01-design-system.md` en la raíz del proyecto. **Nunca** una página completa maquetada.

## Antes de empezar esta fase

Si no lo has hecho ya en esta sesión, lee `../../apple-design/SKILL.md` (ruta relativa desde esta carpeta `phases/`) completo. Los puntos 8 (materiales) y 9 (tipografía) de ese archivo son insumo directo de lo que vas a definir aquí — no los repitas de memoria si no lo has leído.

## Qué construir

### 1. Tipografía — con criterio, no por gusto
Para cada nivel (display/hero, H2 de sección, cuerpo, micro-copy/labels) define y **justifica**:
- Tamaño, peso, tracking, leading — y por qué (jerarquía de información: qué debe leerse primero en un escaneo de 3 segundos).
- **Aplica aquí el punto 9 de `../../apple-design/SKILL.md`** (tracking/leading dependientes del tamaño): el display/hero necesita tracking negativo y leading apretado; el cuerpo necesita tracking neutro/positivo y leading generoso. No definas un solo valor de tracking/leading para toda la escala.
- Si el contenido es largo/denso (marcado en `project.config.md`), prioriza legibilidad de cuerpo sobre personalidad tipográfica — cuerpo cómodo de leer en móvil (mínimo 16px, leading generoso), no comprimido por estética.
- Fuente del sistema por defecto salvo que haya una razón de marca explícita para una fuente custom.

### 2. Paleta de color y materiales — semántica, no decorativa
No entregues solo hexadecimales. Para cada color, di **qué rol cumple**: texto principal, texto secundario/muted, fondo, superficie de card, línea/borde, y 1-2 colores de acento con su significado (ej. "coral = alerta/objeción", "verde = confirmación/garantía").
- Verifica contraste AA mínimo entre texto y fondo en cada combinación que uses.
- Define versión light y dark si el proyecto lo requiere.
- **Si el sistema usa superficies translúcidas** (nav sticky con blur, sheets, overlays), aplica el punto 8 de `../../apple-design/SKILL.md` (jerarquía de materiales): superficies más pesadas/opacas para regiones estructurales, más ligeras para lo interactivo, y nunca dos superficies translúcidas claras apiladas entre sí. Define el contraste de texto sobre esas superficies aquí, no lo improvises en el build.
- **Revisa el campo `sistema_previo` de `project.config.md`.** Si no es "ninguno", ese archivo en `00-context/` es tu punto de partida de tokens — pero evalúa explícitamente qué sirve tal cual para ESTA landing y qué no; nunca lo copies 1:1 sin ese análisis. Si además hay `restricciones_fijas` marcadas en la Fase 0, esos valores quedan congelados — refina alrededor de ellos, no los reemplaces.

### 3. Componentes clave — descritos, no pixel-perfect
Describe (en texto + un boceto simple si ayuda) los componentes que la landing va a reutilizar: botón primario/secundario, card, badge/etiqueta, nav, cita destacada, acordeón. Para cada uno: estados (default/hover/active), y qué información jerárquica resuelve.

### 4. Reglas de espaciado
Define una escala de espaciado (ej. 4/8/16/24/40/64px) y en qué casos se usa cada salto — no espaciados arbitrarios sueltos por sección.

## Formato de salida (`01-design-system.md`)

```markdown
---
project: <nombre>
fase: 1 - sistema de diseño
estado: propuesto | aprobado
---

## Tipografía
...

## Paleta
| Token | Uso | Valor light | Valor dark |
...

## Componentes clave
...

## Espaciado
...
```

## Evaluación antes del gate

Antes de mostrarle el sistema de diseño al usuario, corre el loop de `_evaluation-rubric.md` con estos pesos (esta fase pesa fuerte hacia sistema y rigor, poco hacia lectura porque todavía no hay layout real que escanear):

- Purista: 35%
- Arquitecto de Sistemas: 45%
- Guardián de Lectura: 20%

Muestra siempre la tabla de evaluación junto con el `01-design-system.md` propuesto.

## Gate de salida

Termina siempre preguntando explícitamente: *"¿Apruebas este sistema de diseño para pasar a la Fase 2 (wireframe), o quieres ajustar algo aquí primero?"* No avances sin respuesta afirmativa. Cuando se apruebe, cambia `estado: aprobado` en el frontmatter y actualiza `fase_actual: 2` en `project.config.md`.
LB_EOF_002

mkdir -p "Skills/landing-builder/phases"
cat > "Skills/landing-builder/phases/02-wireframe.md" << 'LB_EOF_003'
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
LB_EOF_003

mkdir -p "Skills/landing-builder/phases"
cat > "Skills/landing-builder/phases/03-build.md" << 'LB_EOF_004'
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
LB_EOF_004

mkdir -p "Skills/landing-builder/phases"
cat > "Skills/landing-builder/phases/_evaluation-rubric.md" << 'LB_EOF_005'
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
LB_EOF_005

mkdir -p "Skills/apple-design"
cat > "Skills/apple-design/SKILL.md" << 'LB_EOF_006'
---
name: apple-design
description: Filosofía de interacción física y motion — cómo diseñar interfaces que responden como objetos reales (springs, interrumpibilidad, materiales, tipografía dependiente del tamaño). Es una dependencia base de cualquier skill que diseñe o construya interfaces, no un módulo opcional de animación — informa decisiones de tipografía/materiales desde el sistema de diseño, de intención de interacción desde el wireframe, y de implementación de motion en el build.
---

# Filosofía de interacción física

La idea central: una interfaz se siente "viva" cuando se comporta como un objeto físico — responde al instante, puede agarrarse y soltarse a medio movimiento, carga inercia, y resiste progresivamente en sus límites en vez de topar en seco. Esto no es una capa de animación que se agrega al final; cambia decisiones desde el sistema de diseño (qué tan translúcido es un material, cómo escala el tracking de una tipografía) y desde el wireframe (qué elementos son arrastrables, dónde hace falta feedback inmediato).

## 1. Respuesta inmediata

El feedback ocurre en el instante del toque/clic inicial, nunca al soltar. Cualquier retraso perceptible entre la acción y la respuesta rompe la sensación de control directo. Esto aplica desde el wireframe (marcar qué elementos necesitan feedback continuo durante el gesto, no solo al terminar) hasta el código (animar en `pointerdown`, no en `click`).

## 2. Manipulación directa

Lo que se arrastra debe seguir el dedo/cursor 1:1, respetando el punto exacto donde se agarró — no saltar al centro del elemento. Cuando el wireframe define un componente arrastrable (un carrusel, un sheet, una barra), esa intención debe quedar anotada ahí, porque cambia cómo se construye el componente después.

## 3. Interrumpibilidad — el principio más importante

Ninguna animación debe bloquear el input. Si el usuario reinicia un gesto a medio vuelo, la interfaz responde de inmediato desde su posición actual en pantalla — nunca desde el destino final "lógico". Esto descarta animaciones de duración fija (`@keyframes`/`transition` simples) para todo lo que el usuario pueda tocar, a favor de springs, que por naturaleza parten del valor actual y pueden redirigirse sin saltos.

## 4. Comportamiento sobre coreografía — usar resortes (springs)

En vez de pensar en duración fija, se piensa en dos parámetros:
- **Damping (amortiguación):** controla el rebote. `1.0` = crítico, sin rebote, asentamiento limpio. Valores menores = más rebote/oscilación.
- **Response:** qué tan rápido llega al destino. No es "duración" — el tiempo de asentamiento emerge de los parámetros, no se fija de antemano.

Regla práctica: la UI normal (menús, paneles que aparecen) usa amortiguación crítica (`~1.0`, sin rebote) — el rebote se reserva exclusivamente para interacciones donde el propio gesto del usuario ya traía momentum (un flick, un drag que se suelta).

## 5. Traspaso de velocidad y proyección de momentum

Cuando se suelta un gesto, la animación que sigue debe continuar con la velocidad exacta con la que iba el dedo — sin costura visible entre "arrastrar" y "animarse solo". Y el punto de destino no debe ser el más cercano desde donde se soltó, sino el que resulta de **proyectar hacia dónde iba** el gesto (como la inercia de un scroll). Esto es lo que hace que un "flick" se sienta como si de verdad hubiera lanzado el objeto.

## 6. Resistencia progresiva en los límites (rubber-banding)

En un borde o límite (fin de un carrusel, tope de un sheet), la resistencia debe crecer progresivamente mientras más se empuja — nunca un tope duro y frío. Un tope duro se siente "congelado"; la resistencia progresiva se siente "responsiva, pero no hay más aquí".

## 7. Consistencia espacial

Lo que entra por un lado debe salir por el mismo lado — un panel que aparece desde la derecha debe cerrarse hacia la derecha, no hacia abajo. Los menús, popovers y sheets deben originarse visualmente desde el elemento que los disparó, no aparecer flotando sin relación espacial con su origen.

## 8. Materiales y profundidad (esto es sistema de diseño, no motion)

La translucidez comunica jerarquía, no es solo estética: materiales más pesados/opacos separan regiones estructurales (barras, sidebars); materiales más ligeros llaman la atención hacia lo interactivo. Nunca apilar dos superficies translúcidas claras entre sí — la legibilidad se rompe. El texto sobre superficies translúcidas necesita más contraste y peso que sobre un fondo sólido — esto se define en la paleta del sistema de diseño, no se improvisa en el build.

## 9. Tipografía dependiente del tamaño (esto también es sistema de diseño)

El espaciado entre letras (tracking) y el interlineado (leading) no son valores fijos — cambian con el tamaño. Texto grande/display necesita tracking negativo (las letras se leen demasiado separadas si crecen sin compensación) y leading apretado. Texto pequeño/cuerpo necesita tracking neutro o levemente positivo y leading más generoso para legibilidad sostenida. Esta regla se aplica al definir la escala tipográfica del sistema de diseño, no después.

## 10. Accesibilidad y movimiento reducido

Movimiento reducido no significa "sin feedback" — significa un equivalente más sobrio: reemplazar deslizamientos/springs/parallax por cross-fades cortos de opacidad, sin rebote. Igual de real: respetar el ajuste de tamaño de texto del usuario (unidades relativas, no píxeles fijos) para que la jerarquía tipográfica no se rompa cuando alguien la escala.

## 11. Rendimiento

Animar únicamente propiedades que el navegador puede componer sin recalcular layout — transformaciones y opacidad. Todo lo demás (color de fondo, tamaño, posición vía top/left) cuesta más caro en cada frame y es la causa más común de animaciones que se sienten "trabadas" en dispositivos de gama media, que son justamente los que más importan en tráfico frío de LATAM en móvil.

## Cómo se usa esto en las 3 fases de un proceso de diseño

- **Sistema de diseño:** los puntos 8 y 9 son insumo directo — la paleta y la escala tipográfica se definen con estas reglas, no se ajustan después.
- **Wireframe:** los puntos 1, 2, 3 y 7 se anotan como intención de interacción por componente (qué se arrastra, qué necesita feedback inmediato, de dónde entra/sale cada panel) — es información de diseño, no de implementación todavía.
- **Build:** los puntos 4, 5, 6, 10 y 11 son las reglas de implementación real del motion — springs, velocidad, rubber-banding, reduced motion, rendimiento.
LB_EOF_006

cat > "AGENTS.md" << 'LB_EOF_007'
# Instrucciones para agentes en este vault

Este vault contiene procesos reutilizables en `Skills/` y datos de proyectos en `Projects/`.

## Construcción de landing pages

Si el usuario pide construir, rediseñar o iterar una landing page:
1. Lee `Skills/landing-builder/SKILL.md` completo antes de hacer nada.
2. Sigue exactamente lo que ese archivo indica (fases, gates de aprobación, rutas relativas a otros archivos como `Skills/apple-design/SKILL.md`).
3. No resumas ni reinterpretes ese proceso de memoria si ya lo leíste antes en otra sesión — vuelve a abrirlo, puede haber cambiado.

No apliques este proceso a ajustes menores de una landing ya construida (eso es un fix puntual). Solo aplica para construir desde cero o iterar estructuralmente.
LB_EOF_007

echo "Listo. Estructura creada:"
find Skills AGENTS.md -type f 2>/dev/null | sort

echo ""
echo "Siguiente paso: pide a tu agente (Codex/Claude/etc.) que lea Skills/landing-builder/SKILL.md"
echo "y arranque el proceso para tu proyecto (el creara Projects/<nombre>/ el solo en la Fase 0)."
