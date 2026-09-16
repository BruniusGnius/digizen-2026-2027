---
project: DIGIZEN
artifact: sistema de diseño refinado
status: propuesto
source_system: ../estilo o sistema de diseño/
source_copy: ../datos/digizen-copy-ola.md
---

# DIGIZEN · Sistema de diseño refinado

Este es un sistema nuevo e independiente para refinar, no reemplazar, el prototipo de onboarding que vive en `../estilo o sistema de diseño/`. El prototipo, su copy, sus pantallas, estados, acuerdos, dashboard y navegación se conservan intactos. Aquí se formalizan los principios, tokens y componentes para aplicarlos después de forma consistente.

## Intención

DIGIZEN acompaña conversaciones familiares sobre vida digital. Debe sentirse claro, sereno y competente: nunca como vigilancia, castigo o una plataforma infantilizada. La experiencia combina una base editorial sobria con momentos expresivos alrededor de ADA.

### Principios

1. **Acompañar, no vigilar.** Privacidad, acuerdos, artefactos y señales de cuidado deben diferenciarse de forma explícita y calmada.
2. **Una decisión por momento.** Cada pantalla prioriza un único siguiente paso; la información auxiliar se mantiene visible sin competir.
3. **La paleta existente es fija.** Se conservan todos los tonos de la propuesta original; el refinamiento solo define sus usos, no los sustituye.
4. **Iconos y bordes también comunican.** La placa de icono y las líneas inferiores/superiores de las cajas son parte del lenguaje de navegación y agrupación; se conservan.
5. **La calidez está en ADA; la estructura es tranquila.** Gradientes, brillos y movimiento pertenecen a la escena de ADA y a feedback puntual, no a todas las superficies.
6. **El criterio es legible.** La jerarquía debe permitir escanear qué construyó el alumno, qué puede hacer la familia y qué profundidad es opcional.
7. **Sistema antes que excepción.** Los mismos tokens resuelven familia, alumno y dashboard; solo cambia la densidad y el lenguaje de cada audiencia.

## Entregables

- [`tokens.css`](tokens.css): variables y componentes base, listos para importarse sin depender del prototipo existente.
- [`preview.html`](preview.html): lámina de referencia con los componentes y sus estados esenciales.

## Tipografía

Se mantiene la pila de sistema usada por el prototipo: `Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`. Es rápida, familiar y robusta en móvil.

| Nivel | Tamaño | Peso | Tracking | Leading | Uso |
| --- | --- | --- | --- | --- | --- |
| Display | `clamp(2.25rem, 5vw, 3.75rem)` | 820 | `-.04em` | 1.03 | Inicio de pantalla y promesa principal. |
| H1 | `clamp(1.9rem, 3.4vw, 2.75rem)` | 800 | `-.032em` | 1.10 | Título de sección. |
| H2 | `1.25–1.5rem` | 780 | `-.018em` | 1.20 | Título de card o módulo. |
| Lead | `1–1.125rem` | 500 | normal | 1.58 | Explicación de una decisión. |
| Cuerpo | `0.875–1rem` | 500 | normal | 1.68 | Lectura sostenida y acuerdos; el peso evita que se pierda sobre los materiales claros u oscuros. |
| Label | `0.6875–0.75rem` | 850 | `.08em` | 1.2 | Progreso y categoría. El microcopy de lectura usa 500, no este peso. |

La escala evita cuerpo menor a 15 px. Los títulos condensan por tracking negativo, no reduciendo legibilidad; el cuerpo conserva aire suficiente para copy emocional y explicativo.

## Color y material

| Token | Valor | Rol |
| --- | --- | --- |
| `--dg-canvas` | `#F6F8FB` | Fondo general. |
| `--dg-surface` | `#FBFCFE` | Lienzo de la experiencia. |
| `--dg-surface-end` | `#F0F4F8` | Cierre del gradiente de fondo. |
| `--dg-raised` | `#FFFFFF` | Cards y controles. |
| `--dg-subtle` | `#EEF4F8` | Superficie secundaria o de lectura. |
| `--dg-soft` | `#8B98AA` | Estado suave, jerarquía terciaria y borde reforzado. |
| `--dg-selected` | `rgba(49,108,255,.08)` | Opción elegida; derivado del azul existente. |
| `--dg-ink` | `#152033` | Texto principal. |
| `--dg-navy` | `#111A34` | Fondo oscuro y contraste estructural. |
| `--dg-muted` | `#617085` | Contexto y ayuda. |
| `--dg-line` | `#DFE7EE` | Bordes y separadores. |
| `--dg-blue` | `#316CFF` | Estructura, navegación, progreso. |
| `--dg-cyan` | `#22BED1` | ADA y acompañamiento positivo. |
| `--dg-violet` | `#7564F4` | Reflexión y voz del alumno. |
| `--dg-coral` | `#FF6B5F` | Señal de cuidado; no CTA. |
| `--dg-orange` | `#F59D36` | Energía, avance o señal de actividad. |
| `--dg-gold` | `#F4C650` | Hito, reconocimiento o logro. |
| `--dg-green` | `#37B879` | Confirmación y guardado. |
| `--dg-action-start/end` | `#316CFF → #22BED1` | CTA primario, exactamente como el eje visual original. |

La paleta se conserva sin nuevos hexadecimales. Las transparencias se limitan a mezclas de los colores existentes en notas editoriales y elementos flotantes; una superficie estructural siempre permanece opaca para evitar capas lavadas.

### Tema oscuro

El sistema original Faro ADA incluye una variante oscura completa. Se activa con `data-theme="dark"` en el elemento `<html>` y conserva su paleta fuente:

