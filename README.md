# IncidentPilot

IncidentPilot is an **agentic production-debugging platform** that turns an incident ticket into an evidence-backed root-cause report.

It is built as a public-safe SDLC/Ops agent workflow: the agent reads a ticket, plans an investigation, queries synthetic CloudWatch-style logs, Athena-like SQL tables, service metrics, distributed traces, deploy metadata, and code snippets, then produces a cited incident report.

## Why this project exists

Most AI projects look like wrappers around a chat API. IncidentPilot is designed to look closer to a production AI engineering system:

- tool-calling agent workflow
- observability data model
- logs, metrics, traces, deploys, SQL, and code search
- deterministic investigation pipeline
- evidence-cited root-cause reports
- CLI and localhost dashboard
- eval harness for agent reliability
- tests, Docker, CI, and clear operating docs

## Demo

Example ticket:

```text
Checkout latency increased for premium users after deploy 4921. p95 went from ~240ms to >1.8s around 14:05 UTC.
```

IncidentPilot will:

1. Parse deploy IDs, service hints, symptoms, and severity.
2. Pull deploy metadata and establish the investigation window.
3. Query anomalous service metrics.
4. Search logs for deploy IDs, symptoms, and impacted request IDs.
5. Run read-only SQL over synthetic observability tables.
6. Inspect traces for impacted requests.
7. Search service code snippets.
8. Rank likely root causes and generate a timeline, cited evidence, runbook, and next steps.

## Architecture

```text
                 +----------------------+
                 | Ticket / Incident    |
                 +----------+-----------+
                            |
                            v
+-------------------------------------------------------------+
| Agentic Investigation Pipeline                              |
|                                                             |
|  parse -> plan -> metrics -> logs -> SQL -> traces -> code  |
|    |        |        |        |      |       |        |      |
|    v        v        v        v      v       v        v      |
| evidence extraction -> scoring -> root cause -> report       |
+-------------------------------------------------------------+
                            |
                            v
+-------------------------------------------------------------+
| Synthetic Observability Store                               |
|                                                             |
| services | deploys | logs | metrics | traces | spans | code |
+-------------------------------------------------------------+
                            |
          +-----------------+-----------------+
          |                                   |
          v                                   v
+-------------------+               +---------------------+
| FastAPI Dashboard |               | CLI                 |
| localhost:8000    |               | incidentpilot.py    |
+-------------------+               +---------------------+
```

## Project structure

```text
IncidentPilot/
  AGENTS.md                  # Instructions for AI coding agents
  TODO.md                    # Roadmap and polish checklist
  README.md                  # Project docs
  incidentpilot.py           # Root CLI entrypoint
  backend/
    app/
      main.py                # FastAPI app and API routes
      cli.py                 # CLI commands
      agent.py               # Deterministic agentic investigation pipeline
      tools.py               # Constrained observability/code/deploy tools
      datastore.py           # SQLite-backed synthetic observability store
      sample_data.py         # Synthetic incidents, logs, metrics, traces, code snippets
      eval.py                # Evaluation harness
      models.py              # Pydantic models
    tests/                   # Pytest suite
  frontend/
    index.html               # Localhost dashboard
  scripts/
    run_demo.py
    run_eval.py
  examples/
    ticket.txt
  docker-compose.yml
  Makefile
```

## Quickstart: localhost dashboard

```bash
cd IncidentPilot/backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000
```

API docs:

```text
http://localhost:8000/docs
```

## Quickstart: CLI

From the repo root:

```bash
python incidentpilot.py investigate --ticket "Checkout latency increased for premium users after deploy 4921"
```

JSON output:

```bash
python incidentpilot.py investigate \
  --ticket "Payment authorization timeouts increased after deploy 2277" \
  --json
```

Read a ticket from a file:

```bash
python incidentpilot.py investigate --file examples/ticket.txt
```

Run evals:

```bash
python incidentpilot.py eval
python incidentpilot.py eval --json
```

List sample incidents:

```bash
python incidentpilot.py list-incidents
```

Inspect synthetic data:

```bash
python incidentpilot.py show-data logs --limit 5
python incidentpilot.py show-data metrics --limit 5
python incidentpilot.py services
```

You can also run the module directly from `backend`:

```bash
cd backend
python -m app.cli eval
```

## Make commands

```bash
make install
make test
make eval
make demo
make serve
```

## Docker

```bash
docker compose up --build
```

Open:

```text
http://localhost:8000
```

## API examples

Investigate a ticket:

```bash
curl -X POST http://localhost:8000/investigate \
  -H 'Content-Type: application/json' \
  -d '{"ticket":"Checkout latency increased for premium users after deploy 4921. p95 went from ~240ms to >1.8s around 14:05 UTC."}'
```

Run evals:

```bash
curl http://localhost:8000/eval/run
```

Inspect data:

```bash
curl http://localhost:8000/data/logs
curl http://localhost:8000/services
```

## Eval metrics

The eval suite measures:

- root-service accuracy
- category accuracy
- deploy detection accuracy
- evidence recall
- hallucinated evidence citation rate
- tool success rate
- average tool calls per investigation
- average evidence count

Example output:

```text
root_service_accuracy: 1.0
category_accuracy: 1.0
deploy_accuracy: 1.0
evidence_recall: 1.0
hallucinated_evidence_rate: 0.0
tool_success_rate: 1.0
```

## Tests

```bash
cd backend
pytest -q
```

## GitHub publishing

Create an empty GitHub repo named `IncidentPilot`, then from this folder run:

```bash
git init
git add .
git commit -m "Initial IncidentPilot project"
git branch -M main
git remote add origin https://github.com/NoHaxJustCode/IncidentPilot.git
git push -u origin main
```

Or use the included helper:

```bash
bash scripts/push_to_github.sh NoHaxJustCode IncidentPilot
```

## Confidentiality and safety

This repo uses synthetic services and fake operational data. Do not add proprietary company logs, tickets, code, metric names, customer identifiers, account IDs, private service names, or internal details.

## Resume bullets

```latex
\resumeProjectHeading
  {\textbf{IncidentPilot -- Agentic Production Debugging Platform} $|$ \emph{Python, FastAPI, SQLite, Tool Calling, Docker, Logs/Metrics/Traces}}{}
  \resumeItemListStart
    \resumeItem{Built an agentic Ops platform that parses incident tickets, queries logs/metrics/traces, deploy metadata, SQL tables, and service code, then generates evidence-cited root-cause reports.}
    \resumeItem{Implemented a deterministic tool-calling pipeline with traceable agent steps for deploy lookup, metric anomaly detection, log search, SQL aggregation, trace inspection, and codebase retrieval.}
    \resumeItem{Created a labeled incident evaluation harness measuring root-cause accuracy, category accuracy, deploy detection, evidence recall, hallucinated citations, and tool success rate across synthetic production incidents.}
    \resumeItem{Shipped both a FastAPI dashboard and CLI interface for investigating tickets, running evals, listing sample incidents, and inspecting synthetic observability data.}
  \resumeItemListEnd
```

## Roadmap

See [`TODO.md`](TODO.md).

## AI agent instructions

See [`AGENTS.md`](AGENTS.md).
