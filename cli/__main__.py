"""
CLI Demo module entry point.

This allows running the demo as:
- python -m cli
- uv run intentkit-demo (after installation)
"""

import asyncio
import sys

from main import main


def run_demo():
    """Entry point for the script command."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDemo terminated by user.")
        sys.exit(0)


if __name__ == "__main__":
    run_demo() 