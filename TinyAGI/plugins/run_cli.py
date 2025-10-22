import sys
import os

# Add the project root to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from TinyAGI.cli.app import CLI

if __name__ == "__main__":
    cli_app = CLI()
    cli_app.run()