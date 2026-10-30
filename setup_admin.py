import secrets
from pathlib import Path
from getpass import getpass
from passlib.hash import pbkdf2_sha256
p=Path(__file__).resolve().parent/'.env'
if p.exists():
    print('Ya existe .env. No se sobrescribirá para proteger tu configuración.')
    raise SystemExit(1)
username=input('Usuario administrador [admin]: ').strip() or 'admin'
password=getpass('Contraseña nueva (mínimo 12 caracteres): ')
if len(password)<12: raise SystemExit('Contraseña demasiado corta')
secret=secrets.token_urlsafe(48)
lines=['CLUB_NAME=Los Intocables','REFRESH_MINUTES=5','PORT=8080',f'ADMIN_USERNAME={username}',f'ADMIN_PASSWORD_HASH={pbkdf2_sha256.hash(password)}',f'SESSION_SECRET={secret}','COOKIE_SECURE=false']
p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Archivo .env creado. No lo compartas ni lo subas a GitHub.')
