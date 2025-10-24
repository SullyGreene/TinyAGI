#!/bin/bash

echo ""
echo "--- Welcome to TinyAGI Unix/Linux Installation ---"
echo "This script will help you set up TinyAGI on your system."
echo ""

# --- 1. Check for Python ---
echo "Checking for Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed or not in your PATH."
    echo "Please install Python 3.9+ and try again."
    exit 1
fi
echo "Python 3 found."

# --- 2. Create a virtual environment ---
echo ""
echo "Creating a local virtual environment in ./.venv..."
python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create the virtual environment."
    exit 1
fi
echo "Virtual environment created."

# --- 3. Install Poetry into the virtual environment ---
echo ""
echo "Installing Poetry into the virtual environment..."
./.venv/bin/python -m pip install poetry
if [ $? -ne 0 ]; then
    echo "Error: Failed to install Poetry."
    exit 1
fi
echo "Poetry installed."

# --- 4. Install project dependencies and run setup ---
echo ""
echo "Installing project dependencies and finalizing setup..."
source ./.venv/bin/activate
poetry install
poetry run python install.py