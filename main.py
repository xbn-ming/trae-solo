#!/usr/bin/env python3
"""报表开发项目主入口"""

import sys
from pathlib import Path
from loguru import logger

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.config import load_config
from src.utils.logger import setup_logger
from scripts.run_pipeline import PipelineOrchestrator


def main():
    """主函数"""
    # 加载配置
    config = load_config()
    
    # 初始化日志
    log_config = config.get('logging', {})
    setup_logger(log_config)
    
    logger.info("="*50)
    logger.info("Trae-Solo 报表开发项目启动")
    logger.info("="*50)
    
    # 创建编排器并运行
    orchestrator = PipelineOrchestrator()
    
    # 示例：生成每日销售报表
    try:
        output_files = orchestrator.run("daily_sales")
        logger.info(f"成功生成报表: {output_files}")
    except Exception as e:
        logger.error(f"报表生成失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
