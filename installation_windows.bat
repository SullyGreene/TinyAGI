@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM --- TinyAGI Windows Installation Script ---
echo.
echo --- Welcome to TinyAGI Windows Installation ---
echo This script will download and set up TinyAGI on your system.
echo.

REM --- 1. Prerequisites Check ---
echo Checking for Git installation...
git --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Git is not installed or not in your PATH.
    echo Please install Git from https://git-scm.com/downloads and ensure it's added to your PATH.
    GOTO EndScript
)
echo Git found.

echo.
echo Checking for Python installation...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in your PATH.
    echo Please install Python 3.9+ from https://www.python.org/downloads/ and ensure it's added to your PATH.
    GOTO EndScript
)
echo Python found.

REM --- 2. Clone Repository ---
SET "INSTALL_PATH=C:\TinyAGI"
SET "REPO_URL=https://github.com/SullyGreene/TinyAGI.git"
echo.
echo Cloning TinyAGI into %INSTALL_PATH%...
IF EXIST "%INSTALL_PATH%" (
    echo Error: The directory %INSTALL_PATH% already exists.
    echo Please remove it or back it up before running this script.
    GOTO EndScript
)
git clone %REPO_URL% "%INSTALL_PATH%"
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to clone the repository. Please check your internet connection and Git setup.
    GOTO EndScript
)
echo Repository cloned successfully.

REM Change to the installation directory for all subsequent operations
CD /D "%INSTALL_PATH%"

REM --- 3. Environment Setup ---
echo.
echo Creating a local virtual environment in .\.venv...
python -m venv .venv
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to create the virtual environment.
    GOTO EndScript
)
echo Virtual environment created.

REM --- 4. Install Poetry & Dependencies ---
echo.
echo Installing Poetry into the virtual environment...
.\.venv\Scripts\python.exe -m pip install poetry
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install Poetry.
    GOTO EndScript
)
echo.
echo Installing project dependencies...
call .\.venv\Scripts\activate.bat
poetry install
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install project dependencies.
    echo Please check pyproject.toml and your network connection.
    GOTO EndScript
)

REM --- 5. Finalize Setup ---
echo.
echo Finalizing setup...
poetry run python install.py
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Finalization script failed.
    GOTO EndScript
)

REM --- 6. Create 'agi' Alias and Add to PATH ---
echo.
SET /P "ADD_TO_PATH=Do you want to add '%INSTALL_PATH%' to your user PATH environment variable? (y/n): "
IF /I "%ADD_TO_PATH%"=="y" (
    echo Adding '%INSTALL_PATH%' to user PATH...
    setx PATH "%PATH%;%INSTALL_PATH%"
    IF %ERRORLEVEL% NEQ 0 (
        echo Warning: Failed to automatically add to PATH. You may need to do this manually.
    ) ELSE (
        echo Successfully added to user PATH.
        echo Please open a NEW terminal for the 'agi' command to be available.
    )
)

echo.
:EndScript
echo --- TinyAGI Installation Complete! ---
echo You can now run the CLI by navigating to '%INSTALL_PATH%' and running 'cli.bat'.
echo If you added to PATH, open a new terminal and simply type 'agi'.
echo Remember to configure your .env file in '%INSTALL_PATH%' with necessary API keys.
echo.
echo Press any key to exit...
pause >nul
ENDLOCAL