#!/usr/bin/env python3
"""Run every lesson entrypoint and append results to a log.

Authorized continuous study runner. Uses the course .venv when present.
Does not push. Continues after failures.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASES = ROOT / "phases"
LOG = ROOT / "learning-artifacts" / "run-log.jsonl"
SUMMARY = ROOT / "learning-artifacts" / "run-summary.md"
VENV_PY = ROOT / ".venv" / "bin" / "python"


def python_bin() -> str:
    return str(VENV_PY) if VENV_PY.exists() else sys.executable


def discover_entry(lesson: Path) -> Path | None:
    code = lesson / "code"
    if not code.is_dir():
        return None
    preferred = [
        "main.py",
        "perceptron.py",
        "vectors.py",
        "pytorch_intro.py",
        "jax_intro.py",
        "debug_neural_nets.py",
        "gpu_check.py",
        "verify.py",
        "first_api_call.py",
    ]
    for name in preferred:
        candidate = code / name
        if candidate.is_file():
            return candidate
    pys = sorted(
        p
        for p in code.glob("*.py")
        if p.is_file() and not p.name.startswith("test") and "test_" not in p.name
    )
    return pys[0] if pys else None


def lessons(phase_filter: str | None = None, after: str | None = None):
    rows = []
    for phase in sorted(PHASES.glob("[0-9][0-9]-*")):
        if phase_filter and phase.name != phase_filter and not phase.name.startswith(phase_filter):
            continue
        for lesson in sorted(phase.iterdir()):
            if not lesson.is_dir() or not lesson.name[:2].isdigit():
                continue
            key = f"{phase.name}/{lesson.name}"
            rows.append((key, phase, lesson))
    if after:
        rows = [r for r in rows if r[0] > after]
    return rows


def append_log(row: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_summary() -> None:
    if not LOG.exists():
        return
    rows = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    ok = sum(1 for r in rows if r.get("status") == "ok")
    fail = sum(1 for r in rows if r.get("status") == "fail")
    skip = sum(1 for r in rows if r.get("status") == "skip")
    lines = [
        "# Curriculum run summary",
        "",
        f"Updated: {datetime.now(timezone.utc).isoformat()}",
        f"Total logged: {len(rows)} · ok={ok} · fail={fail} · skip={skip}",
        "",
        "| Lesson | Status | Seconds | Note |",
        "|--------|--------|---------|------|",
    ]
    for r in rows[-80:]:
        note = (r.get("note") or "").replace("|", "/")[:80]
        lines.append(
            f"| `{r.get('lesson','')}` | {r.get('status')} | {r.get('seconds',0)} | {note} |"
        )
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_one(key: str, lesson: Path, timeout: int) -> dict:
    entry = discover_entry(lesson)
    now = datetime.now(timezone.utc).isoformat()
    if entry is None:
        row = {
            "ts": now,
            "lesson": key,
            "status": "skip",
            "seconds": 0,
            "note": "no python entrypoint",
            "exit": None,
        }
        append_log(row)
        return row

    cmd = [python_bin(), str(entry.relative_to(ROOT))]
    # beginner verify needs a route
    if entry.name == "verify.py":
        cmd.extend(["--route", "beginner"])

    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
        )
        seconds = round(time.time() - start, 2)
        out_tail = (proc.stdout or "")[-400:].strip().replace("\n", " | ")
        err_tail = (proc.stderr or "")[-400:].strip().replace("\n", " | ")
        note = out_tail or err_tail or f"exit {proc.returncode}"
        status = "ok" if proc.returncode == 0 else "fail"
        row = {
            "ts": now,
            "lesson": key,
            "status": status,
            "seconds": seconds,
            "note": note[:240],
            "exit": proc.returncode,
            "entry": str(entry.relative_to(ROOT)),
        }
    except subprocess.TimeoutExpired:
        row = {
            "ts": now,
            "lesson": key,
            "status": "fail",
            "seconds": timeout,
            "note": f"timeout after {timeout}s",
            "exit": None,
            "entry": str(entry.relative_to(ROOT)),
        }
    except Exception as exc:  # noqa: BLE001
        row = {
            "ts": now,
            "lesson": key,
            "status": "fail",
            "seconds": round(time.time() - start, 2),
            "note": f"{type(exc).__name__}: {exc}",
            "exit": None,
            "entry": str(entry.relative_to(ROOT)),
        }
    append_log(row)
    return row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", default=None, help="Phase dir prefix, e.g. 03")
    parser.add_argument("--after", default=None, help="Only lessons after this key")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    phase_filter = None
    if args.phase:
        phase_filter = args.phase if "-" in args.phase else args.phase.zfill(2)

    rows = lessons(phase_filter=phase_filter, after=args.after)
    if args.limit:
        rows = rows[: args.limit]

    print(f"Running {len(rows)} lessons with {python_bin()}", flush=True)
    ok = fail = skip = 0
    for i, (key, _phase, lesson) in enumerate(rows, 1):
        row = run_one(key, lesson, args.timeout)
        status = row["status"]
        if status == "ok":
            ok += 1
        elif status == "skip":
            skip += 1
        else:
            fail += 1
        print(f"[{i}/{len(rows)}] {status:4} {key} ({row.get('seconds')}s)", flush=True)
        if i % 5 == 0:
            write_summary()

    write_summary()
    print(f"Done ok={ok} fail={fail} skip={skip}", flush=True)
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
