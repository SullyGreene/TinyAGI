# install.py
import subprocess
import sys
import os
import shutil

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
    print("--- TinyAGI Post-Install Setup ---")

    _setup_env_file()

    print("\n--- TinyAGI Setup Complete! ---")
    if sys.platform == "win32":
        print("You can now run the CLI with: cli.bat")
        print("Or start the server with: start_server.bat")
    else:
        print("You can now run the CLI with: poetry run cli")
        print("Or start the server with: poetry run start")
    print("Remember to configure your .env file with necessary API keys.")

if __name__ == "__main__":
    main()
