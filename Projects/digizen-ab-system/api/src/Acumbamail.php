<?php
declare(strict_types=1);

function dz_sync_acumbamail(int $leadId): void {
    $db = dz_db();
    $stmt = $db->prepare('SELECT id, name, email, variant, utm_source, marketing_consent,
        acumbamail_attempts FROM leads WHERE id = ?');
    $stmt->execute([$leadId]);
    $lead = $stmt->fetch();
    if (!$lead || !$lead['email'] || !(bool)$lead['marketing_consent']) return;
    $url = dz_config()['acumbamail_webhook_url'] ?? '';
    if ($url === '') return;
    if (!str_starts_with($url, 'https://')) throw new RuntimeException('Acumbamail webhook must use HTTPS');

    $attempts = (int)$lead['acumbamail_attempts'] + 1;
    $ch = curl_init($url);
    if ($ch === false) throw new RuntimeException('Could not initialize webhook');
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => json_encode([
            'email' => $lead['email'], 'nombre' => $lead['name'],
            'variante_ab' => $lead['variant'], 'utm_source' => $lead['utm_source'],
            'list_id' => dz_config()['acumbamail_list_id'] ?? '1544280',
            'double_optin' => 0, 'welcome_email' => 0, 'update_subscriber' => 0,
        ], JSON_THROW_ON_ERROR),
        CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 4,
        CURLOPT_CONNECTTIMEOUT => 2,
    ]);
    $result = curl_exec($ch);
    $http = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    $response = is_string($result) ? json_decode($result, true) : null;
    // Esta cuenta devuelve HTTP 200 y serializa el JSON de éxito como cadena.
    if (is_string($response)) $response = json_decode($response, true);
    $ok = in_array($http, [200, 201], true) && is_array($response)
        && isset($response['id'], $response['email'])
        && strcasecmp((string)$response['email'], (string)$lead['email']) === 0;
    curl_close($ch);
    $update = $db->prepare('UPDATE leads SET acumbamail_status = ?, acumbamail_attempts = ?,
        acumbamail_next_retry_at = ?, acumbamail_last_error = ? WHERE id = ?');
    $update->execute([
        $ok ? 'synced' : 'retry', $attempts,
        $ok ? null : date('Y-m-d H:i:s', time() + min(86400, 300 * (2 ** min($attempts, 8)))),
        $ok ? null : 'HTTP ' . (int)$http . (in_array($http, [200, 201], true) ? ' invalid_response' : ''), $leadId,
    ]);
}
