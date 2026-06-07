from __future__ import annotations

from typing import Any, Dict, List

from . import sample_data


def tables() -> Dict[str, List[Dict[str, Any]]]:
    return {
        "services": sample_data.SERVICES,
        "deploys": sample_data.DEPLOYS,
        "metrics": sample_data.METRICS,
        "logs": sample_data.LOGS,
        "traces": sample_data.TRACES,
        "code": sample_data.CODE,
    }
