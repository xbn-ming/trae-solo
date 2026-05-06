"""统一报表引擎"""

from pathlib import Path
from typing import Any, Optional
import pandas as pd
from loguru import logger

from src.report.excel_generator import ExcelGenerator
from src.report.pdf_generator import PDFGenerator
from src.report.html_generator import HTMLGenerator


class ReportEngine:
    """统一报表引擎
    
    根据配置自动生成多种格式的报表
    """
    
    GENERATORS = {
        'excel': ExcelGenerator,
        'pdf': PDFGenerator,
        'html': HTMLGenerator,
    }
    
    def __init__(self, config: dict[str, Any] | None = None):
        """初始化报表引擎
        
        Args:
            config: 报表配置
        """
        self.config = config or {}
        self.generators = {}
    
    def get_generator(self, format_type: str) -> Any:
        """获取指定格式的生成器
        
        Args:
            format_type: 格式类型 (excel, pdf, html)
            
        Returns:
            对应的生成器实例
        """
        if format_type not in self.generators:
            if format_type not in self.GENERATORS:
                raise ValueError(f"不支持的报表格式: {format_type}")
            
            format_config = self.config.get(format_type, {})
            generator_class = self.GENERATORS[format_type]
            self.generators[format_type] = generator_class(format_config)
        
        return self.generators[format_type]
    
    def generate(
        self,
        data: pd.DataFrame,
        filename: str,
        formats: list[str],
        title: str = "报表",
        **kwargs
    ) -> list[Path]:
        """生成多种格式的报表
        
        Args:
            data: 报表数据
            filename: 基础文件名（不含扩展名）
            formats: 要生成的格式列表
            title: 报表标题
            **kwargs: 传递给生成器的额外参数
            
        Returns:
            list[Path]: 生成的文件路径列表
        """
        output_files = []
        
        for format_type in formats:
            try:
                generator = self.get_generator(format_type)
                output_file = generator.generate(
                    data=data,
                    filename=filename,
                    title=title,
                    **kwargs
                )
                output_files.append(output_file)
                logger.info(f"成功生成 {format_type} 报表: {output_file}")
            except Exception as e:
                logger.error(f"生成 {format_type} 报表失败: {e}")
        
        return output_files
