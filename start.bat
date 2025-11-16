@echo off
REM Flusso RAG Demo - Windows Startup Script

echo ========================================
echo   Flusso RAG Demo - Starting Server
echo ========================================
echo.

REM Check if virtual environment exists
if exist venv\ (
    echo [*] Activating virtual environment...
    call venv\Scripts\activate
) else (
    echo [!] Virtual environment not found. Creating one...
    python -m venv venv
    call venv\Scripts\activate
    echo [*] Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo [*] Starting Flask server...
echo.
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

cd backend
python app.py

pause
