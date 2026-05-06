"""过滤转换器"""

from typing import Any, Callable
import pandas as pd
from loguru import logger

from src.transform.base_transformer import BaseTransformer


class FilterTransformer(BaseTransformer):
    """数据过滤转换器
    
    支持条件过滤和 SQL 表达式过滤
    """
    
    def transform(
        self,
        df: pd.DataFrame,
        condition: Callable[[pd.DataFrame], pd.Series] | str | None = None,
        query_expr: str | None = None,
        **kwargs
    ) -> pd.DataFrame:
        """过滤数据
        
        Args:
            df: 输入的 DataFrame
            condition: 过滤条件函数或布尔 Series
            query_expr: pandas query 表达式字符串
            **kwargs: 额外参数
            
        Returns:
            pd.DataFrame: 过滤后的 DataFrame
        """
        original_len = len(df)
        
        if query_expr:
            logger.debug(f"使用 query 表达式过滤: {query_expr}")
            result = df.query(query_expr)
        elif callable(condition):
            logger.debug("使用函数条件过滤")
            mask = condition(df)
            result = df[mask]
        elif isinstance(condition, pd.Series):
            logger.debug("使用布尔 Series 过滤")
            result = df[condition]
        else:
            logger.warning("未指定过滤条件，返回原始数据")
            return df
        
        filtered_count = original_len - len(result)
        logger.info(f"过滤完成: 移除 {filtered_count} 行，剩余 {len(result)} 行")
        
        return result
