#!/usr/bin/env python3
"""Valida variables locales sin imprimir valores ni copiar secretos."""
from pathlib import Path
from urllib.parse import urlparse

env = Path(__file__).resolve().parents[1] / 'digizen-ab-testing/.env'
if not env.is_file():
    raise SystemExit('Falta .env local de digizen-ab-testing')
values = {}
for line in env.read_text().splitlines():
    line = line.strip()
    if not line or line.startswith('#') or '=' not in line:
        continue
    key, value = line.split('=', 1)
    values[key.strip()] = value.strip().strip('"').strip("'")

required = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'ACUMBAMAIL_INBOUND_WEBHOOK_URL']
missing = [key for key in required if not values.get(key)]
if missing:
    raise SystemExit('Variables pendientes: ' + ', '.join(missing))
if values['DB_HOST'] != 'localhost' or values['DB_NAME'] != 'u502287134_digizen_conv':
    raise SystemExit('Host o base MySQL no coinciden con la configuración validada')
if urlparse(values['ACUMBAMAIL_INBOUND_WEBHOOK_URL']).scheme != 'https':
    raise SystemExit('El webhook de Acumbamail debe usar HTTPS')
print('Configuración local: MySQL y webhook presentes; no se mostraron valores privados.')
print('ADA real, versión del aviso de privacidad y pruebas PHP/MySQL siguen pendientes.')
