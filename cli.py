#!/usr/bin/env python

# MIT License
# Copyright (c) 2025 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# cli.py

from TinyAGI.cli.ui import run_cli_ui

if __name__ == '__main__':
    try:
        run_cli_ui()
    except KeyboardInterrupt:
        print("\nExiting CLI. Goodbye!")
