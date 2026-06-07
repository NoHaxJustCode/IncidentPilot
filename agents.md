# agents.md

Guidance for AI-assisted development on IncidentPilot.

## Goals

- Keep all data synthetic.
- Preserve both interfaces: CLI and localhost dashboard.
- Keep investigation reports evidence-based.
- Keep default behavior deterministic and testable.

## Key files

```text
incidentpilot.py             # root CLI entrypoint
backend/app/main.py          # FastAPI routes
backend/app/cli.py           # CLI commands
backend/app/agent.py         # investigation pipeline
backend/app/tools.py         # synthetic-data tools
backend/app/sample_data.py   # synthetic incidents and observability data
backend/app/eval.py          # evaluation harness
frontend/index.html          # dashboard
TODO.md                      # roadmap
```

## Development commands

```bash
make install
make test
make eval
make demo
make serve
```

## Contribution rules

1. Every root-cause claim should be supported by evidence IDs.
2. SQL helpers must remain read-only.
3. Add or update eval cases when changing investigation behavior.
4. Do not add private logs, tickets, account IDs, internal code, or proprietary service names.
5. Keep README commands copy-pasteable.
