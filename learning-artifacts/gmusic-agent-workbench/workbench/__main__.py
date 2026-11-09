"""CLI: python3 -m workbench run --demo | rag-eval"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from workbench.loop import run_demo
from workbench.rag_eval import run_gate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="workbench", description="Gmusic Agent Workbench")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="Run an agent session")
    run_p.add_argument("--demo", action="store_true", help="Offline repair demo")
    run_p.add_argument(
        "--with-rag-gate",
        action="store_true",
        help="Also run retrieval regression gate after the demo",
    )
    run_p.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Workbench root",
    )

    rag_p = sub.add_parser("rag-eval", help="Compare baseline vs candidate rankings")
    rag_p.add_argument(
        "--candidate",
        default="candidate_ok.json",
        help="Candidate rankings file under fixtures/retrieval/",
    )
    rag_p.add_argument("--k", type=int, default=3)
    rag_p.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
    )

    args = parser.parse_args(argv)

    if args.cmd == "run":
        if not args.demo:
            print("Only --demo is implemented in MVP 0.1.x", file=sys.stderr)
            return 2
        result = run_demo(args.root)
        print(json.dumps(result, indent=2))
        print(f"\nEvidence: {result['evidence']}")
        code = 0 if result["outcome"] == "pass" else 1
        if args.with_rag_gate:
            gate = run_gate(args.root, candidate_name="candidate_ok.json")
            print("\nRAG gate:")
            print(json.dumps({
                "pass": gate["pass"],
                "regressions": gate["regressions"],
                "mean_delta_ndcg": gate["mean_delta_ndcg"],
                "evidence_path": gate["evidence_path"],
            }, indent=2))
            if not gate["pass"]:
                code = 1
        return code

    if args.cmd == "rag-eval":
        report = run_gate(args.root, candidate_name=args.candidate, k=args.k)
        print(json.dumps(report, indent=2))
        return 0 if report["pass"] else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
