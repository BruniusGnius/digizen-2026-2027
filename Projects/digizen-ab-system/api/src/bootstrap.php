<?php
declare(strict_types=1);

const DZ_EXPERIMENT = 'digizen_landing_ab_2026_10';

function dz_config(): array {
    static $config;
    if ($config === null) {
        $file = dirname(__DIR__) . '/config/secrets.php';
        if (!is_file($file)) {
            throw new RuntimeException('Private configuration is missing');
        }
        $config = require $file;
    }
    return $config;
}

function dz_db(): PDO {
    static $db;
    if ($db === null) {
        $c = dz_config();
        $db = new PDO(
            'mysql:host=' . $c['db_host'] . ';dbname=' . $c['db_name'] . ';charset=utf8mb4',
            $c['db_user'], $c['db_password'],
            [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
             PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
             PDO::ATTR_EMULATE_PREPARES => false]
        );
    }
    return $db;
}

function dz_json(int $status, array $body): never {
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode($body, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
}

function dz_method(string $expected): void {
    if (($_SERVER['REQUEST_METHOD'] ?? '') !== $expected) {
        header('Allow: ' . $expected);
        dz_json(405, ['ok' => false, 'error' => 'method_not_allowed']);
    }
}

function dz_same_origin(): void {
    $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
    $allowed = dz_config()['allowed_origin'] ?? 'https://digizen.gnius.club';
    if ($origin !== '' && $origin !== $allowed) {
        dz_json(403, ['ok' => false, 'error' => 'origin_not_allowed']);
    }
    $fetchSite = $_SERVER['HTTP_SEC_FETCH_SITE'] ?? '';
    if ($fetchSite !== '' && !in_array($fetchSite, ['same-origin', 'none'], true)) {
        dz_json(403, ['ok' => false, 'error' => 'origin_not_allowed']);
    }
}

function dz_input(int $maxBytes = 8192): array {
    if (!str_starts_with(strtolower($_SERVER['CONTENT_TYPE'] ?? ''), 'application/json')) {
        dz_json(415, ['ok' => false, 'error' => 'json_required']);
    }
    if ((int)($_SERVER['CONTENT_LENGTH'] ?? 0) > $maxBytes) {
        dz_json(413, ['ok' => false, 'error' => 'too_large']);
    }
    $raw = file_get_contents('php://input', false, null, 0, $maxBytes + 1);
    if ($raw === false || strlen($raw) > $maxBytes) {
        dz_json(413, ['ok' => false, 'error' => 'too_large']);
    }
    try {
        $body = json_decode($raw, true, 20, JSON_THROW_ON_ERROR);
    } catch (JsonException) {
        dz_json(400, ['ok' => false, 'error' => 'invalid_json']);
    }
    if (!is_array($body) || array_is_list($body)) {
        dz_json(400, ['ok' => false, 'error' => 'invalid_json']);
    }
    return $body;
}

function dz_str(array $body, string $key, int $max = 255): ?string {
    $value = $body[$key] ?? null;
    if ($value === null || $value === '') return null;
    if (!is_string($value)) dz_json(422, ['ok' => false, 'error' => 'invalid_' . $key]);
    $value = trim($value);
    if (strlen($value) > $max) dz_json(422, ['ok' => false, 'error' => 'invalid_' . $key]);
    return $value === '' ? null : $value;
}

function dz_variant(array $body): string {
    $v = dz_str($body, 'variant', 1);
    if (!in_array($v, ['A', 'B'], true)) dz_json(422, ['ok' => false, 'error' => 'invalid_variant']);
    return $v;
}

function dz_landing(array $body, string $variant): string {
    $id = dz_str($body, 'landing_id', 100);
    $expected = $variant === 'A' ? 'digizen-landing' : 'digizen-landing-b-v04-claude';
    if ($id !== $expected) dz_json(422, ['ok' => false, 'error' => 'invalid_landing']);
    return $id;
}

function dz_attribution(array $body): array {
    $out = [];
    foreach (['utm_source' => 100, 'utm_medium' => 100, 'utm_campaign' => 150,
              'utm_content' => 150, 'utm_term' => 150] as $key => $max) {
        $out[$key] = dz_str($body, $key, $max);
    }
    return $out;
}

function dz_legal_document(string $type): array {
    $documents = dz_config()['legal_documents'] ?? [];
    $document = $documents[$type] ?? null;
    if (!is_array($document) || !isset($document['version'], $document['url'], $document['sha256'])
        || $document['version'] === 'pending' || !preg_match('/^[a-f0-9]{64}$/i', (string)$document['sha256'])) {
        dz_json(503, ['ok' => false, 'error' => 'legal_documents_not_configured']);
    }
    return $document;
}

function dz_record_consent(PDO $db, array $values): void {
    $config = dz_config();
    $key = (string)($config['consent_receipt_key'] ?? '');
    if ($key === '') throw new RuntimeException('Consent receipt key is missing');
    $ip = (string)($_SERVER['REMOTE_ADDR'] ?? '');
    $ua = (string)($_SERVER['HTTP_USER_AGENT'] ?? '');
    $timestamp = gmdate('Y-m-d H:i:s');
    $ipProof = $ip === '' ? null : hash_hmac('sha256', $ip, $key);
    $uaHash = $ua === '' ? null : hash('sha256', $ua);
    $sealData = implode('|', [$values['subject_type'], $values['lead_id'] ?? '', $values['visitor_id'] ?? '',
        $values['document_type'], $values['document_version'], $values['document_sha256'], $values['action'], $timestamp]);
    $receiptHmac = hash_hmac('sha256', $sealData, $key);
    $stmt = $db->prepare('INSERT INTO consent_receipts
      (environment, subject_type, lead_id, checkout_session_id, visitor_id, document_type, document_version,
       document_url, document_sha256, action, categories_json, source, landing_id, variant, entry_url,
       ip_proof_hmac, user_agent_hash, receipt_hmac, created_at_utc)
      VALUES (:environment, :subject_type, :lead_id, :checkout_session_id, :visitor_id, :document_type, :document_version,
       :document_url, :document_sha256, :action, :categories_json, :source, :landing_id, :variant, :entry_url,
       :ip_proof_hmac, :user_agent_hash, :receipt_hmac, :created_at_utc)');
    $stmt->execute(array_merge($values, [
      'environment' => $config['environment'] ?? 'production', 'checkout_session_id' => $values['checkout_session_id'] ?? null,
      'categories_json' => isset($values['categories_json']) ? json_encode($values['categories_json'], JSON_UNESCAPED_SLASHES) : null,
      'ip_proof_hmac' => $ipProof, 'user_agent_hash' => $uaHash, 'receipt_hmac' => $receiptHmac, 'created_at_utc' => $timestamp,
    ]));
}

function dz_fail(Throwable $e): never {
    error_log('[digizen-api] ' . $e->getMessage());
    dz_json(500, ['ok' => false, 'error' => 'server_error']);
}
