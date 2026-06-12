import pytest
import yaml
import os
from core.client import APIClient


def load_cases(filename: str) -> list:
    path = os.path.join(os.path.dirname(__file__), f"../data/testcases/{filename}")
    with open(path) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def client(env):
    return APIClient(env)


def pytest_addoption(parser):
    parser.addoption("--env", default="test", help="test environment: test or prod")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")
