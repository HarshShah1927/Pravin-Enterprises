@echo off
setlocal enabledelayedexpansion

REM Change into project root directory
cd /d "%~dp0"

REM Create virtual environment if missing
if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment for this script
call "venv\Scripts\activate.bat"

REM Install dependencies only when Django is not present
python -c "import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('django') else 1)" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
)

REM Create .env from example when missing
if not exist ".env" (
    echo Creating .env from .env.example...
    copy /Y .env.example .env >nul
    echo Please review and update .env with your Twilio/Email credentials before continuing.
)

echo Applying database migrations...
python manage.py migrate

echo Starting Django development server...
python manage.py runserver
