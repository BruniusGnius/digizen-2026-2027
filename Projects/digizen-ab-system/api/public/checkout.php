<?php
declare(strict_types=1);
header('Cache-Control: no-store');
header('Content-Type: application/json; charset=utf-8');
http_response_code(503);
echo json_encode(['ok' => false, 'error' => 'payments_paused']);
