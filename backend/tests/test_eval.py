from app.eval import run_eval


def test_eval_passes_sample_incidents():
    result = run_eval()
    assert result.total == 3
    assert result.root_service_accuracy == 1.0
    assert result.category_accuracy == 1.0
    assert result.deploy_accuracy == 1.0
    assert result.tool_success_rate == 1.0
