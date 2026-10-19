<?php
declare(strict_types=1);
if (PHP_SAPI !== 'cli') exit(1);
require __DIR__ . '/bootstrap.php';
$username = $argv[1] ?? '';
if (!preg_match('/^[a-zA-Z0-9._-]{3,100}$/', $username)) { fwrite(STDERR, "Uso: php create-admin.php usuario\n"); exit(1); }
if (!stream_isatty(STDIN)) { fwrite(STDERR, "Se requiere una terminal interactiva.\n"); exit(1); }
$sttyStatus = 1;
system('stty -echo', $sttyStatus);
if ($sttyStatus !== 0) { fwrite(STDERR, "No se pudo ocultar la contraseña.\n"); exit(1); }
fwrite(STDOUT, "Contraseña para $username: ");
try { $password = trim((string)fgets(STDIN)); }
finally { system('stty echo'); fwrite(STDOUT, "\n"); }
if (strlen($password) < 12) { fwrite(STDERR, "Mínimo 12 caracteres.\n"); exit(1); }
$stmt = dz_db()->prepare('INSERT INTO admin_users (username, password_hash) VALUES (?, ?)');
$stmt->execute([$username, password_hash($password, PASSWORD_DEFAULT)]);
fwrite(STDOUT, "Cuenta creada.\n");
