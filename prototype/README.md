# GenAI Security Guardian Prototypes

This folder contains runnable code that demonstrates the proposed GenAI Security Guardian semantic conventions:
- `apply_guardrail` span (`gen_ai.operation.name=apply_guardrail`)
- `gen_ai.security.finding` event (one event per finding)

The recommended entry point is the deterministic story suite in `prototype/stories/` (includes a small trace viewer UI).

## Key paths

- Story scenarios + trace viewer: [`prototype/stories/README.md`](./stories/README.md)
- Trace coverage map: [`prototype/stories/TRACE_COVERAGE.md`](./stories/TRACE_COVERAGE.md)
- Guardian span + event helpers: [`prototype/otel_guardian_utils.py`](./otel_guardian_utils.py)
- OTel exporter wiring + env loading: [`prototype/otel_bootstrap.py`](./otel_bootstrap.py)
- Original single-file prototype: [`prototype/genai_guardrail_instrumentation_prototype.py`](./genai_guardrail_instrumentation_prototype.py)
- Optional realism helpers: [`prototype/demo_chat.py`](./demo_chat.py), [`prototype/demo_tools.py`](./demo_tools.py)

## Quickstart (stories + viewer)

```bash
cd prototype

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-appinsights.txt

# Configure credentials (git-ignored)
cp stories/.env.example stories/.env.local

# Run stories and launch the trace viewer
python stories/run_and_view.py --story 4 5 7 10 11

# Opt-in (SENSITIVE): include input/output message content
python stories/run_and_view.py --story 4 5 7 10 11 --capture-content
```

## Content capture (opt-in)

Sensitive content is never captured by default. Enable explicitly via:
- CLI: `--capture-content`
- Env: `OTEL_DEMO_CAPTURE_GUARDIAN_CONTENT=true`

When enabled, demos may emit:
- `gen_ai.input.messages`, `gen_ai.output.messages`
- `gen_ai.security.content.*.value`

## References

- Spec proposal doc: `docs/gen-ai/gen-ai-security.md`
- Model definitions: `model/gen-ai/`
