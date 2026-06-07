from __future__ import annotations

from typing import Any, Dict, List

from .models import Evidence, InvestigationReport, ToolCall
from . import tools


def _call(name: str, args: Dict[str, Any], rows: List[Dict[str, Any]], success: bool = True) -> ToolCall:
    return ToolCall(name=name, args=args, result_count=len(rows), success=success)


def _evidence_from_rows(rows: List[Dict[str, Any]], source: str) -> List[Evidence]:
    evidence: List[Evidence] = []
    for row in rows:
        evidence.append(
            Evidence(
                id=row.get("id", f"{source}_{len(evidence)}"),
                source=source,
                service=row.get("service", "unknown"),
                summary=row.get("summary") or row.get("message") or row.get("snippet") or str(row),
                data=row,
            )
        )
    return evidence


def classify_category(ticket: str, evidence: List[Evidence]) -> str:
    text = " ".join([ticket] + [e.summary for e in evidence]).lower()
    if "duplicate" in text:
        return "data_duplication"
    if "timeout" in text:
        return "timeout_regression"
    if "latency" in text or "slow" in text or "p95" in text:
        return "latency_regression"
    return "unknown"


def investigate(ticket: str) -> InvestigationReport:
    tool_calls: List[ToolCall] = []
    evidence: List[Evidence] = []

    deploy_id = tools.extract_deploy_id(ticket)
    service = tools.infer_service(ticket, deploy_id)

    deploy_rows = tools.get_deploys(deploy_id or "")
    tool_calls.append(_call("get_deploys", {"query": deploy_id or ""}, deploy_rows))
    evidence.extend(_evidence_from_rows(deploy_rows, "deploys"))

    metric_rows = tools.query_metrics(service)
    tool_calls.append(_call("query_metrics", {"service": service}, metric_rows))
    evidence.extend(_evidence_from_rows(metric_rows, "metrics"))

    log_query = deploy_id or service or ""
    log_rows = tools.search_logs(log_query, service)
    tool_calls.append(_call("search_logs", {"query": log_query, "service": service}, log_rows))
    evidence.extend(_evidence_from_rows(log_rows, "logs"))

    sql_rows: List[Dict[str, Any]] = []
    try:
        if service:
            sql_rows = tools.read_only_sql(f"select * from logs where service = '{service}'")
        else:
            sql_rows = tools.read_only_sql("select * from logs")
        tool_calls.append(_call("read_only_sql", {"table": "logs", "service": service}, sql_rows))
        evidence.extend(_evidence_from_rows(sql_rows, "sql"))
    except Exception:
        tool_calls.append(_call("read_only_sql", {"table": "logs", "service": service}, [], success=False))

    trace_rows = tools.inspect_traces(service)
    tool_calls.append(_call("inspect_traces", {"service": service}, trace_rows))
    evidence.extend(_evidence_from_rows(trace_rows, "traces"))

    code_rows = tools.search_code(service or ticket, service)
    tool_calls.append(_call("search_code", {"query": service or ticket, "service": service}, code_rows))
    evidence.extend(_evidence_from_rows(code_rows, "code"))

    deduped: Dict[str, Evidence] = {}
    for item in evidence:
        deduped[item.id] = item
    evidence = list(deduped.values())

    service_scores: Dict[str, int] = {}
    for item in evidence:
        service_scores[item.service] = service_scores.get(item.service, 0) + 1
    if service_scores:
        root_service = max(service_scores, key=service_scores.get)
    else:
        root_service = service

    category = classify_category(ticket, evidence)
    confidence = min(0.95, 0.45 + 0.08 * len(evidence)) if root_service else 0.2

    timeline = []
    for item in evidence:
        timestamp = item.data.get("timestamp")
        if timestamp:
            timeline.append(f"{timestamp}: {item.summary}")

    evidence_ids = ", ".join(item.id for item in evidence[:5]) or "no evidence"
    summary = (
        f"Likely root cause is {category} in {root_service}. "
        f"Deploy {deploy_id or 'unknown'} is supported by evidence: {evidence_ids}."
    )

    next_steps = [
        "Review the implicated deploy diff.",
        "Roll back or disable the suspected feature flag if customer impact is ongoing.",
        "Add a regression test for the detected failure mode.",
    ]
    runbook = [
        "Confirm metric spike timing against deploy timing.",
        "Sample impacted request traces.",
        "Search logs for the deploy ID and request IDs.",
        "Validate the fix with the same eval scenario.",
    ]

    return InvestigationReport(
        ticket=ticket,
        root_service=root_service,
        category=category,
        deploy_id=deploy_id,
        confidence=round(confidence, 2),
        summary=summary,
        timeline=timeline,
        evidence=evidence,
        tool_calls=tool_calls,
        next_steps=next_steps,
        runbook=runbook,
    )
