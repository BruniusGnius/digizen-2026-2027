# Metaprompt — Digizen Landing B-v3

Pega este archivo completo como primer mensaje de una conversación nueva. Da contexto
autocontenido: no asumas nada de una conversación anterior sobre este proyecto.

## 0. Antes de responder nada

1. Lee `AGENTS.md` en la raíz del vault (ya se te habrá cargado como instrucción de
   proyecto si trabajas dentro de este repo). Contiene una regla no negociable: si vas a
   construir/rediseñar/iterar una landing, primero lees `Skills/landing-builder/SKILL.md`
   **completo**, y sigues su proceso de 3 fases con gates de aprobación. No lo resumas de
   memoria si ya lo leíste antes — vuelve a abrirlo.
2. Ese mismo skill te pide leer `Skills/apple-design/SKILL.md` completo antes de la Fase 1.
3. **Regla dura, sin excepción:** nunca modifiques `Projects/digizen-landing` (versión A) ni
   `Projects/digizen-landing-b` (el original generado con Codex). Este proyecto nuevo vive en
   `Projects/digizen-landing-b-v3/` y no toca esas carpetas para nada, ni de lectura casual
   que derive en edición.

## 1. Qué es esto

Una tercera iteración de la landing de Digizen (producto de Gnius Club — mentor de IA para
que adolescentes entrenen criterio digital). Hubo una v1 (Codex, descartada por diseño), una
v2 (Angular, con buenas decisiones de animación pero mucha fricción de proceso), y ahora esta
v3 busca ser la versión "pro": más simple, más eficiente de construir, con las lecciones de
las dos iteraciones anteriores ya incorporadas de inicio en vez de redescubrirlas a las malas.

- Nombre de proyecto: `digizen-landing-b-v3`
- Carpeta: `Projects/digizen-landing-b-v3/` (ya tiene `00-context/` con este archivo y el
  copy — ver abajo)

## 2. Copy fuente (ya resuelto — no perder tiempo re-preguntando)

Ya está guardado, literal, en `Projects/digizen-landing-b-v3/00-context/COPY-PUBLICADO.md`.
Se extrajo del sitio renderizado en
`Digizen-Cinco-Creencias-Diseno-2026-09-22/sitio/dist/index.html`, que el usuario señaló
como más completo que el `COPY-PUBLICADO.md` de iteraciones previas (incluye el FAQ con
respuestas completas). Trátalo como fuente de verdad literal — no omitir, resumir,
parafrasear ni inventar, por la regla de fidelidad del landing-builder.

## 3. Insumos de sistema de diseño (para Fase 0.2 / Fase 1)

Existen estos insumos previos en el vault, todos opcionales como punto de partida (nunca
copiar 1:1 sin evaluar — eso ya lo dice `phases/01-design-system.md`):

- `creador de landings/insumos/estilo o sistema de diseño/Tipografía esencial.html` —
  catálogo de composiciones tipográficas. El usuario lo señaló explícitamente como el
  insumo para desarrollar las "capas" tipográficas de este proyecto. Ábrelo y léelo.
- `creador de landings/insumos/sistema-diseno-refinado/tokens.css` + `preview.html` — un
  sistema de diseño refinado de una iteración previa; revisar si aplica.
- `Projects/digizen-landing-b-v2/DIGIZEN — Sistema tipográfico.html` y
  `Projects/digizen-landing-b-v2/Scroll Patterns — Especimen Completo.html` — catálogo de
  ~49 composiciones tipográficas editoriales y 14 patrones de animación GSAP con código de
  referencia, usados en la v2. Siguen siendo un vocabulario válido de composición/animación.
- `Projects/digizen-landing-b-v2/` en general (código Angular) — **no lo copies como base de
  código**, pero es la referencia de qué ya se validó con el usuario (ver sección 5). Si
  necesitas ver cómo se resolvió algo concreto, es legítimo abrirlo y leerlo.
- **Imágenes/escenas ya generadas**, en
  `Projects/digizen-landing-b-v2/angular-build/public/assets/scenes/`:
  `01-dinner.webp`, `02-facial-recognition.webp` (+ `-alt`), `03-eyes.webp`,
  `03-eyes-wide.webp`, `04-shield.webp`, `05-crossing.webp` (+ `-alt`),
  `06-rules.webp` (+ `-alt`), `07-together-father-son.webp`,
  `07-together-mother-daughter.webp`, `08-autonomy-father.webp`,
  `08-autonomy-mother.webp`. Reutilizables para B-v3 — no hace falta regenerarlas de cero
  salvo que el usuario pida algo distinto.
  **Ojo:** el mapeo capítulo→imagen que usó la v2 (en su `content.ts`) **no coincide 1:1**
  con el de la referencia `dist/index.html` documentada en `VISION-NARRATIVA.md` sección
  1.1 (ahí, por ejemplo, el capítulo 02 sella con una imagen de "candados", y en la v2 ese
  mismo capítulo usa `02-facial-recognition.webp` — temas relacionados pero no la misma
  imagen). Además la v2 le puso imagen a capítulos que, según la regla de la sección 1.1
  (la imagen solo aparece donde hay un concepto que sellar), probablemente no deberían
  llevarla. **No asumas el mapeo de la v2 — decide la asignación final en Fase 2**, usando
  la tabla de la sección 1.1 de `VISION-NARRATIVA.md` como referencia de qué capítulos sí
  llevan imagen y en qué punto de la sección va (al final del argumento, no al inicio).

