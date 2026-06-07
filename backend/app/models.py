from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class InvestigationRequest(BaseModel):
    ticket: str = Field(..., min_length=1)


class Evidence(BaseModel):
    id: str
    source: str
    service: str
    summary: str
    data: Dict[str, Any] = Field(default_factory=dict)


class ToolCall(BaseModel):
    name: str
    args: Dict[str, Any] = Field(default_factory=dict)
    result_count: int = 0
    success: bool = True


class InvestigationReport(BaseModel):
    ticket: str
    root_service: Optional[str]
    category: Optional[str]
    deploy_id: Optional[str]
    confidence: float
    summary: str
    timeline: List[str]
    evidence: List[Evidence]
    tool_calls: List[ToolCall]
    next_steps: List[str]
    runbook: List[str]


class EvalResult(BaseModel):
    total: int
    root_service_accuracy: float
    category_accuracy: float
    deploy_accuracy: float
    evidence_recall: float
    hallucinated_evidence_rate: float
    tool_success_rate: float
    average_tool_calls: float
