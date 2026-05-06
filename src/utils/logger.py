"""日志配置"""

import sys
from pathlib import Path
from typing import Any, Optional
from loguru import logger


def setup_logger(config: Optional[dict[str, Any]] = None) -> None:
    """配置日志系统
    
    Args:
        config: 日志配置字典
    """
    logger.remove()
    
    default_config = {
        'level': 'INFO',
        'format': "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{line} - {message}",
        'handlers': {
            'console': {
                'enabled': True,
                'level': 'INFO',
            },
            'file': {
                'enabled': True,
                'level': 'DEBUG',
                'path': './logs/reporting.log',
                'max_bytes': 10485760,
                'backup_count': 5,
            }
        }
    }
    
    if config:
        default_config.update(config)
    
    log_format = default_config.get('format')
    log_level = default_config.get('level', 'INFO')
    handlers = default_config.get('handlers', {})
    
    console_config = handlers.get('console', {})
    if console_config.get('enabled', True):
        logger.add(
            sys.stderr,
            level=console_config.get('level', log_level),
            format=log_format,
            colorize=True
        )
    
    file_config = handlers.get('file', {})
    if file_config.get('enabled', True):
        log_path = Path(file_config.get('path', './logs/reporting.log'))
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.add(
            str(log_path),
            level=file_config.get('level', 'DEBUG'),
            format=log_format,
            rotation=file_config.get('max_bytes', '10 MB'),
            retention=file_config.get('backup_count', 5),
            encoding='utf-8'
        )
    
    logger.info("日志系统初始化完成")
