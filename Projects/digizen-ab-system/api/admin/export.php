<?php
declare(strict_types=1);
require __DIR__ . '/_load.php';
$user = dz_admin_require();
$filters = dz_admin_filters();
[$where, $values] = dz_admin_where($filters);
$columns = ['public_code', 'name', 'email', 'phone', 'preferred_channel', 'variant', 'landing_id',
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'referral_code',
    'referred_by', 'referrer_url', 'marketing_consent', 'sales_stage', 'demo_status',
    'next_action_at', 'last_contact_at', 'created_at'];
$stmt = dz_db()->prepare('SELECT ' . implode(', ', $columns) . ' FROM leads' . $where . ' ORDER BY created_at DESC LIMIT 10000');
$stmt->execute($values);
dz_audit((int)$user['id'], 'leads_exported', ['filter_fields' => array_keys(array_filter($filters))]);
header('Content-Type: text/csv; charset=utf-8');
header('Content-Disposition: attachment; filename="digizen-leads-' . date('Y-m-d') . '.csv"');
header('Cache-Control: no-store');
$out = fopen('php://output', 'w');
fwrite($out, "\xEF\xBB\xBF");
fputcsv($out, $columns);
while ($row = $stmt->fetch()) {
    $safe = [];
    foreach ($columns as $column) {
        $value = (string)($row[$column] ?? '');
        if (preg_match('/^[\s]*[=+@\-]/u', $value)) $value = "'" . $value;
        $safe[] = $value;
    }
    fputcsv($out, $safe);
}
fclose($out);
