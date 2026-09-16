---
name: apple-design
description: Filosofía de interacción física y motion — cómo diseñar interfaces que responden como objetos reales (springs, interrumpibilidad, materiales, tipografía dependiente del tamaño). Es una dependencia base de cualquier skill que diseñe o construya interfaces, no un módulo opcional de animación — informa decisiones de tipografía/materiales desde el sistema de diseño, de intención de interacción desde el wireframe, y de implementación de motion en el build.
---

# Filosofía de interacción física

La idea central: una interfaz se siente "viva" cuando se comporta como un objeto físico — responde al instante, puede agarrarse y soltarse a medio movimiento, carga inercia, y resiste progresivamente en sus límites en vez de topar en seco. Esto no es una capa de animación que se agrega al final; cambia decisiones desde el sistema de diseño (qué tan translúcido es un material, cómo escala el tracking de una tipografía) y desde el wireframe (qué elementos son arrastrables, dónde hace falta feedback inmediato).

## 1. Respuesta inmediata

El feedback ocurre en el instante del toque/clic inicial, nunca al soltar. Cualquier retraso perceptible entre la acción y la respuesta rompe la sensación de control directo. Esto aplica desde el wireframe (marcar qué elementos necesitan feedback continuo durante el gesto, no solo al terminar) hasta el código (animar en `pointerdown`, no en `click`).

## 2. Manipulación directa

Lo que se arrastra debe seguir el dedo/cursor 1:1, respetando el punto exacto donde se agarró — no saltar al centro del elemento. Cuando el wireframe define un componente arrastrable (un carrusel, un sheet, una barra), esa intención debe quedar anotada ahí, porque cambia cómo se construye el componente después.

## 3. Interrumpibilidad — el principio más importante

Ninguna animación debe bloquear el input. Si el usuario reinicia un gesto a medio vuelo, la interfaz responde de inmediato desde su posición actual en pantalla — nunca desde el destino final "lógico". Esto descarta animaciones de duración fija (`@keyframes`/`transition` simples) para todo lo que el usuario pueda tocar, a favor de springs, que por naturaleza parten del valor actual y pueden redirigirse sin saltos.

## 4. Comportamiento sobre coreografía — usar resortes (springs)

En vez de pensar en duración fija, se piensa en dos parámetros:
- **Damping (amortiguación):** controla el rebote. `1.0` = crítico, sin rebote, asentamiento limpio. Valores menores = más rebote/oscilación.
- **Response:** qué tan rápido llega al destino. No es "duración" — el tiempo de asentamiento emerge de los parámetros, no se fija de antemano.

Regla práctica: la UI normal (menús, paneles que aparecen) usa amortiguación crítica (`~1.0`, sin rebote) — el rebote se reserva exclusivamente para interacciones donde el propio gesto del usuario ya traía momentum (un flick, un drag que se suelta).

## 5. Traspaso de velocidad y proyección de momentum

Cuando se suelta un gesto, la animación que sigue debe continuar con la velocidad exacta con la que iba el dedo — sin costura visible entre "arrastrar" y "animarse solo". Y el punto de destino no debe ser el más cercano desde donde se soltó, sino el que resulta de **proyectar hacia dónde iba** el gesto (como la inercia de un scroll). Esto es lo que hace que un "flick" se sienta como si de verdad hubiera lanzado el objeto.

## 6. Resistencia progresiva en los límites (rubber-banding)

En un borde o límite (fin de un carrusel, tope de un sheet), la resistencia debe crecer progresivamente mientras más se empuja — nunca un tope duro y frío. Un tope duro se siente "congelado"; la resistencia progresiva se siente "responsiva, pero no hay más aquí".

## 7. Consistencia espacial

Lo que entra por un lado debe salir por el mismo lado — un panel que aparece desde la derecha debe cerrarse hacia la derecha, no hacia abajo. Los menús, popovers y sheets deben originarse visualmente desde el elemento que los disparó, no aparecer flotando sin relación espacial con su origen.

## 8. Materiales y profundidad (esto es sistema de diseño, no motion)

La translucidez comunica jerarquía, no es solo estética: materiales más pesados/opacos separan regiones estructurales (barras, sidebars); materiales más ligeros llaman la atención hacia lo interactivo. Nunca apilar dos superficies translúcidas claras entre sí — la legibilidad se rompe. El texto sobre superficies translúcidas necesita más contraste y peso que sobre un fondo sólido — esto se define en la paleta del sistema de diseño, no se improvisa en el build.

## 9. Tipografía dependiente del tamaño (esto también es sistema de diseño)

El espaciado entre letras (tracking) y el interlineado (leading) no son valores fijos — cambian con el tamaño. Texto grande/display necesita tracking negativo (las letras se leen demasiado separadas si crecen sin compensación) y leading apretado. Texto pequeño/cuerpo necesita tracking neutro o levemente positivo y leading más generoso para legibilidad sostenida. Esta regla se aplica al definir la escala tipográfica del sistema de diseño, no después.

## 10. Accesibilidad y movimiento reducido

Movimiento reducido no significa "sin feedback" — significa un equivalente más sobrio: reemplazar deslizamientos/springs/parallax por cross-fades cortos de opacidad, sin rebote. Igual de real: respetar el ajuste de tamaño de texto del usuario (unidades relativas, no píxeles fijos) para que la jerarquía tipográfica no se rompa cuando alguien la escala.

## 11. Rendimiento

Animar únicamente propiedades que el navegador puede componer sin recalcular layout — transformaciones y opacidad. Todo lo demás (color de fondo, tamaño, posición vía top/left) cuesta más caro en cada frame y es la causa más común de animaciones que se sienten "trabadas" en dispositivos de gama media, que son justamente los que más importan en tráfico frío de LATAM en móvil.

## Cómo se usa esto en las 3 fases de un proceso de diseño

- **Sistema de diseño:** los puntos 8 y 9 son insumo directo — la paleta y la escala tipográfica se definen con estas reglas, no se ajustan después.
- **Wireframe:** los puntos 1, 2, 3 y 7 se anotan como intención de interacción por componente (qué se arrastra, qué necesita feedback inmediato, de dónde entra/sale cada panel) — es información de diseño, no de implementación todavía.
- **Build:** los puntos 4, 5, 6, 10 y 11 son las reglas de implementación real del motion — springs, velocidad, rubber-banding, reduced motion, rendimiento.
