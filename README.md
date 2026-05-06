# Trae-Solo 报表开发项目

基于 Python + pandas 的企业级报表开发框架，支持多数据源、ETL 处理和多种报表格式输出。

## 快速开始

### 环境要求

- Python 3.9+

### 安装

```bash
# 克隆项目
git clone <repository-url>
cd trae-solo

# 安装依赖
pip install -e ".[dev]"

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写实际配置
```

### 运行

```bash
# 生成全部报表
python main.py --report all

# 生成指定报表
python main.py --report daily_sales

# 使用自定义配置
python main.py --report daily_sales --start-date 2024-01-01 --end-date 2024-01-31
```

### 测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行测试并生成覆盖率报告
pytest tests/ --cov=src --cov-report=html
```

## 项目结构

```
├── config/              # 配置文件
│   └── settings.yaml    # 数据源、输出、报表定义
├── src/                 # 源代码
│   ├── extract/         # 数据提取层（MySQL/PostgreSQL/API/文件）
│   ├── transform/       # 数据转换层（聚合/过滤/连接/格式化）
│   ├── clean/           # 数据清洗层
│   ├── report/          # 报表生成层（Excel/PDF/HTML）
│   └── utils/           # 工具函数（配置/日志/辅助）
├── scripts/             # 脚本工具
├── tests/               # 测试代码
├── data/                # 数据目录
├── logs/                # 日志目录
└── docs/                # 文档目录
```

## 核心功能

- **多数据源支持**: MySQL, PostgreSQL, REST API, CSV/Excel/JSON/Parquet 文件
- **ETL 处理**: 数据提取、转换、清洗、聚合
- **多格式输出**: Excel, PDF, HTML
- **配置驱动**: YAML 配置，支持环境变量替换
- **管道编排**: 完整的 ETL + 报表生成流水线

## 文档

- [Code Wiki](./CODE_WIKI.md) - 完整的项目架构和技术文档
