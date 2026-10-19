<?php
declare(strict_types=1);
require __DIR__ . '/_load.php';
dz_method('POST');
dz_same_origin();
$body = dz_input();
$name = dz_str($body, 'name', 150);
$email = dz_str($body, 'email', 190);
$phone = dz_str($body, 'phone', 50);
if (!$name || (!$email && !$phone)) dz_json(422, ['ok' => false, 'error' => 'name_and_contact_required']);
if ($email && $phone) dz_json(422, ['ok' => false, 'error' => 'choose_one_contact_method']);
if ($email && !filter_var($email, FILTER_VALIDATE_EMAIL)) dz_json(422, ['ok' => false, 'error' => 'invalid_email']);
if ($phone && !preg_match('/^\+?[0-9\s()\-]{8,30}$/', $phone)) dz_json(422, ['ok' => false, 'error' => 'invalid_phone']);
$channel = dz_str($body, 'preferred_channel', 20);
if (!in_array($channel, ['correo', 'whatsapp'], true) || ($channel === 'correo' && !$email) || ($channel === 'whatsapp' && !$phone)) {
    dz_json(422, ['ok' => false, 'error' => 'invalid_channel']);
}
if (($body['terms_accepted'] ?? null) !== true) dz_json(422, ['ok' => false, 'error' => 'terms_required']);
if (($body['privacy_accepted'] ?? null) !== true) dz_json(422, ['ok' => false, 'error' => 'privacy_required']);
if (!is_bool($body['marketing_consent'] ?? null)) dz_json(422, ['ok' => false, 'error' => 'invalid_marketing_consent']);
$variant = dz_variant($body);
$landing = dz_landing($body, $variant);
if (($body['experiment_key'] ?? null) !== DZ_EXPERIMENT) dz_json(422, ['ok' => false, 'error' => 'invalid_experiment']);
$visitor = dz_str($body, 'visitor_id', 100);
if ($visitor && !preg_match('/^[a-zA-Z0-9_-]{8,100}$/', $visitor)) dz_json(422, ['ok' => false, 'error' => 'invalid_visitor']);
$utm = dz_attribution($body);
$config = dz_config();
$environment = $config['environment'] ?? 'production';
if ($environment === 'preview') {
    $qaEmail = $email !== null && preg_match('/^bruno\+[a-z0-9._-]+@gnius\.club$/i', $email);
    $qaPhone = $phone !== null && preg_replace('/\D/', '', $phone) === '525500000000';
    if (!str_starts_with($name, 'QA ') || ($email !== null && !$qaEmail)
        || ($phone !== null && !$qaPhone) || ($email === null && !$qaPhone)) {
        dz_json(403, ['ok' => false, 'error' => 'preview_qa_only']);
    }
}
$demoUrl = $config['demo_url'] ?? '';
$privacyVersion = $config['privacy_notice_version'] ?? 'pending';
$termsDocument = dz_legal_document('terms');
$privacyDocument = dz_legal_document('privacy');
$mockAllowed = ($config['allow_mock_demo'] ?? false) === true
    && ($config['allowed_origin'] ?? '') === 'https://digizen-demo.gnius.club'
    && ($_SERVER['HTTP_HOST'] ?? '') === 'digizen-demo.gnius.club';
// El demo ficticio solo funciona en localhost o en el subdominio de pruebas configurado.
if ($demoUrl === '' || $privacyVersion === 'pending' || !filter_var($demoUrl, FILTER_VALIDATE_URL)
    || parse_url($demoUrl, PHP_URL_SCHEME) !== 'https'
    || (str_contains($demoUrl, '.example') && PHP_SAPI !== 'cli-server' && !$mockAllowed)) {
    dz_json(503, ['ok' => false, 'error' => 'demo_not_configured']);
}
try {
    $code = strtoupper(bin2hex(random_bytes(6)));
    $db = dz_db();
    $db->beginTransaction();
    $stmt = $db->prepare('INSERT INTO leads
        (environment, public_code, name, email, phone, preferred_channel, marketing_consent,
         privacy_notice_version, privacy_accepted_at, demo_status, landing_id, variant,
         visitor_id, entry_url, referrer_url, referral_code, utm_source, utm_medium,
         utm_campaign, utm_content, utm_term, acumbamail_status)
        VALUES (:environment, :public_code, :name, :email, :phone, :preferred_channel, :marketing_consent,
         :privacy_notice_version, NOW(), :demo_status, :landing_id, :variant,
         :visitor_id, :entry_url, :referrer_url, :referral_code, :utm_source, :utm_medium,
         :utm_campaign, :utm_content, :utm_term, :acumbamail_status)');
    $stmt->execute([
        'environment' => $environment,
        'public_code' => $code, 'name' => $name, 'email' => $email, 'phone' => $phone,
        'preferred_channel' => $channel, 'marketing_consent' => (int)$body['marketing_consent'],
        'privacy_notice_version' => $privacyVersion, 'demo_status' => 'listo',
        'landing_id' => $landing, 'variant' => $variant, 'visitor_id' => $visitor,
        'entry_url' => dz_str($body, 'entry_url', 500), 'referrer_url' => dz_str($body, 'referrer_url', 500),
        'referral_code' => dz_str($body, 'referral_code', 100),
        'utm_source' => $utm['utm_source'], 'utm_medium' => $utm['utm_medium'],
        'utm_campaign' => $utm['utm_campaign'], 'utm_content' => $utm['utm_content'],
        'utm_term' => $utm['utm_term'],
        'acumbamail_status' => ($email && $body['marketing_consent']) ? 'pending' : 'not_applicable',
    ]);
    $leadId = (int)$db->lastInsertId();
    $receiptBase = [
        'subject_type' => 'lead', 'lead_id' => $leadId, 'visitor_id' => $visitor, 'action' => 'accepted',
        'source' => 'ada_form', 'landing_id' => $landing, 'variant' => $variant,
        'entry_url' => dz_str($body, 'entry_url', 500),
    ];
    foreach (['terms' => $termsDocument, 'privacy' => $privacyDocument] as $type => $document) {
        dz_record_consent($db, array_merge($receiptBase, [
            'document_type' => $type, 'document_version' => $document['version'],
            'document_url' => $document['url'], 'document_sha256' => $document['sha256'],
        ]));
    }
    $db->commit();
    // El envío a Acumbamail se procesa por cron; nunca retrasa el acceso al demo.
    dz_json(201, ['ok' => true, 'lead_id' => $leadId, 'public_code' => $code,
        'demo_url' => $demoUrl, 'demo_simulated' => $mockAllowed && str_contains($demoUrl, '.example')]);
} catch (Throwable $e) {
    if (isset($db) && $db->inTransaction()) $db->rollBack();
    dz_fail($e);
}
