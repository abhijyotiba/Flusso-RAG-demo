@echo off
REM Quick deployment script for Render

echo ========================================
echo   Flusso RAG Demo - GitHub Setup
echo ========================================
echo.

echo This script will help you push the code to GitHub
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/5] Initializing Git repository...
git init

echo.
echo [2/5] Adding files...
git add .

echo.
echo [3/5] Creating initial commit...
git commit -m "Initial commit - Flusso RAG Demo for Render deployment"

echo.
echo ========================================
echo   Next Steps:
echo ========================================
echo.
echo 1. Create a new repository on GitHub:
echo    https://github.com/new
echo.
echo 2. Name it: flusso-rag-demo (or your choice)
echo.
echo 3. Make it Private (recommended)
echo.
echo 4. DON'T initialize with README
echo.
echo 5. After creating, run these commands:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/flusso-rag-demo.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo ========================================
echo.

pause
