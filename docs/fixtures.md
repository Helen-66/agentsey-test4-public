# Fixture 使用说明

本文档说明 `conftest.py` 中定义的 fixture 的作用、作用域和使用方式，以及如何自定义新的 fixture。

## 已定义的 Fixture

### `env`

- **作用**：获取当前测试运行的目标环境名称（如 `test` 或 `prod`）。通过命令行参数 `--env` 传入，默认值为 `test`。
- **作用域**：`session`（整个测试会话共享同一个实例）
- **使用方式**：

```python
def test_example(env):
    print(f"当前环境: {env}")  # 输出 "test" 或 "prod"
```

运行测试时可通过命令行指定环境：

```bash
pytest --env=prod
```

### `client`

- **作用**：根据 `env` fixture 提供的环境名称，创建一个 `APIClient` 实例，用于发送 HTTP 请求。`APIClient` 会自动加载对应环境的配置文件（`config/{env}.yaml`）中的 `base_url`、`timeout` 和 `headers`。
- **作用域**：`session`（整个测试会话共享同一个实例）
- **依赖**：`env`
- **使用方式**：

```python
def test_get_users(client):
    response = client.get("/api/users")
    assert response.status_code == 200
```

## 辅助函数

### `load_cases(filename: str) -> list`

- **作用**：从 `data/testcases/` 目录加载 YAML 格式的测试用例数据。
- **使用方式**：

```python
from conftest import load_cases

cases = load_cases("users.yaml")
```

## 如何自定义新的 Fixture

在 `conftest.py` 中添加新的 fixture 函数即可。以下是一些常见模式：

### 基本 fixture

```python
@pytest.fixture
def sample_data():
    """每个测试函数调用时都会创建新的实例"""
    return {"name": "test", "value": 123}
```

### 带作用域的 fixture

```python
@pytest.fixture(scope="module")
def db_connection():
    """同一模块内的测试共享连接"""
    conn = create_connection()
    yield conn
    conn.close()
```

### 依赖其他 fixture

```python
@pytest.fixture
def auth_client(client):
    """基于已有的 client fixture 创建带认证的客户端"""
    client.session.headers.update({"Authorization": "Bearer test-token"})
    return client
```

### 作用域说明

| 作用域 | 说明 |
|--------|------|
| `function` | 默认值，每个测试函数独立创建 |
| `class` | 同一测试类内共享 |
| `module` | 同一模块（文件）内共享 |
| `session` | 整个测试会话共享 |

### 注意事项

- `session` 作用域的 fixture 不能依赖更小作用域的 fixture。
- 使用 `yield` 可以在测试结束后执行清理逻辑。
- fixture 名称即为测试函数参数名，pytest 会自动注入。
