@echo off
cd /d "%~dp0"
if not exist .venv (py -m venv .venv)
call .venv\Scripts\activate
python -m pip install -r requirements.txt
if not exist .env (copy .env.example .env & echo IMPORTANTE: edita .env con contrasena y secreto seguros antes de usar admin.)
python -m uvicorn main:app --host 127.0.0.1 --port 8081
pause
