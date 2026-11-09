# Gmusic Agent Workbench

Portfolio MVP: un agente de reparación offline propone un patch en un workspace
desechable, el firewall exige aprobación de un solo uso, corre tests y deja un
evidence bundle auditable.

Basado en las superficies del curso: agent loop, tool firewall, traces, workbench pack.

## Quick start

```bash
cd learning-artifacts/gmusic-agent-workbench
python3 -m workbench run --demo
python3 -m workbench run --demo --with-rag-gate --with-trace-debug
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

## Next slices

- MCP tools (`mcp-at-scale`) y jobs durables
- Live planner con modelo (API key) detrás del mismo firewall
