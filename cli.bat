@echo off
REM --- TinyAGI CLI Launcher for Windows ---
echo Starting TinyAGI Interactive CLI...
echo Type 'help' for a list of commands or 'exit' to quit.

call .\.venv\Scripts\activate.bat
poetry run cli %*