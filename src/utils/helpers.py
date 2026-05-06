"""通用辅助函数"""

from datetime import datetime
from typing import Any, Optional
import pandas as pd


def format_currency(value: float, symbol: str = "¥", decimals: int = 2) -> str:
    """格式化货币值
    
    Args:
        value: 数值
        symbol: 货币符号
        decimals: 小数位数
        
    Returns:
        格式化后的货币字符串
    """
    return f"{symbol}{value:,.{decimals}f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """格式化百分比
    
    Args:
        value: 数值（0-1 范围）
        decimals: 小数位数
        
    Returns:
        格式化后的百分比字符串
    """
    return f"{value:.{decimals}%}"


def format_date(date_value: Any, format_str: str = "%Y-%m-%d") -> str:
    """格式化日期
    
    Args:
        date_value: 日期值
        format_str: 日期格式
        
    Returns:
        格式化后的日期字符串
    """
    if isinstance(date_value, pd.Timestamp):
        return date_value.strftime(format_str)
    elif isinstance(date_value, datetime):
        return date_value.strftime(format_str)
    elif isinstance(date_value, str):
        dt = pd.to_datetime(date_value)
        return dt.strftime(format_str)
    else:
        return str(date_value)


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """安全除法（避免除零错误）
    
    Args:
        numerator: 分子
        denominator: 分母
        default: 除零时的默认值
        
    Returns:
        除法结果
    """
    if denominator == 0:
        return default
    return numerator / denominator


def flatten_dict(d: dict[str, Any], parent_key: str = '', sep: str = '.') -> dict[str, Any]:
    """扁平化嵌套字典
    
    Args:
        d: 嵌套字典
        parent_key: 父键前缀
        sep: 键分隔符
        
    Returns:
        扁平化后的字典
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
