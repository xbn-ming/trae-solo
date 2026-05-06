"""HTML 报表生成器"""

from pathlib import Path
from typing import Any, Optional
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from loguru import logger

from src.report.base_generator import BaseReportGenerator


class HTMLGenerator(BaseReportGenerator):
    """HTML 报表生成器
    
    使用 Jinja2 模板引擎生成 HTML 报表
    """
    
    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self.template_dir = self.config.get("template_dir", "src/report/templates")
        self.autoescape = self.config.get("autoescape", True)
        
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=self.autoescape
        )
    
    def generate(
        self,
        data: pd.DataFrame,
        filename: str,
        template_name: str = "base_report.html",
        title: str = "报表",
        context: Optional[dict[str, Any]] = None,
        **kwargs
    ) -> Path:
        """生成 HTML 报表
        
        Args:
            data: 报表数据 DataFrame
            filename: 输出文件名
            template_name: 模板文件名
            title: 报表标题
            context: 额外的模板上下文
            **kwargs: 额外参数
            
        Returns:
            Path: 生成的文件路径
        """
        filename = self._ensure_extension(filename, ".html")
        output_file = self.output_path / filename
        
        logger.info(f"生成 HTML 报表: {output_file}")
        
        template = self.env.get_template(template_name)
        
        table_data = self._prepare_table_data(data)
        
        render_context = {
            "title": title,
            "data": data,
            "table_data": table_data,
            "columns": data.columns.tolist(),
            "row_count": len(data),
        }
        if context:
            render_context.update(context)
        
        html_content = template.render(**render_context)
        
        output_file.write_text(html_content, encoding="utf-8")
        logger.info(f"HTML 报表生成完成: {output_file}")
        
        return output_file
    
    def _prepare_table_data(self, data: pd.DataFrame) -> list[dict[str, Any]]:
        """准备表格数据"""
        return data.to_dict(orient="records")
