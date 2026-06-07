from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List

from . import sample_data


MUTATION_WORDS = {"insert", "update", "delete", "drop", "alter", "create", "replace", "truncate", "attach", "pragma"}


def _matches(row: Dict[str, Any], query: str) -> bool:
    haystack = " ".join(str(v).lower() for v in row.values())
    return query.lower() in haystack


def list_services() -> List[Dict[str, Any]]:
    return sample_data.SERVICES


def get_deploys(query: str = "") -> List[Dict[str, Any]]:
    if not query:
        return sample_data.DEPLOYS
    return [row for row in sample_data.DEPLOYS if _matches(row, query)]


def search_logs(query: str = "", service: str | None = None) -> List[Dict[str, Any]]:
    rows = sample_data.LOGS
    if service:
        rows = [row for row in rows if row["service"] == service]
    if query:
        rows = [row for row in rows if _matches(row, query)]
    return rows


def query_metrics(service: str | None = None) -> List[Dict[str, Any]]:
    rows = sample_data.METRICS
    if service:
        rows = [row for row in rows if row["service"] == service]
    return rows


def inspect_traces(service: str | None = None, request_id: str | None = None) -> List[Dict[str, Any]]:
    rows = sample_data.TRACES
    if service:
        rows = [row for row in rows if row["service"] == service]
    if request_id:
        rows = [row for row in rows if row["request_id"] == request_id]
    return rows


def search_code(query: str = "", service: str | None = None) -> List[Dict[str, Any]]:
    rows = sample_data.CODE
    if service:
        rows = [row for row in rows if row["service"] == service]
    if query:
        rows = [row for row in rows if _matches(row, query)]
    return rows


def read_only_sql(sql: str) -> List[Dict[str, Any]]:
    lowered = sql.lower()
    if any(word in lowered for word in MUTATION_WORDS):
        raise ValueError("Only read-only SQL-style queries are supported")

    table_match = re.search(r"from\s+(\w+)", lowered)
    if not table_match:
        raise ValueError("Expected a FROM clause")

    tables = {
        "logs": sample_data.LOGS,
        "metrics": sample_data.METRICS,
        "deploys": sample_data.DEPLOYS,
        "traces": sample_data.TRACES,
        "code": sample_data.CODE,
        "services": sample_data.SERVICES,
    }
    table = table_match.group(1)
    if table not in tables:
        raise ValueError(f"Unknown table: {table}")

    rows = list(tables[table])
    service_match = re.search(r"service\s*=\s*'([^']+)'", sql, flags=re.IGNORECASE)
    if service_match:
        service = service_match.group(1)
        rows = [row for row in rows if row.get("service") == service]
    return rows


def extract_deploy_id(ticket: str) -> str | None:
    match = re.search(r"deploy\s+(\d+)", ticket, flags=re.IGNORECASE)
    return match.group(1) if match else None


def infer_service(ticket: str, deploy_id: str | None = None) -> str | None:
    text = ticket.lower()
    for service in [row["name"] for row in sample_data.SERVICES]:
        short = service.replace("-service", "")
        if service in text or short in text:
            return service
    if deploy_id:
        deploys = get_deploys(deploy_id)
        if deploys:
            return deploys[0]["service"]
    return None
