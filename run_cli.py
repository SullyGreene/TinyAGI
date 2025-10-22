# run_cli.py
import subprocess
import sys

def main():
    """Runs the CLI application using 'poetry run cli'."""
    command = ["poetry", "run", "cli"] + sys.argv[1:]
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print("Error: 'poetry' command not found.", file=sys.stderr)
        print("Please ensure Poetry is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        # The error from the CLI itself will be printed, so we just exit.
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
