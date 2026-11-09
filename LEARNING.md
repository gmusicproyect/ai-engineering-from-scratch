# My AI Engineering Path
<!-- Managed by the ai-engineering-from-scratch learning skills.
     Repo: https://github.com/rohitg00/ai-engineering-from-scratch -->

## Mission
Completar todas las fases y lecciones del currículo. Ejecutar el código de cada lección, registrar el resultado y seguir sin pedir confirmación por lección. Sin quiz. Sin push al remoto del autor.

## Placement
- Date: 2026-11-09
- Score: self-selected
- Entry point: Fase 3: Núcleo de aprendizaje profundo
- Pace: continuo (autorizado por JP 2026-11-09)

## Path
| Phase | Name | Status | Est. hours |
|-------|------|--------|------------|
| 0 | Preparación y herramientas | Do | 16 |
| 1 | Fundamentos de matemáticas | Do | 23 |
| 2 | Fundamentos de aprendizaje automático | Do | 26 |
| 3 | Núcleo de aprendizaje profundo | Done | 15 |
| 4 | Visión por computadora | Do | 27 |
| 5 | Lenguaje: de los fundamentos a lo avanzado | Do | 30 |
| 6 | Voz y audio | Do | 18 |
| 7 | Transformers a fondo | Do | 14 |
| 8 | IA generativa | Do | 14 |
| 9 | Aprendizaje por refuerzo | Do | 13 |
| 10 | Modelos de lenguaje desde cero | Do | 26 |
| 11 | Ingeniería de modelos de lenguaje | Do | 19 |
| 12 | IA multimodal | Do | 65 |
| 13 | Herramientas y protocolos | Do | 76 |
| 14 | Ingeniería de agentes | Do | 55 |
| 15 | Sistemas autónomos | Do | 20 |
| 16 | Multiagente y enjambres | Do | 28 |
| 17 | Infraestructura y producción | Do | 34 |
| 18 | Ética, seguridad y alineación | Do | 31 |
| 19 | Proyectos finales | Do | 620 |

## Siguiente
- Runner terminó 542/542: ok=523 · fail=11 · skip=8. Ver `learning-artifacts/run-summary.md`.
- Fallos pendientes de reintento/arreglo (deps o timeout). Push no hecho.

## Progress log
| Date | Lesson | Quiz | Note |
|------|--------|------|------|
| 2026-11-09 | 00-setup-and-tooling/01-dev-environment | 0/3 | Stack instalado. Preflight 2/2 PASS. Quiz no aprobado; queda en repaso. |
| 2026-11-09 | 00-setup-and-tooling/02-git-and-collaboration | — | `.gitignore` ya excluye pesos. Sin push al repo del autor. |
| 2026-11-09 | 03-deep-learning-core/01-the-perceptron | — | `perceptron.py` exit 0. AND/OR/NOT OK. XOR 1 capa falla. XOR 2 capas OK. |
| 2026-11-09 | 03-deep-learning-core/02-multi-layer-networks | — | `main.py` exit 0. XOR 2-2-1 OK. Círculo 2-8-1 con pesos aleatorios 17.5%. Forward pass interno trazado. |
| 2026-11-09 | 03-deep-learning-core/03-backpropagation | — | `main.py` exit 0. XOR loss 1.07→0.003. Círculo accuracy 70%→100%. |

| 2026-11-09 | 03-deep-learning-core/05-loss-functions | — | runner ok. ccuracy=98.0% /     Epoch 100: loss=0.0342, accuracy=98.0% /     Epoch 150: loss=0.0256, a |
| 2026-11-09 | 03-deep-learning-core/06-optimizers | — | runner ok. 30 /   AdamW (lr=0.001, wd=0.01)               : acc=99.0%, loss=0.0612, reached 85%: epoc |
| 2026-11-09 | 03-deep-learning-core/07-regularization | — | runner ok. 99.3%      97.3%     2.0% /   Dropout p=0.3                       96.0%      98.0%    -2.0 |
| 2026-11-09 | 03-deep-learning-core/08-weight-initialization | — | runner ok. 0.213427     0.205097         3.9% /   Random(1.0) + Sigmoid              0.257682     0.0 |
| 2026-11-09 | 03-deep-learning-core/09-learning-rate-schedules | — | runner ok. /2  Step 3T/4     Step T /   ------------------------------------------------------------  |
| 2026-11-09 | 03-deep-learning-core/10-mini-framework | — | runner ok. 98.0% /  / ====================================================================== / FRAMEW |
| 2026-11-09 | 03-deep-learning-core/11-intro-to-pytorch | — | runner ok. 4 /  /   Time: 7.0s (0.7s/epoch) /   Final Test Accuracy: 0.9842 /  / ==================== |
| 2026-11-09 | 03-deep-learning-core/12-intro-to-jax | — | runner fail. grad/vmap/jit OK; MNIST fails: sklearn fetch_openml TypeError with pandas 3.x |
| 2026-11-09 | 03-deep-learning-core/13-debugging-neural-networks | — | runner ok. ========================= / GRADIENT CHECK (smooth model + MSE loss for clean finite diffe |

## Review queue
- 00-setup-and-tooling/01-dev-environment — orden de las cuatro capas, para qué sirve uv, cómo comprobar la GPU

## Registro
Hecho el 2026-11-09. El estudio se implementa en el repositorio, sin quiz. Método de trabajo: `instruccionesAgentes` instalado en `.cursor/rules/` y estado en `.agents/PROJECT_STATUS.md`.

| Qué | Evidencia |
|-----|-----------|
| Curso clonado | `origin` = https://github.com/rohitg00/ai-engineering-from-scratch.git, rama `main` |
| Entorno | `.venv` Python 3.12.16, NumPy, Matplotlib, Jupyter, PyTorch 2.15.0. Metal sí. CUDA no. |
| Preflight | `.venv/bin/python phases/00-setup-and-tooling/01-dev-environment/code/verify.py --route beginner --show-later` → 2/2 PASS |
| Perceptrón | `.venv/bin/python phases/03-deep-learning-core/01-the-perceptron/code/perceptron.py` → exit 0 |
| Redes varias capas | `.venv/bin/python phases/03-deep-learning-core/02-multi-layer-networks/code/main.py` → exit 0. XOR resuelto. Círculo sin entrenar 17.5%. |
| Backpropagation | `.venv/bin/python phases/03-deep-learning-core/03-backpropagation/code/main.py` → exit 0. XOR y círculo entrenados. |
| Pantallas Fase 0 | 13 HTML en `learning-artifacts/fase-00-pantalla/` |
| Protocolo | `.cursor/rules/01-identidad-del-ejecutor.mdc`, `02-protocolo-criterio-fable.mdc`, `loop.mdc` |
