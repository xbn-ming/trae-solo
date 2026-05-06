"""数据转换器抽象基类"""

from abc import ABC, abstractmethod
from typing import Any
import pandas as pd


class BaseTransformer(ABC):
    """数据转换器抽象基类
    
    所有具体的数据转换器都应该继承这个基类，
    并实现 transform 方法来处理数据。
    """
    
    def __init__(self, config: dict[str, Any] | None = None):
        """初始化转换器
        
        Args:
            config: 转换器配置字典
        """
        self.config = config or {}
    
    @abstractmethod
    def transform(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """转换数据
        
        Args:
            df: 输入的 DataFrame
            **kwargs: 额外的转换参数
            
        Returns:
            pd.DataFrame: 转换后的 DataFrame
        """
        pass
