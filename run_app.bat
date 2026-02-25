@echo off
setlocal

REM Change to the directory of this script
cd /d "%~dp0"

REM Name of the virtual environment folder
set VENV_DIR=venv

REM Check if virtual environment exists
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo Creating virtual environment...
    py -m venv "%VENV_DIR%" 2>nul
    if errorlevel 1 (
        echo "py" launcher not found or venv creation failed, trying "python"...
        python -m venv "%VENV_DIR%"
        if errorlevel 1 (
            echo Failed to create virtual environment. Make sure Python is installed and on PATH.
            pause
            exit /b 1
        )
    )
)

REM Activate virtual environment
call "%VENV_DIR%\Scripts\activate.bat"

REM Install dependencies
if exist "requirements.txt" (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
) else (
    echo requirements.txt not found. Installing Flask directly...
    pip install flask
)

REM Run the Flask app
echo Starting app.py...
python app.py

echo.
echo Application stopped.
pause

endlocal
