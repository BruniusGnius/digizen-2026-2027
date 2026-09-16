# DIGIZEN · Plan de escenas y metaprompts

## Estado por escena (revisión 2026-09-15, ronda v02 sin ADA)

| Sección landing | Copy real de la sección | Imagen actual | Veredicto | Acción |
|---|---|---|---|---|
| Hero (`hero-title`) | "Le quitaste el celular… con el tuyo en la mano" — hipocresía del padre, no reflexión del hijo solo | `dg-scene-a01-hero-phone-hypocrisy.png` | **Resuelto 2026-09-15** — papá absorto en su propio celular sin ver a su hijo, hijo con brazos cruzados y fastidio genuino, tensión sin pelea ni gritos | — |
| Beat 1 "Nadie te enseñó esto" | El adulto también anda pegado a su celular ("tú también andas pegado al tuyo") | `dg-scene-a02-parent-phone-attachment.png` | **Corregido 2026-09-15** — la versión anterior mostraba solo alivio/celular boca abajo; no comunicaba que ella también tiene apego al dispositivo. Nueva versión: mamá con ambas manos en el celular, atención total, justo antes del momento de reconocimiento | — |
| Beat 2 "Lo que de verdad duele" | Cerca en cuerpo, lejos en conexión por el celular | `dg-scene-a03-mother-son-dinner.png` | **Resuelto 2026-09-15 (v11)** — mamá e hijo sentados cerca; el celular es la única barrera. Ida y vuelta de estilo: se probaron variantes con paleta cálida/velo y trazo casi fotográfico que se alejaban del canon (`digizen-v05-mision-clara-asset-gpt-image-2-v01.png`); la clave fue quitar "over a photographic base" del prompt — la canon es pintura digital desde cero, no foto retocada | — |
| Beat 3 "Bloquear no te lo devuelve" | Bloquear solo pospone la decisión | placeholder "reloj reactivo al scroll" (con lógica en app.ts) | Ese slot es un componente interactivo planeado, no una ilustración — se revirtió el reemplazo accidental por a04 | Mantener como placeholder de reloj; no es un slot de imagen IA |
| Beat 4 "Otro camino" | Criterio que la pantalla no puede comprar | diagrama CSS `dg-criteria-visual` (interactivo, `app.ts:288`) | **No funciona**, hay que sustituirlo por una imagen | Diseñar nueva escena + decidir si se conserva la interacción o se vuelve estática |
| "Seguridad por diseño" / ADA | Privacidad, familia en el circuito, IA con reglas | a06 ai-rules-family | Funciona, con fix de orientación (imagen volteada con CSS `.dg-media--flip` para que el adolescente mire hacia el texto) | Aplicado |
| "Antes de decidir" (ADA + guardas) | — | a05 criterion-mission | No conectaba con esta sección | Redefinir o remover |
| Beat 6 "Presencia, no vigilancia" | Pacto de acompañamiento | a07 pinky-promise | Sin feedback explícito — pendiente de revisión | — |
| Generación Fundadora | Familia empieza hoy | a08 founder-start | Concepto correcto, ejecución con error (respaldo del laptop se ve transparente, el monitor no debería verse desde atrás) | Regenerar con encuadre que evite el sesgo del laptop |
| CTA (decision-portrait, `cta-parent-cutout-v01.png`) | — | asset placeholder existente | Pendiente de generar | Definir escena |

**Reglas de proceso adoptadas:** una imagen por escena (sin variantes mobile/desktop generadas por IA — el recorte de formato se hace en Photoshop); sin caption/pie de foto visible (`data-label` solo para placeholders temporales); ir imagen por imagen con aprobación antes de continuar; no reemplazar componentes interactivos (JS/scroll) por imágenes estáticas sin confirmar.


