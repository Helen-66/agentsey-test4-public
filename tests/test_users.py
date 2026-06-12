import pytest
import yaml
import os
from utils.assert_helper import assert_status, assert_json_field


def load_cases(filename):
    path = os.path.join(os.path.dirname(__file__), f"../data/testcases/{filename}")
    with open(path) as f:
        return yaml.safe_load(f)


cases = load_cases("users.yaml")


@pytest.mark.parametrize("case", cases, ids=[c["name"] for c in cases])
def test_users(client, case):
    method = case["method"].lower()
    kwargs = {}
    if "params" in case:
        kwargs["params"] = case["params"]
    if "body" in case:
        kwargs["json"] = case["body"]

    response = getattr(client, method)(case["path"], **kwargs)
    assert_status(response, case["expected_status"])
    for field, value in case.get("expected_fields", {}).items():
        assert_json_field(response, field, value)
