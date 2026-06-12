def assert_status(response, expected_code: int):
    assert response.status_code == expected_code, \
        f"Expected {expected_code}, got {response.status_code}: {response.text}"

def assert_json_field(response, field: str, expected):
    data = response.json()
    assert data.get(field) == expected, \
        f"Field '{field}': expected {expected}, got {data.get(field)}"
