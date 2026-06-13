# 测试框架运行说明

## 环境要求

- Python 3.10+

## 环境配置

1. 克隆项目并进入项目目录：

```bash
git clone <repository-url>
cd <project-directory>
```

2. 创建并激活虚拟环境（推荐）：

```bash
python3 -m venv venv
source venv/bin/activate
```

## 依赖安装

```bash
pip install -r requirements.txt
```

主要依赖：
- pytest - 测试框架
- requests - HTTP 请求库
- pyyaml - YAML 配置解析
- pytest-html - HTML 测试报告生成

## 测试执行

### 运行所有测试（默认使用 test 环境）

```bash
pytest
```

### 指定测试环境

```bash
pytest --env test
pytest --env prod
```

### 运行指定测试文件

```bash
pytest tests/test_users.py
```

### 查看测试报告

测试完成后，HTML 报告会自动生成在 `reports/report.html`。

## 环境配置文件

- `config/test.yaml` - 测试环境配置
- `config/prod.yaml` - 生产环境配置

## 项目结构

```
├── config/          # 环境配置文件
├── core/            # 核心模块（API 客户端等）
├── data/            # 测试数据（YAML 用例）
├── tests/           # 测试用例
├── utils/           # 工具函数
├── conftest.py      # pytest 全局 fixture
├── pytest.ini       # pytest 配置
└── requirements.txt # 项目依赖
```
