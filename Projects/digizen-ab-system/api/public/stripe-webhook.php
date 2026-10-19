<?php
declare(strict_types=1);
header('Cache-Control: no-store');
http_response_code(503);
// Pagos pausados por decisión del usuario. No procesar eventos sin configuración aprobada.
