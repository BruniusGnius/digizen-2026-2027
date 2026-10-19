<?php
declare(strict_types=1);
require __DIR__ . '/_load.php';
$user = dz_admin_require();
$filters = dz_admin_filters();
[$where, $values] = dz_admin_where($filters);
$stmt = dz_db()->prepare('SELECT id, name, email, phone, preferred_channel, variant, utm_source,
    referral_code, referred_by, sales_stage, next_action_at, created_at FROM leads' . $where . ' ORDER BY created_at DESC LIMIT 200');
$stmt->execute($values);
$rows = $stmt->fetchAll();
$body = '<form method="get" class="card toolbar">';
foreach (['q' => 'Buscar', 'variant' => 'Variante', 'sales_stage' => 'Etapa',
          'utm_source' => 'Origen', 'referral_code' => 'Referido'] as $key => $label) {
    $body .= '<label>' . dz_e($label) . '<input name="' . dz_e($key) . '" value="' . dz_e($filters[$key]) . '"></label>';
}
$body .= '<button type="submit">Filtrar</button></form>';
$body .= '<p>Se muestran hasta 200 solicitudes recientes. <a href="/conversion-admin/export.php?' . dz_e(http_build_query($filters)) . '">Descargar CSV filtrado</a></p>';
$body .= '<table><thead><tr><th>Fecha</th><th>Nombre</th><th>Contacto</th><th>Variante</th><th>Origen</th><th>Referido por</th><th>Canal</th><th>Etapa</th><th>Próxima acción</th></tr></thead><tbody>';
foreach ($rows as $row) {
    $body .= '<tr><td>' . dz_e($row['created_at']) . '</td><td><a href="/conversion-admin/lead.php?id=' . (int)$row['id'] . '">' . dz_e($row['name']) . '</a></td>'
        . '<td>' . dz_e($row['email'] ?: $row['phone']) . '</td><td>' . dz_e($row['variant']) . '</td>'
        . '<td>' . dz_e($row['utm_source'] ?: 'Sin etiquetar') . '</td><td>' . dz_e($row['referred_by'] ?: $row['referral_code']) . '</td>'
        . '<td>' . dz_e($row['preferred_channel']) . '</td><td>' . dz_e($row['sales_stage']) . '</td>'
        . '<td>' . dz_e($row['next_action_at']) . '</td></tr>';
}
$body .= '</tbody></table>';
dz_admin_page('Leads', $body);
