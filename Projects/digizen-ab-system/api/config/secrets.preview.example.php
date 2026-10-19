<?php
// Plantilla SOLO para el subdominio de pruebas. Copiar a secrets.php fuera de public_html.
// La demo usa la base DIGIZEN compartida por decisión del usuario.
// Los registros se marcan environment=preview para su limpieza antes del lanzamiento.
return [
    'db_host' => '',
    'db_name' => '',
    'db_user' => '',
    'db_password' => '',
    'environment' => 'preview',
    'allowed_origin' => 'https://digizen-demo.gnius.club',
    'demo_url' => 'https://ada-demo.example/',
    'allow_mock_demo' => true,
    'acumbamail_webhook_url' => '', // Solo URL privada, fuera de public_html.
    'acumbamail_list_id' => '1544280',
    'privacy_notice_version' => 'gnius-club-reference-preview-2026-10-14', // Identificador de referencia de prueba, no revisión legal.
    'consent_receipt_key' => '', // Clave aleatoria exclusiva del entorno preview.
    'legal_documents' => [
        'terms' => ['version' => 'preview-pending', 'url' => 'https://digizen.gnius.club/terminos-y-condiciones-digizen.html', 'sha256' => ''],
        'privacy' => ['version' => 'preview-pending', 'url' => 'https://gnius.club/aviso-de-privacidad.html', 'sha256' => ''],
        'cookies' => ['version' => 'preview-pending', 'url' => 'https://digizen.gnius.club/politica-de-cookies-digizen.html', 'sha256' => ''],
    ],
];
