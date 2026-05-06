"""文件数据提取器"""

from typing import Any, Dict, Optional, Union
from pathlib import Path
import pandas as pd
from loguru import logger

from src.extract.base_extractor import BaseExtractor


class FileExtractor(BaseExtractor):
    """文件数据提取器
    
    支持 CSV、Excel、JSON、Parquet 格式
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_path = Path(config.get("base_path", "./data/raw"))
        self.supported_formats = config.get("supported_formats", ["csv", "excel", "json", "parquet"])
    
    def connect(self) -> None:
        """验证基础路径存在"""
        if not self.base_path.exists():
            self.base_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"创建数据目录: {self.base_path}")
        else:
            logger.info(f"数据目录已存在: {self.base_path}")
    
    def disconnect(self) -> None:
        """文件提取器无需关闭连接"""
        pass
    
    def extract(self, filepath: Union[str, Path], **kwargs) -> pd.DataFrame:
        """从文件提取数据
        
        Args:
            filepath: 文件路径（相对于 base_path 或绝对路径）
            **kwargs: 传递给 pandas 读取函数的额外参数
            
        Returns:
            pd.DataFrame: 文件数据
            
        Raises:
            ValueError: 不支持的文件格式
            FileNotFoundError: 文件不存在
        """
        file_path = Path(filepath)
        if not file_path.is_absolute():
            file_path = self.base_path / file_path
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        suffix = file_path.suffix.lower().lstrip(".")
        
        logger.debug(f"读取文件: {file_path}")
        
        if suffix == "csv":
            df = pd.read_csv(file_path, **kwargs)
        elif suffix in ["xlsx", "xls"]:
            df = pd.read_excel(file_path, **kwargs)
        elif suffix == "json":
            df = pd.read_json(file_path, **kwargs)
        elif suffix == "parquet":
            df = pd.read_parquet(file_path, **kwargs)
        else:
            raise ValueError(f"不支持的文件格式: {suffix}，支持的格式: {self.supported_formats}")
        
        logger.info(f"文件提取完成: {file_path.name}，共 {len(df)} 行数据")
        return df
