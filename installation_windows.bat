@echo off
SETLOCAL

REM --- TinyAGI Windows Installation Script ---
echo.
echo --- Welcome to TinyAGI Windows Installation ---
echo This script will help you set up TinyAGI on your system.
echo.

REM 1. Check for Python
echo Checking for Python installation...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in your PATH.
    echo Please install Python 3.8+ from https://www.python.org/downloads/ and ensure it's added to your PATH during installation.
    echo Exiting installation.
    GOTO :EOF
)
echo Python found.

REM 2. Check for Poetry
echo.
echo Checking for Poetry installation...
poetry --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Poetry is not installed or not in your PATH.
    echo Please install Poetry by running:
    echo   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
    echo Or visit: https://python-poetry.org/docs/#installation
    echo After installing Poetry, please restart your terminal and run this script again.
    echo Exiting installation.
    GOTO :EOF
)
echo Poetry found.

REM 3. Run the main install.py script
echo.
echo Running the main TinyAGI setup script (install.py)...
echo This will install dependencies, download NLTK data, and set up your .env file.

REM Use 'poetry run python' to ensure install.py runs within the Poetry virtual environment
poetry run python install.py

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo An error occurred during the TinyAGI setup. Please review the messages above.
) ELSE (
    echo.
    echo --- TinyAGI Installation Complete! ---
    echo You can now run the CLI with: poetry run cli
    echo Or start the server with: poetry run start
    echo Remember to configure your .env file with necessary API keys.
)

echo.
echo Press any key to exit.
pause >nul
ENDLOCAL