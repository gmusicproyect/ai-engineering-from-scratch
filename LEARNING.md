# My AI Engineering Path
<!-- Managed by the ai-engineering-from-scratch learning skills.
     Repo: https://github.com/rohitg00/ai-engineering-from-scratch -->

## Mission
Recorrer el currículo fase por fase. En cada lección: entender qué enseña, qué hace falta, e implementarlo en el repositorio para poder aprenderlo. Sin quiz.

## Placement
- Date: 2026-11-09
- Score: self-selected
- Entry point: Fase 3: Núcleo de aprendizaje profundo
- Pace: 1 lección por sesión

## Path
| Phase | Name | Status | Est. hours |
|-------|------|--------|------------|
| 0 | Preparación y herramientas | Skip | 16 |
| 1 | Fundamentos de matemáticas | Skip | 23 |
| 2 | Fundamentos de aprendizaje automático | Skip | 26 |
| 3 | Núcleo de aprendizaje profundo | Do | 15 |
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

## Progress log
| Date | Lesson | Quiz | Note |
|------|--------|------|------|
| 2026-11-09 | 00-setup-and-tooling/01-dev-environment | 0/3 | Pidió instalar el stack completo y que yo diera las respuestas. Queda en repaso. |
| 2026-11-09 | 00-setup-and-tooling/02-git-and-collaboration | — | El repositorio ya cumple la lección: .gitignore excluye pesos y el historial muestra cómo se agregaron las lecciones. No se pregunta más. |
| 2026-11-09 | 03-deep-learning-core/01-the-perceptron | — | Se corrió perceptron.py. AND, OR y NOT convergen. Un perceptrón no resuelve XOR. Dos capas sí. |

## Review queue
- 00-setup-and-tooling/01-dev-environment — orden de las cuatro capas, para qué sirve uv, cómo comprobar la GPU

## Registro
Hecho el 2026-11-09. El estudio se implementa en el repositorio, sin quiz.

| Qué | Evidencia |
|-----|-----------|
| Curso clonado | `origin` = https://github.com/rohitg00/ai-engineering-from-scratch.git, rama `main` |
| Entorno | `.venv` con Python 3.12.16, NumPy 2.5.4, Matplotlib 3.11.2, Jupyter, PyTorch 2.15.0. Metal sí. CUDA no. También wget, pnpm 12.18.0, cargo 1.99.1 y Julia 1.13.3 |
| Preflight | `.venv/bin/python phases/00-setup-and-tooling/01-dev-environment/code/verify.py --route beginner --show-later` terminó 2/2 y el resto en PASS |
| Git de la lección 2 | `.gitignore` ya excluye `*.pt`, `*.pth`, `*.safetensors`, `models/`, `checkpoints/` y `.venv/`. No hay push: `origin` es el repositorio del autor |
| Perceptrón | `.venv/bin/python phases/03-deep-learning-core/01-the-perceptron/code/perceptron.py` salió 0. AND, OR y NOT convergieron. XOR con una neurona falló. XOR con dos capas quedó bien |
| Pantalla en español | 13 páginas de la Fase 0 en `.lesson-screen/screens/`, copiadas a `learning-artifacts/fase-00-pantalla/` para que Git las guarde |
| Forma de estudio | Una lección por vez. Fase 3 en curso. Fases 0, 1 y 2 quedan en Skip hasta que se pidan |
