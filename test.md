# 测试运行说明

## 环境要求

- Python 3.8+

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行测试

### 运行全部测试（默认 test 环境）

```bash
pytest
```

### 指定环境运行

```bash
# test 环境
pytest --env test

# prod 环境
pytest --env prod

# dev 环境
pytest --env dev
```

### 只运行集成测试

```bash
pytest -m integration
```

测试报告会自动生成至 `reports/report.html`。

## 环境配置

各环境配置文件位于 `config/` 目录下（如 `test.yaml`、`prod.yaml`、`dev.yaml`），可在其中修改 `base_url`、`timeout`、请求头等参数。
