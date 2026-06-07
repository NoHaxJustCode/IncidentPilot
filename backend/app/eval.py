from __future__ import annotations

from . import sample_data
from .agent import investigate
from .models import EvalResult


def run_eval() -> EvalResult:
    total = len(sample_data.INCIDENTS)
    root_ok = 0
    category_ok = 0
    deploy_ok = 0
    evidence_recall_total = 0.0
    hallucinated = 0
    cited = 0
    tool_success = 0
    tool_total = 0
    tool_calls = 0

    for case in sample_data.INCIDENTS:
        report = investigate(case["ticket"])
        root_ok += int(report.root_service == case["expected_service"])
        category_ok += int(report.category == case["expected_category"])
        deploy_ok += int(report.deploy_id == case["expected_deploy_id"])

        actual_ids = {item.id for item in report.evidence}
        expected_ids = set(case["expected_evidence_ids"])
        evidence_recall_total += len(actual_ids & expected_ids) / len(expected_ids)

        for item in report.evidence:
            cited += 1
            if not item.id:
                hallucinated += 1
        for call in report.tool_calls:
            tool_total += 1
            tool_success += int(call.success)
        tool_calls += len(report.tool_calls)

    return EvalResult(
        total=total,
        root_service_accuracy=root_ok / total,
        category_accuracy=category_ok / total,
        deploy_accuracy=deploy_ok / total,
        evidence_recall=evidence_recall_total / total,
        hallucinated_evidence_rate=(hallucinated / cited) if cited else 0.0,
        tool_success_rate=(tool_success / tool_total) if tool_total else 0.0,
        average_tool_calls=tool_calls / total,
    )
