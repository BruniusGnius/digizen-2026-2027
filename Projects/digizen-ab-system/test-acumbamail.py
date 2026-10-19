#!/usr/bin/env python3
"""Prueba controlada del webhook de entrada; nunca imprime su URL ni la respuesta completa."""
from pathlib import Path
from urllib.parse import urlparse
import argparse
import json
import re
import subprocess

ENV = Path(__file__).resolve().parents[1] / 'digizen-ab-testing/.env'


def webhook_url() -> str:
    for line in ENV.read_text().splitlines():
        if line.startswith('ACUMBAMAIL_INBOUND_WEBHOOK_URL='):
            url = line.split('=', 1)[1].strip().strip('"').strip("'")
            if urlparse(url).scheme != 'https':
                raise SystemExit('El webhook privado no tiene HTTPS')
            return url
    raise SystemExit('Falta el webhook privado en .env')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--email', help='Correo de prueba bajo control del usuario')
    parser.add_argument('--variant', choices=['A', 'B'], default='A')
    parser.add_argument('--send', action='store_true', help='Envía un único POST real a Acumbamail')
    args = parser.parse_args()
    url = webhook_url()
    payload = {
        'email': args.email, 'nombre': 'DIGIZEN QA', 'variante_ab': args.variant,
        'utm_source': 'qa_webhook', 'list_id': '1544280',
        'double_optin': 0, 'welcome_email': 0, 'update_subscriber': 0,
    }
    print('Webhook HTTPS configurado. Campos:', ', '.join(payload.keys()))
    if not args.send:
        print('Solo revisión local; no se envió ningún contacto.')
        return
    if not args.email or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', args.email):
        raise SystemExit('Para --send indica un correo de prueba válido con --email')
    try:
        response = subprocess.run([
            'curl', '--silent', '--show-error', '--max-time', '12',
            '--proto', '=https', '--request', 'POST',
            '--header', 'Content-Type: application/json',
            '--data-binary', '@-', '--write-out', '\n%{http_code}', url,
        ], input=json.dumps(payload), text=True, capture_output=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired) as error:
        print('No se pudo completar la conexión:', type(error).__name__)
        return
    if response.returncode != 0:
        print('No se pudo completar la conexión; código curl:', response.returncode)
        return
    raw, status_text = response.stdout.rsplit('\n', 1)
    status = int(status_text)
    if status not in (200, 201):
        print('Acumbamail respondió HTTP', status, '(cuerpo omitido para proteger datos).')
        return
    try:
        body = json.loads(raw)
    except (ValueError, json.JSONDecodeError):
        print('Acumbamail devolvió una respuesta no JSON.')
        return
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except ValueError:
            body = None
    valid = (isinstance(body, dict) and body.get('id') is not None
             and str(body.get('email', '')).lower() == args.email.lower())
    print('HTTP:', status, '| alta confirmada:', valid, '| id devuelto:', isinstance(body, dict) and body.get('id') is not None)


if __name__ == '__main__':
    main()
