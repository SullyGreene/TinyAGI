@echo off
REM --- TinyAGI Virtual Environment Activator ---
echo.
echo Activating the TinyAGI virtual environment...
echo You can now run commands like 'pip install --upgrade pip' or 'poetry update'.
echo Type 'exit' to leave the virtual environment and close this window.
echo.

REM Start a new command prompt session and run the activate script within it.
REM The /K switch keeps the command prompt open after activation.
cmd /K "%~dp0.venv\Scripts\activate.bat"
