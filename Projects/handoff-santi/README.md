# Digizen · landings A y B — avance para Santi

> **No es la versión final.** Es un avance de las dos versiones de la landing de Digizen, al 5 de octubre de 2026.
> Sirve como referencia visual y de diseño, y para detectar qué hay que implementar de pagos y backend.
> El texto, el diseño y la estructura todavía pueden cambiar.

A y B son dos propuestas de la misma página: mismo producto y mismos precios, distinta forma de contarlo.
Las dos están completas de frente (front), y ninguna está conectada a un servicio: no cobran ni guardan datos.

## Verlas publicadas

| | Landing | Reglas de ADA |
| --- | --- | --- |
| **A** | https://bruniusgnius.github.io/digizen-2026-2027/ | https://bruniusgnius.github.io/digizen-2026-2027/reglas-de-ada |
| **B** | https://bruniusgnius.github.io/digizen-2026-2027/b-v04-claude/ | https://bruniusgnius.github.io/digizen-2026-2027/b-v04-claude/reglas-de-ada.html |

## Qué hay aquí

| Carpeta | Qué es | Tecnología |
| --- | --- | --- |
| `landing-a/` | La landing A: página larga con secciones, tema claro y oscuro | Angular 21 + Tailwind 4 |
| `landing-b/` | La landing B: recorrido guiado por el scroll, ya generado | HTML estático + Tailwind 4 + GSAP |

## Cómo correrlas en local

**Landing A**

```bash
cd landing-a
npm install
npm start
```

Abre `http://localhost:4200`. Todo el contenido está en `src/app/app.html`, el comportamiento en `src/app/app.ts` y los estilos y variables de diseño en `src/styles.css`.

**Landing B**

```bash
cd landing-b
python3 -m http.server 8080
```

Abre `http://localhost:8080`. Las páginas (`index.html`, `reglas-de-ada.html`) ya vienen generadas. Las acciones de los botones están en `js/dz-actions.js`. Para recompilar los estilos: `npm install` y `npm run css`. El comando `npm run html` no funciona en esta copia: el generador lee textos fuente que no se incluyen aquí.

## Qué hace hoy cada acción

Nada de esto llega a un servidor. Donde dice «emite», la página lanza un evento en `window` y nadie lo recibe todavía.

### Landing A

| Acción | Qué hace hoy |
| --- | --- |
| «Pagar de contado» (tarjeta de precio) | Emite `digizen:checkout` con `{ plan: 'contado' }` |
| «Elegir 10 mensualidades» (tarjeta de precio) | Emite `digizen:checkout` con `{ plan: 'mensualidades' }` |
| «Inscribir a mi hijo» (menú, paneles de decisión, barra móvil) | Lleva a la sección de precio. No inicia un pago |
| Formulario «Conversa con ADA» en la página | Campos `name`, `email` y `whatsapp` (opcional). El botón no envía ni emite nada |
| «Conversar con ADA» / «Tengo dudas» (6 botones) | Abre un diálogo con los mismos tres campos (`dialog-name`, `dialog-email`, `dialog-whatsapp`). El botón no envía ni emite nada |
| WhatsApp del pie | Enlace a `wa.me/522218481116` con un mensaje prellenado |
| Correo del pie | `mailto:info@gnius.club` |
| Aviso de privacidad | Enlace a `https://gnius.club/aviso-de-privacidad.html` |

El punto de entrada del pago es la función `checkout()` en `landing-a/src/app/app.ts`.

### Landing B

| Acción | Qué hace hoy |
| --- | --- |
| «Pagar de contado» | Emite `digizen:checkout` con `{ plan: 'contado' }` |
| «Elegir pagos diferidos» | Emite `digizen:checkout` con `{ plan: 'diferido' }` |
| «Inscribir a mi hijo» del menú y del cierre | Lleva a las tarjetas de precio |
| «Inscribir a mi hijo» dentro del recorrido | Emite `digizen:checkout` con `{ plan: null }` |
| «Conversar con ADA primero» | Abre un diálogo: nombre, canal (correo o WhatsApp) y un solo dato de contacto. Al enviar valida y emite `digizen:ada-request` con `{ name, channel, contact }`. El diálogo no muestra confirmación |

