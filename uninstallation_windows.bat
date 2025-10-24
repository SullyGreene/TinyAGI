@echo off
SETLOCAL

REM --- TinyAGI Windows Uninstallation Script ---
echo.
echo --- Welcome to TinyAGI Uninstallation ---
echo.
echo WARNING: This will permanently remove TinyAGI and all its files
echo from your system. This action cannot be undone.
echo.

SET "INSTALL_PATH=C:\TinyAGI"

IF NOT EXIST "%INSTALL_PATH%" (
    echo TinyAGI installation not found at '%INSTALL_PATH%'.
    echo Nothing to do.
    GOTO EndScript
)

SET /P "CONFIRM=Are you sure you want to uninstall TinyAGI from '%INSTALL_PATH%'? (y/n): "
IF /I NOT "%CONFIRM%"=="y" (
    echo Uninstallation cancelled.
    GOTO EndScript
)

echo.
echo Uninstalling TinyAGI...

REM --- 1. Remove the installation directory ---
echo Removing directory: %INSTALL_PATH%
rmdir /s /q "%INSTALL_PATH%"
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to remove the directory '%INSTALL_PATH%'.
    echo It might be in use by another program, or you may need to run this script as an administrator.
    GOTO EndScript
)

:EndScript
echo.
echo --- TinyAGI Uninstallation Complete! ---
echo.
echo IMPORTANT: If you previously added TinyAGI to your system PATH,
echo you will need to remove it manually from your Environment Variables.
echo.
echo Press any key to exit...
pause >nul
ENDLOCAL