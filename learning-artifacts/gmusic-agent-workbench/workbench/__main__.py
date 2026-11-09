"""CLI: python3 -m workbench run --demo"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from workbench.loop import run_demo


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="workbench", description="Gmusic Agent Workbench")
    sub = parser.add_subparsers(dest="cmd", required=True)
    run_p = sub.add_parser("run", help="Run an agent session")
    run_p.add_argument("--demo", action="store_true", help="Offline repair demo")
    run_p.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Workbench root",
    )
    args = parser.parse_args(argv)

    if args.cmd == "run":
        if not args.demo:
            print("Only --demo is implemented in MVP 0.1.0", file=sys.stderr)
            return 2
        result = run_demo(args.root)
        print(json.dumps(result, indent=2))
        print(f"\nEvidence: {result['evidence']}")
        return 0 if result["outcome"] == "pass" else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
