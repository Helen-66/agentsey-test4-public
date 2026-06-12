import requests
import yaml
import os


def load_config(env: str) -> dict:
    config_path = os.path.join(os.path.dirname(__file__), f"../config/{env}.yaml")
    with open(config_path) as f:
        return yaml.safe_load(f)


class APIClient:
    def __init__(self, env: str):
        config = load_config(env)
        self.base_url = config["base_url"]
        self.timeout = config.get("timeout", 10)
        self.session = requests.Session()
        self.session.headers.update(config.get("headers", {}))

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        return self.session.request(method, url, timeout=self.timeout, **kwargs)

    def get(self, path: str, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs):
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.request("DELETE", path, **kwargs)
