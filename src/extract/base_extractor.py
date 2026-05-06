"""数据提取器抽象基类"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import pandas as pd


class BaseExtractor(ABC):
    """数据提取器抽象基类
    
    所有具体的数据提取器都应该继承这个基类，
    并实现 extract 方法来获取数据。
    """
    
    def __init__(self, config: Dict[str, Any]):
        """初始化提取器
        
        Args:
            config: 数据源配置字典
        """
        self.config = config
        self.connection = None
    
    @abstractmethod
    def connect(self) -> None:
        """建立数据源连接"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """关闭数据源连接"""
        pass
    
    @abstractmethod
    def extract(self, query: str, params: Optional[tuple] = None) -> pd.DataFrame:
        """提取数据
        
        Args:
            query: 查询语句或数据获取指令
            params: 查询参数
            
        Returns:
            pd.DataFrame: 提取的数据
        """
        pass
    
    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.disconnect()
