<?php
declare(strict_types=1);
require __DIR__ . '/_load.php';
dz_method('POST');
dz_same_origin();
$body = dz_input(4096);
if (($body['experiment_key'] ?? null) !== DZ_EXPERIMENT) dz_json(422, ['ok' => false, 'error' => 'invalid_experiment']);
$variant = dz_variant($body);
$landing = dz_landing($body, $variant);
$visitor = dz_str($body, 'visitor_id', 100);
if (!$visitor || !preg_match('/^[a-zA-Z0-9_-]{8,100}$/', $visitor)) dz_json(422, ['ok' => false, 'error' => 'invalid_visitor']);
$action = dz_str($body, 'action', 20);
if (!in_array($action, ['accepted', 'revoked'], true)) dz_json(422, ['ok' => false, 'error' => 'invalid_action']);
$categories = $body['categories'] ?? null;
if (!is_array($categories) || array_keys($categories) !== ['performance', 'marketing']
    || !is_bool($categories['performance']) || !is_bool($categories['marketing'])) {
    dz_json(422, ['ok' => false, 'error' => 'invalid_categories']);
}
$document = dz_legal_document('cookies');
try {
    dz_record_consent(dz_db(), [
        'subject_type' => 'visitor', 'lead_id' => null, 'visitor_id' => $visitor,
        'document_type' => 'cookies', 'document_version' => $document['version'],
        'document_url' => $document['url'], 'document_sha256' => $document['sha256'],
        'action' => $action, 'categories_json' => $categories, 'source' => 'cookie_preferences',
        'landing_id' => $landing, 'variant' => $variant, 'entry_url' => dz_str($body, 'entry_url', 500),
    ]);
    dz_json(201, ['ok' => true]);
} catch (Throwable $e) { dz_fail($e); }
