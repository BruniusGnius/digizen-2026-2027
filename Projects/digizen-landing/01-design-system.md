---
project: DIGIZEN
fase: 1 - sistema de diseño
estado: aprobado
source_system: ../../creador de landings/insumos/estilo o sistema de diseño/
source_copy: 00-context/digizen-copy-ola.md
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

---

# Revisión visual v2 — propuesta

**Estado de la revisión:** aprobado por el usuario el 2026-09-11.

Esta propuesta reemplaza los tokens y tratamientos visuales anteriores para la landing Angular; no cambia el wireframe aprobado ni el copy fuente.

## Alcance congelado

- Se conservan literalmente el copy, la diagramación, orden de secciones, columnas, CTAs, pricing, diálogo ADA, responsive e interacciones.
- No se elimina ningún bloque, icono, imagen ni contenido.
- Se conserva la estrategia de titulares gris/negro: fragmento secundario gris (`.dg-h2-muted`) y mensaje principal en negro/ink.
- Se conserva el acento de acción actual: violeta `#6448EA` en CTAs y decisiones prioritarias.

## Fusión de la referencia ADA V05

La referencia aporta una gramática de producto clara: base gris-azulada fría, superficie blanca, borde fino, sombra contenida, navy para confianza y color concentrado en iconos y estados. Se adoptan esos rasgos, no su arquitectura ni copy. Se eliminan de la landing las retículas y gradientes ambientales expansivos; el color se reserva para señales, ADA, estados y acciones.

## Tipografía

Se conserva `Inter` variable desde Google Fonts. La escala deja de usar pesos extremos en el cuerpo para que el contraste de peso sea visible y cómodo en lectura larga.

| Nivel | Tamaño | Peso | Tracking | Leading | Uso |
| --- | --- | --- | --- | --- | --- |
| Display | `clamp(2.75rem, 5.4vw, 4.6rem)` | 780 | `-.045em` | `.98` | Hero en ink sólido. |
| H2 principal | `clamp(2rem, 3.4vw, 3.45rem)` | 760 | `-.035em` | `1.06` | Mensaje negro/ink. |
| H2 secundario | Hereda H2 | 560 | `-.025em` | `1.06` | Fragmento gris; regla existente preservada. |
| H3 | `1.3–1.8rem` | 720 | `-.018em` | `1.2` | Módulos y cards. |
| Lead | `1–1.12rem` | 520 | `0` | `1.58` | Apoyo de la promesa. |
| Cuerpo | `1rem` | 450 | `0` | `1.72` | Lectura sostenida. |
| Strong | Hereda | 700 | `0` | Hereda | Énfasis semántico. |
| Kicker | `.6875rem` | 800 | `.08em` | `1.2` | Categoría y estado. |

## Paleta y material

| Token | Light | Dark | Función |
| --- | --- | --- | --- |
| `--dg-canvas` | `#F6F8FB` | `#0F1728` | Fondo frío continuo. |
| `--dg-raised` | `#FFFFFF` | `#172338` | Cards y controles. |
| `--dg-subtle` | `#EEF4F8` | `#202E45` | Panel secundario e icono tonal. |
| `--dg-ink` | `#152033` | `#F4F7FB` | Titular negro/ink y texto fuerte. |
| `--dg-muted` | `#617085` | `#AAB7C8` | Titular gris y texto secundario. |
| `--dg-line` | `#DFE7EE` | `rgba(223, 231, 238, .16)` | Bordes y divisores. |
| `--dg-navy` | `#111A34` | `#050A14` | Confianza y contraste estructural. |
| `--dg-accent` | `#6448EA` | `#A595FF` | CTA y decisión principal. |
| `--dg-cyan` | `#22BED1` | `#43DEEA` | ADA. |
| `--dg-coral` | `#FF6B5F` | `#FF8077` | Cuidado, nunca CTA principal. |
| `--dg-green` | `#37B879` | `#63D59F` | Confirmación. |
| `--dg-gold` | `#F4C650` | `#FFD477` | Logro, uso restringido. |

Secciones y cards conservan su posición. Sus superficies pasan a ser opacas, con borde de 1 px, radio de 8 px y una sola sombra suave. El nav sticky puede mantener blur, pero con una base suficientemente opaca y sin apilar transparencias claras.

## Componentes

| Componente | Tratamiento visual | Estructura preservada |
| --- | --- | --- |
| Nav | Barra ligera, borde discreto y progreso violeta. | Logo, links, tema, CTA y comportamiento scroll. |
| Botón primario | Violeta sólido, texto blanco, radio 12 px y respuesta inmediata. | Copy, icono y destino. |
| Botón secundario | Superficie elevada, borde fino e ink. | Copy, icono y destino. |
| Kicker | Label sin cápsula dominante, con marcador breve. | Copy y posición. |
| Card | Superficie opaca, borde fino, radio 8 px, sombra suave. | Todas las grids y contenido interno. |
| Icono | Placa compacta de 42–46 px, radio 12–14 px, color semántico y pictograma lineal. | Iconos y orden existentes. |
| Acordeón/cita | Divisor claro e índice/regla semántica, sin gradiente expansivo. | Preguntas, copy y apertura actual. |

## Auditoría fuente → artefacto

| Fuente | Cobertura |
| --- | --- |
| `00-context/digizen-copy-ola.md` | Sin cambios; esta fase no altera copy. |
| Wireframe y build Angular | Preservados: sin cambios de diagramación, estructura, CTA ni interacción. |
| `digizen-ada-proposal-v05-mision-clara-2026-08-25.html` | Se toman paleta fría, materiales, bordes, sombras, iconos y tipografía; no se toma su arquitectura ni copy. |

### Evaluación — Fase 1, ronda 1

| Lente | Puntaje | Objeciones |
| --- | --- | --- |
| Purista | 4.5/5 | Mantener el color auxiliar solo en funciones semánticas. |
| Arquitecto de Sistemas | 4.7/5 | Sustituir hardcodeados equivalentes por estos tokens al construir. |
| Guardián de Lectura | 4.6/5 | Verificar contraste de la línea gris del H2 en móvil. |

**Puntaje ponderado:** 4.6 / 5  
**Resultado:** aprobado internamente.
