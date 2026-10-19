<?php
declare(strict_types=1);
require __DIR__ . '/_load.php';
dz_method('GET');
try {
    dz_db()->query('SELECT 1');
    dz_json(200, ['ok' => true, 'service' => 'digizen-conversion-api', 'database' => 'ready']);
} catch (Throwable $e) {
    dz_fail($e);
}
