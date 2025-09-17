@echo off
echo ====================================
echo   Iniciando backend y frontend...
echo ====================================


:: --- Backend ---
echo Activando entorno virtual...
cd backend
call venv\Scripts\activate

:: Instalar requirements desde la raíz
if exist ..\requirements.txt (
    echo Instalando dependencias de Python desde requirements.txt...
    pip install -r ..\requirements.txt
) else (
    echo No se encontro requirements.txt en la raiz del proyecto
)

:: Migraciones
echo Ejecutando makemigrations y migrate...
python manage.py makemigrations
python manage.py migrate

:: Poblar la base de datos con seeders
echo Ejecutando seeders...
python manage.py shell < tfg\seeders.py

:: Levantar backend en nueva ventana
echo Iniciando servidor Django...
start cmd /k "python manage.py runserver"
cd ..

:: --- Frontend ---
echo Iniciando frontend con npm...
cd frontend

if exist package.json (
    echo Instalando dependencias de Node...
    call npm install
    echo Levantando frontend...
    start cmd /k "npm start"
) else (
    color 0C
    echo ERROR: No se encontro package.json en frontend\
    color 0A
)

cd ..

echo ====================================
echo   Todo listo: backend y frontend arriba
echo ====================================
pause