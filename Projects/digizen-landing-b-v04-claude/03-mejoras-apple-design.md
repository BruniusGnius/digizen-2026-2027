---
project: digizen-landing-b-v04-claude
fase: 3 - build
documento: plan de mejoras con la skill apple-design (propuesta; no se aplica nada sin aprobación)
estado: aprobado A y B (2026-09-29); C descartado por ahora
fecha: 2026-09-29
---

# Plan de mejoras · apple-design

Revisión de `output-code/` contra los 11 principios de `Skills/apple-design/SKILL.md` y contra lo que ya dice el sistema de diseño aprobado. Regla que sigue vigente: **no se tocan las estaciones, los scrubs ni la forma de scrollear.**

## A. Lo que el sistema aprobado pide y todavía no está (corregir)

| # | Qué falta | Principio | Qué haría | Esfuerzo |
|---|---|---|---|---|
| A1 | **El FAQ abre y cierra de golpe.** El sistema dice «apertura con resorte crítico, que se puede interrumpir». | §3 interrumpibilidad, §4 resortes | Animar la altura de la respuesta con un resorte sin rebote; si se toca a medio camino, revierte desde donde está. El indicador gira con el mismo resorte. | bajo |
| A2 | **Los enlaces de texto no responden al tocar** (el sistema pide opacidad 0.7 en `pointerdown`). | §1 respuesta inmediata | Respuesta en `pointerdown` para enlaces, los botones del canal del formulario y la fila del FAQ. | bajo |
| A3 | **El diálogo de ADA aparece de golpe** y sin relación con el botón que lo abrió. | §7 consistencia espacial | Que emerja desde el botón que lo abrió (escala 0.96 → 1 + fundido, con resorte) y vuelva hacia él al cerrarse. Sigue apareciendo centrado. | bajo |

## B. Mejoras apple-design que recomiendo

| # | Mejora | Principio | Qué cambia para el usuario | Esfuerzo |
|---|---|---|---|---|
| B1 | **Resortes de verdad en lo que se toca.** Hoy botones, menú y diálogo usan curvas de duración fija. | §4 | Un token de resorte crítico (sin rebote) para todo lo interactivo: se siente más físico y siempre parte del estado actual. | bajo |
| B2 | **Cerrar el menú deslizándolo con el dedo.** | §2 manipulación directa, §5 velocidad, §6 resistencia | En móvil, el panel sigue al dedo 1:1; al soltarlo se cierra o se queda según la velocidad del gesto, y si se empuja hacia el lado cerrado ofrece resistencia progresiva. No toca el scroll de la página. | medio |
| B3 | **Tipografía óptica de Inter.** Inter tiene eje de tamaño óptico (14–32). | §9 tipografía por tamaño | Los golpes grandes usan la versión «display» de la fuente (más fina y compacta) y el cuerpo la de texto, automáticamente. Mismos tamaños. | bajo |
| B4 | **Números tabulares en precios y datos** («$4,990.», «$599.», «7 de cada 10»). | §9 | Cifras alineadas y del mismo ancho; se ven más limpias. | muy bajo |
| B5 | **Seguro de texto grande.** Las paradas miden un encuadre fijo; si alguien agranda el texto de su navegador, una parada podría no caber y cortarse. | §10 accesibilidad | Si el texto del usuario es más grande que el normal (o una parada no cabe), la página pasa sola al modo de flujo, sin pines. Para el resto, nada cambia. | medio |
| B6 | **Scrub más suave en las secuencias.** | §11 rendimiento | Decodificar cada cuadro antes de dibujarlo, para que el video con scroll no dé tirones en equipos medios. | bajo |
| B7 | **`will-change` solo mientras un pin está activo.** | §11 | Menos trabajo del navegador en las transiciones de cada parada, sin reservar memoria el resto del tiempo. | bajo |

## C. Opciones que cambian una regla aprobada (solo si las quieres)

| # | Opción | Principio | Choque |
|---|---|---|---|
| C1 | **Material translúcido detrás del logo flotante y del botón del menú** (una píldora con desenfoque) en lugar de la sombra sobre imágenes. | §8 materiales | El sistema dice «todo opaco, sin blur». |
| C2 | **Formulario de ADA como hoja inferior en móvil** (sube desde abajo y se cierra deslizando). | §2, §5, §7 | Pediste el modal al centro. |

## D. No recomiendo (cambiarían el scroll o las estaciones)

- Arrastrar el carrusel del cap. 02 o el mazo de tarjetas con el dedo.
- Scroll suavizado (ScrollSmoother) o inercia propia.

## E. Verificación (lo que falta para cerrar la fase)

Hasta ahora nada se ha visto en un navegador. Con tu permiso para abrir el navegador integrado:
1. Recorrido completo en desktop, tablet y móvil (paradas, scrubs, snap, logo, menú, formulario).
2. Movimiento reducido (modo de flujo).
3. Conexión limitada (4G y 3G rápida) para confirmar que cada secuencia y escena llega antes de su parada.
4. Rendimiento y accesibilidad (Lighthouse), y la rúbrica de la fase con `03-build-notes.md`.

## Orden sugerido

A1 → A2 → A3 → B1 → B4 → B3 → B6 → B7 → B5 → B2, y al final la verificación (E). Las de C, solo si las apruebas.
