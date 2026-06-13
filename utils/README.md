# utils 工具函数说明

## assert_helper.py

断言辅助函数，用于简化 HTTP 响应的断言操作。

### `assert_status(response, expected_code)`

断言 HTTP 响应状态码。

| 参数 | 类型 | 说明 |
|------|------|------|
| `response` | `requests.Response` | HTTP 响应对象 |
| `expected_code` | `int` | 期望的状态码 |

**示例：**

```python
from utils.assert_helper import assert_status

response = client.get("/api/users")
assert_status(response, 200)
```

---

### `assert_json_field(response, field, expected)`

断言 JSON 响应体中某个字段的值。

| 参数 | 类型 | 说明 |
|------|------|------|
| `response` | `requests.Response` | HTTP 响应对象 |
| `field` | `str` | 要断言的字段名 |
| `expected` | `any` | 期望的字段值 |

**示例：**

```python
from utils.assert_helper import assert_json_field

response = client.get("/api/users/1")
assert_json_field(response, "name", "Alice")
assert_json_field(response, "status", "active")
```

---

### 组合使用示例

```python
from utils.assert_helper import assert_status, assert_json_field

response = client.post("/api/users", json={"name": "Bob"})
assert_status(response, 201)
assert_json_field(response, "name", "Bob")
```
