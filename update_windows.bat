@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM --- TinyAGI Windows Update Script ---
echo.
echo --- Welcome to TinyAGI Update ---
echo This script will update your TinyAGI installation to the latest version.
echo.

SET "INSTALL_PATH=C:\TinyAGI"

IF NOT EXIST "%INSTALL_PATH%" (
    echo Error: TinyAGI installation not found at '%INSTALL_PATH%'.
    echo Please run 'installation_windows.bat' first.
    GOTO EndScript
)

REM Change to the installation directory
CD /D "%INSTALL_PATH%"
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to change directory to %INSTALL_PATH%.
    GOTO EndScript
)

REM --- 1. Check for Git ---
echo Checking for Git installation...
git --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Git is not installed or not in your PATH.
    echo Please install Git from https://git-scm.com/downloads.
    GOTO EndScript
)
echo Git found.

REM --- 2. Pull latest changes from Git ---
echo.
echo Pulling latest changes from the repository...
git pull origin main
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to pull latest changes. Please check your internet connection or Git configuration.
    GOTO EndScript
)
echo Repository updated.

REM --- 3. Update dependencies and run post-install setup ---
echo.
echo Activating virtual environment and updating dependencies...
call ".\.venv\Scripts\activate.bat"
poetry install
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to update project dependencies.
    echo Please check pyproject.toml and your network connection.
    GOTO EndScript
)
poetry run python install.py

:EndScript
echo.
echo --- TinyAGI Update Complete! ---
echo Press any key to exit...
pause >nul
ENDLOCAL