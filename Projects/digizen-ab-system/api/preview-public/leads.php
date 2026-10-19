<?php
declare(strict_types=1);
function reply(int $status, array $body): never {
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode($body);
    exit;
}
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') reply(405, ['ok' => false, 'error' => 'method_not_allowed']);
if (($_SERVER['HTTP_HOST'] ?? '') !== 'digizen-demo.gnius.club'
    || !in_array($_SERVER['HTTP_ORIGIN'] ?? '', ['', 'https://digizen-demo.gnius.club'], true)) {
    reply(403, ['ok' => false, 'error' => 'origin_not_allowed']);
}
if (!str_starts_with(strtolower($_SERVER['CONTENT_TYPE'] ?? ''), 'application/json')
    || (int)($_SERVER['CONTENT_LENGTH'] ?? 0) > 8192) {
    reply(415, ['ok' => false, 'error' => 'invalid_request']);
}
try {
    $body = json_decode(file_get_contents('php://input', false, null, 0, 8193), true, 20, JSON_THROW_ON_ERROR);
} catch (Throwable) {
    reply(400, ['ok' => false, 'error' => 'invalid_json']);
}
if (!is_array($body) || array_is_list($body)) reply(400, ['ok' => false, 'error' => 'invalid_json']);
$name = $body['name'] ?? null;
$email = $body['email'] ?? null;
$phone = $body['phone'] ?? null;
$channel = $body['preferred_channel'] ?? null;
if (!is_string($name) || trim($name) === '' || strlen($name) > 150 || (!$email && !$phone)) {
    reply(422, ['ok' => false, 'error' => 'name_and_contact_required']);
}
if ($email && $phone) reply(422, ['ok' => false, 'error' => 'choose_one_contact_method']);
if ($email !== null && (!is_string($email) || !filter_var($email, FILTER_VALIDATE_EMAIL))) {
    reply(422, ['ok' => false, 'error' => 'invalid_email']);
}
if ($phone !== null && (!is_string($phone) || !preg_match('/^\+?[0-9\s()\-]{8,30}$/', $phone))) {
    reply(422, ['ok' => false, 'error' => 'invalid_phone']);
}
if (!in_array($channel, ['correo', 'whatsapp'], true)
    || ($channel === 'correo' && !$email) || ($channel === 'whatsapp' && !$phone)
    || ($body['terms_accepted'] ?? null) !== true
    || ($body['privacy_accepted'] ?? null) !== true
    || !is_bool($body['marketing_consent'] ?? null)
    || ($body['experiment_key'] ?? null) !== 'digizen_landing_ab_2026_10'
    || !in_array($body['variant'] ?? null, ['A', 'B'], true)) {
    reply(422, ['ok' => false, 'error' => 'invalid_request']);
}
// No escribir el cuerpo de la solicitud: este endpoint muestra el flujo, no capta leads.
reply(201, ['ok' => true, 'simulated' => true, 'demo_simulated' => true,
    'lead_id' => random_int(100000, 999999),
    'public_code' => strtoupper(bin2hex(random_bytes(6))),
    'demo_url' => 'https://ada-demo.example/']);
