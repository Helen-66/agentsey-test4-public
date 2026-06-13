# CI/CD 集成说明

本文档说明如何将测试框架集成到 CI/CD 流水线中。

## GitHub Actions 集成

在项目根目录创建 `.github/workflows/test.yml` 文件：

```yaml
name: API Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest --env test

      - name: Upload test report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-report
          path: reports/report.html
```

## 配置说明

| 参数 | 说明 |
|------|------|
| `on.push.branches` | 触发 CI 的目标分支 |
| `python-version` | Python 版本，需 3.10+ |
| `--env test` | 指定测试环境（可替换为 `prod`） |

## 测试报告

每次 CI 运行后，HTML 报告会作为 Artifact 上传，可在 Actions 页面下载查看。

## 多环境测试

如需同时测试多个环境，可使用矩阵策略：

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        env: [test, prod]

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - run: pip install -r requirements.txt

      - name: Run tests (${{ matrix.env }})
        run: pytest --env ${{ matrix.env }}

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: report-${{ matrix.env }}
          path: reports/report.html
```
