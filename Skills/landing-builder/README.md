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
