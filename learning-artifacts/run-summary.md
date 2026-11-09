# Curriculum run summary

Total unique: 542 · ok=534 · fail=0 · skip=8

First full pass: ok=523 · fail=11 · skip=8. All 11 failures re-run and fixed locally on 2026-11-09.

## Failures

None remaining. Previous failures and how they were resolved:

- `00-setup-and-tooling/09-data-management`: installed `datasets` in `.venv`
- `01-math-foundations/10-dimensionality-reduction`: OpenML/pandas fallback → synthetic data
- `02-ml-fundamentals/11-ensemble-methods`: AdaBoost without deprecated `algorithm=`
- `02-ml-fundamentals/12-hyperparameter-tuning`: smaller search grids/budgets
- `03-deep-learning-core/12-intro-to-jax`: OpenML MNIST fallback → synthetic
- `04-computer-vision/16-vision-pipeline-capstone`: deps / prior env fix (re-run OK)
- `11-llm-engineering/02-few-shot-cot`: offline bank check without API key
- `11-llm-engineering/16-langgraph-state-machines`: optional LangGraph import + offline tool check
- `19-capstone-projects/37-loading-pretrained-weights`: `safetensors` installed
- `19-capstone-projects/42-large-corpus-downloader`: `zstandard` installed
- `19-capstone-projects/43-hdf5-tokenized-corpus`: `h5py` installed

## Skips

No Python entrypoint (docs/setup only):

- `00-setup-and-tooling/02-git-and-collaboration`
- `00-setup-and-tooling/06-python-environments`
- `00-setup-and-tooling/07-docker-for-ai`
- `00-setup-and-tooling/08-editor-setup`
- `00-setup-and-tooling/10-terminal-and-shell`
- `00-setup-and-tooling/11-linux-for-ai`
- `16-multi-agent-and-swarms/01-why-multi-agent`
- `16-multi-agent-and-swarms/03-communication-protocols`
