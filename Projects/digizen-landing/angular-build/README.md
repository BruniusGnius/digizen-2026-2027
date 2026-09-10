# DIGIZEN · Landing Generación Fundadora

Build Angular/Tailwind de la arquitectura aprobada en `../Digizen Landing Refinado.dc.html`.

## Desarrollo

```bash
npm install
npm start
```

## Producción y pruebas

```bash
npm run build
npm test -- --watch=false
```

## Integraciones

Los botones de compra emiten `digizen:checkout` con `{ plan }`, donde `plan` puede ser `mensual`, `ciclo-msi` o `contado`. Deben conectarse al checkout real en la aplicación anfitriona.

El formulario ADA está deliberadamente desacoplado hasta recibir el endpoint, contrato de campos y estados aprobados. No transmite datos en esta versión.

## Assets reemplazables

- `public/assets/digizen/logo-digizen-horizontal-light.svg`
- `public/assets/digizen/logo-digizen-horizontal-dark.svg`

Conservar los nombres permite sustituir ambos logos sin modificar la navegación. Las imágenes Picsum se registran en `../03-asset-manifest.md`.
