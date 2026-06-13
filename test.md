# Running the Test Suite

## Prerequisites

- Python 3.x
- pip

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run All Tests

```bash
pytest
```

This uses settings from `pytest.ini`: tests are discovered in the `tests/` directory and an HTML report is generated at `reports/report.html`.

## Run Against a Specific Environment

The `--env` option selects the target environment (default: `test`):

```bash
pytest --env test
pytest --env prod
```

## Run a Specific File or Test

```bash
# run a single file
pytest tests/test_users.py

# run a single test by name
pytest tests/test_users.py -k "test_users"
```

## Configuration Files

| File | Purpose |
|---|---|
| `pytest.ini` | Sets default options and test paths |
| `conftest.py` | Shared fixtures (`client`, `env`) and custom CLI options |

## Test Report

After each run, an HTML report is written to `reports/report.html`. Open it in a browser to see per-test results, captured output, and failure details.
