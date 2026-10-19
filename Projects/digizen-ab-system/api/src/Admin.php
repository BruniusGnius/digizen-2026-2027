<?php
declare(strict_types=1);

function dz_admin_session(): void {
    if (session_status() === PHP_SESSION_ACTIVE) return;
    if (($_SERVER['HTTPS'] ?? '') !== 'on' && ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') !== 'https'
        && PHP_SAPI !== 'cli-server') {
        http_response_code(403); exit('HTTPS required');
    }
    session_name('digizen_admin');
    session_set_cookie_params(['lifetime' => 0, 'path' => '/conversion-admin/', 'secure' => true,
        'httponly' => true, 'samesite' => 'Strict']);
    ini_set('session.use_strict_mode', '1');
    session_start();
    header('Cache-Control: no-store');
    header('X-Robots-Tag: noindex, nofollow');
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: no-referrer');
}

function dz_admin_user(): ?array {
    dz_admin_session();
    if (isset($_SESSION['last_active']) && time() - (int)$_SESSION['last_active'] > 1800) {
        $_SESSION = [];
        session_regenerate_id(true);
        return null;
    }
    $id = (int)($_SESSION['admin_id'] ?? 0);
    if ($id < 1) return null;
    $_SESSION['last_active'] = time();
    $stmt = dz_db()->prepare('SELECT id, username, can_export_notes FROM admin_users WHERE id = ?');
    $stmt->execute([$id]);
    return $stmt->fetch() ?: null;
}

function dz_admin_require(): array {
    $user = dz_admin_user();
    if (!$user) { header('Location: /conversion-admin/login.php'); exit; }
    return $user;
}

function dz_csrf(): string {
    dz_admin_session();
    if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(24));
    return $_SESSION['csrf'];
}

function dz_check_csrf(): void {
    if (!hash_equals(dz_csrf(), (string)($_POST['csrf'] ?? ''))) {
        http_response_code(403); exit('Invalid request');
    }
}

function dz_e(?string $s): string { return htmlspecialchars($s ?? '', ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }

function dz_audit(int $userId, string $action, array $detail = []): void {
    $stmt = dz_db()->prepare('INSERT INTO admin_audit (admin_user_id, action, detail) VALUES (?, ?, ?)');
    $stmt->execute([$userId, $action, json_encode($detail)]);
}

function dz_admin_filters(): array {
    $f = [];
    foreach (['q', 'variant', 'sales_stage', 'utm_source', 'referral_code'] as $key) {
        $f[$key] = substr(trim((string)($_GET[$key] ?? '')), 0, 100);
    }
    return $f;
}

function dz_admin_where(array $f): array {
    $where = []; $values = [];
    if ($f['q'] !== '') {
        $where[] = '(name LIKE ? OR email LIKE ? OR phone LIKE ? OR public_code LIKE ?)';
        $pattern = '%' . $f['q'] . '%';
        array_push($values, $pattern, $pattern, $pattern, $pattern);
    }
    foreach (['variant', 'sales_stage', 'utm_source', 'referral_code'] as $key) {
        if ($f[$key] !== '') { $where[] = $key . ' = ?'; $values[] = $f[$key]; }
    }
    return [$where ? ' WHERE ' . implode(' AND ', $where) : '', $values];
}

function dz_admin_page(string $title, string $body): void {
    echo '<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">';
    echo '<meta name="robots" content="noindex,nofollow"><title>' . dz_e($title) . ' · DIGIZEN</title>';
    echo '<style>body{font:16px/1.45 system-ui;margin:2rem auto;max-width:1100px;padding:0 1rem;color:#18233a}a{color:#153ba6}input,select,textarea,button{font:inherit;padding:.5rem}label{display:inline-grid;gap:.25rem;margin:.4rem}table{border-collapse:collapse;width:100%;margin:1rem 0}td,th{border:1px solid #ddd;padding:.6rem;text-align:left;vertical-align:top}tr:nth-child(even){background:#f6f7fa}.error{color:#a10}.toolbar{display:flex;gap:1rem;flex-wrap:wrap}.card{padding:1rem;border:1px solid #ddd;border-radius:.5rem;margin:1rem 0}textarea{width:100%;min-height:7rem}</style>';
    echo '<header><h1>DIGIZEN · ventas</h1><nav><a href="/conversion-admin/">Leads</a> · <form method="post" action="/conversion-admin/logout.php" style="display:inline"><input type="hidden" name="csrf" value="' . dz_e(dz_csrf()) . '"><button type="submit">Salir</button></form></nav></header>' . $body . '</html>';
}
