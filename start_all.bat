@echo off
REM Script mejorado para iniciar TFG-Valorant
cd /d "%~dp0"
cls
color 0A

echo.
echo ====================================
echo   TFG-VALORANT - Iniciando Sistema
echo ====================================
echo.

REM Verificar carpeta backend
if not exist backend (
    color 0C
    echo ERROR: Carpeta 'backend' no encontrada
    pause
    exit /b 1
)

REM Verificar carpeta frontend
if not exist frontend (
    color 0C
    echo ERROR: Carpeta 'frontend' no encontrada
    pause
    exit /b 1
)

color 0A
echo [1/5] Preparando backend...

cd backend

REM Crear venv si no existe
if not exist venv (
    echo   Creating virtual environment...
    python -m venv venv
)

REM Activar venv
call venv\Scripts\activate.bat

REM Instalar dependencias
echo [2/5] Instalando dependencias...
pip install -q django djangorestframework django-cors-headers pillow requests >nul 2>&1
pip install -q -r requirements.txt >nul 2>&1
REM Migraciones
echo [3/5] Configurando base de datos...
python manage.py migrate --noinput >nul 2>&1

REM Cargar datos
echo [4/5] Cargando datos iniciales...
python manage.py shell -c "exec(open('tfg/seeders.py').read())" >nul 2>&1

REM Crear superuser admin automaticamente
echo   Creating admin user...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@test.com', 'admin123')" >nul 2>&1

REM Iniciar backend
echo [5/5] Iniciando servidores...
echo.
echo   Backend : http://localhost:8000
start "Django-Backend" cmd /k python manage.py runserver 0.0.0.0:8000

REM Esperar
timeout /t 3 /nobreak

REM Iniciar frontend
cd ..\frontend

REM Instalar npm deps si no existen
if not exist node_modules (
    echo    [AVISO] node_modules no encontrado. Instalando...
    echo    (Esto puede tardar unos minutos, por favor espere...)
    call npm install --silent >nul 2>&1
)

echo   Frontend: http://localhost:3000
start "React-Frontend" cmd /c "npm start"

cd ..\..

echo.
color 0B
echo ====================================
echo   Sistema iniciado correctamente
echo ====================================
echo.
echo URLs:
echo   Dashboard   : http://localhost:3000
echo   Admin Panel : http://localhost:8000/admin
echo   API         : http://localhost:8000/api
echo.
echo Credenciales Admin (Panel):
echo   Username: admin
echo   Password: admin123
echo.
echo Espere a que ambas ventanas muestren "Server running" y "Compiled successfully"
echo.
pause
exit /b 0