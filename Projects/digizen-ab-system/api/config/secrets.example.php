<?php
// Copiar SOLO en /home/u502287134/digizen-conversion-api/config/secrets.php.
// Nunca publicar ni incorporar al repositorio el archivo con valores reales.
return [
    'db_host' => '', // Copiar el valor real de DB_HOST del .env local al preparar la publicación.
    'db_name' => '', // Copiar DB_NAME real; no inferir credenciales de ejemplos.
    'db_user' => '', // Copiar DB_USER real.
    'db_password' => '',
    'environment' => 'production',
    'allowed_origin' => 'https://digizen.gnius.club',
    'demo_url' => '', // URL real de ADA; dejar vacía hasta que ADA la entregue y se pruebe.
    'allow_mock_demo' => false, // Activar solo en configuración privada del subdominio de pruebas.
    'acumbamail_webhook_url' => '',
    'acumbamail_list_id' => '1544280',
    'privacy_notice_version' => 'pending', // Enlazar Gnius Club; verificar el texto y registrar su versión real.
    'consent_receipt_key' => '', // Generar una clave aleatoria exclusiva, fuera de la base y de Git.
    'legal_documents' => [
        'terms' => ['version' => 'pending', 'url' => 'https://digizen.gnius.club/terminos-y-condiciones-digizen.html', 'sha256' => ''],
        'privacy' => ['version' => 'pending', 'url' => 'https://gnius.club/aviso-de-privacidad.html', 'sha256' => ''],
        'cookies' => ['version' => 'pending', 'url' => 'https://digizen.gnius.club/politica-de-cookies-digizen.html', 'sha256' => ''],
    ],
];
