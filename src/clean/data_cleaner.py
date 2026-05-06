"""数据清洗器"""

from typing import Any, Optional
import pandas as pd
from loguru import logger


class DataCleaner:
    """数据清洗器
    
    提供常用的数据清洗功能：
    - 去重
    - 缺失值处理
    - 异常值剔除
    """
    
    def __init__(self, config: dict[str, Any] | None = None):
        """初始化清洗器
        
        Args:
            config: 清洗配置
        """
        self.config = config or {}
    
    def remove_duplicates(
        self,
        df: pd.DataFrame,
        subset: Optional[list[str]] = None,
        keep: str = 'first'
    ) -> pd.DataFrame:
        """移除重复数据
        
        Args:
            df: 输入的 DataFrame
            subset: 用于判断重复的列
            keep: 保留策略 ('first', 'last', False)
            
        Returns:
            pd.DataFrame: 去重后的 DataFrame
        """
        original_len = len(df)
        result = df.drop_duplicates(subset=subset, keep=keep)
        removed = original_len - len(result)
        logger.info(f"去重完成: 移除 {removed} 条重复记录")
        return result
    
    def handle_missing_values(
        self,
        df: pd.DataFrame,
        strategy: str = 'drop',
        columns: Optional[list[str]] = None,
        fill_value: Any = None
    ) -> pd.DataFrame:
        """处理缺失值
        
        Args:
            df: 输入的 DataFrame
            strategy: 处理策略 ('drop', 'fill_mean', 'fill_median', 'fill_mode', 'fill_value')
            columns: 要处理的列（默认所有列）
            fill_value: 固定填充值
            
        Returns:
            pd.DataFrame: 处理后的 DataFrame
        """
        if columns is None:
            columns = df.columns.tolist()
        
        result = df.copy()
        missing_before = result[columns].isnull().sum().sum()
        
        if strategy == 'drop':
            result = result.dropna(subset=columns)
        elif strategy == 'fill_mean':
            result[columns] = result[columns].fillna(result[columns].mean(numeric_only=True))
        elif strategy == 'fill_median':
            result[columns] = result[columns].fillna(result[columns].median(numeric_only=True))
        elif strategy == 'fill_mode':
            for col in columns:
                mode_value = result[col].mode()
                if len(mode_value) > 0:
                    result[col] = result[col].fillna(mode_value[0])
        elif strategy == 'fill_value':
            result[columns] = result[columns].fillna(fill_value)
        else:
            raise ValueError(f"不支持的缺失值处理策略: {strategy}")
        
        missing_after = result[columns].isnull().sum().sum()
        logger.info(f"缺失值处理完成: {missing_before} -> {missing_after}")
        
        return result
    
    def remove_outliers(
        self,
        df: pd.DataFrame,
        columns: list[str],
        method: str = 'iqr',
        threshold: float = 1.5
    ) -> pd.DataFrame:
        """移除异常值
        
        Args:
            df: 输入的 DataFrame
            columns: 要检查的数值列
            method: 检测方法 ('iqr', 'zscore')
            threshold: 异常值阈值
            
        Returns:
            pd.DataFrame: 移除异常值后的 DataFrame
        """
        result = df.copy()
        original_len = len(result)
        mask = pd.Series([True] * len(result))
        
        for col in columns:
            if col not in result.columns:
                logger.warning(f"列 '{col}' 不存在，跳过")
                continue
            
            if not pd.api.types.is_numeric_dtype(result[col]):
                logger.warning(f"列 '{col}' 不是数值类型，跳过")
                continue
            
            if method == 'iqr':
                Q1 = result[col].quantile(0.25)
                Q3 = result[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                mask = mask & (result[col] >= lower_bound) & (result[col] <= upper_bound)
            elif method == 'zscore':
                z_scores = (result[col] - result[col].mean()) / result[col].std()
                mask = mask & (z_scores.abs() <= threshold)
            else:
                raise ValueError(f"不支持的异常值检测方法: {method}")
        
        result = result[mask]
        removed = original_len - len(result)
        logger.info(f"异常值移除完成: 移除 {removed} 条记录")
        
        return result
    
    def clean(
        self,
        df: pd.DataFrame,
        steps: list[dict[str, Any]]
    ) -> pd.DataFrame:
        """执行完整的清洗流程
        
        Args:
            df: 输入的 DataFrame
            steps: 清洗步骤列表
            
        Returns:
            pd.DataFrame: 清洗后的 DataFrame
        """
        result = df.copy()
        
        for step in steps:
            action = step.get('action')
            
            if action == 'remove_duplicates':
                result = self.remove_duplicates(
                    result,
                    subset=step.get('subset'),
                    keep=step.get('keep', 'first')
                )
            elif action == 'handle_missing_values':
                result = self.handle_missing_values(
                    result,
                    strategy=step.get('strategy', 'drop'),
                    columns=step.get('columns'),
                    fill_value=step.get('fill_value')
                )
            elif action == 'remove_outliers':
                result = self.remove_outliers(
                    result,
                    columns=step.get('columns', []),
                    method=step.get('method', 'iqr'),
                    threshold=step.get('threshold', 1.5)
                )
            else:
                logger.warning(f"未知的清洗动作: {action}")
        
        return result