## 4. Stack técnico

- **Composición: Tailwind CSS.** Esto es una restricción fija del usuario, no se discute en
  Fase 1.
- **Framework de implementación: déjalo abierto para la Fase 3**, pero ten en cuenta esta
  recomendación surgida de la v2: el ciclo de vida de Angular + su dev server (sobre todo en
  volúmenes externos, ver sección 6) hizo muy lento y frágil iterar timing de animación
  GSAP/ScrollTrigger. Una alternativa real: prototipar cada sección como HTML plano +
  GSAP (mismo formato que `Scroll Patterns — Especimen Completo.html`) hasta que la
  composición y el timing se sientan bien — iteración instantánea, sin rebuilds — y recién
  después portarlo a un framework (Angular u otro) si hace falta para producción. Coméntaselo
  al usuario como opción en la Fase 3, no lo decidas solo.

## 5. Visión narrativa del usuario (insumo directo para Fase 1 y Fase 2)

Ya está desarrollada completa en `00-context/VISION-NARRATIVA.md` — ábrela y léela entera
antes de la Fase 1, no la resumas de este párrafo. Contiene:
- El principio rector (texto como protagonista) y sus consecuencias prácticas.
- Los dos registros tipográficos (Registro A "amable/cálido" y Registro B "brutalista pero
  estético", reservado para momentos de golpe/tensión/reflexión) con criterios de cómo
  reconocer una frase candidata a Registro B dentro del copy.
- El patrón de 4 partes del capítulo 1 (título → contenido → puente semibrutalista → golpe
  lapidario), presentado explícitamente como **hipótesis a explorar, no plantilla fija**.
- Un **mapeo borrador capítulo por capítulo** (los 12) con candidatas a Registro B ya
  identificadas contra el copy real de `COPY-PUBLICADO.md` — algunos capítulos no siguen el
  patrón de 4 partes en absoluto (cap. 2 es eco+respuesta x4, cap. 9 no tiene golpe, cap. 10
  tiene dos golpes). Ese mapeo es un borrador de Claude, no algo que el usuario ya aprobó
  línea por línea — coméntalo con él antes de darlo por definitivo en Fase 2.
- Preguntas abiertas para Fase 1 (sección 5 de ese documento): si hace falta un tercer
  tratamiento tipográfico para datos/cifras y para copy de venta punchy, y cómo tratar
  visualmente un capítulo sin golpe de Registro B.

**Regla de arquitectura de animación, no negociable (sección 6 de `VISION-NARRATIVA.md`):**
la landing es **un recorrido continuo de scroll resuelto con GSAP + ScrollTrigger**, donde
**Pin + Scrub es el patrón dominante** — las secciones son paradas ("escalas") dentro de ese
recorrido, congeladas y con su contenido atado al scroll (reversible), no bloques que solo
hacen fade-in al llegar. Es el modelo del capítulo 01 de la v2 (4 pantallas en un mismo pin,
con `snap`) generalizado a toda la landing. Los otros 13 patrones del catálogo de
`Scroll Patterns — Especimen Completo.html` se usan dentro de esa lógica cuando una sección
puntual lo pida, no como alternativas sueltas. Esto refuerza la recomendación de la sección
4 (prototipar en HTML+GSAP plano primero): si casi toda la landing depende de pines
scrub sincronizados, la fricción de iterar timing dentro del ciclo de vida de un framework
pesa todavía más que en la v2.

## 6. Lecciones técnicas validadas en la v2 (úsalas, no las redescubras)

### Animación / GSAP ScrollTrigger
- **Secuencia cinematográfica de un solo uso** (ej. un hero: zoom-out extremo → pausa real →
  disolvencia → texto): pin + UNA sola timeline **autoplay disparada por `onEnter`/
  `onEnterBack`, en tiempo real (sin scrub)**. Así el orden queda garantizado sin depender de
  la velocidad de scroll del usuario. No uses `scrub` para esto — con inercia (`scrub:0.6` o
  similar), el scroll rápido puede adelantarse a que la fase anterior termine visualmente,
  y dos fases se solapan.
- **Secuencia de LECTURA con varias pantallas dentro de un mismo pin** (ej. título → viñetas
  → frase puente → revelación): usar **`scrub` real atado a la posición de scroll**
  (`scrub: 0.4` + `animation: timeline` + `snap` a paradas). Esto es bidireccional por
  diseño: revertir el scroll revierte la lámina. **Nunca** un disparo de una sola vez
  (`onEnter` no reversible) para contenido que el usuario espera poder regresar scrolleando
  hacia arriba — se detectó y corrigió este error explícitamente en la v2.
- Pines de distancia de scroll muy larga (varias pantallas de alto) son frágiles: un
  `ScrollTrigger.refresh()` tardío (por fonts o imágenes que cargan después) puede
  desincronizar el mapeo scroll↔timeline y dejar un panel atorado en opacidad 0 de forma
  intermitente. Prefiere segmentos de pin más cortos, o fuerza un refresh explícito después
  de que carguen los assets pesados de esa sección.
- `prefers-reduced-motion: reduce`: **nunca cancelar el movimiento, solo degradarlo**
  (regla de proyecto explícita del usuario). Para secuencias que normalmente van pineadas,
  en este modo **no uses pin** — conviértelas en contenido de flujo normal (stacking
  vertical con `position: static`) con reveals independientes por bloque. Una animación sin
  pin pero cuyo timing depende de que el usuario se quede quieto en una pantalla
  (`toggleActions` sin pin, con crossfades por tiempo) falla: nada lo detiene ahí, y el
  contenido nunca termina de revelarse antes de que el scroll normal lo saque de vista.

### Tipografía / color
- **Nunca gris** (un color tipo `--muted`) en texto romano (no itálico) pequeño o cercano al
  tamaño de body — pierde legibilidad y "rasgos tipográficos" (queja textual del usuario).
  Usar el color de tinta principal ahí.
- El peso base de la tipografía visible debe estar **arriba de Regular, tirando a Medium**
  — nunca 400 como default.
- Fuentes variables de alto contraste de trazo (ej. Playfair Display itálica) pueden
  necesitar pesos bastante altos (700+) para que el cambio de peso realmente se perciba — no
  asumas que 500–600 ya se lee como "medium" en ese tipo de letra.
- Cuidado con dobles sistemas de numeración compitiendo visualmente en la misma pantalla (ej.
  un numeral de capítulo grande tipo "01" + una lista numerada 01–05 justo debajo) — genera
  confusión y no aporta si no está en el copy. El usuario terminó quitando los numerales de
  capítulo por completo en la v2.

### Fidelidad de copy (ya lo dice el skill, remarcado porque se violó varias veces en la v2)
- Compara cada título/subtítulo/bullet contra el heading y el texto REAL del copy fuente. En
  la v2 se inventaron subtítulos/"eyebrows" que no existían en la fuente (los headings del
  copy son de una sola línea) — no repetir ese patrón.
- Nunca colapsar una lista de viñetas del copy en un párrafo corrido resumido — cada viñeta
  va completa, literal. También pasó en la v2 (la sección de inscripción/precios).
- Antes de cada gate del landing-builder, corre de verdad la auditoría fuente → artefacto
  que pide el skill — no la saltes por ir más rápido.

### Entorno de este vault
- Si el proyecto vive en este volumen externo (`/Volumes/SACHI/...`) y usas un dev server con
  file-watching (Angular, Vite, etc.), no confíes en que detecte cambios de archivo — puede
  no reconstruir. Para verificar un cambio, detén y vuelve a levantar el servidor de preview,
  no solo esperes.
- Al verificar animaciones scroll-driven en un navegador automatizado: haz scroll real
  (gradual) en vez de saltos grandes con `scrollTo`, y espera a que `document.fonts.ready` se
  resuelva antes de medir posiciones — los saltos de layout por fuentes cargando tarde
  produjeron mediciones falsas repetidamente en la v2.

## 7. Qué se espera de ti ahora mismo

No es momento de escribir código. Sigue el proceso del skill:

1. Confirma que leíste `AGENTS.md`, `Skills/landing-builder/SKILL.md` completo y
   `Skills/apple-design/SKILL.md` completo.
2. Fase 0: el copy y el nombre de proyecto ya están resueltos (secciones 1–2 de este
   archivo) — no se lo vuelvas a preguntar al usuario. Sí hace falta el cuestionario de
   contexto de `0.3` (público objetivo, tono de marca en adjetivos, objetivo de conversión,
   restricciones fijas — Tailwind ya es una restricción fija, ver sección 4) y confirmar si
   usa alguno de los insumos de la sección 3 como sistema previo a refinar. Crea
   `project.config.md` con todo esto.
3. Detente en el primer gate (fin de Fase 1 — sistema de diseño) y espera aprobación
   explícita del usuario antes de pasar a wireframe. No avances fases por tu cuenta.
