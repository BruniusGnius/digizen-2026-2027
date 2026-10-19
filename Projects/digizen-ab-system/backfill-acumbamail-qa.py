#!/usr/bin/env python3
"""Completa solo cuatro contactos QA existentes de Acumbamail.

Requiere que el webhook mapee update_subscriber -> update_subscriber.
Sin --send no realiza llamadas.
"""
from pathlib import Path
from urllib.parse import urlparse
import argparse
import json
import subprocess


ENV = Path(__file__).resolve().parents[1] / 'digizen-ab-testing/.env'
CONTACTS = (
    ('bruno+ada_a_qa@gnius.club', 'QA ADA A', 'A', 'qa_ab_2026_10'),
    ('bruno+acumbamail_webhook_qa3@gnius.club', 'DIGIZEN QA', 'A', 'qa_webhook'),
    ('bruno+acumbamail_webhook_qa2@gnius.club', 'DIGIZEN QA', 'A', 'qa_webhook'),
    ('bruno+acumbamail_webhook_qa@gnius.club', 'DIGIZEN QA', 'A', 'qa_webhook'),
)


def webhook_url() -> str:
    for line in ENV.read_text().splitlines():
        if line.startswith('ACUMBAMAIL_INBOUND_WEBHOOK_URL='):
            url = line.split('=', 1)[1].strip().strip('"').strip("'")
            parsed = urlparse(url)
            if parsed.scheme != 'https' or not parsed.netloc:
                raise SystemExit('El webhook privado no tiene una URL HTTPS válida')
            return url
    raise SystemExit('Falta el webhook privado en .env')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--send', action='store_true', help='Actualiza los cuatro contactos QA')
    args = parser.parse_args()
    print('Contactos QA:', len(CONTACTS))
    for email, nombre, variante, utm_source in CONTACTS:
        print(email, '|', nombre, '|', variante, '|', utm_source)
    if not args.send:
        print('Solo revisión: no se envió ninguna solicitud.')
        return
    url = webhook_url()
    for email, nombre, variante, utm_source in CONTACTS:
        payload = {
            'email': email, 'nombre': nombre, 'variante_ab': variante,
            'utm_source': utm_source, 'list_id': '1544280',
            'double_optin': 0, 'welcome_email': 0, 'update_subscriber': 1,
        }
        response = subprocess.run([
            'curl', '--silent', '--show-error', '--max-time', '12', '--proto', '=https',
            '--request', 'POST', '--header', 'Content-Type: application/json',
            '--data-binary', '@-', '--write-out', '\n%{http_code}', url,
        ], input=json.dumps(payload), text=True, capture_output=True, timeout=15)
        if response.returncode:
            print(email, '| curl_error', response.returncode)
            raise SystemExit(1)
        raw, status_text = response.stdout.rsplit('\n', 1)
        try:
            data = json.loads(raw)
            if isinstance(data, str):
                data = json.loads(data)
        except (ValueError, TypeError):
            data = None
        ok = (int(status_text) in (200, 201) and isinstance(data, dict)
              and str(data.get('email', '')).lower() == email.lower()
              and data.get('id') is not None)
        print(email, '| HTTP', status_text, '| response_valid', ok)
        if not ok:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
