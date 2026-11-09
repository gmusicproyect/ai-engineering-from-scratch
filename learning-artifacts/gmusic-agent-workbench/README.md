# Gmusic Agent Workbench

Portfolio MVP: un agente de reparación offline propone un patch en un workspace
desechable, el firewall exige aprobación de un solo uso, corre tests y deja un
evidence bundle auditable.

Basado en las superficies del curso: agent loop, tool firewall, traces, workbench pack.

## Quick start

```bash
cd learning-artifacts/gmusic-agent-workbench
python3 -m workbench run --demo
python3 -m workbench run --demo --planner offline --with-rag-gate --with-trace-debug --with-mcp
python3 -m workbench plan --planner offline
python3 -m workbench mcp-demo
# Stdio MCP-subset server (initialize / tools/list / tools/call):
# python3 -m workbench mcp-serve
# Optional live hook (stdlib urllib). Falls back offline if no key / bad response:
# OPENAI_API_KEY=... python3 -m workbench run --demo --planner live
python3 -m workbench rag-eval
python3 -m workbench rag-eval --candidate candidate_regress.json  # exit 1
python3 -m workbench trace-debug
python3 -m unittest discover -s tests -v
```


## What the demo proves

1. Tests fallan en el fixture (greeting incorrecto).
2. `write_file` sin aprobación → `needs_approval`.
3. Misma request con token de un solo uso → patch aplicado.
4. Write fuera de scope → reject auditado.
5. Tests pasan; evidence en `outputs/evidence/`.

## Layout

```text
gmusic-agent-workbench/
├── SPEC.md                 # intención, restricciones, criterios
├── AGENTS.md               # contrato para el agente
├── policy/                 # roles + scope
├── fixtures/sample_app/    # app con bug deliberado
├── workbench/              # runtime Python stdlib
├── tests/                  # 5+ tests
└── outputs/                # workspace + evidence (generado)
```

## RAG regression gate (0.2.0)

Fixtures en `fixtures/retrieval/` (queries Gmusic: refunds, tuning, cancel).
Compara baseline vs candidate; falla si alguna query pierde NDCG.

## Trace debugger (0.3.0)

Analiza `outputs/evidence/trace.jsonl`: wall/own time, decisiones de tools,
anomalías (reject, approval sin consumir, verify rojo) y timeline HTML.
Opcional: `--baseline` otra traza para detectar regresiones (`more_rejects`).

## Live planner (0.4.0)

`workbench/planner.py` propone el patch; el firewall sigue gobernando writes.
Default `--planner offline` (heurística desde stderr/`task_notes`).
`--planner live` usa OpenAI-compatible HTTP si hay `OPENAI_API_KEY`; si falla,
cae a offline. Evidence: `outputs/evidence/plan.json` + evento `plan` en el trace.

## MCP tools (0.5.0)

Subset MCP over newline JSON-RPC: `initialize`, `tools/list`, `tools/call`.
Tools read-only: `catalog_search`, `get_document`, `rag_compare`, `plan_repair`
(plan propose only — no writes). Catalog in `fixtures/mcp/catalog.json`.
Evidence: `outputs/evidence/mcp-session.json`. Not full MCP conformance.
