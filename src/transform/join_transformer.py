"""连接转换器"""

from typing import Any, Literal
import pandas as pd
from loguru import logger

from src.transform.base_transformer import BaseTransformer


class JoinTransformer(BaseTransformer):
    """多表连接转换器
    
    支持 pandas merge 操作
    """
    
    def transform(
        self,
        df: pd.DataFrame,
        other: pd.DataFrame,
        on: list[str] | str | None = None,
        left_on: list[str] | str | None = None,
        right_on: list[str] | str | None = None,
        how: Literal['left', 'right', 'inner', 'outer', 'cross'] = 'inner',
        **kwargs
    ) -> pd.DataFrame:
        """连接两个 DataFrame
        
        Args:
            df: 左侧 DataFrame
            other: 右侧 DataFrame
            on: 连接列名（两表列名相同）
            left_on: 左侧连接列名
            right_on: 右侧连接列名
            how: 连接方式
            **kwargs: 传递给 pandas.merge 的额外参数
            
        Returns:
            pd.DataFrame: 连接后的 DataFrame
        """
        logger.debug(f"执行连接: how={how}, on={on}, left_on={left_on}, right_on={right_on}")
        
        result = pd.merge(
            df,
            other,
            on=on,
            left_on=left_on,
            right_on=right_on,
            how=how,
            **kwargs
        )
        
        logger.info(f"连接完成: {len(df)} x {len(other)} -> {len(result)} 行")
        
        return result
