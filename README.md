# IncidentPilot

IncidentPilot is an agentic production-debugging platform that turns an incident ticket into an evidence-backed root-cause report.

The project uses fully synthetic data. It can parse a ticket, inspect deploy metadata, query local logs/metrics/traces, run read-only SQL, search service-code snippets, and return a cited investigation report.

## Highlights

- CLI and localhost dashboard
- FastAPI backend
- SQLite-backed synthetic observability store
- Tool-calling investigation pipeline
- Evaluation harness
- Tests, Docker, and CI

## Run the dashboard

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://localhost:8000`.

## Run the CLI

```bash
python incidentpilot.py investigate --ticket "Checkout latency increased for premium users after deploy 4921"
python incidentpilot.py eval
python incidentpilot.py list-incidents
python incidentpilot.py show-data logs --limit 5
```

## Tests

```bash
cd backend
pytest -q
```

## Eval metrics

The eval suite reports root-service accuracy, category accuracy, deploy accuracy, evidence recall, hallucinated evidence rate, and tool success rate.

## Roadmap

See `TODO.md`.
