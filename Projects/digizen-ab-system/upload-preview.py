#!/usr/bin/env python3
"""Sincroniza solo la demostración pública al subdominio nuevo; dry-run por defecto."""
from pathlib import Path
import argparse
import re
import shlex
import subprocess

HERE = Path(__file__).resolve().parent
ENV = HERE.parent / 'digizen-ab-testing/.env'
SOURCE = HERE / 'preview-package/public'
TARGET = '/home/u502287134/domains/gnius.club/public_html/digizen-demo/'
KEY = HERE / '.ssh/digizen_demo_ed25519'


def env_values():
    values = {}
    for line in ENV.read_text().splitlines():
        if line.strip() and not line.lstrip().startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Transfiere después de revisar el dry-run')
    args = parser.parse_args()
    values = env_values()
    host, port, user = (values.get('SSH_HOST', ''), values.get('SSH_PORT', ''), values.get('SSH_USER', ''))
    if not re.fullmatch(r'[a-zA-Z0-9.-]+', host) or not port.isdigit() or not re.fullmatch(r'[a-zA-Z0-9_-]+', user):
        raise SystemExit('SSH_HOST, SSH_PORT o SSH_USER no válidos en .env')
    if not (SOURCE / 'index.html').is_file() or not (SOURCE / 'api/leads.php').is_file():
        raise SystemExit('Ejecuta preview.py antes de sincronizar')
    if not KEY.is_file():
        raise SystemExit('Falta la clave SSH local exclusiva de digizen-demo')
    if 'digizen-demo.gnius.club' not in (SOURCE / 'api/leads.php').read_text():
        raise SystemExit('La API local no corresponde al subdominio de pruebas')
    remote = f'{user}@{host}'
    ssh = ['ssh', '-i', str(KEY), '-o', 'IdentitiesOnly=yes',
           '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes', '-p', port, remote]
    check = subprocess.run(ssh + ['test', '-d', TARGET.rstrip('/')])
    if check.returncode:
        raise SystemExit('No se pudo comprobar por SSH la carpeta exacta de pruebas. No se transfirió nada.')
    command = ['rsync', '-av', '--itemize-changes', '--no-perms', '--no-owner', '--no-group']
    if not args.apply:
        command.append('--dry-run')
    transport = 'ssh -i ' + shlex.quote(str(KEY)) + ' -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=yes -p ' + port
    command += ['-e', transport, str(SOURCE) + '/', f'{remote}:{TARGET}']
    print('Destino único:', TARGET, flush=True)
    print('Modo:', 'TRANSFERENCIA' if args.apply else 'DRY-RUN', flush=True)
    result = subprocess.run(command)
    if result.returncode:
        raise SystemExit('rsync terminó con error; revisa la salida. No se tocó /digizen.')
    if not args.apply:
        print('Revisa el manifiesto. Para transferir, repite con --apply.')
    else:
        print('Transferencia completada al subdominio de pruebas. Verifica /api/health.php.')


if __name__ == '__main__':
    main()