> Estado: propuesta para revision antes de generar imagenes.  
> Fuente canon prioritaria: `digizen-v05-mision-clara-image-canon-2026-09-15.md`.  
> Autor/fuente operativa del canon: `digibrand`, instancia que trabajo el canon visual de DIGIZEN V05 Mision Clara en `operations/digizen/product-design/docs/digizen-v05-mision-clara-image-canon-2026-09-15.md`.  
> Copia local de trabajo: `Projects/digizen-landing/digizen-v05-mision-clara-image-canon-2026-09-15.md`.  
> Fuentes de contenido y marca: `project.config.md`, `00-context/digizen-copy-ola.md`, `00-context/digizen-ada-proposal-v05-mision-clara-2026-08-25.html`, `01-design-system.md`, `03-asset-manifest.md`, brief revamp logo Digizen.

## Canon visual operativo

- Centro emocional: "Estoy pensando mejor mi vida digital con una guia que me acompana."
- Tesis: acompanamiento inteligente sin vigilancia; criterio y autonomia, nunca control.
- **DECISION 2026-09-15: ADA no aparece en las ilustraciones.** Las primeras generaciones (hero, parent-relief, dinner-distance) mostraron a ADA como figura femenina azul, translucida y gigante, con lectura no deseada de "diosa"/aparicion religiosa — ruido visual y fuera de tesis. Se descarta el "triangulo" adolescente+ADA+decision como composicion; el par visual pasa a ser persona(s) + decision digital, con ADA representada solo por iconografia abstracta (burbujas, simbolos) si acaso, nunca como figura humana/mentora. ADA como personaje (UI/chat del producto) se maneja aparte, fuera de estas ilustraciones.
- Adolescente: secundaria/prepa temprana, rasgos naturales, hoodie o ropa casual amplia, gesto tranquilo e introspectivo, mano cerca del rostro, agencia visible.
- Tecnologia: celular cotidiano como punto de partida para pensar; no evidencia, no inspeccion, no chats completos, no datos intimos.
- Estilo: ilustracion premium de producto, semi-realista, editorial painterly, brochazos visibles, impasto controlado, dry-brush, capas acuareladas, luz limpia, fondos claros/cloud.
- No usar: 3D render, CGI plastico, clay toy, fotografia stock, hiperrealismo limpio, anime/cute, flat vector corporativo, cyberpunk, IA neon, robot, bot, androide.
- Semiotica prohibida: candados, escudos defensivos, ojos, huellas biometricas, miras, lupas, camaras, radares, dashboards de monitoreo, likes, fama, metricas, megafonos, birretes, pizarrones.
- Color: azul/cyan/teal dominantes; blanco/cloud para aire; coral, verde o gold solo como acentos suaves.

## Escenas propuestas

| Slot | Archivo destino sugerido | Ratio | Seccion | Escena |
|---|---|---:|---|---|
| A01 | `hero-teen-ada-reflection` | 4:5 + 16:9 | Hero | Adolescente reflexiona con celular cotidiano; ADA grande como guia suave; el conflicto del papa queda sugerido, no acusado. |
| A02 | `parent-relief-no-bad-parent` | 4:5 + 16:9 | Beat 1 | Adulto baja la guardia junto a un celular face down; alivio y humanidad, sin sermon. |
| A03 | `dinner-distance-phone` | 4:5 + 16:9 | Beat 2 | Cena familiar con distancia emocional: hijo presente pero absorbido; adulto intenta reconectar. |
| A04 | `crosswalk-digital-criterion` | 4:5 | Beat 3/4 | Metafora de cruce: adulto acompana a hijo a mirar ambos lados en una calle-digital suave. |
| A05 | `ada-criterion-mission-cover` | 16:10 | Beat 5 ADA | Portada de mision: adolescente + ADA + feed convertido en mapa de decision. |
| A06 | `ai-rules-family-loop` | 3:4 | Seguridad IA | IA con reglas: adolescente conserva privacidad; adulto ve avance suficiente sin inspeccionar. |
| A07 | `pinky-presence-promise` | 4:5 + posible transparente | Beat 6 | Meniques con liston sutil; pacto de acompanamiento, no romance ni infantilizacion. |
| A08 | `founder-start-today-family` | 16:9 | Oferta/cierre | Familia inicia hoy con una ruta clara; ADA como guia cercana, esperanza sin presion comercial. |

