# ESTADO — AI Engineering from Scratch
Última actualización: 2026-11-09

## En curso
- Runner continuo de las 542 lecciones: `learning-artifacts/run_curriculum.py` (PID en `run-curriculum.out`).
- JP autorizó no pedir confirmación por lección.
- Fase 3: 12/13 ok. Fallo: `12-intro-to-jax` (MNIST/sklearn+pandas). Demos grad/vmap/jit sí corrieron.

## Bloqueado / Pendiente
- Push no autorizado (G1).
- JAX MNIST: TypeError en `fetch_openml` con pandas 3.x.
- Cola de repaso: 00/01 entorno (quiz 0/3).

## Decisiones vigentes (referencia rápida)
- Completar todas las fases ejecutando el entrypoint Python de cada lección.
- Log: `learning-artifacts/run-log.jsonl`. Resumen: `learning-artifacts/run-summary.md`.
- Sin quiz. Sin push.
- Timeout por lección: 180s. Continúa tras fallos.

## Reglas duras activas
- G1–G7 vigentes. Cero push sin OK de JP.

## Última verificación conocida
- Fase 3 runner: 12 ok, 1 fail. Fecha: 2026-11-09.
- Curriculum runner: arrancó y avanza desde Fase 0.
