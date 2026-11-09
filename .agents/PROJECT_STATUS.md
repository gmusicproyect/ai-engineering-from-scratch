# ESTADO — AI Engineering from Scratch
Última actualización: 2026-11-09

## En curso
- Listo para el siguiente ticket: Fase 3, lección 02 (redes de varias capas).
- Comando: `.venv/bin/python phases/03-deep-learning-core/02-multi-layer-networks/code/main.py`

## Bloqueado / Pendiente
- Push no autorizado. `origin` = repo del autor. No empujar sin OK de JP.
- Cola de repaso: 00/01 entorno (quiz 0/3).

## Decisiones vigentes (referencia rápida)
- Una lección por vez, implementando en el repositorio, sin quiz.
- Entrada: Fase 3. Fases 0, 1 y 2 en Skip hasta que JP las pida.
- Método: identidad + Criterio Fable + loop. Spec y mini-brief antes de ejecutar. Gates G1–G7.
- Tests del loop: `python3 scripts/run_lesson_tests.py`
- Build del loop: `node site/build.js`
- Verify del loop: NO DEFINIDO

## Reglas duras activas
- G1. Ningún push sin autorización explícita de JP en esa sesión.
- G2. Todo SQL de producción se muestra completo antes de ejecutar.
- G3. `db:seed` nunca corre en producción de forma amplia.
- G4. Ningún secret ni credencial en código, seed ni UI.
- G5. Ninguna dependencia nueva sin justificación escrita en la spec.
- G6. Migraciones: idempotentes y revisadas antes de aplicarlas a producción.
- G7. Borrado de datos, archivos o ramas: confirmación explícita de JP, siempre.

## Última verificación conocida
- Preflight beginner `--show-later`: 2/2 required PASS, opcionales PASS, Metal available. Fecha: 2026-11-09.
- Perceptrón: exit 0. XOR 1 capa falla; 2 capas OK.
- Pantallas Fase 0: 13 HTML en `learning-artifacts/fase-00-pantalla/`.
- Workspace ordenado: reglas, estado y registro alineados. Sin push.
