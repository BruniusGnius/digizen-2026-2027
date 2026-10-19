<?php
declare(strict_types=1);
if (PHP_SAPI !== 'cli') exit(1);
require __DIR__ . '/bootstrap.php';
require __DIR__ . '/Acumbamail.php';
$stmt = dz_db()->query("SELECT id FROM leads WHERE acumbamail_status IN ('pending', 'retry')
    AND (acumbamail_next_retry_at IS NULL OR acumbamail_next_retry_at <= NOW())
    AND acumbamail_attempts < 8 ORDER BY id LIMIT 50");
foreach ($stmt->fetchAll(PDO::FETCH_COLUMN) as $id) {
    try { dz_sync_acumbamail((int)$id); }
    catch (Throwable $e) {
        error_log('[digizen-acumbamail] ' . $e->getMessage());
        $update = dz_db()->prepare("UPDATE leads SET acumbamail_status = 'retry',
            acumbamail_attempts = acumbamail_attempts + 1,
            acumbamail_next_retry_at = DATE_ADD(NOW(), INTERVAL 30 MINUTE),
            acumbamail_last_error = 'connection_error' WHERE id = ?");
        $update->execute([(int)$id]);
    }
}
