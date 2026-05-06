"""PostgreSQL 数据提取器"""

from typing import Any, Dict, Optional
import pandas as pd
from sqlalchemy import create_engine
from loguru import logger

from src.extract.base_extractor import BaseExtractor


class PostgresExtractor(BaseExtractor):
    """PostgreSQL 数据库数据提取器"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.engine = None
    
    def connect(self) -> None:
        """建立 PostgreSQL 连接"""
        host = self.config.get("host", "localhost")
        port = self.config.get("port", 5432)
        database = self.config.get("database", "")
        username = self.config.get("username", "postgres")
        password = self.config.get("password", "")
        options = self.config.get("options", {})
        
        connection_string = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
        if options:
            params = "&".join([f"{k}={v}" for k, v in options.items()])
            connection_string += f"?{params}"
        
        self.engine = create_engine(connection_string)
        self.connection = self.engine.connect()
        logger.info(f"PostgreSQL 连接成功: {host}:{port}/{database}")
    
    def disconnect(self) -> None:
        """关闭 PostgreSQL 连接"""
        if self.connection:
            self.connection.close()
            logger.info("PostgreSQL 连接已关闭")
    
    def extract(self, query: str, params: Optional[tuple] = None) -> pd.DataFrame:
        """从 PostgreSQL 提取数据
        
        Args:
            query: SQL 查询语句
            params: SQL 参数
            
        Returns:
            pd.DataFrame: 查询结果
        """
        if not self.connection:
            raise RuntimeError("未建立数据库连接，请先调用 connect()")
        
        logger.debug(f"执行 SQL: {query}")
        logger.debug(f"参数: {params}")
        
        df = pd.read_sql(query, self.connection, params=params)
        logger.info(f"提取完成，共 {len(df)} 行数据")
        return df
