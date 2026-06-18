# 环境配置文件说明

`config/` 目录存放各环境的配置文件，文件名格式为 `{env}.yaml`，通过 `load_config(env)` 加载。

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `env` | string | 是 | 环境标识，与文件名保持一致（如 `test`、`prod`） |
| `base_url` | string | 是 | API 的根地址，所有请求路径均拼接在此之后 |
| `timeout` | int | 否 | 请求超时时间（秒），默认值为 `10` |
| `headers` | map | 否 | 附加到每个请求的 HTTP 头，默认包含 `Content-Type: application/json` |

## 现有环境

- `test.yaml` — 测试环境，指向 `https://test-api.example.com`
- `prod.yaml` — 生产环境，指向 `https://api.example.com`

## 新增自定义环境

1. 在 `config/` 目录下新建 `{env}.yaml` 文件，例如 `staging.yaml`：

```yaml
env: staging
base_url: https://staging-api.example.com
timeout: 15
headers:
  Content-Type: application/json
```

2. 在代码或测试中通过环境名称加载：

```python
from core.client import APIClient

client = APIClient(env="staging")
```
