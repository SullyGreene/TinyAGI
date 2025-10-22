# install.py
import subprocess
import sys
import os
import shutil

def _check_poetry_installed():
    """Checks if Poetry is installed and available in PATH."""
    print("Checking for Poetry installation...")
    try:
        subprocess.run(["poetry", "--version"], check=True, capture_output=True)
        print("Poetry is installed.")
        return True
    except FileNotFoundError:
        print("Error: 'poetry' command not found.", file=sys.stderr)
        print("Please ensure Poetry is installed and in your PATH.", file=sys.stderr)
        print("Installation guide: https://python-poetry.org/docs/#installation", file=sys.stderr)
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error checking Poetry version: {e}", file=sys.stderr)
        print(e.stderr.decode(), file=sys.stderr)
        return False

def _install_dependencies():
    """Installs project dependencies using Poetry."""
    print("\nInstalling project dependencies with Poetry...")
    try:
        subprocess.run(["poetry", "install"], check=True)
        print("Dependencies installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during dependency installation: {e}", file=sys.stderr)
        print(e.stderr.decode(), file=sys.stderr)
        return False

def _download_nltk_data():
    """Runs the download_nltk.py script if it exists."""
    nltk_script_path = os.path.join(os.path.dirname(__file__), "download_nltk.py")
    if os.path.exists(nltk_script_path):
        print("\nDownloading NLTK data (if required)...")
        try:
            # Use poetry run python to ensure it uses the project's virtual environment
            subprocess.run(["poetry", "run", "python", nltk_script_path], check=True)
            print("NLTK data download script executed.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error downloading NLTK data: {e}", file=sys.stderr)
            print(e.stderr.decode(), file=sys.stderr)
            return False
    else:
        print("\n'download_nltk.py' not found. Skipping NLTK data download step.")
        return True # Not a critical error if the script is missing

def _setup_env_file():
    """Copies .env.example to .env if .env does not exist."""
    env_example_path = os.path.join(os.path.dirname(__file__), ".env.example")
    env_path = os.path.join(os.path.dirname(__file__), ".env")

    if os.path.exists(env_example_path):
        if not os.path.exists(env_path):
            print("\nSetting up .env file...")
            try:
                shutil.copyfile(env_example_path, env_path)
                print(f"'{env_example_path}' copied to '{env_path}'.")
                print("Please edit your .env file with your API keys and configurations.")
                return True
            except Exception as e:
                print(f"Error copying .env.example to .env: {e}", file=sys.stderr)
                return False
        else:
            print("\n'.env' file already exists. Skipping .env setup.")
            return True
    else:
        print("\n'.env.example' not found. Skipping .env setup.")
        return True # Not a critical error if the example file is missing

def main():
    """Orchestrates the installation process for TinyAGI."""
    print("--- TinyAGI Installation Script ---")

    if not _check_poetry_installed():
        sys.exit(1)

    if not _install_dependencies():
        sys.exit(1)

    # NLTK data download is optional/context-dependent, so we don't exit on failure here
    _download_nltk_data() 

    if not _setup_env_file():
        sys.exit(1)

    print("\n--- TinyAGI Installation Complete! ---")
    print("You can now run the CLI with: poetry run cli")
    print("Or start the server with: poetry run start")
    print("Remember to configure your .env file with necessary API keys.")

if __name__ == "__main__":
    main()
