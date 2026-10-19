<?php
declare(strict_types=1);
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$home = getenv('DIGIZEN_API_HOME') ?: '/home/u502287134/digizen-conversion-api';
require_once $home . '/src/bootstrap.php';
