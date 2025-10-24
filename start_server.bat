@echo off
REM --- TinyAGI Server Launcher for Windows ---
echo Starting TinyAGI Server...

call .\.venv\Scripts\activate.bat
poetry run start %*