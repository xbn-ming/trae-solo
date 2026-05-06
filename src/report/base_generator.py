"""报表生成器抽象基类"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
import pandas as pd


class BaseReportGenerator(ABC):
    """报表生成器抽象基类
    
    所有具体的报表生成器都应该继承这个基类，
    并实现 generate 方法来生成报表文件。
    """
    
    def __init__(self, config: dict[str, Any] | None = None):
        """初始化生成器
        
        Args:
            config: 报表配置字典
        """
        self.config = config or {}
        self.output_path = Path(self.config.get("output_path", "./src/report/output"))
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    def generate(
        self,
        data: pd.DataFrame,
        filename: str,
        **kwargs
    ) -> Path:
        """生成报表文件
        
        Args:
            data: 报表数据
            filename: 输出文件名
            **kwargs: 额外参数
            
        Returns:
            Path: 生成的文件路径
        """
        pass
    
    def _ensure_extension(self, filename: str, extension: str) -> str:
        """确保文件名有正确的扩展名"""
        if not filename.endswith(extension):
            filename += extension
        return filename