Para escucharlos:

```js
window.addEventListener('digizen:checkout', (e) => {
  // e.detail.plan → A: 'contado' | 'mensualidades' · B: 'contado' | 'diferido' | null
});

window.addEventListener('digizen:ada-request', (e) => {
  // solo en B: e.detail → { name, channel: 'correo' | 'whatsapp', contact }
});
```

### Diferencias entre A y B que conviene resolver antes de conectar

1. **Nombre del plan a plazos:** `'mensualidades'` en A, `'diferido'` en B.
2. **Datos de «Conversa con ADA»:** A pide nombre, correo y WhatsApp opcional, y no emite evento. B pide nombre y un solo contacto con su canal, y sí lo emite.
3. **«Inscribir a mi hijo» sin plan elegido:** en A siempre lleva a las tarjetas de precio; en B uno de los botones emite el evento sin plan.

## Lo que el texto publicado promete

Son citas literales de la landing A. Cada una implica algo que el backend tiene que cumplir.

**Precio y formas de pago**
- «El ciclo completo de 12 meses cuesta $5,990. Es un solo precio. No hay cuota de inscripción aparte ni cargos escondidos.»
- De contado, «Precio fundador» de $4,990: «Te ahorras $1,000 por pagarlo completo.» «Vale hasta el 15 de noviembre.»
- A plazos, $599 × 10: «Terminas de pagar en el mes diez; ADA sigue con tu hijo hasta el doce.» «No es una suscripción.»
- «En los dos casos tu hijo empieza hoy y tiene el ciclo completo.»
- «Precio fundador congelado cuando lo reinscribas al siguiente nivel: nunca te sube mientras sigas.»
- «Después del 15 de noviembre, el precio sube para los que lleguen tarde.»

**Garantía**
- «Los 30 días cuentan desde la primera conversación de tu hijo con ADA, no desde que pagas. Si no es para ustedes, cancelas en un clic y te devolvemos tu dinero: todo, si pagaste de contado; la primera mensualidad, y ya no se cobra ninguna más, si elegiste mensualidades.»

**Conversar con ADA antes de pagar**
- «Déjanos tus datos y te mandamos tu acceso a tu correo en un minuto.»
- «El acceso llega a tu correo. WhatsApp queda como dato opcional para seguimiento.»

**Lo que incluye la inscripción**
- «Tu boleta de progreso: ves su avance sin vigilarlo.»
- «SAFE gratis todo el ciclo: los microcursos de Gnius Club para papás (seguridad y vida digital en familia).»
- «Código de descuento en Alquimistas de I.A.»
- «Tú estás en el circuito: recibes su avance (qué está construyendo, qué está aprendiendo a decidir) sin espiar sus conversaciones, porque un hijo espiado deja de hablar.»

La landing B usa los mismos precios ($5,990, $4,990 y $599 × 10) y la garantía de 30 días, pero su texto no menciona la fecha del 15 de noviembre.

## Pendientes conocidos del frente

- **Ruta de reglas en la A.** `/reglas-de-ada` se resuelve en el navegador. En un hospedaje estático la dirección directa responde 404 y se rescata con `404.html`; el servidor final necesita reescribir esa ruta a `index.html`.
- **Dominio.** La A declara `https://digizen.gnius.club/` como dirección canónica y en sus etiquetas para compartir. La imagen para compartir todavía es la anterior.
- **Medición.** Ninguna de las dos tiene analítica ni píxeles instalados.
- **Aviso de privacidad.** El enlace lleva al aviso general de Gnius Club.

## Qué no incluye

Los originales de las imágenes (PNG y PSD), los respaldos, los bocetos, las notas de proceso y las versiones descartadas. Si necesitas algo de eso, pídeselo a Bruno.

## Si vas a construir sobre este código

Esta copia se arma desde el repositorio de trabajo y se vuelve a generar cuando las landings cambian: lo que se edite aquí se pierde en la siguiente actualización. Antes de construir encima, acuerda con Bruno dónde se va a trabajar.
