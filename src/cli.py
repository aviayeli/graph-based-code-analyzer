"""Interactive terminal CLI menu — SDK layer interface (Lecture 4 constraint)."""
from __future__ import annotations

import sys

from src.config import settings
from src.mixins import LoggingMixin


class CLIMenu(LoggingMixin):
    """REPL-style terminal menu that dispatches to Graphify SDK actions."""

    _ACTIONS: dict[str, tuple[str, str]] = {
        "1": ("Run Pipeline", "_run_pipeline"),
        "2": ("Run FinOps",   "_run_finops"),
        "3": ("Exit",         "_exit"),
    }

    def start(self) -> None:
        """Enter the menu loop. Blocks until the user selects Exit."""
        self.configure_root_logging(level=settings.log_level, fmt=settings.log_format)
        while True:
            self._print_menu()
            choice = input("Select an option: ").strip()
            entry = self._ACTIONS.get(choice)
            if entry is None:
                print(f"Unknown option '{choice}'. Please try again.\n")
                continue
            getattr(self, entry[1])()

    # ── private handlers ──────────────────────────────────────────────────────

    def _print_menu(self) -> None:
        print("\n=== Graphify CLI ===")
        for key, (label, _) in self._ACTIONS.items():
            print(f"  [{key}] {label}")
        print()

    def _run_pipeline(self) -> None:
        from src.pipeline import Pipeline

        print("Starting full pipeline...\n")
        Pipeline().run()
        print("\nPipeline complete.\n")

    def _run_finops(self) -> None:
        from src.finops import FinOpsAnalyzer

        print("Running FinOps benchmark...\n")
        graph_out = settings.vault_path / "graph.json"
        finops = FinOpsAnalyzer(
            repo_root=settings.workspace_dir,
            graph_path=graph_out,
        )
        results = finops.run_benchmarks()
        finops.write_report(results, settings.docs_dir / "finops_report.md")
        print("\nFinOps complete.\n")

    def _exit(self) -> None:
        print("Goodbye.\n")
        sys.exit(0)
