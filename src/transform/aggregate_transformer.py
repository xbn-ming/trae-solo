"""聚合转换器"""

from typing import Any, Optional
import pandas as pd
from loguru import logger

from src.transform.base_transformer import BaseTransformer


class AggregateTransformer(BaseTransformer):
    """数据聚合转换器
    
    支持 GROUP BY 聚合操作
    """
    
    def transform(
        self,
        df: pd.DataFrame,
        group_by: list[str],
        aggregations: Optional[dict[str, Any]] = None,
        **kwargs
    ) -> pd.DataFrame:
        """对数据进行聚合
        
        Args:
            df: 输入的 DataFrame
            group_by: 分组列名列表
            aggregations: 聚合规则字典，如 {'amount': 'sum', 'count': 'count'}
            **kwargs: 额外参数
            
        Returns:
            pd.DataFrame: 聚合后的 DataFrame
        """
        if not group_by:
            logger.warning("未指定分组列，返回原始数据")
            return df
        
        if aggregations is None:
            aggregations = {col: 'first' for col in df.columns if col not in group_by}
        
        logger.debug(f"执行聚合: group_by={group_by}, aggregations={aggregations}")
        
        result = df.groupby(group_by).agg(aggregations).reset_index()
        logger.info(f"聚合完成: {len(df)} 行 -> {len(result)} 行")
        
        return result