## Metaprompts high-fidelity

### A01 · Hero · `hero-teen-ada-reflection`

Premium editorial painterly illustration for Digizen, a Mexican / LatAm teenager in early secondary school sitting in a calm home environment, holding a smartphone as everyday context, thoughtful expression, hand near chin, hoodie texture with visible dry-brush strokes, subtle emotional tension without blame, a large soft translucent female mentor presence in blue and cyan beside the teen, ADA as conversational guide not robot, abstract app symbols for reflection and progress floating softly, cloud-white airy background, blue/cyan/teal dominant palette with tiny coral warmth, semi-realistic natural face, painterly impasto texture, watercolor-like translucent layers, clean light, gentle shadows, 4:5 portrait with safe negative space for landing copy and adaptable 16:9 crop, 50mm editorial framing, eye-level, shallow atmospheric depth, no readable text, no brand logos, no locks, no shields, no eyes, no cameras, no biometric marks, no monitoring dashboard, no dark cyber aesthetic, no 3D render, no stock photo, no anime, no influencer pose, calm, competent, reflective, hopeful.

### A02 · Beat 1 · `parent-relief-no-bad-parent`

Premium semi-realistic painterly illustration, Mexican / LatAm parent at a kitchen table after a difficult screen-time night, shoulders softening, one hand near a phone placed face down, expression shifting from guilt to relief, quiet domestic morning, ceramic mug, notebook, cotton hoodie, lived-in but clean home, emotional thesis: not a bad parent, just no manual, cloud-white and pale blue-gray atmosphere, tiny cyan guidance accent, soft coral human warmth, visible brush strokes, controlled impasto, dry-brush fabric and table texture, watercolor edge softness, 4:5 portrait with calm empty space, 70mm intimate framing, natural side light, gentle shadows, no child confrontation, no scolding, no surveillance feeling, no locks, no eyes, no cameras, no warning UI, no school props, no text, no stock-photo realism, no glossy 3D, compassionate, grounded, serene.

### A03 · Beat 2 · `dinner-distance-phone`

Editorial painterly illustration for a family edtech product, Mexican / LatAm family dinner table, adolescent present but emotionally distant, eyes lowered toward a phone near the table, parent across from them trying gently to catch their gaze, quiet pause, not accusatory, food half-served, glasses, warm household details, visible emotional space between characters, no human mentor figure, only soft ambient warm bokeh in the background, 4:3 cinematic framing, 35mm eye-level, warm dining light mixed with cool phone glow, muted off-white, blue-gray, teal, soft coral skin warmth, brushy semi-realistic faces, dry-brush clothing, painterly ceramic and wood textures, no readable app UI, no notifications, no metrics, no monitoring dashboard, no tears, no melodrama, no locks, no cameras, no 3D render, no stock photo, no second mentor figure, no ghost or spirit presence, intimate, restrained, credible for Mexican parents.

### A04 · Beat 3/4 · `crosswalk-digital-criterion`

Poetic premium painterly illustration, parent and child standing together at a calm city crosswalk that subtly transforms into a soft digital decision path, parent gently indicating both directions, child looking up with agency, smartphone held casually not as problem evidence, road markings become luminous decision lines, feed fragments appear as abstract watercolor tiles dissolving into a legible path in the distance with no human figure inside the light, dawn light, cloud-white air, teal and blue guidance, violet reflection, tiny green confirmation, 3:4 vertical composition, 28mm mild wide framing, low-to-eye-level, visible brush strokes, controlled impasto, soft dry-brush pavement, no barriers, no police, no blocking, no locks, no shields, no cameras, no eyes, no warning signs, no robots, no classroom, no likes, no metrics, no text, no human silhouette in the light path, hopeful, lucid, future-opening.

### A05 · Beat 5 criterio · `criterion-mission-cover`

