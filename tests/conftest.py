"""测试配置与 fixtures"""

import pytest
from pathlib import Path
import pandas as pd

from src.utils.config_loader import ConfigLoader


@pytest.fixture
def sample_data():
    """提供示例数据"""
    return pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=10),
        'product': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C'],
        'amount': [100.50, 200.30, 150.75, 300.00, 250.60, 180.90, 320.40, 210.80, 160.20, 290.50],
        'quantity': [10, 20, 15, 30, 25, 18, 32, 21, 16, 29],
        'customer_id': [1, 2, 1, 3, 2, 1, 3, 2, 1, 3]
    })


@pytest.fixture
def sample_config():
    """提供示例配置"""
    return {
        'data_sources': {
            'mysql': {
                'host': 'localhost',
                'port': 3306,
                'database': 'test_db',
                'username': 'root',
                'password': 'test'
            }
        },
        'reports': {
            'test_report': {
                'name': '测试报表',
                'data_source': 'mysql',
                'query': 'SELECT * FROM test_table',
                'output_formats': ['excel', 'html']
            }
        }
    }


@pytest.fixture
def temp_output_dir(tmp_path):
    """提供临时输出目录"""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir
