from app.eval import run_eval


def test_eval_model_shape():
    result = run_eval()
    data = result.model_dump()
    assert "root_service_accuracy" in data
    assert "hallucinated_evidence_rate" in data
