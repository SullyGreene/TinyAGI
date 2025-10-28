@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM --- TinyAGI Full Suite Installer (Core Engine + Web UI) ---
echo.
echo --- TinyAGI Full Suite Installer ---
echo This script will install the core TinyAGI engine and the Streamlit Web UI.
echo It assumes you have already cloned the TinyAGI repository.
echo.

REM --- 1. Define Paths ---
SET "TINYAGI_DIR=%~dp0"
SET "UI_REPO_URL=https://github.com/SullyGreene/TinyAGI-Hub-Streamlit.git"
SET "TEMP_UI_DIR=%TINYAGI_DIR%temp_ui_source"

REM --- 2. Run the Core TinyAGI Installation ---
echo.
echo --- Step 1: Installing Core TinyAGI Engine ---
IF NOT EXIST "%TINYAGI_DIR%install.bat" (
    echo Error: 'install.bat' not found. This script must be run from the root of the TinyAGI repository.
    GOTO EndScript
)
call "%TINYAGI_DIR%install.bat"
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Core TinyAGI installation failed. Aborting.
    GOTO EndScript
)
echo --- Core TinyAGI Engine Installed Successfully ---
echo.

REM --- 3. Clone the Web UI Repository ---
echo.
echo --- Step 2: Downloading Web UI Source ---
echo Cloning Web UI repository into a temporary folder...
rmdir /s /q "%TEMP_UI_DIR%" >nul 2>&1
git clone %UI_REPO_URL% "%TEMP_UI_DIR%"
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to clone the Web UI repository. Please check your internet connection.
    GOTO EndScript
)
echo Web UI source downloaded.
echo.

REM --- 4. Run the Web UI Installer ---
echo.
echo --- Step 3: Installing Web UI into TinyAGI ---
IF NOT EXIST "%TEMP_UI_DIR%\install_ui.bat" (
    echo Error: 'install_ui.bat' not found in the downloaded UI repository.
    GOTO Cleanup
)
call "%TEMP_UI_DIR%\install_ui.bat"
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Web UI installation failed.
    GOTO Cleanup
)

:Cleanup
echo.
echo --- Step 4: Cleaning up temporary files ---
rmdir /s /q "%TEMP_UI_DIR%"
echo Cleanup complete.

:EndScript
echo.
echo --- TinyAGI Full Suite Installation Complete! ---
echo You can run the CLI with 'cli.bat' or the Web UI with 'start_web_ui.bat'.
echo.
echo Press any key to exit...
pause >nul
ENDLOCAL