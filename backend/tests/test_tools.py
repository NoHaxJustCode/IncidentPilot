import pytest

from app import tools


def test_search_logs_by_deploy():
    rows = tools.search_logs("4921")
    assert rows
    assert rows[0]["service"] == "checkout-service"


def test_read_only_sql_blocks_mutation():
    with pytest.raises(ValueError):
        tools.read_only_sql("drop table logs")


def test_infer_service_from_deploy():
    assert tools.infer_service("latency after deploy 2277", "2277") == "payment-service"
