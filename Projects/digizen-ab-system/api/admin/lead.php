<?php
declare(strict_types=1);
require __DIR__ . '/_load.php';
$user = dz_admin_require();
$id = filter_var($_GET['id'] ?? null, FILTER_VALIDATE_INT, ['options' => ['min_range' => 1]]);
if (!$id) { http_response_code(400); exit('Invalid lead'); }
$stmt = dz_db()->prepare('SELECT * FROM leads WHERE id = ?');
$stmt->execute([$id]);
$lead = $stmt->fetch();
if (!$lead) { http_response_code(404); exit('Not found'); }
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    dz_check_csrf();
    $stage = (string)($_POST['sales_stage'] ?? '');
    if (!in_array($stage, ['nuevo', 'contactado', 'en_seguimiento', 'convertido', 'descartado'], true)) {
        http_response_code(422); exit('Invalid stage');
    }
    $referredBy = substr(trim((string)($_POST['referred_by'] ?? '')), 0, 150);
    $nextAction = trim((string)($_POST['next_action_at'] ?? ''));
    if ($nextAction !== '' && !preg_match('/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/', $nextAction)) {
        http_response_code(422); exit('Invalid date');
    }
    $note = substr(trim((string)($_POST['note'] ?? '')), 0, 5000);
    $db = dz_db();
    $db->beginTransaction();
    try {
        $update = $db->prepare('UPDATE leads SET sales_stage = ?, referred_by = ?, next_action_at = ? WHERE id = ?');
        $update->execute([$stage, $referredBy ?: null, $nextAction ? str_replace('T', ' ', $nextAction) . ':00' : null, $id]);
        if ($note !== '') {
            $insert = $db->prepare('INSERT INTO lead_notes (lead_id, admin_user_id, body) VALUES (?, ?, ?)');
            $insert->execute([$id, $user['id'], $note]);
        }
        dz_audit((int)$user['id'], 'lead_updated', ['lead_id' => $id]);
        $db->commit();
    } catch (Throwable $e) { $db->rollBack(); throw $e; }
    header('Location: /conversion-admin/lead.php?id=' . $id); exit;
}
$body = '<div class="card"><h2>' . dz_e($lead['name']) . ' · ' . dz_e($lead['public_code']) . '</h2>';
foreach (['email' => 'Correo', 'phone' => 'Teléfono', 'preferred_channel' => 'Canal',
          'created_at' => 'Fecha', 'variant' => 'Variante', 'landing_id' => 'Landing',
          'utm_source' => 'Origen', 'utm_medium' => 'Medio', 'utm_campaign' => 'Campaña',
          'utm_content' => 'Contenido', 'utm_term' => 'Término', 'referral_code' => 'Código de referido',
          'referrer_url' => 'Sitio de procedencia', 'demo_status' => 'Estado de demo',
          'acumbamail_status' => 'Acumbamail', 'marketing_consent' => 'Consentimiento de marketing',
          'privacy_notice_version' => 'Versión aviso de privacidad'] as $key => $label) {
    $value = $key === 'marketing_consent' ? ((bool)$lead[$key] ? 'Sí' : 'No') : (string)($lead[$key] ?? '');
    $body .= '<p><strong>' . dz_e($label) . ':</strong> ' . dz_e($value) . '</p>';
}
$body .= '</div><form method="post" class="card"><h2>Seguimiento</h2><input type="hidden" name="csrf" value="' . dz_e(dz_csrf()) . '">';
$body .= '<label>Etapa<select name="sales_stage">';
foreach (['nuevo', 'contactado', 'en_seguimiento', 'convertido', 'descartado'] as $stage) {
    $body .= '<option value="' . $stage . '"' . ($lead['sales_stage'] === $stage ? ' selected' : '') . '>' . $stage . '</option>';
}
$body .= '</select></label><label>Referenciado por<input name="referred_by" value="' . dz_e($lead['referred_by']) . '"></label>';
$body .= '<label>Próxima acción<input type="datetime-local" name="next_action_at" value="' . dz_e($lead['next_action_at'] ? str_replace(' ', 'T', substr($lead['next_action_at'], 0, 16)) : '') . '"></label>';
$body .= '<label>Nota<textarea name="note" maxlength="5000"></textarea></label><button type="submit">Guardar</button></form>';
$stmt = dz_db()->prepare('SELECT n.body, n.created_at, u.username FROM lead_notes n JOIN admin_users u ON u.id = n.admin_user_id WHERE n.lead_id = ? ORDER BY n.created_at DESC LIMIT 100');
$stmt->execute([$id]);
$body .= '<section class="card"><h2>Notas</h2>';
foreach ($stmt->fetchAll() as $note) {
    $body .= '<p><small>' . dz_e($note['created_at']) . ' · ' . dz_e($note['username']) . '</small><br>' . nl2br(dz_e($note['body'])) . '</p>';
}
$body .= '</section>';
dz_admin_page('Solicitud', $body);
