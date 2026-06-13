import os
import pytest
import requests


TEAM_ID = os.getenv("INFER_TEAM_ID", "e3b2d519-6238-5349-bc06-6f67e74b0d86")
CONTROL_COOKIE = os.getenv("INFER_CONTROL_COOKIE")


@pytest.mark.integration
def test_team_credit_balance_actual_api():
    if not CONTROL_COOKIE:
        pytest.skip("INFER_CONTROL_COOKIE is required for the real API test")

    response = requests.get(
        "https://infer-dev.agentsey.ai/api/control-plane/team-credit-balance",
        params={"teamId": TEAM_ID},
        headers={
            "accept": "*/*",
            "content-type": "application/json",
            "referer": "https://infer-dev.agentsey.ai/dashboard/models",
            "user-agent": "pytest-requests",
        },
        cookies={"__infer_control": CONTROL_COOKIE},
        timeout=10,
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, dict), data
    assert data, "response json should not be empty"
