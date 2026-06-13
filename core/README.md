# API 客户端使用说明

## 初始化

`APIClient` 通过环境名称加载对应的配置文件（`config/<env>.yaml`）。

```python
from core.client import APIClient

client = APIClient(env="prod")   # 加载 config/prod.yaml
client = APIClient(env="test")   # 加载 config/test.yaml
```

配置文件字段：

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `base_url` | 接口根地址 | 必填 |
| `timeout` | 请求超时秒数 | `10` |
| `headers` | 公共请求头 | `{}` |

## 请求方法

所有方法均接受额外的 `kwargs`，会透传给底层 `requests.Session.request`。

```python
# GET
response = client.get("/users", params={"page": 1})

# POST
response = client.post("/users", json={"name": "Alice"})

# PUT
response = client.put("/users/1", json={"name": "Bob"})

# DELETE
response = client.delete("/users/1")

# 通用方法
response = client.request("PATCH", "/users/1", json={"name": "Carol"})
```

## 响应处理

返回值为 `requests.Response` 对象。

```python
response = client.get("/users/1")

response.status_code   # HTTP 状态码，如 200
response.json()        # 解析 JSON 响应体
response.text          # 原始响应文本
response.raise_for_status()  # 非 2xx 时抛出 HTTPError
```
