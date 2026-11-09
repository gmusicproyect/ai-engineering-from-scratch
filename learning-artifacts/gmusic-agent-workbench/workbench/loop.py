"""Offline agent loop: observe → propose → firewall → apply → verify → evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from workbench.evidence import write_bundle
from workbench.firewall import Firewall, load_roles
from workbench.trace import TraceLog
from workbench.workspace import materialize, resolve_inside

ROOT = Path(__file__).resolve().parent.parent
FIXED_GREETING = (
    '"""Minimal Gmusic sample surface with a deliberate greeting bug."""\n'
    "\n"
    "\n"
    "def greeting(name: str = \"alumno\") -> str:\n"
    "    return f\"Hola {name}, Bienvenido a Gmusic Academy\"\n"
    "\n"
    "\n"
    "def health() -> dict[str, str]:\n"
    "    return {\"status\": \"ok\", \"product\": \"Gmusic Academy\"}\n"
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_demo(root: Path | None = None) -> dict[str, Any]:
    root = root or ROOT
    fixture = root / "fixtures" / "sample_app"
    out_root = root / "outputs"
    workspace = out_root / "workspace"
    evidence_dir = out_root / "evidence"

    materialize(fixture, workspace)
    roles = load_roles(root / "policy" / "roles.json")
    scope = load_json(root / "policy" / "scope_contract.json")
    board = load_json(root / "task_board.json")
    task = next(t for t in board["tasks"] if t["id"] == board["active_task_id"])

    fw = Firewall(
        roles=roles,
        allowed_paths=set(scope["allowed_paths"]),
        workspace_root=workspace,
    )
    trace = TraceLog(evidence_dir / "trace.jsonl")
    trace.emit("session_start", task_id=task["id"], role="repairer")

    state = {
        "schema_version": 1,
        "pack_version": (root / "VERSION").read_text(encoding="utf-8").strip(),
        "status": "running",
        "active_task_id": task["id"],
        "last_event": "session_start",
        "workspace_path": str(workspace),
    }
    save_json(root / "agent_state.json", state)

    steps = 0
    # 1) Observe failing tests
    steps += 1
    before = _run_tests(workspace)
    trace.emit("verify", phase="before", **before)

    # 2) Read the buggy file
    steps += 1
    ok, reason = fw.check(
        role="repairer",
        tool="read_file",
        args={"path": "app.py"},
        request_id="r1",
    )
    assert ok, reason
    content = resolve_inside(workspace, "app.py").read_text(encoding="utf-8")
    trace.emit("tool", tool="read_file", path="app.py", bytes=len(content), decision="allow")

    # 3) Attempt write WITHOUT approval — must reject
    steps += 1
    ok, reason = fw.check(
        role="repairer",
        tool="write_file",
        args={"path": "app.py", "content": FIXED_GREETING},
        request_id="r2",
    )
    assert not ok and reason.startswith("needs_approval:"), reason
    approval_token = reason.split(":", 1)[1]
    trace.emit(
        "tool",
        tool="write_file",
        path="app.py",
        decision="needs_approval",
        approval_token=approval_token,
    )

    # 4) Same write WITH approval — must allow and apply
    steps += 1
    ok, reason = fw.check(
        role="repairer",
        tool="write_file",
        args={"path": "app.py", "content": FIXED_GREETING},
        request_id="r2",
        approval_token=approval_token,
    )
    assert ok, reason
    resolve_inside(workspace, "app.py").write_text(FIXED_GREETING, encoding="utf-8")
    trace.emit("tool", tool="write_file", path="app.py", decision="allow", applied=True)

    # 5) Out-of-scope write must reject
    steps += 1
    ok, reason = fw.check(
        role="repairer",
        tool="write_file",
        args={"path": "secrets/token.txt", "content": "nope"},
        request_id="r3",
        approval_token=None,
    )
    # Even issuing approval path: first check path before approval for out of scope
    # Our firewall checks path before approval — should reject immediately.
    assert not ok, "out-of-scope write must fail"
    trace.emit("tool", tool="write_file", path="secrets/token.txt", decision="reject", reason=reason)

    # 6) Verify after
    steps += 1
    after = _run_tests(workspace)
    trace.emit("verify", phase="after", **after)
    outcome = "pass" if after["exit_code"] == 0 else "fail"

    bundle = write_bundle(
        evidence_dir,
        task_id=task["id"],
        outcome=outcome,
        audit=fw.audit,
        verify={"before": before, "after": after},
        steps=steps,
        residual_risk=(
            "Patch lives only in disposable outputs/workspace; not merged to product."
            if outcome == "pass"
            else "Acceptance tests still failing; do not merge."
        ),
    )
    trace.emit("session_end", outcome=outcome, evidence=str(bundle))

    state.update({"status": outcome, "last_event": "session_end"})
    save_json(root / "agent_state.json", state)

    board["tasks"][0]["status"] = "done" if outcome == "pass" else "blocked"
    save_json(root / "task_board.json", board)

    return {
        "outcome": outcome,
        "steps": steps,
        "workspace": str(workspace),
        "evidence": str(bundle),
        "before_exit": before["exit_code"],
        "after_exit": after["exit_code"],
        "audit_events": len(fw.audit),
    }


def _run_tests(workspace: Path) -> dict[str, Any]:
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "test_app", "-v"],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return {
        "exit_code": proc.returncode,
        "stdout_tail": (proc.stdout or "")[-500:],
        "stderr_tail": (proc.stderr or "")[-500:],
        "command": "python3 -m unittest test_app -v",
    }
