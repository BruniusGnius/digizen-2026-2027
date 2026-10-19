#!/usr/bin/env python3
"""Servidor de prueba local: archivos de staging y API simulada en memoria."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import json
import re
import secrets

ROOT = Path(__file__).resolve().parent / 'staging'
EXPERIMENT = 'digizen_landing_ab_2026_10'
DEMO_URL = 'https://ada-demo.example/'


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if urlsplit(self.path).path.endswith('.php'):
            return self.reply(404, {'ok': False, 'error': 'not_found'})
        return super().do_GET()

    def do_POST(self):
        path = urlsplit(self.path).path
        if path not in ('/api/leads.php', '/api/events.php'):
            return self.reply(404, {'ok': False, 'error': 'not_found'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length <= 0 or length > 32_768:
                raise ValueError('invalid_length')
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict):
                raise ValueError('invalid_body')
        except (ValueError, json.JSONDecodeError):
            return self.reply(400, {'ok': False, 'error': 'invalid_json'})
        if path == '/api/events.php':
            return self.reply(202, {'ok': True, 'simulated': True})
        if body.get('experiment_key') != EXPERIMENT or body.get('variant') not in ('A', 'B'):
            return self.reply(422, {'ok': False, 'error': 'invalid_experiment'})
        name = body.get('name')
        email = body.get('email')
        phone = body.get('phone')
        channel = body.get('preferred_channel')
        if not isinstance(name, str) or not name.strip() or not (email or phone):
            return self.reply(422, {'ok': False, 'error': 'name_and_contact_required'})
        if channel not in ('correo', 'whatsapp') or (channel == 'correo' and not email) or (channel == 'whatsapp' and not phone):
            return self.reply(422, {'ok': False, 'error': 'invalid_channel'})
        if email and (not isinstance(email, str) or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email)):
            return self.reply(422, {'ok': False, 'error': 'invalid_email'})
        if phone and (not isinstance(phone, str) or not re.fullmatch(r'\+?[0-9\s()\-]{8,30}', phone)):
            return self.reply(422, {'ok': False, 'error': 'invalid_phone'})
        if body.get('terms_accepted') is not True or body.get('privacy_accepted') is not True or not isinstance(body.get('marketing_consent'), bool):
            return self.reply(422, {'ok': False, 'error': 'legal_consent_required'})
        return self.reply(201, {
            'ok': True, 'simulated': True, 'demo_simulated': True,
            'lead_id': secrets.randbelow(900000) + 100000,
            'public_code': secrets.token_hex(6).upper(),
            'demo_url': DEMO_URL,
        })

    def reply(self, status, body):
        payload = json.dumps(body).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        # No registrar nombres, correos, teléfonos ni cuerpos de solicitud.
        pass


if __name__ == '__main__':
    if not (ROOT / 'index.html').is_file():
        raise SystemExit('Primero ejecuta stage.py para crear staging/ local.')
    server = ThreadingHTTPServer(('127.0.0.1', 8765), Handler)
    print('Simulación local: http://127.0.0.1:8765/ (Ctrl+C para detener)')
    server.serve_forever()
