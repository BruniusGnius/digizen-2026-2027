# Origen de estas skills

- Fuente: https://github.com/greensock/gsap-skills (repositorio oficial de GreenSock), carpeta `skills/`.
- Commit: `aed9cfd` · copiado el 2026-09-26.
- Licencia: MIT (ver `LICENSE` en esta carpeta).
- Los archivos `*/SKILL.md` y `llms.txt` son copia exacta, sin modificar. Para actualizarlos, vuelve a copiar desde el repo; no los edites aquí.

## Qué skill abrir

| Skill | Cuándo |
|---|---|
| `gsap-core/SKILL.md` | Tweens, eases, stagger, `gsap.matchMedia()` (breakpoints y reduced motion). |
| `gsap-timeline/SKILL.md` | Secuencias, position parameter, labels, `defaults`. |
| `gsap-scrolltrigger/SKILL.md` | Pin, scrub, snap, horizontal (`containerAnimation`), batch, refresh. |
| `gsap-plugins/SKILL.md` | SplitText, ScrollSmoother, ScrollTo, Flip, CustomEase, GSDevTools. |
| `gsap-performance/SKILL.md` | Transforms/opacity, `will-change`, rendimiento de ScrollTrigger. |
| `gsap-utils/SKILL.md` | `clamp`, `mapRange`, `toArray`, `snap`, `wrap`. |
| `gsap-frameworks/SKILL.md` | Vue, Nuxt, Svelte (no cubre Angular). |
| `gsap-react/SKILL.md` | React/Next (`useGSAP`). |

## Notas locales (revisión del 2026-09-26)

- **Bug en el ejemplo horizontal** de `gsap-scrolltrigger/SKILL.md`: usa `Max.max` (no existe; es `Math.max`) y asigna a `xPercent` un valor calculado en píxeles. Tomar el patrón, no copiar el código tal cual.
- **Reduced motion:** `gsap-core` sugiere `duration: 0` cuando `reduceMotion` es verdadero. En los proyectos de este vault manda la regla del usuario: degradar (crossfades cortos, sin pin), nunca cancelar.
- **`autoAlpha`:** oculta con `visibility: hidden`, lo que saca el elemento del árbol de accesibilidad. Úsalo en capas decorativas; para texto de lectura en paradas pineadas prefiere `opacity` + `pointer-events`, para que un lector de pantalla pueda alcanzarlo.
