"""CLI: python3 -m workbench run --demo | rag-eval | trace-debug | plan"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from workbench.loop import run_demo
from workbench.planner import plan_repair
from workbench.rag_eval import run_gate
from workbench.trace_debug import debug_trace, run_on_workbench


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="workbench", description="Gmusic Agent Workbench")
    sub = parser.add_subparsers(dest="cmd", required=True)
    default_root = Path(__file__).resolve().parent.parent

    run_p = sub.add_parser("run", help="Run an agent session")
    run_p.add_argument("--demo", action="store_true", help="Offline repair demo")
    run_p.add_argument(
        "--planner",
        choices=("offline", "live"),
        default="offline",
        help="offline heuristic (default) or live model hook if OPENAI_API_KEY is set",
    )
    run_p.add_argument("--with-rag-gate", action="store_true")
    run_p.add_argument("--with-trace-debug", action="store_true")
    run_p.add_argument("--root", type=Path, default=default_root)

    rag_p = sub.add_parser("rag-eval", help="Compare baseline vs candidate rankings")
    rag_p.add_argument("--candidate", default="candidate_ok.json")
    rag_p.add_argument("--k", type=int, default=3)
    rag_p.add_argument("--root", type=Path, default=default_root)

    tr_p = sub.add_parser("trace-debug", help="Analyze a workbench JSONL trace")
    tr_p.add_argument("--trace", type=Path, default=None)
    tr_p.add_argument("--baseline", type=Path, default=None)
    tr_p.add_argument("--root", type=Path, default=default_root)

    plan_p = sub.add_parser("plan", help="Propose a repair without applying it")
    plan_p.add_argument("--planner", choices=("offline", "live"), default="offline")
    plan_p.add_argument("--root", type=Path, default=default_root)

    args = parser.parse_args(argv)

    if args.cmd == "run":
        if not args.demo:
            print("Only --demo is implemented in MVP 0.4.x", file=sys.stderr)
            return 2
        result = run_demo(args.root, planner_mode=args.planner)
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

    if args.cmd == "plan":
        fixture = args.root / "fixtures" / "sample_app" / "app.py"
        board = json.loads((args.root / "task_board.json").read_text(encoding="utf-8"))
        task = next(t for t in board["tasks"] if t["id"] == board["active_task_id"])
        # Simulate failing stderr from a dry unittest when possible.
        import subprocess

        proc = subprocess.run(
            [sys.executable, "-m", "unittest", "test_app", "-v"],
            cwd=args.root / "fixtures" / "sample_app",
            capture_output=True,
            text=True,
            timeout=60,
        )
        plan = plan_repair(
            path="app.py",
            content=fixture.read_text(encoding="utf-8"),
            stderr=proc.stderr or "",
            task_notes=str(task.get("notes", "")),
            mode=args.planner,
        )
        print(json.dumps(plan.to_dict(), indent=2, ensure_ascii=False))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
