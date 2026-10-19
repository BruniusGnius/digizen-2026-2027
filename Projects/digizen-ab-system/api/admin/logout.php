<?php
declare(strict_types=1);
require __DIR__ . '/_load.php';
dz_admin_session();
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { http_response_code(405); exit('POST required'); }
dz_check_csrf();
$_SESSION = [];
session_destroy();
header('Location: /conversion-admin/login.php');
