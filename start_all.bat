@echo off
echo ====================================
echo   Iniciando backend y frontend...
echo ====================================


echo Activando entorno virtual...
cd backend
call venv\Scripts\activate

if exist ..\requirements.txt (
    echo Instalando dependencias de Python desde requirements.txt...
    pip install -r ..\requirements.txt
) else (
    echo No se encontro requirements.txt en la raiz del proyecto
)

echo Ejecutando makemigrations y migrate...
python manage.py makemigrations
python manage.py migrate

echo Ejecutando seeders...
python manage.py shell < tfg\seeders.py

echo Iniciando servidor Django...
start cmd /k "python manage.py runserver"
cd ..

echo Iniciando frontend con npm...
cd frontend

if exist package.json (
    echo Instalando dependencias de Node...
    call npm install
    call npm install react-slick slick-carousel
    echo Levantando frontend...
    start cmd /k "npm start"
) else (
    color 0C
    echo ERROR: No se encontro package.json en frontend\
    color 0A
)

cd ..
echo ====================================
echo   Backend y frontend iniciados...
echo ====================================
pause