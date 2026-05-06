# Trae-Solo 报表开发项目 - 代码 Wiki

> 本文档提供项目的完整技术架构说明，包括项目结构、核心模块、关键类与函数、依赖关系以及运行配置等关键信息。

---

## 📋 目录

- [项目概述](#项目概述)
- [项目架构](#项目架构)
- [目录结构](#目录结构)
- [核心模块说明](#核心模块说明)
- [关键类与函数](#关键类与函数)
- [依赖关系](#依赖关系)
- [项目运行方式](#项目运行方式)
- [开发指南](#开发指南)
- [常见问题](#常见问题)

---

## 项目概述

**项目名称**: trae-solo 报表开发项目

**项目状态**: ✅ 已初始化

**项目描述**: 
基于 Python + pandas 的企业级报表开发框架，采用 ETL 架构模式，支持从多种数据源（MySQL、PostgreSQL、REST API、CSV/Excel/JSON/Parquet 文件）提取数据，经过数据清洗、转换和聚合处理后，生成 Excel、PDF、HTML 等多种格式的报表。

**技术栈**: 
- **核心语言**: Python 3.9+
- **数据处理**: pandas
- **数据源**: SQLAlchemy, PyMySQL, psycopg2-binary, requests
- **报表生成**: xlsxwriter, openpyxl, weasyprint, Jinja2
- **配置管理**: PyYAML, python-dotenv
- **日志**: loguru
- **测试**: pytest, pytest-cov
- **代码质量**: black, ruff, mypy

---

## 项目架构

### 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        应用层 (Application)                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   main.py       │  │ run_pipeline.py │  │   CLI 命令行     │ │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘ │
└───────────┼────────────────────┼────────────────────┼───────────┘
            │                    │                    │
┌───────────▼────────────────────▼────────────────────▼───────────┐
│                    业务逻辑层 (PipelineOrchestrator)              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Extract → Transform → Clean → Generate Reports         │   │
│  └─────────────────────────────────────────────────────────┘   │
└───────────────────────────┬───────────────────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────────┐
│                      数据处理层 (Data Processing)               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │   Extract    │  │  Transform   │  │        Clean         │ │
│  │  - MySQL     │  │  - Aggregate │  │  - Remove Duplicates │ │
│  │  - Postgres  │  │  - Filter    │  │  - Handle Missing    │ │
│  │  - API       │  │  - Join      │  │  - Remove Outliers   │ │
│  │  - File      │  │  - Format    │  │                      │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
└───────────────────────────┬───────────────────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────────┐
│                    报表生成层 (Report Generation)               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │    Excel     │  │     PDF      │  │        HTML          │ │
│  │  xlsxwriter  │  │ weasyprint   │  │      Jinja2          │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
```

### 架构说明

项目采用 **ETL（Extract-Transform-Load）+ 报表生成** 的分层架构：

1. **提取层（Extract）**: 统一接口从不同数据源获取数据
2. **转换层（Transform）**: 对数据进行聚合、过滤、连接、格式化
3. **清洗层（Clean）**: 去重、处理缺失值、移除异常值
4. **生成层（Generate）**: 生成多种格式的报表输出

每层通过抽象基类定义统一接口，具体实现可独立替换和扩展。

---

## 目录结构

```
/workspace/
├── README.md                    # 项目说明文档
├── CODE_WIKI.md                 # 代码 Wiki 文档（本文件）
├── main.py                      # 主入口文件
├── pyproject.toml               # Python 项目配置和依赖声明
├── .env.example                 # 环境变量配置模板
├── .gitignore                   # Git 忽略文件配置
│
├── config/                      # 配置文件目录
│   └── settings.yaml            # 数据源、报表定义、日志等统一配置
│
├── src/                         # 源代码目录
│   ├── __init__.py              # 统一导出入口
│   ├── config.py                # 配置加载快捷方式
│   ├── extract/                 # 数据提取层
│   │   ├── __init__.py
│   │   ├── base_extractor.py    #   抽象基类，定义统一接口
│   │   ├── mysql_extractor.py   #   MySQL 数据源提取器
│   │   ├── postgres_extractor.py#   PostgreSQL 数据源提取器
│   │   ├── api_extractor.py     #   REST API 数据源提取器
│   │   └── file_extractor.py    #   文件数据源提取器（CSV/Excel/JSON/Parquet）
│   ├── transform/               # 数据转换层
│   │   ├── __init__.py
│   │   ├── base_transformer.py  #   抽象基类
│   │   ├── aggregate_transformer.py # 聚合转换器（GROUP BY）
│   │   ├── filter_transformer.py  # 过滤转换器（条件/SQL表达式）
│   │   ├── join_transformer.py    # 连接转换器（多表JOIN）
│   │   └── format_transformer.py  # 格式转换器（货币/百分比/日期）
│   ├── clean/                   # 数据清洗层
│   │   ├── __init__.py
│   │   └── data_cleaner.py      #   去重/缺失值处理/异常值剔除
│   ├── report/                  # 报表生成层
│   │   ├── __init__.py
│   │   ├── base_generator.py    #   抽象基类
│   │   ├── excel_generator.py   #   Excel 报表生成器（xlsxwriter）
│   │   ├── pdf_generator.py     #   PDF 报表生成器（weasyprint）
│   │   ├── html_generator.py    #   HTML 报表生成器（jinja2）
│   │   ├── report_engine.py     #   统一报表引擎
│   │   ├── templates/           #   报表模板目录
│   │   │   ├── base_report.html     #   基础报表模板
│   │   │   └── daily_sales.html     #   销售报表模板
│   │   └── output/              #   报表输出目录（运行时生成）
│   └── utils/                   # 工具模块
│       ├── __init__.py
│       ├── config_loader.py     #   YAML 配置加载 + 环境变量解析
│       ├── logger.py            #   日志配置（控制台+文件轮转）
│       └── helpers.py           #   通用辅助函数
│
├── scripts/                     # 脚本工具
│   └── run_pipeline.py          #   ETL 管道编排器
│
├── tests/                       # 测试代码目录
│   ├── conftest.py              #   Pytest fixtures 配置
│   ├── unit/                    #   单元测试
│   │   ├── test_helpers.py      #     辅助函数测试
│   │   └── test_transform.py    #     转换器测试
│   └── integration/             #   集成测试
│       ├── test_config.py       #     配置加载器测试
│       └── test_extractor.py    #     数据提取器测试
│
├── data/                        # 数据目录
│   ├── raw/                     #   原始数据
│   └── processed/               #   处理后数据
│
├── logs/                        # 日志目录
└── docs/                        # 文档目录
```

### 关键目录说明

| 目录 | 说明 |
|------|------|
| `config/` | 集中管理所有配置，支持环境变量替换 |
| `src/extract/` | 数据提取层，支持多种数据源的统一接口 |
| `src/transform/` | 数据转换层，提供聚合、过滤、连接、格式化 |
| `src/clean/` | 数据清洗层，处理去重、缺失值、异常值 |
| `src/report/` | 报表生成层，支持 Excel/PDF/HTML 输出 |
| `src/utils/` | 工具函数，包括配置加载、日志、辅助函数 |
| `scripts/` | 管道编排脚本，串联完整 ETL 流程 |
| `tests/` | 单元测试和集成测试 |
| `data/raw/` | 存放原始数据文件 |
| `data/processed/` | 存放处理后的数据 |

---

## 核心模块说明

### 1. 数据提取模块（Extract）

**文件路径**: `src/extract/`

**职责描述**: 
提供统一的数据提取接口，支持从多种数据源获取数据并返回 pandas DataFrame。

**主要组件**:
- [BaseExtractor](src/extract/base_extractor.py): 抽象基类，定义 `connect()`, `disconnect()`, `extract()` 接口
- [MySQLExtractor](src/extract/mysql_extractor.py): MySQL 数据源提取器，使用 SQLAlchemy 连接
- [PostgresExtractor](src/extract/postgres_extractor.py): PostgreSQL 数据源提取器
- [APIExtractor](src/extract/api_extractor.py): REST API 数据提取器，支持重试机制
- [FileExtractor](src/extract/file_extractor.py): 文件数据提取器，支持 CSV/Excel/JSON/Parquet

**依赖模块**:
- pandas（数据处理）
- sqlalchemy（数据库连接）
- requests（API 请求）

---

### 2. 数据转换模块（Transform）

**文件路径**: `src/transform/`

**职责描述**: 
对提取的数据进行各种转换操作，包括聚合、过滤、连接和格式化。

**主要组件**:
- [BaseTransformer](src/transform/base_transformer.py): 抽象基类，定义 `transform()` 接口
- [AggregateTransformer](src/transform/aggregate_transformer.py): 聚合转换器，支持 GROUP BY 操作
- [FilterTransformer](src/transform/filter_transformer.py): 过滤转换器，支持条件函数和 query 表达式
- [JoinTransformer](src/transform/join_transformer.py): 连接转换器，支持多种 JOIN 方式
- [FormatTransformer](src/transform/format_transformer.py): 格式转换器，支持货币、百分比、日期格式化

**依赖模块**:
- pandas（数据处理）

---

### 3. 数据清洗模块（Clean）

**文件路径**: `src/clean/`

**职责描述**: 
对数据进行清洗操作，确保数据质量。

**主要组件**:
- [DataCleaner](src/clean/data_cleaner.py): 数据清洗器，提供去重、缺失值处理、异常值剔除功能

**依赖模块**:
- pandas（数据处理）

---

### 4. 报表生成模块（Report）

**文件路径**: `src/report/`

**职责描述**: 
将处理后的数据生成各种格式的报表文件。

**主要组件**:
- [BaseReportGenerator](src/report/base_generator.py): 抽象基类，定义 `generate()` 接口
- [ExcelGenerator](src/report/excel_generator.py): Excel 报表生成器，支持冻结窗格、自动筛选
- [PDFGenerator](src/report/pdf_generator.py): PDF 报表生成器，使用 weasyprint 引擎
- [HTMLGenerator](src/report/html_generator.py): HTML 报表生成器，使用 Jinja2 模板引擎
- [ReportEngine](src/report/report_engine.py): 统一报表引擎，根据配置自动生成多种格式

**依赖模块**:
- pandas（数据处理）
- xlsxwriter/openpyxl（Excel 生成）
- weasyprint（PDF 生成）
- jinja2（HTML 模板渲染）

---

### 5. 工具模块（Utils）

**文件路径**: `src/utils/`

**职责描述**: 
提供项目通用的工具函数和基础设施支持。

**主要组件**:
- [ConfigLoader](src/utils/config_loader.py): YAML 配置加载器，支持环境变量替换（`${VAR:default}` 语法）
- [setup_logger](src/utils/logger.py): 日志系统配置，支持控制台和文件轮转输出
- [helpers.py](src/utils/helpers.py): 通用辅助函数（货币格式化、百分比格式化、日期格式化、安全除法等）

---

### 6. 管道编排模块（Pipeline）

**文件路径**: `scripts/run_pipeline.py`

**职责描述**: 
串联完整的 ETL + 报表生成流程，提供命令行接口。

**主要组件**:
- [PipelineOrchestrator](scripts/run_pipeline.py): ETL 管道编排器，包含 `extract_data()`, `transform_data()`, `generate_reports()`, `run()` 方法

---

## 关键类与函数

### 核心类说明

#### 类名：BaseExtractor

**文件位置**: [src/extract/base_extractor.py](src/extract/base_extractor.py)

**职责描述**:
数据提取器抽象基类，定义统一的数据提取接口。所有具体提取器必须继承此类。

**主要方法**:

| 方法名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `connect()` | 无 | None | 建立数据源连接 |
| `disconnect()` | 无 | None | 关闭数据源连接 |
| `extract(query, params)` | `query: str`, `params: Optional[tuple]` | `pd.DataFrame` | 提取数据 |

**使用示例**:
```python
class MySQLExtractor(BaseExtractor):
    def connect(self):
        self.engine = create_engine(self.connection_string)
        self.connection = self.engine.connect()
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
    
    def extract(self, query, params=None):
        return pd.read_sql(query, self.connection, params=params)
```

---

#### 类名：BaseTransformer

**文件位置**: [src/transform/base_transformer.py](src/transform/base_transformer.py)

**职责描述**:
数据转换器抽象基类，定义统一的数据转换接口。

**主要方法**:

| 方法名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `transform(df, **kwargs)` | `df: pd.DataFrame` | `pd.DataFrame` | 转换数据 |

---

#### 类名：DataCleaner

**文件位置**: [src/clean/data_cleaner.py](src/clean/data_cleaner.py)

**职责描述**:
提供完整的数据清洗功能，包括去重、缺失值处理、异常值剔除。

**主要方法**:

| 方法名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `remove_duplicates(df, subset, keep)` | `df: pd.DataFrame` | `pd.DataFrame` | 移除重复数据 |
| `handle_missing_values(df, strategy, columns)` | `df: pd.DataFrame` | `pd.DataFrame` | 处理缺失值 |
| `remove_outliers(df, columns, method)` | `df: pd.DataFrame` | `pd.DataFrame` | 移除异常值 |
| `clean(df, steps)` | `df: pd.DataFrame`, `steps: list` | `pd.DataFrame` | 执行完整清洗流程 |

---

#### 类名：BaseReportGenerator

**文件位置**: [src/report/base_generator.py](src/report/base_generator.py)

**职责描述**:
报表生成器抽象基类，定义统一的报表生成接口。

**主要方法**:

| 方法名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `generate(data, filename, **kwargs)` | `data: pd.DataFrame`, `filename: str` | `Path` | 生成报表文件 |

---

#### 类名：ReportEngine

**文件位置**: [src/report/report_engine.py](src/report/report_engine.py)

**职责描述**:
统一报表引擎，根据配置自动生成多种格式的报表。

**主要方法**:

| 方法名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `generate(data, filename, formats, title)` | `data: pd.DataFrame`, `formats: list[str]` | `list[Path]` | 生成多格式报表 |
| `get_generator(format_type)` | `format_type: str` | `BaseReportGenerator` | 获取指定格式生成器 |

---

#### 类名：PipelineOrchestrator

**文件位置**: [scripts/run_pipeline.py](scripts/run_pipeline.py)

**职责描述**:
ETL + 报表生成管道编排器，串联完整的数据处理流程。

**主要方法**:

| 方法名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `extract_data(report_config, params)` | `report_config: dict` | `pd.DataFrame` | 执行数据提取 |
| `transform_data(data, transformations)` | `data: pd.DataFrame` | `pd.DataFrame` | 执行数据转换 |
| `generate_reports(data, report_config)` | `data: pd.DataFrame` | `list` | 生成报表 |
| `run(report_name, params)` | `report_name: str` | `list` | 运行完整流程 |

---

#### 类名：ConfigLoader

**文件位置**: [src/utils/config_loader.py](src/utils/config_loader.py)

**职责描述**:
YAML 配置加载器，支持环境变量替换。

**主要方法**:

| 方法名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `load()` | 无 | None | 加载配置文件 |
| `get(key, default)` | `key: str` | Any | 获取配置值（支持点号分隔的嵌套键） |
| `get_all()` | 无 | dict | 获取完整配置 |
| `reload()` | 无 | None | 重新加载配置 |

---

### 核心函数说明

#### 函数名：setup_logger

**文件位置**: [src/utils/logger.py](src/utils/logger.py)

**函数签名**:
```python
def setup_logger(config: Optional[dict] = None) -> None
```

**参数说明**:

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `config` | dict | 否 | None | 日志配置字典 |

**使用示例**:
```python
from src.utils.logger import setup_logger

setup_logger({
    'level': 'DEBUG',
    'handlers': {
        'console': {'enabled': True, 'level': 'INFO'},
        'file': {'enabled': True, 'path': './logs/app.log'}
    }
})
```

---

#### 函数名：format_currency

**文件位置**: [src/utils/helpers.py](src/utils/helpers.py)

**函数签名**:
```python
def format_currency(value: float, symbol: str = "¥", decimals: int = 2) -> str
```

**参数说明**:

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `value` | float | 是 | - | 数值 |
| `symbol` | str | 否 | "¥" | 货币符号 |
| `decimals` | int | 否 | 2 | 小数位数 |

**返回值**:
- 类型：str
- 说明：格式化后的货币字符串

---

## 依赖关系

### 外部依赖

#### 主要依赖包

| 依赖名称 | 版本 | 用途 | 官方文档 |
|----------|------|------|----------|
| pandas | >=2.0.0 | 数据处理和分析 | https://pandas.pydata.org |
| openpyxl | >=3.1.0 | Excel 文件读取 | https://openpyxl.readthedocs.io |
| xlsxwriter | >=3.1.0 | Excel 文件生成 | https://xlsxwriter.readthedocs.io |
| sqlalchemy | >=2.0.0 | 数据库连接和 ORM | https://www.sqlalchemy.org |
| pymysql | >=1.1.0 | MySQL 数据库驱动 | https://pymysql.readthedocs.io |
| psycopg2-binary | >=2.9.0 | PostgreSQL 数据库驱动 | https://www.psycopg.org |
| requests | >=2.31.0 | HTTP 请求库 | https://requests.readthedocs.io |
| pyyaml | >=6.0 | YAML 配置文件解析 | https://pyyaml.org |
| python-dotenv | >=1.0.0 | 环境变量加载 | https://saurabh-kumar.com/python-dotenv |
| jinja2 | >=3.1.0 | 模板引擎 | https://jinja.palletsprojects.com |
| weasyprint | >=60.0 | PDF 生成引擎 | https://weasyprint.org |
| loguru | >=0.7.0 | 日志库 | https://github.com/Delgan/loguru |

#### 开发依赖

| 依赖名称 | 版本 | 用途 |
|----------|------|------|
| pytest | >=7.0.0 | 单元测试框架 |
| pytest-cov | >=4.0.0 | 测试覆盖率 |
| black | >=23.0.0 | 代码格式化 |
| ruff | >=0.1.0 | 代码检查 |
| mypy | >=1.0.0 | 类型检查 |

### 内部依赖

#### 模块依赖图

```
main.py
  └── PipelineOrchestrator (scripts/run_pipeline.py)
        ├── ConfigLoader (src/utils/config_loader.py)
        ├── setup_logger (src/utils/logger.py)
        │
        ├── Extractors (src/extract/)
        │   ├── BaseExtractor
        │   ├── MySQLExtractor → sqlalchemy, pymysql
        │   ├── PostgresExtractor → sqlalchemy, psycopg2
        │   ├── APIExtractor → requests
        │   └── FileExtractor → pandas
        │
        ├── DataCleaner (src/clean/data_cleaner.py)
        │   └── pandas
        │
        ├── Transformers (src/transform/)
        │   ├── AggregateTransformer → pandas
        │   ├── FilterTransformer → pandas
        │   ├── JoinTransformer → pandas
        │   └── FormatTransformer → pandas
        │
        └── ReportEngine (src/report/report_engine.py)
            ├── ExcelGenerator → xlsxwriter
            ├── PDFGenerator → weasyprint
            └── HTMLGenerator → jinja2
```

### 依赖管理

**包管理工具**: pip (通过 pyproject.toml)

**安装依赖命令**:
```bash
pip install -e ".[dev]"
```

**更新依赖命令**:
```bash
pip install --upgrade -e ".[dev]"
```

---

## 项目运行方式

### 环境要求

- **Python**: 3.9+
- **pip**: 最新稳定版
- **数据库**: MySQL/PostgreSQL（可选，根据数据源需求）

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/xbn-ming/trae-solo.git
cd trae-solo
```

#### 2. 安装依赖

```bash
pip install -e ".[dev]"
```

#### 3. 配置环境变量

```bash
# 复制环境配置模板
cp .env.example .env

# 编辑 .env 文件，填写实际的数据库连接信息等
```

#### 4. 验证安装

```bash
python -c "from src.config import load_config; print('安装成功')"
```

### 运行命令

#### 生成报表

```bash
# 生成全部报表
python main.py --report all

# 生成指定报表
python main.py --report daily_sales

# 使用自定义配置文件
python main.py --report daily_sales --config config/custom_settings.yaml

# 指定日期范围
python main.py --report daily_sales --start-date 2024-01-01 --end-date 2024-01-31
```

#### 直接运行管道脚本

```bash
python scripts/run_pipeline.py --report daily_sales
```

#### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/unit/test_helpers.py -v

# 运行测试并生成覆盖率报告
pytest tests/ --cov=src --cov-report=html
```

### 配置文件说明

**配置文件位置**: `config/settings.yaml`

**主要配置项**:

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `data_sources` | dict | 数据源配置（mysql/postgresql/api/file） |
| `output` | dict | 输出配置（base_path/formats） |
| `reports` | dict | 报表定义列表 |
| `logging` | dict | 日志配置 |
| `global` | dict | 全局配置（时区、批量大小等） |

**环境变量替换**: 配置文件中支持 `${VAR:default}` 语法引用环境变量：

```yaml
data_sources:
  mysql:
    host: "${MYSQL_HOST:localhost}"
    port: "${MYSQL_PORT:3306}"
```

---

## 开发指南

### 代码规范

**代码格式化工具**: black
**代码检查工具**: ruff
**类型检查工具**: mypy

**命名规范**:
- 类名：PascalCase（如 `MySQLExtractor`）
- 函数/方法名：snake_case（如 `extract_data`）
- 变量名：snake_case（如 `report_config`）
- 常量名：UPPER_SNAKE_CASE（如 `DEFAULT_TIMEOUT`）
- 文件名：snake_case（如 `base_extractor.py`）

### 提交规范

**Git Commit Message 格式**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type 类型说明**:
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具链相关

### 测试指南

**测试框架**: pytest

**测试目录结构**:
```
tests/
├── conftest.py          # 全局 fixtures
├── unit/                # 单元测试
└── integration/         # 集成测试
```

**运行测试**:
```bash
# 运行所有测试
pytest tests/ -v

# 运行单元测试
pytest tests/unit/ -v

# 运行集成测试
pytest tests/integration/ -v

# 生成覆盖率报告
pytest tests/ --cov=src --cov-report=html
```

**编写测试示例**:
```python
import pytest
from src.transform.aggregate_transformer import AggregateTransformer

def test_aggregate_transform(sample_df):
    transformer = AggregateTransformer()
    result = transformer.transform(
        sample_df,
        group_by=['category'],
        aggregations={'amount': 'sum'}
    )
    assert len(result) == 3
    assert 'amount' in result.columns
```

---

## 常见问题

### Q1: 如何添加新的数据源？

**解决方案**:
1. 在 `src/extract/` 目录下创建新的提取器文件（如 `oracle_extractor.py`）
2. 继承 `BaseExtractor` 类
3. 实现 `connect()`, `disconnect()`, `extract()` 三个方法
4. 在 `src/extract/__init__.py` 中导出新类
5. 在 `scripts/run_pipeline.py` 的 `EXTRACTORS` 字典中注册

```python
from src.extract.oracle_extractor import OracleExtractor

class PipelineOrchestrator:
    EXTRACTORS = {
        'mysql': MySQLExtractor,
        'oracle': OracleExtractor,
        # ...
    }
```

---

### Q2: 如何添加新的报表格式？

**解决方案**:
1. 在 `src/report/` 目录下创建新的生成器文件（如 `csv_generator.py`）
2. 继承 `BaseReportGenerator` 类
3. 实现 `generate()` 方法
4. 在 `src/report/__init__.py` 中导出新类
5. 在 `src/report/report_engine.py` 的 `GENERATORS` 字典中注册

---

### Q3: 如何自定义报表模板？

**解决方案**:
1. 在 `src/report/templates/` 目录下创建新的 HTML 模板文件
2. 使用 Jinja2 模板语法
3. 在报表配置中指定模板名称

```yaml
reports:
  custom_report:
    name: "自定义报表"
    template: "custom_template.html"
```

---

### Q4: 如何处理大数据量？

**解决方案**:
1. 在配置文件中调整 `batch_size` 参数
2. 使用 pandas 的分块读取功能
3. 考虑使用数据库端的聚合操作减少数据传输

---

## 附录

### 相关资源

- [项目仓库](https://github.com/xbn-ming/trae-solo)
- [问题反馈](https://github.com/xbn-ming/trae-solo/issues)

### 更新日志

| 版本 | 日期 | 更新内容 | 作者 |
|------|------|----------|------|
| 0.1.0 | 2026-05-06 | 初始版本，创建完整的报表开发框架 | - |

---

本文档最后更新：2026-05-06
