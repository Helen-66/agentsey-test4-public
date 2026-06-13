# 常见问题 FAQ

## 1. 如何安装项目依赖？

```bash
pip install -r requirements.txt
```

确保使用 Python 3.8+ 版本。

## 2. 运行测试时报 `ModuleNotFoundError`，怎么办？

请确认已安装所有依赖：

```bash
pip install -r requirements.txt
```

如果使用虚拟环境，确保已激活对应的虚拟环境后再安装依赖。

## 3. 如何切换测试环境？

通过 `--env` 参数指定环境：

```bash
# test 环境（默认）
pytest --env test

# dev 环境
pytest --env dev

# prod 环境
pytest --env prod
```

环境配置文件位于 `config/` 目录下（如 `test.yaml`、`dev.yaml`、`prod.yaml`）。

## 4. 如何添加新的测试用例？

在 `data/testcases/` 目录下创建或编辑 YAML 文件，按照以下格式添加用例：

```yaml
- name: 用例名称
  method: GET
  path: /api/endpoint
  params:
    key: value
  expected_status: 200
  expected_fields:
    field_name: expected_value
```

然后在 `tests/` 目录下创建对应的测试文件，使用 `load_cases()` 加载用例并通过 `@pytest.mark.parametrize` 参数化执行。

## 5. 测试报告在哪里查看？

测试报告自动生成至 `reports/report.html`，运行测试后用浏览器打开即可查看。

## 6. 如何只运行特定标记的测试？

使用 `-m` 参数筛选标记：

```bash
# 只运行集成测试
pytest -m integration
```

可在 `pytest.ini` 中查看和添加自定义标记。

## 7. 请求超时怎么办？

在对应环境的配置文件（如 `config/test.yaml`）中调整 `timeout` 值：

```yaml
timeout: 30
```

默认超时时间为 10 秒。

## 8. 如何添加自定义请求头？

在环境配置文件的 `headers` 字段中添加：

```yaml
headers:
  Content-Type: application/json
  Authorization: Bearer your-token
```

## 9. 如何只运行单个测试文件或用例？

```bash
# 运行单个文件
pytest tests/test_users.py

# 运行文件中的特定用例（通过用例名称匹配）
pytest tests/test_users.py -k "用例名称关键字"
```

## 10. 测试失败时如何调试？

- 使用 `-v` 查看详细输出：`pytest -v`
- 使用 `-s` 显示 print 输出：`pytest -s`
- 使用 `--tb=short` 或 `--tb=long` 控制错误堆栈显示级别
- 查看生成的 HTML 报告获取完整请求和响应信息
