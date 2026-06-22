"""Entry-point dispatcher for the graph-based-code-analyzer pipeline."""
from __future__ import annotations

import sys


def main() -> int:
    from src.cli import CLIMenu

    CLIMenu().start()
    return 0


if __name__ == "__main__":
    sys.exit(main())
