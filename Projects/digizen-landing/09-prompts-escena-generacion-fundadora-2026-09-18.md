# Escena "Generación Fundadora" · prompt de reemplazo (2026-09-18)

Sustituye `scenes/dg-scene-a08-founder-start.png` (1184×672, ~16:9).
El contenedor (`.dg-founder-media`) no fija proporción: la imagen se muestra a su relación
natural, así que no hay recorte que cuidar. Mantener ~16:9 horizontal.

## Qué se conserva y qué cambia

La escena actual —adulto y adolescente frente a una laptop, cómplices— **funciona** y se
conserva. Cambian tres cosas:

1. **El gesto**: de mirar la pantalla juntos a un *choca esos cinco*. El bloque habla de
   empezar hoy y de ser los primeros; el gesto celebra una decisión, no la contempla.
2. **El fondo**: hoy compite con las figuras. Tiene dos cuadros enmarcados, una puerta
   abierta a un jardín con palmera y buganvilia, una planta grande, una mochila y una taza.
   Se diluye.
3. **La laptop**: el canon registra que esta imagen se descartó porque **el respaldo salió
   transparente**. Va negativo explícito.

## Quién aparece: mamá con su hija adolescente

| Pareja | Veces en el set |
|---|---|
| papá + hijo | **3** (hero, esta escena, CTA "¿Ya viste suficiente?") |
| mamá + hijo | 2 (cena, presencia) |
| mamá + hija | 1 (CTA final) |
| papá + hija | 1 (seguridad) |
| mamá sola / papá solo | 1 y 1 |

Poner aquí mamá + hija baja el papá+hijo a dos y equilibra el conjunto.

---

## Prompt

```
Scene: a Mexican mother and her teenage daughter sit side by side at the dining table with
an open laptop in front of them, caught in the middle of a high five — palms meeting above
the keyboard, both of them laughing, shoulders lifted, the easy delight of two people who
have just decided something together and are pleased about it. Their hands are clearly
drawn, fingers natural and complete, palms meeting cleanly.

The laptop is solid and opaque, its lid and back completely non-transparent, its screen
showing only a soft glow and reflection with nothing readable on it.

The background is kept deliberately simple and airy: a plain wall, a single small plant,
and nothing else — no framed pictures, no open doorway, no garden, no backpack, no
clutter. The room reads as calm and uncluttered so that the two figures and their meeting
hands are the only thing the eye goes to. Warm afternoon light. Mother and daughter have
visibly different skin tones within the same family.
```

## Riesgos a vigilar

- **Las manos.** Dos palmas encontrándose es de lo más difícil para estos modelos: salen
  dedos de más, fusionados o en ángulos imposibles. El prompt lo pide explícito, pero es lo
  primero que hay que revisar al ampliar la imagen. Si falla dos veces seguidas, la
  alternativa segura es **el instante justo después**: las dos riendo con las manos ya
  bajando, que cuenta lo mismo sin el encuentro de palmas.
- **El fondo vuelve a llenarse.** Estos modelos añaden objetos por su cuenta para "componer".
  Por eso el prompt lista lo prohibido uno por uno en vez de pedir "fondo simple".
- **La laptop transparente**, que es el fallo documentado de la versión actual.
