<?php
declare(strict_types=1);
require __DIR__ . '/_load.php';
dz_admin_session();
if (dz_admin_user()) { header('Location: /conversion-admin/'); exit; }
$error = '';
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    dz_check_csrf();
    $username = substr(trim((string)($_POST['username'] ?? '')), 0, 100);
    $password = (string)($_POST['password'] ?? '');
    $stmt = dz_db()->prepare('SELECT * FROM admin_users WHERE username = ?');
    $stmt->execute([$username]);
    $user = $stmt->fetch();
    $locked = $user && $user['locked_until'] && strtotime($user['locked_until']) > time();
    if ($user && !$locked && password_verify($password, $user['password_hash'])) {
        $stmt = dz_db()->prepare('UPDATE admin_users SET failed_attempts = 0, locked_until = NULL, last_login_at = NOW() WHERE id = ?');
        $stmt->execute([$user['id']]);
        session_regenerate_id(true);
        $_SESSION['admin_id'] = (int)$user['id'];
        $_SESSION['last_active'] = time();
        dz_audit((int)$user['id'], 'login');
        header('Location: /conversion-admin/'); exit;
    }
    if ($user && !$locked) {
        $attempts = (int)$user['failed_attempts'] + 1;
        $until = $attempts >= 5 ? date('Y-m-d H:i:s', time() + 900) : null;
        $stmt = dz_db()->prepare('UPDATE admin_users SET failed_attempts = ?, locked_until = ? WHERE id = ?');
        $stmt->execute([$attempts, $until, $user['id']]);
    }
    usleep(300000);
    $error = 'Usuario o contraseña incorrectos, o cuenta bloqueada temporalmente.';
}
$body = '<form method="post" class="card"><input type="hidden" name="csrf" value="' . dz_e(dz_csrf()) . '">'
    . '<label>Usuario<input name="username" autocomplete="username" required></label>'
    . '<label>Contraseña<input type="password" name="password" autocomplete="current-password" required></label>'
    . '<button type="submit">Entrar</button></form>';
if ($error) $body = '<p class="error">' . dz_e($error) . '</p>' . $body;
dz_admin_page('Acceso', $body);
