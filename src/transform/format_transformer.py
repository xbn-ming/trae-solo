"""格式转换器"""

from typing import Any, Optional
import pandas as pd
from loguru import logger

from src.transform.base_transformer import BaseTransformer


class FormatTransformer(BaseTransformer):
    """数据格式转换器
    
    支持货币、百分比、日期等格式转换
    """
    
    FORMATTERS = {
        'currency': lambda x: f"¥{x:,.2f}",
        'percentage': lambda x: f"{x:.2%}",
        'date': lambda x: pd.to_datetime(x).strftime('%Y-%m-%d'),
        'number': lambda x: f"{x:,.2f}",
        'integer': lambda x: int(x),
    }
    
    def transform(
        self,
        df: pd.DataFrame,
        column: str,
        format_type: str,
        custom_format: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """转换列格式
        
        Args:
            df: 输入的 DataFrame
            column: 要转换的列名
            format_type: 格式类型 (currency, percentage, date, number, integer)
            custom_format: 自定义格式化字符串
            **kwargs: 额外参数
            
        Returns:
            pd.DataFrame: 格式转换后的 DataFrame
        """
        if column not in df.columns:
            raise ValueError(f"列 '{column}' 不存在于 DataFrame 中")
        
        if custom_format:
            formatter = lambda x: custom_format.format(x)
        elif format_type in self.FORMATTERS:
            formatter = self.FORMATTERS[format_type]
        else:
            raise ValueError(f"不支持的格式类型: {format_type}，支持的类型: {list(self.FORMATTERS.keys())}")
        
        logger.debug(f"转换格式: column={column}, format_type={format_type}")
        
        result = df.copy()
        result[column] = result[column].apply(formatter)
        logger.info(f"格式转换完成: {column} ({format_type})")
        
        return result
