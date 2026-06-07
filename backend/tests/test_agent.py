from app.agent import investigate


def test_investigate_checkout_ticket():
    report = investigate("Checkout latency increased for premium users after deploy 4921")
    assert report.root_service == "checkout-service"
    assert report.category == "latency_regression"
    assert report.deploy_id == "4921"
    assert report.evidence
    assert report.tool_calls
