"""YAML 配置加载器"""

import os
import re
from pathlib import Path
from typing import Any
import yaml
from dotenv import load_dotenv
from loguru import logger


class ConfigLoader:
    """YAML 配置加载器
    
    支持环境变量替换（${VAR:default} 格式）
    """
    
    ENV_PATTERN = re.compile(r'\$\{([^}]+)\}')
    
    def __init__(self, config_path: str | Path):
        """初始化配置加载器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = Path(config_path)
        self._config = {}
        self.load()
    
    def load(self) -> None:
        """加载配置文件"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
        
        logger.info(f"加载配置文件: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            raw_config = yaml.safe_load(f)
        
        self._config = self._resolve_env_vars(raw_config)
        logger.info("配置文件加载完成")
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值（支持点号分隔的嵌套键）
        
        Args:
            key: 配置键，如 'data_sources.mysql.host'
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_all(self) -> dict[str, Any]:
        """获取完整配置"""
        return self._config.copy()
    
    def reload(self) -> None:
        """重新加载配置"""
        self.load()
    
    def _resolve_env_vars(self, config: Any) -> Any:
        """递归解析配置中的环境变量
        
        Args:
            config: 配置字典
            
        Returns:
            解析后的配置
        """
        if isinstance(config, dict):
            return {k: self._resolve_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [self._resolve_env_vars(item) for item in config]
        elif isinstance(config, str):
            return self._replace_env_vars(config)
        else:
            return config
    
    def _replace_env_vars(self, value: str) -> str:
        """替换字符串中的环境变量
        
        Args:
            value: 包含环境变量引用的字符串
            
        Returns:
            替换后的字符串
        """
        def replace_match(match):
            env_expr = match.group(1)
            if ':' in env_expr:
                var_name, default = env_expr.split(':', 1)
                return os.environ.get(var_name, default)
            else:
                return os.environ.get(env_expr, match.group(0))
        
        return self.ENV_PATTERN.sub(replace_match, value)
