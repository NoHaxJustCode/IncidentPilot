from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from . import sample_data, tools
from .agent import investigate
from .eval import run_eval
from .models import InvestigationRequest

app = FastAPI(title="IncidentPilot", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index():
    frontend = Path(__file__).resolve().parents[2] / "frontend" / "index.html"
    if frontend.exists():
        return frontend.read_text(encoding="utf-8")
    return "<h1>IncidentPilot</h1><p>POST /investigate to investigate a ticket.</p>"


@app.post("/investigate")
def investigate_ticket(request: InvestigationRequest):
    return investigate(request.ticket)


@app.get("/eval/run")
def eval_run():
    return run_eval()


@app.get("/incidents")
def incidents():
    return sample_data.INCIDENTS


@app.get("/services")
def services():
    return tools.list_services()


@app.get("/data/{table}")
def data(table: str, limit: int = 20):
    tables = {
        "logs": sample_data.LOGS,
        "metrics": sample_data.METRICS,
        "deploys": sample_data.DEPLOYS,
        "traces": sample_data.TRACES,
        "code": sample_data.CODE,
        "services": sample_data.SERVICES,
    }
    if table not in tables:
        return {"error": f"unknown table: {table}"}
    return tables[table][:limit]