Premium product illustration in Digizen visual canon, Mexican / LatAm teenager in hoodie inside an airy cloud-white mission scene, smartphone in hand as everyday context, serene focused gesture, messy feed tiles reorganizing into an abstract map of decisions, no readable words, clean white card forms with fine pale borders, blue/cyan/teal dominant palette, coral dilemma accent, green progress accent, gold achievement speck, visible digital painterly brush strokes, impasto highlights, watercolor translucent UI layers, semi-realistic face, thoughtful hand-near-chin posture, 16:9 horizontal framing for landing/product module, 35mm slight top-down editorial angle, luminous clean studio-home light, gentle shadows, no mentor figure, no second person, no surveillance dashboard, no private chats, no locks, no eyes, no cameras, no circuit brain, no neon AI glow, no robot, no glossy 3D, no flat vector, confident, serene, useful.

### A06 · Seguridad IA · `ai-rules-family-loop`

Editorial painterly illustration about safe AI with rules and family in the loop, Mexican / LatAm adolescent in a calm private reflection space with smartphone, serene and focused, parent nearby seeing abstract progress and topic cards from a respectful distance, not reading the phone, privacy boundary shown through soft translucent watercolor panels between them, public rules represented as simple abstract white cards with no readable text, emotional tone: transparent safety and trust, 3:4 portrait, centered layered composition, cloud-white background, blue/cyan/teal palette, green confirmation, tiny coral care signal, visible brush strokes, controlled impasto, dry-brush clothing and soft paper textures, clean daylight, gentle shadows, no mentor figure, no second guiding presence, no locks, no defensive shields, no eyes, no cameras, no radar, no warning triangles, no code rain, no cyberpunk, no romance chatbot cues, no robot, no monitoring dashboard, reassuring, competent, calm for skeptical parents.

### A07 · Beat 6 · `pinky-presence-promise`

Close premium painterly illustration of a pinky promise between parent and child, two Mexican / LatAm hands connected by a thin soft ribbon in cyan-to-coral accent, gesture of accompaniment and trust, smartphone resting aside face down as context not evidence, subtle white agreement card edge with no readable text, warm domestic table, cloud-white airy background, tactile skin rendered semi-realistically with painterly brush strokes, woven ribbon texture, dry-brush highlights, controlled impasto, soft watercolor edges, 3:4 portrait with possible transparent-background variant, 85mm macro-style framing, shallow depth, warm natural light with cool cyan rim, no hearts, no glitter, no romance, no infantilization, no legal heaviness, no locks, no cameras, no eyes, no surveillance symbols, no text, emotional meaning: presence not vigilance, criterion not control, both on the same side.

### A08 · Oferta/cierre · `founder-start-today-family`

Hopeful Digizen painterly editorial illustration, bright Mexican / LatAm home morning, parent and adolescent looking together at a clean tablet or laptop showing only abstract mission path shapes, calm and supportive mood between them, no sales pressure, sense of starting today through open doorway, backpack ready, fresh light, family on the same side, white/cloud atmosphere, blue/cyan/teal dominant palette with violet reflection, green readiness and soft coral warmth, semi-realistic natural faces, contemporary casual clothes, visible brush strokes, controlled impasto, dry-brush fabric, watercolor UI layers, 16:9 landing composition, 35mm eye-level medium-wide framing, warm sunlight with cool ambient fill, gentle shadows, no mentor figure, no second guiding presence, no checkout UI, no credit cards, no readable text, no waiting room, no classroom, no locks, no shields, no cameras, no metrics, no likes, no robots, calm confidence, relief, future opening.

## Decisiones pendientes antes de generar

1. Confirmar si producimos 8 escenas o reducimos a 6 fusionando A02 con A01 y A08 con CTA/fundadores.
2. ~~Confirmar si ADA debe aparecer...~~ **Resuelto 2026-09-15: ADA no aparece en ninguna ilustracion.** Todos los metaprompts deben reescribirse quitando la figura de ADA; las 4 imagenes ya generadas (hero x2, parent-relief, dinner-distance) se descartan/regeneran sin ella.
3. Confirmar herramienta: el MCP Imagine.art no aparece disponible en esta sesion. OpenArt aparece como plugin instalable y menciona GPT Image 2, pero no esta instalado.
