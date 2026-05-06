"""REST API 数据提取器"""

from typing import Any, Dict, Optional
import pandas as pd
import requests
from loguru import logger

from src.extract.base_extractor import BaseExtractor


class APIExtractor(BaseExtractor):
    """REST API 数据提取器"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get("base_url", "")
        self.timeout = config.get("timeout", 30)
        self.retry_count = config.get("retry_count", 3)
        self.headers = config.get("headers", {})
    
    def connect(self) -> None:
        """初始化 API 会话"""
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        logger.info(f"API 会话已创建: {self.base_url}")
    
    def disconnect(self) -> None:
        """关闭 API 会话"""
        if self.session:
            self.session.close()
            logger.info("API 会话已关闭")
    
    def extract(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """从 API 提取数据
        
        Args:
            endpoint: API 端点路径
            params: 查询参数
            
        Returns:
            pd.DataFrame: API 返回的数据
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"请求 API: {url}")
        logger.debug(f"参数: {params}")
        
        for attempt in range(self.retry_count):
            try:
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.timeout
                )
                response.raise_for_status()
                data = response.json()
                
                df = pd.DataFrame(data) if isinstance(data, list) else pd.DataFrame([data])
                logger.info(f"API 提取完成，共 {len(df)} 行数据")
                return df
                
            except requests.RequestException as e:
                logger.warning(f"API 请求失败 (尝试 {attempt + 1}/{self.retry_count}): {e}")
                if attempt == self.retry_count - 1:
                    raise
        
        raise RuntimeError("API 请求失败，已达到最大重试次数")