| Rol | Light | Dark |
| --- | --- | --- |
| Fondo | `#F5F8FA` | `#071018` |
| Superficie | `#FFFFFF` | `#0F1D28` |
| Superficie secundaria | `#EDF4F6` | `#132938` |
| Texto | `#10202D` | `#EDF8FF` |
| Texto secundario | `#61717F` | `#A7B8C6` |
| Línea | `#D7E3E8` | `rgba(172,204,222,.22)` |
| Cyan ADA | `#12C8D6` | `#43DEEA` |
| Azul | `#2478FF` | `#75AAFF` |
| Coral | `#FF665C` | `#FF8077` |
| Ámbar | `#FFC557` | `#FFD477` |
| Verde | `#35BD85` | `#63D59F` |
| Violeta | `#8068FF` | `#AA98FF` |

No es un filtro: cards, selector, bordes, iconos, retícula, escena ADA y sombras reciben tokens de tema. La lámina incluye un control para revisar ambas variantes.

## Espaciado, forma y elevación

Escala única: `4 / 8 / 12 / 16 / 24 / 32 / 48 px`.

- `8–12`: icono con texto, label con título, elementos de una misma unidad.
- `16`: padding de controles y separación de ideas cercanas.
- `24`: separación estándar entre grupos dentro de una pantalla.
- `32`: módulos independientes.
- `48`: cambio de bloque o pausa visual.

Los controles usan 12 px de radio y 48 px de altura mínima. Las cards usan 18 px, y la escena ADA 24 px. Hay dos elevaciones: `--dg-shadow-card` para contenido y `--dg-shadow-float` para menú, diálogo o elemento que se superpone.

## Componentes

Todos los componentes parten de una sola gramática: superficie blanca, borde de 1 px `--dg-line`, radio de 16 px, padding de 16 px y sombra sutil. Los cambios de color, icono o regla inferior expresan significado; no crean una familia visual distinta.

| Componente | Uso | Estados |
| --- | --- | --- |
| Botón primario | Avanzar o confirmar una decisión. | Default, hover, active, disabled, focus visible. |
| Botón secundario | Ruta alternativa o acción de bajo peso. | Default, hover, active, focus visible. |
| Kicker | Ubicación de una pantalla; nunca CTA. | Neutro, con indicador ADA. |
| Card de elección | Edad, interés, método de invitación, avatar. | Reposo, hover, seleccionado, focus. |
| Panel editorial | Privacidad, acuerdo, artefacto, nota de cuidado. | Acento cyan, violet o coral según semántica. |
| Placa de icono | Identifica misión, tema, señal o estado sin reemplazar el título textual. | Círculo tonal de 46 px con icono lineal. Azul (estructura), cyan (ADA), violeta (reflexión), coral (cuidado), dorado (hito), verde (confirmación). |
| Caja con regla | Encierra una unidad de reporte, selector o profundidad opcional. | Línea superior e inferior `--dg-line`; borde inferior semántico cuando el bloque lo necesita. |
| Tarjeta de principio | Comunica una promesa de producto o principio de acompañamiento sin imponerse sobre el contenido. | Deriva de las cards del sistema fuente: sin altura fija, borde `--dg-line` de 1 px, icono lineal de 46 px dentro de halo tonal y franja inferior de 6 px. Título 20 px y cuerpo 14 px. Cyan = señales, dorado = privacidad, verde = conversación. |
| Chips | Contexto corto en dashboard. | Informativo, no accionable por defecto. |
| Acordeón | Profundidad opcional para familia. | Cerrado, abierto y focus. |
| Escena ADA | Momento expresivo de la guía. | Superficie con gradiente, un solo cue flotante. |

## Responsive y accesibilidad

- Desktop: retícula de 12 columnas; contenido extenso se desplaza dentro de la pantalla, sin recortar paneles.
- Tablet: dos columnas cuando la escena ADA agrega valor; de lo contrario, una columna.
- Móvil: una columna; CTA apilados a ancho completo; no hay decisiones que dependan de precisión.
- Objetivo táctil mínimo de 44 px; CTA de 48 px.
- Foco visible de 3 px para todos los controles.
- `prefers-reduced-motion` elimina animación decorativa y conserva los estados finales.
- Coral se reserva para cuidado y no depende solo del color: se acompaña de título y texto.

## Mapeo al prototipo existente

| Área actual | Aplicación del sistema refinado |
| --- | --- |
| Bienvenida y escena de ADA | Display + CTA primario + escena expresiva. |
| Principios de producto | Cards con halo de icono y franja inferior; se usan para promesas de alto nivel, nunca para métricas o datos densos. |
| Privacidad y artefactos | Panel editorial cyan; texto explica el límite de información. |
| Acuerdo familiar y de alumno | Panel editorial + acción de confirmación sostenida. |
| Perfil, etapa e intereses | Cards de elección y estado seleccionado. |
| Invitación | Cards de método + acción secundaria por canal. |
| Dashboard familiar | Chips, cards, acordeones y semántica de cuidado. |
| Iconos y reglas de caja | La placa mantiene 46 px / radio 15 px; las líneas de caja se conservan en selectores, vista semanal y profundidad. |
| Modo revisión | Elemento flotante, visualmente separado del producto. |

## Restricción importante

El sistema de origen referencia assets de logo, ADA, acuerdo y avatares que no están presentes dentro de `insumos`. Este sistema no elimina ni sustituye esas referencias; al aplicar el refinamiento al prototipo se deberán restaurar los binarios originales para una validación visual completa.
