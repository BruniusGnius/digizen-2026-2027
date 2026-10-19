-- Ejecutar únicamente en la base exclusiva u502287134_digizen_conv.
CREATE TABLE IF NOT EXISTS events (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  environment VARCHAR(20) NOT NULL DEFAULT 'production',
  event_name VARCHAR(100) NOT NULL,
  experiment_key VARCHAR(100) NOT NULL,
  visitor_id VARCHAR(100) NULL,
  lead_id BIGINT UNSIGNED NULL,
  landing_id VARCHAR(100) NOT NULL,
  variant CHAR(1) NOT NULL,
  path VARCHAR(255) NULL,
  section_id VARCHAR(100) NULL,
  section_label VARCHAR(255) NULL,
  cta VARCHAR(100) NULL,
  plan VARCHAR(50) NULL,
  device_type VARCHAR(20) NULL,
  utm_source VARCHAR(100) NULL,
  utm_medium VARCHAR(100) NULL,
  utm_campaign VARCHAR(150) NULL,
  utm_content VARCHAR(150) NULL,
  utm_term VARCHAR(150) NULL,
  payload JSON NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY idx_events_variant_created (variant, created_at),
  KEY idx_events_environment_created (environment, created_at),
  KEY idx_events_visitor (visitor_id),
  KEY idx_events_name_created (event_name, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS leads (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  environment VARCHAR(20) NOT NULL DEFAULT 'production',
  public_code CHAR(12) NOT NULL UNIQUE,
  name VARCHAR(150) NOT NULL,
  email VARCHAR(190) NULL,
  phone VARCHAR(50) NULL,
  preferred_channel VARCHAR(20) NOT NULL,
  marketing_consent TINYINT(1) NOT NULL DEFAULT 0,
  privacy_notice_version VARCHAR(50) NOT NULL,
  privacy_accepted_at DATETIME NOT NULL,
  interest VARCHAR(50) NOT NULL DEFAULT 'ada_demo',
  sales_stage VARCHAR(30) NOT NULL DEFAULT 'nuevo',
  demo_status VARCHAR(30) NOT NULL DEFAULT 'solicitado',
  demo_accessed_at DATETIME NULL,
  landing_id VARCHAR(100) NOT NULL,
  variant CHAR(1) NOT NULL,
  visitor_id VARCHAR(100) NULL,
  entry_url VARCHAR(500) NULL,
  referrer_url VARCHAR(500) NULL,
  referral_code VARCHAR(100) NULL,
  referred_by VARCHAR(150) NULL,
  utm_source VARCHAR(100) NULL,
  utm_medium VARCHAR(100) NULL,
  utm_campaign VARCHAR(150) NULL,
  utm_content VARCHAR(150) NULL,
  utm_term VARCHAR(150) NULL,
  assigned_to BIGINT UNSIGNED NULL,
  next_action_at DATETIME NULL,
  last_contact_at DATETIME NULL,
  acumbamail_status VARCHAR(30) NOT NULL DEFAULT 'not_applicable',
  acumbamail_attempts SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  acumbamail_next_retry_at DATETIME NULL,
  acumbamail_last_error VARCHAR(255) NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY idx_leads_created (created_at),
  KEY idx_leads_environment_created (environment, created_at),
  KEY idx_leads_variant (variant, created_at),
  KEY idx_leads_sales (sales_stage, next_action_at),
  KEY idx_leads_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS lead_notes (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  lead_id BIGINT UNSIGNED NOT NULL,
  admin_user_id BIGINT UNSIGNED NOT NULL,
  body TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY idx_notes_lead (lead_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS admin_users (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  can_export_notes TINYINT(1) NOT NULL DEFAULT 0,
  failed_attempts SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  locked_until DATETIME NULL,
  last_login_at DATETIME NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS admin_audit (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  admin_user_id BIGINT UNSIGNED NOT NULL,
  action VARCHAR(50) NOT NULL,
  detail JSON NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY idx_audit_user_created (admin_user_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Pagos en pausa: esquema reservado, sin endpoints de cobro activos.
CREATE TABLE IF NOT EXISTS checkout_sessions (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  stripe_session_id VARCHAR(255) NOT NULL UNIQUE,
  lead_id BIGINT UNSIGNED NULL,
  visitor_id VARCHAR(100) NULL,
  landing_id VARCHAR(100) NULL,
  variant CHAR(1) NULL,
  plan VARCHAR(50) NULL,
  student_count TINYINT UNSIGNED NULL,
  amount_total INT UNSIGNED NULL,
  currency CHAR(3) NULL,
  status VARCHAR(40) NOT NULL,
  metadata JSON NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS purchases (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  stripe_session_id VARCHAR(255) NOT NULL UNIQUE,
  lead_id BIGINT UNSIGNED NULL,
  plan VARCHAR(50) NULL,
  student_count TINYINT UNSIGNED NULL,
  amount_total INT UNSIGNED NULL,
  currency CHAR(3) NULL,
  status VARCHAR(40) NOT NULL,
  paid_at DATETIME NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Ledger inmutable de evidencia legal. Los consentimientos no se actualizan ni se
-- borran: cada aceptación, cambio o revocación genera un nuevo recibo.
CREATE TABLE IF NOT EXISTS consent_receipts (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  environment VARCHAR(20) NOT NULL DEFAULT 'production',
  subject_type VARCHAR(30) NOT NULL,
  lead_id BIGINT UNSIGNED NULL,
  checkout_session_id VARCHAR(255) NULL,
  visitor_id VARCHAR(100) NULL,
  document_type VARCHAR(40) NOT NULL,
  document_version VARCHAR(80) NOT NULL,
  document_url VARCHAR(500) NOT NULL,
  document_sha256 CHAR(64) NOT NULL,
  action VARCHAR(20) NOT NULL,
  categories_json JSON NULL,
  source VARCHAR(50) NOT NULL,
  landing_id VARCHAR(100) NULL,
  variant CHAR(1) NULL,
  entry_url VARCHAR(500) NULL,
  ip_proof_hmac CHAR(64) NULL,
  user_agent_hash CHAR(64) NULL,
  receipt_hmac CHAR(64) NOT NULL,
  created_at_utc DATETIME NOT NULL,
  KEY idx_consent_lead_created (lead_id, created_at_utc),
  KEY idx_consent_checkout_created (checkout_session_id, created_at_utc),
  KEY idx_consent_visitor_created (visitor_id, created_at_utc),
  KEY idx_consent_document_created (document_type, created_at_utc)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
