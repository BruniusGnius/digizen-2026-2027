<!doctype html>
<html lang="es" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="csrf-token" content="{{ csrf_token() }}">
  <meta name="color-scheme" content="light">
  <meta name="description" content="Inscripción · Ciclo Digizen — tus 12 meses empiezan HOY">
  <title>DIGIZEN · Generación Fundadora</title>
  @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="dg-system">
  <a class="skip-link" href="#main-content">Ir al contenido</a>
  @yield('content')
  <script type="application/json" id="digizen-config">{!! json_encode(config('digizen.frontend'), JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT) !!}</script>
</body>
</html>
