# 数据驱动测试说明

本框架通过 YAML 文件实现数据驱动测试，将测试数据与测试逻辑分离，便于维护和扩展测试用例。

## 核心原理

框架使用 `pytest.mark.parametrize` 结合 YAML 文件，将每条 YAML 数据自动转化为独立的测试用例。测试逻辑只需编写一次，通过不同的数据组合即可覆盖多种场景。

## YAML 测试用例格式

测试数据文件存放在 `data/testcases/` 目录下，每个 YAML 文件包含一组测试用例列表。

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 用例标识，用于测试报告展示 |
| description | string | 否 | 用例描述 |
| method | string | 是 | HTTP 请求方法（GET/POST/PUT/DELETE） |
| path | string | 是 | API 请求路径 |
| params | object | 否 | URL 查询参数 |
| body | object | 否 | 请求体（JSON） |
| expected_status | int | 是 | 期望的 HTTP 状态码 |
| expected_fields | object | 否 | 期望响应 JSON 中包含的字段及值 |

### 示例文件

`data/testcases/users.yaml`：

```yaml
- name: get_user_success
  description: 获取用户信息成功
  method: GET
  path: /api/users/1
  params: {}
  expected_status: 200
  expected_fields:
    id: 1

- name: create_user_success
  description: 创建用户成功
  method: POST
  path: /api/users
  body:
    name: test_user
    email: test@example.com
  expected_status: 201
  expected_fields:
    name: test_user
```

## 测试代码实现

### 加载 YAML 数据

通过 `load_cases` 函数读取 YAML 文件并解析为 Python 列表：

```python
import yaml
import os

def load_cases(filename):
    path = os.path.join(os.path.dirname(__file__), f"../data/testcases/{filename}")
    with open(path) as f:
        return yaml.safe_load(f)
```

### 参数化测试用例

使用 `pytest.mark.parametrize` 将数据列表注入测试函数，每条数据生成一个独立的测试用例：

```python
import pytest

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
```

`ids` 参数使用每条用例的 `name` 字段，使测试报告中显示可读的用例名称。

## 添加新测试用例

### 1. 在已有 YAML 文件中追加用例

直接在对应的 YAML 文件中添加新的数据条目即可，无需修改测试代码：

```yaml
- name: get_user_not_found
  description: 获取不存在的用户
  method: GET
  path: /api/users/9999
  params: {}
  expected_status: 404
  expected_fields: {}
```

### 2. 新建测试模块

如需测试新的 API 模块，按以下步骤操作：

1. 在 `data/testcases/` 下创建新的 YAML 文件（如 `orders.yaml`）
2. 在 `tests/` 下创建对应的测试文件（如 `test_orders.py`）
3. 在测试文件中加载数据并编写参数化测试

```python
# tests/test_orders.py
import pytest
from utils.assert_helper import assert_status, assert_json_field

def load_cases(filename):
    path = os.path.join(os.path.dirname(__file__), f"../data/testcases/{filename}")
    with open(path) as f:
        return yaml.safe_load(f)

cases = load_cases("orders.yaml")

@pytest.mark.parametrize("case", cases, ids=[c["name"] for c in cases])
def test_orders(client, case):
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
```

## 运行测试

```bash
# 运行所有测试
pytest

# 运行指定测试文件
pytest tests/test_users.py

# 运行指定用例（通过用例名称过滤）
pytest -k "get_user_success"

# 指定测试环境
pytest --env test
```

## 目录结构

```
data/
└── testcases/
    ├── users.yaml       # 用户模块测试数据
    └── orders.yaml      # 订单模块测试数据（示例）
tests/
├── test_users.py        # 用户模块测试
└── test_orders.py       # 订单模块测试（示例）
```
