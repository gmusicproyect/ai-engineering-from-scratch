"""CLI: python3 -m workbench run --demo | rag-eval | trace-debug"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from workbench.loop import run_demo
from workbench.rag_eval import run_gate
from workbench.trace_debug import debug_trace, run_on_workbench


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="workbench", description="Gmusic Agent Workbench")
    sub = parser.add_subparsers(dest="cmd", required=True)
    default_root = Path(__file__).resolve().parent.parent

    run_p = sub.add_parser("run", help="Run an agent session")
    run_p.add_argument("--demo", action="store_true", help="Offline repair demo")
    run_p.add_argument("--with-rag-gate", action="store_true")
    run_p.add_argument("--with-trace-debug", action="store_true")
    run_p.add_argument("--root", type=Path, default=default_root)

    rag_p = sub.add_parser("rag-eval", help="Compare baseline vs candidate rankings")
    rag_p.add_argument("--candidate", default="candidate_ok.json")
    rag_p.add_argument("--k", type=int, default=3)
    rag_p.add_argument("--root", type=Path, default=default_root)

    tr_p = sub.add_parser("trace-debug", help="Analyze a workbench JSONL trace")
    tr_p.add_argument(
        "--trace",
        type=Path,
        default=None,
        help="Path to trace.jsonl (default: outputs/evidence/trace.jsonl)",
    )
    tr_p.add_argument("--baseline", type=Path, default=None, help="Optional baseline trace")
    tr_p.add_argument("--root", type=Path, default=default_root)

    args = parser.parse_args(argv)

    if args.cmd == "run":
        if not args.demo:
            print("Only --demo is implemented in MVP 0.3.x", file=sys.stderr)
            return 2
        result = run_demo(args.root)
        print(json.dumps(result, indent=2))
        print(f"\nEvidence: {result['evidence']}")
        code = 0 if result["outcome"] == "pass" else 1
        if args.with_rag_gate:
            gate = run_gate(args.root, candidate_name="candidate_ok.json")
            print("\nRAG gate:")
            print(
                json.dumps(
                    {
                        "pass": gate["pass"],
                        "regressions": gate["regressions"],
                        "mean_delta_ndcg": gate["mean_delta_ndcg"],
                        "evidence_path": gate["evidence_path"],
                    },
                    indent=2,
                )
            )
            if not gate["pass"]:
                code = 1
        if args.with_trace_debug:
            report = run_on_workbench(args.root)
            print("\nTrace debug:")
            print(
                json.dumps(
                    {
                        "pass": report["pass"],
                        "anomalies": report["summary"]["anomalies"],
                        "wall_ms": report["summary"]["wall_ms"],
                        "html_path": report["html_path"],
                        "json_path": report["json_path"],
                    },
                    indent=2,
                )
            )
        return code

    if args.cmd == "rag-eval":
        report = run_gate(args.root, candidate_name=args.candidate, k=args.k)
        print(json.dumps(report, indent=2))
        return 0 if report["pass"] else 1

    if args.cmd == "trace-debug":
        trace = args.trace or (args.root / "outputs" / "evidence" / "trace.jsonl")
        evidence = args.root / "outputs" / "evidence"
        report = debug_trace(
            trace,
            out_json=evidence / "trace-report.json",
            out_html=evidence / "trace.html",
            baseline_path=args.baseline,
        )
        print(json.dumps(report, indent=2))
        return 0 if report["pass"] else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
