# GenAI Memory Prototype (Stories + Trace Viewer)

This directory contains runnable, non-normative code demonstrating the GenAI **memory operation** semantic conventions through a small story suite and an Azure Application Insights trace viewer.

**Key paths**
- Stories + viewer docs: `prototype/memory/scenarios/README.md`
- One-command runner + viewer: `prototype/memory/scenarios/run_and_view.py`
- Viewer UI: `prototype/memory/scenarios/trace_viewer.py`
- App Insights query logic: `prototype/memory/scenarios/trace_retriever.py`
- Instrumentation helpers (Python): `prototype/memory/core/python/genai_memory_otel`

## Quickstart

```bash
cd prototype/memory

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-appinsights.txt

# Configure credentials (git-ignored)
cp scenarios/.env.sample scenarios/.env.local

# Run stories + export to App Insights + launch viewer
python3 scenarios/run_and_view.py

# Opt-in (SENSITIVE): include input/output messages, queries, and memory content
python3 scenarios/run_and_view.py --capture-content
```

## Notes

- The viewer queries App Insights via Entra ID (Azure CLI): run `az login` and set `APPINSIGHTS_RESOURCE_ID` (or `APPINSIGHTS_APP` + `APPINSIGHTS_RESOURCE_GROUP`).
- Real LLM calls are optional; if `OPENAI_API_KEY` is unset (or the `openai` package isn’t installed), stories fall back to a mock model.
