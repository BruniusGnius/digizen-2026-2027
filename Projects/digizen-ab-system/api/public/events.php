<?php
declare(strict_types=1);
require __DIR__ . '/_load.php';
dz_method('POST');
dz_same_origin();
$body = dz_input(4096);
$allowed = ['page_view', 'section_reached', 'scroll_depth_reached', 'pricing_reached',
    'cta_clicked', 'ada_request_opened', 'ada_request_submitted', 'checkout_started',
    'rules_opened', 'rules_section_reached', 'rules_cta_clicked', 'faq_opened',
    'ada_demo_confirmation_viewed', 'purchase_confirmation_viewed'];
$name = dz_str($body, 'event_name', 100);
if (!in_array($name, $allowed, true)) dz_json(422, ['ok' => false, 'error' => 'invalid_event']);
$variant = dz_variant($body);
$landing = dz_landing($body, $variant);
if (($body['experiment_key'] ?? null) !== DZ_EXPERIMENT) dz_json(422, ['ok' => false, 'error' => 'invalid_experiment']);
$visitor = dz_str($body, 'visitor_id', 100);
if ($visitor !== null && !preg_match('/^[a-zA-Z0-9_-]{8,100}$/', $visitor)) dz_json(422, ['ok' => false, 'error' => 'invalid_visitor']);
$lead = filter_var($body['lead_id'] ?? null, FILTER_VALIDATE_INT, ['options' => ['min_range' => 1]]) ?: null;
$utm = dz_attribution($body);
foreach ($utm as $key => $value) {
    if ($value && (filter_var($value, FILTER_VALIDATE_EMAIL) || preg_match('/\+?\d[\d\s().-]{7,}/', $value))) {
        $utm[$key] = null;
    }
}
// Lista blanca estricta: nunca guardar payloads arbitrarios que puedan incluir PII.
$props = [];
foreach (['section_index', 'scroll_depth', 'elapsed_ms'] as $key) {
    if (isset($body[$key]) && is_numeric($body[$key])) $props[$key] = (int)$body[$key];
}
try {
    $stmt = dz_db()->prepare('INSERT INTO events
        (environment, event_name, experiment_key, visitor_id, lead_id, landing_id, variant, path,
         section_id, section_label, cta, plan, device_type, utm_source, utm_medium,
         utm_campaign, utm_content, utm_term, payload)
         VALUES (:environment, :event_name, :experiment_key, :visitor_id, :lead_id, :landing_id, :variant, :path,
         :section_id, :section_label, :cta, :plan, :device_type, :utm_source, :utm_medium,
         :utm_campaign, :utm_content, :utm_term, :payload)');
    $stmt->execute([
        'environment' => dz_config()['environment'] ?? 'production',
        'event_name' => $name, 'experiment_key' => DZ_EXPERIMENT,
        'visitor_id' => $visitor, 'lead_id' => $lead, 'landing_id' => $landing, 'variant' => $variant,
        'path' => dz_str($body, 'path', 255), 'section_id' => dz_str($body, 'section_id', 100),
        'section_label' => dz_str($body, 'section_label', 255), 'cta' => dz_str($body, 'cta', 100),
        'plan' => dz_str($body, 'plan', 50), 'device_type' => dz_str($body, 'device_type', 20),
        'utm_source' => $utm['utm_source'], 'utm_medium' => $utm['utm_medium'],
        'utm_campaign' => $utm['utm_campaign'], 'utm_content' => $utm['utm_content'],
        'utm_term' => $utm['utm_term'], 'payload' => json_encode($props),
    ]);
    dz_json(201, ['ok' => true, 'event_id' => (int)dz_db()->lastInsertId()]);
} catch (Throwable $e) {
    dz_fail($e);
}
