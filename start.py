# start.py
import subprocess
import sys
from dotenv import load_dotenv

load_dotenv()

def main():
    """Starts the application using 'poetry run start'."""
    print("Starting the application...")
    try:
        subprocess.run(["poetry", "run", "start"], check=True)
    except FileNotFoundError:
        print("Error: 'poetry' command not found.", file=sys.stderr)
        print("Please ensure Poetry is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error starting application: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
