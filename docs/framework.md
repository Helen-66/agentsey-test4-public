# API Test Framework Documentation

## Overview

This is a data-driven API testing framework built on pytest. It separates test logic from test data: test cases are defined in YAML files, and the framework executes them against configurable environments via a shared HTTP client.

## Project Structure

```
├── config/              # Environment configuration files (YAML)
│   ├── test.yaml
│   └── prod.yaml
├── core/
│   └── client.py        # APIClient – HTTP session wrapper
├── data/
│   └── testcases/       # YAML-defined test case payloads
│       └── users.yaml
├── tests/               # pytest test modules
│   └── test_users.py
├── utils/
│   └── assert_helper.py # Response assertion helpers
├── conftest.py          # Session-scoped fixtures and CLI options
└── pytest.ini           # pytest configuration
```

## Technical Implementation

### `core/client.py` — APIClient

`APIClient` is the central HTTP client. On construction it loads the environment config, sets `base_url`, `timeout`, and session-level headers, then exposes `get`, `post`, `put`, and `delete` convenience methods that all delegate to a single `request()` method.

```python
client = APIClient(env="test")
response = client.get("/api/users/1")
```

Key details:
- Uses `requests.Session` for connection pooling and shared headers.
- `load_config(env)` resolves `config/<env>.yaml` relative to `core/`.

### `utils/assert_helper.py` — Assertion Helpers

| Function | Purpose |
|---|---|
| `assert_status(response, code)` | Asserts HTTP status code with a descriptive failure message. |
| `assert_json_field(response, field, expected)` | Deserializes the response body and asserts a top-level JSON field value. |

### `conftest.py` — Fixtures

| Fixture / Hook | Scope | Purpose |
|---|---|---|
| `env` | session | Reads `--env` CLI option (default: `test`). |
| `client` | session | Instantiates a single `APIClient` shared across all tests. |
| `load_cases(filename)` | – | Helper that loads a YAML file from `data/testcases/`. |
| `pytest_addoption` | – | Registers the `--env` option with pytest. |

### `tests/test_users.py` — Test Module

Loads `data/testcases/users.yaml`, parametrizes a single test function over every case, and for each case:
1. Calls the appropriate HTTP method with optional `params` or `body`.
2. Asserts the response status code.
3. Iterates over `expected_fields` and asserts each field value.

### `data/testcases/users.yaml` — Test Case Schema

Each entry in a test case YAML file follows this structure:

```yaml
- name: <unique identifier>          # required – used as the pytest test ID
  description: <human-readable text> # optional
  method: GET | POST | PUT | DELETE  # required
  path: /api/...                     # required – appended to base_url
  params:                          # optional – URL query parameters
  body: {}                           # optional – JSON request body
  expected_status: 200               # required – expected HTTP status code
  expected_fields:                   # optional – key/value assertions on response JSON
    field_name: expected_value
```

## Data Flow

```
pytest --env <env>
       │
       ▼
conftest.py: pytest_addoption resolves --env
       │
       ▼
conftest.py: client fixture → APIClient(env)
       │                          │
       │                          ▼
       │                  config/<env>.yaml
       │                  (base_url, timeout, headers)
       │
       ▼
tests/test_*.py: load_cases("*.yaml")
       │
       ▼
data/testcases/*.yaml → list of test case dicts
       │
       ▼
@pytest.mark.parametrize → one test per case
       │
       ▼
client.<method>(path, params/body)
       │
       ▼
requests.Session → HTTP request to base_url + path
       │
       ▼
Response → assert_status() + assert_json_field()
       │
       ▼
pytest-html → reports/report.html
```

## Configuration

Environment configs live in `config/`. Each file is a YAML document with the following keys:

| Key | Required | Default | Description |
|---|---|---|---|
| `base_url` | yes | – | Root URL prepended to every request path. |
| `timeout` | no | `10` | Request timeout in seconds. |
| `headers` | no | `{}` | Headers added to every request in the session. |

**Example (`config/test.yaml`):**
```yaml
env: test
base_url: https://test-api.example.com
timeout: 10
headers:
  Content-Type: application/json
```

Select the environment at runtime:
```bash
pytest --env test   # default
pytest --env prod
```

## Running Tests

```bash
pip install -r requirements.txt

# run all tests (test environment)
pytest

# run against production
pytest --env prod

# run a single file
pytest tests/test_users.py

# HTML report is written to reports/report.html automatically
```

## Extension Points

### Add a new API under test

1. Create `data/testcases/<resource>.yaml` following the schema above.
2. Create `tests/test_<resource>.py` that loads the new YAML and applies the same parametrize pattern as `test_users.py`.

### Add a new environment

Create `config/<env>.yaml` with at minimum a `base_url`, then run `pytest --env <env>`.

### Add new assertion helpers

Add functions to `utils/assert_helper.py` and import them in any test module.

### Add new HTTP methods or auth

Extend `APIClient` in `core/client.py`. For example, to support bearer token auth, update the session headers in `__init__` or add a `set_token()` method.
