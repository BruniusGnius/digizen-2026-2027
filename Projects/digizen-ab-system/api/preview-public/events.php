<?php
declare(strict_types=1);
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { http_response_code(405); exit; }
if (($_SERVER['HTTP_HOST'] ?? '') !== 'digizen-demo.gnius.club'
    || !in_array($_SERVER['HTTP_ORIGIN'] ?? '', ['', 'https://digizen-demo.gnius.club'], true)) {
    http_response_code(403); exit;
}
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
http_response_code(202);
echo json_encode(['ok' => true, 'simulated' => true]);
