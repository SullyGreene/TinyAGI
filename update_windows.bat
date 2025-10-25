@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM --- TinyAGI Windows Update Script ---
echo.
echo --- Welcome to TinyAGI Update ---
echo This script will update your TinyAGI installation to the latest version.
echo.

REM --- 1. Locate Installation and Change Directory ---
SET "INSTALL_PATH=%~dp0"
CD /D "%INSTALL_PATH%"

IF NOT EXIST ".venv" (
    echo Error: Could not find the '.venv' directory.
    echo Please run this script from the root of your TinyAGI installation folder.
    GOTO EndScript
)

REM --- 2. Prerequisites Check ---
echo Checking for Git installation...
git --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Git is not installed or not in your PATH.
    echo Please install Git from https://git-scm.com/downloads.
    GOTO EndScript
)
echo Git found.

echo.
echo --- 3. Fetch Latest Version from Repository ---
echo Pulling latest changes from the repository...
echo Fetching latest version from the 'main' branch...
git fetch origin main
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to fetch updates from the repository. Please check your internet connection or Git configuration.
    GOTO EndScript
)

echo.
echo WARNING: The next step will overwrite any local changes to repository files (like agents, tools, or core code).
echo Untracked files (like your .env file or custom configs) will NOT be affected.
echo.
SET /P "CONFIRM=Are you sure you want to proceed with the update? (y/n): "
IF /I NOT "%CONFIRM%"=="y" (
    echo Update cancelled by user.
    GOTO EndScript
)

echo.
echo Forcing update to the latest version...
git reset --hard origin/main
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to reset the repository to the latest version.
    GOTO EndScript
)
echo Repository successfully updated to the latest version.

echo. 
echo --- 4. Update Dependencies & Finalize ---
echo Activating virtual environment and updating dependencies...

REM Remove the lock file to force dependency re-resolution from pyproject.toml
IF EXIST "poetry.lock" (
    echo Removing old poetry.lock file...
    del poetry.lock
)

call .\.venv\Scripts\activate.bat
poetry install
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to update project dependencies.
    echo Please check pyproject.toml and your network connection.
    GOTO EndScript
)
echo Dependencies are up to date.

echo.
echo Running post-update setup...
poetry run python install.py

:EndScript
echo.
echo --- TinyAGI Update Successfully Completed! ---
echo Press any key to exit...
pause >nul
ENDLOCAL