"""辅助函数测试"""

from datetime import datetime
import pandas as pd
from src.utils.helpers import (
    format_currency,
    format_percentage,
    format_date,
    safe_divide,
    flatten_dict
)


def test_format_currency():
    """测试货币格式化"""
    assert format_currency(1234.56) == "¥1,234.56"
    assert format_currency(0) == "¥0.00"
    assert format_currency(1000000, symbol="$") == "$1,000,000.00"
    assert format_currency(123.456, decimals=3) == "¥123.456"


def test_format_percentage():
    """测试百分比格式化"""
    assert format_percentage(0.1234) == "12.34%"
    assert format_percentage(1.0) == "100.00%"
    assert format_percentage(0.5, decimals=1) == "50.0%"


def test_format_date():
    """测试日期格式化"""
    dt = datetime(2024, 1, 15)
    assert format_date(dt) == "2024-01-15"
    assert format_date(dt, "%Y/%m/%d") == "2024/01/15"
    
    ts = pd.Timestamp("2024-01-15")
    assert format_date(ts) == "2024-01-15"
    
    assert format_date("2024-01-15") == "2024-01-15"


def test_safe_divide():
    """测试安全除法"""
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(10, 0) == 0.0
    assert safe_divide(10, 0, default=-1) == -1
    assert safe_divide(0, 5) == 0.0


def test_flatten_dict():
    """测试字典扁平化"""
    nested = {
        'a': 1,
        'b': {
            'c': 2,
            'd': {
                'e': 3
            }
        }
    }
    
    expected = {
        'a': 1,
        'b.c': 2,
        'b.d.e': 3
    }
    
    assert flatten_dict(nested) == expected
    assert flatten_dict({'a': 1}) == {'a': 1}
    assert flatten_dict({}) == {}
