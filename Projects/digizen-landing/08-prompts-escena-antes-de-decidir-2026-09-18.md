# Escena "Antes de decidir" · prompts de reemplazo (2026-09-18)

Sustituye `scenes/dg-scene-a05-criterion-mission.png`.
Contenedor actual: `<figure class="dg-media aspect-[4/3]">` → **4:3 horizontal**.
(La imagen actual mide 1184×672, que es 16:9, así que hoy se recorta. Al entregar la nueva
se ajusta el contenedor a la proporción real, como se hizo en presencia y seguridad.)

## Por qué se reemplaza

El copy de la sección le habla al padre y le pide que pruebe él:

> *"Y la prueba no te la pedimos por fe: **habla TÚ con ADA primero**. Interrógala. Trata
> de sacarla de sus reglas. Pregúntale lo que un niño le preguntaría… Nadie más en este
> mercado te deja **auditar a la IA de tu hijo antes de pagar**."*

La imagen actual muestra a **un adolescente** con el celular y un mapa de tarjetas
flotantes. El protagonista está equivocado: sale el hijo donde el texto dice "tú".

## Quién aparece: el papá, solo

Recuento del set con las escenas nuevas ya colocadas:

| Escena | Quién |
|---|---|
| Hero, CTA "¿Ya viste suficiente?" | papá + hijo |
| Beat 1 | **mamá sola** |
| Beat 2 (cena), Presencia | mamá + hijo |
| Seguridad | papá + hija |
| CTA final | mamá + hija |

Hay una madre sola y ningún padre solo. Va aquí, y además una figura única rompe la
seriación de "adulto + adolescente" que ya tienen cinco escenas seguidas.

## Sin íconos flotantes

La sección de seguridad ya los usa y ahí traducen sus cuatro tarjetas. Aquí no hay nada
que traducir: el asunto es un padre poniendo a prueba algo. Tarjetas flotando serían
adorno, y repetirían el recurso de la escena anterior.

---

## OPCIÓN 1 · El papá interroga a ADA, con burbujas y mesa de trabajo (recomendada)

```
Scene: a Mexican father in his forties sits alone at a small home desk in the evening,
leaning forward over the phone held in both hands, typing with his thumbs. His expression
is the specific one of someone testing something and starting to be convinced against his
own expectations: eyebrows slightly raised, the beginning of a surprised half-smile, fully
absorbed. He is alone; no teenager is present.

Two or three soft rounded chat bubbles rise from the phone into the air beside him,
painted into the artwork with the same visible brush texture as the rest — one bubble
tilted toward him and the others away, so they read as a back-and-forth conversation. The
bubbles are empty: no letters, no words, no readable text of any kind, only clean painted
shapes in violet and cyan with a soft glow.

Beside the phone on the desk lie a spiral notebook open to a page of handwritten marks and
a pen he has just put down, a pair of reading glasses, and a mug of coffee that has gone
cold. Nothing in the scene carries readable text: the notebook shows only the rhythm of
handwriting, never actual letters or words, and there are no books with titles on their
spines. A lamp is on and the rest of the house is quiet. Medium close shot, framed tight
on him, his hands and the desk surface.
```

**Por qué funciona:** la escena es *él probando*, que es lo que pide el copy. La expresión
hace el trabajo emocional —no es un padre preocupado, es uno que vino a desconfiar y se
está quedando— y los objetos cuentan la auditoría sin una sola palabra escrita: la libreta
dice que lleva rato, los lentes que se puso a leer con atención, el café frío cuánto tiempo.

**Por qué sin libros:** los lomos con títulos son una trampa conocida de estos modelos —
salen con letras inventadas y deformes, y el canon prohíbe texto legible. Además un padre
rodeado de manuales de IA deja de ser el lector de esta landing, que desconfía pero no
investiga.

**Por qué plano cerrado:** la escena de seguridad ya es mesa + dispositivo en plano abierto
de habitación. El encuadre corto es lo que evita que se parezcan.

## OPCIÓN 2 · El papá audita en la laptop

```
Scene: a Mexican father in his forties sits alone at the dining table at night with an open
laptop, one hand on the trackpad and the other holding his chin, leaning in to read. His
expression is deliberate and evaluating — he is auditing something, not browsing — with the
first hint of a satisfied nod. He is alone; no teenager is present. A cooling cup of coffee
and a notebook sit beside the laptop. The laptop is solid and opaque, its lid and back
completely non-transparent, its screen showing only soft glow and reflection with nothing
readable on it. Quiet evening light in an ordinary lived-in Mexican home.
```

**Por qué funciona:** la laptop y la libreta dicen "auditoría" mejor que un celular; se lee
como alguien que se sentó a revisar en serio, no a curiosear.

**Su riesgo:** la sección de seguridad ya tiene una laptop. Dos laptops en escenas cercanas
empiezan a parecerse, que es justo lo que corregimos. Si va esta, conviene que el encuadre
sea más cerrado que el de seguridad — plano medio corto, no plano de habitación.

---

## Recomendación

**La 1.** El celular lo diferencia de la escena de seguridad, que ya tiene laptop y plano
abierto; y la sección de abajo ofrece recibir el acceso por WhatsApp, así que un padre
probando desde el teléfono conecta con lo que va a hacer al llenar el formulario.

## Sobre el estilo

Las dos últimas escenas se parecían entre sí por tres cosas a la vez: mismo halo saturado,
misma paleta y mismo encuadre de adulto+adolescente sentados. Aquí ya cambian el número de
figuras y el momento del día. Para el halo, mantener la intensidad **baja** de la última
generación de seguridad —aire blanco, pinceladas que retroceden— y no volver al bloque
denso de la primera.


---

# Bloque de estilo para ESTA escena · paleta pálida del hero

El halo saturado violeta/azul es el de las escenas de seguridad y presencia. Aquí se pide
el tratamiento de las primeras escenas (`a01-hero`, `a03-cena`): barridos amplios,
translúcidos y desaturados que **retroceden** en vez de competir con la figura.

Sustituye la cláusula de `Background:` del bloque canónico por esta:

```
Style: modern photo-illustration — faces and skin read with real photographic quality and
detail (sharp, lifelike, believable human likeness, natural skin texture and lighting),
intervened with visible painterly brush strokes: thick directional strokes in the hair,
visible loose brush marks and texture breaks in the clothing fabric, crisp dark contour
accents. Background: an off-white painted canvas covered in broad, soft, translucent brush
sweeps in pale sky blue, mint green, pale coral and soft lavender — washed out and low in
saturation, with feathered edges that blend into the white, so the background recedes into
atmosphere and never competes with the figure. No dense block of saturated colour, no hard
edged paint slabs, no vivid impasto halo behind him. The painted chat bubbles are the most
saturated thing in the picture and should stand out against that pale ground.
Composition: the figure fits completely within the frame with comfortable margin on all
sides — no cropped limbs, nothing bleeding off any edge. No readable text, no logos, no
locks, no surveillance icons, no melodrama, no 3D render, no stock photo look, no smooth
vector look, no ADA, no second mentor figure, no ghost or spirit presence.
```

**Los negativos son los que hacen el trabajo.** `no dense block of saturated colour`,
`no hard edged paint slabs`, `no vivid impasto halo` — sin esas tres frases el modelo
vuelve solo al bloque violeta, porque es lo que "multicolor halo" le sugiere.

Y la última frase invierte la jerarquía a propósito: con el fondo pálido, **las burbujas
pasan a ser el elemento más saturado**, así que se vuelven el foco en vez de perderse.
