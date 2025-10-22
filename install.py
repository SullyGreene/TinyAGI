# install.py
import subprocess
import sys

def main():
    """Installs dependencies using Poetry."""
    print("Installing dependencies with Poetry...")
    try:
        subprocess.run(["poetry", "install"], check=True)
        print("Installation complete.")
    except FileNotFoundError:
        print("Error: 'poetry' command not found.", file=sys.stderr)
        print("Please ensure Poetry is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error during installation: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
