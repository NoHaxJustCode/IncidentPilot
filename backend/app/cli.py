from __future__ import annotations

import argparse
import json
from typing import Any

from .agent import investigate
from .eval import run_eval
from . import sample_data, tools


def _dump(obj: Any) -> str:
    if hasattr(obj, "model_dump"):
        return json.dumps(obj.model_dump(), indent=2)
    return json.dumps(obj, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(prog="incidentpilot", description="Agentic incident investigation CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    investigate_cmd = sub.add_parser("investigate", help="Investigate an incident ticket")
    investigate_cmd.add_argument("--ticket", help="Ticket text")
    investigate_cmd.add_argument("--file", help="Read ticket from file")
    investigate_cmd.add_argument("--json", action="store_true", help="Print raw JSON")

    sub.add_parser("eval", help="Run evaluation suite").add_argument("--json", action="store_true")
    sub.add_parser("list-incidents", help="List bundled synthetic incidents")
    sub.add_parser("services", help="List services")

    data_cmd = sub.add_parser("show-data", help="Show synthetic data table")
    data_cmd.add_argument("table", choices=["logs", "metrics", "deploys", "traces", "code", "services"])
    data_cmd.add_argument("--limit", type=int, default=10)

    args = parser.parse_args()

    if args.command == "investigate":
        ticket = args.ticket
        if args.file:
            with open(args.file, "r", encoding="utf-8") as handle:
                ticket = handle.read().strip()
        if not ticket:
            raise SystemExit("Provide --ticket or --file")
        report = investigate(ticket)
        if args.json:
            print(_dump(report))
        else:
            print(report.summary)
            print(f"confidence: {report.confidence}")
            print("\nevidence:")
            for item in report.evidence:
                print(f"- [{item.id}] {item.summary}")
            print("\nnext steps:")
            for step in report.next_steps:
                print(f"- {step}")
        return

    if args.command == "eval":
        result = run_eval()
        if args.json:
            print(_dump(result))
        else:
            for key, value in result.model_dump().items():
                print(f"{key}: {value}")
        return

    if args.command == "list-incidents":
        for item in sample_data.INCIDENTS:
            print(f"{item['id']}: {item['ticket']}")
        return

    if args.command == "services":
        print(_dump(tools.list_services()))
        return

    if args.command == "show-data":
        tables = {
            "logs": sample_data.LOGS,
            "metrics": sample_data.METRICS,
            "deploys": sample_data.DEPLOYS,
            "traces": sample_data.TRACES,
            "code": sample_data.CODE,
            "services": sample_data.SERVICES,
        }
        print(_dump(tables[args.table][: args.limit]))


if __name__ == "__main__":
    main()
