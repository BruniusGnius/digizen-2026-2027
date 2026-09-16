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
