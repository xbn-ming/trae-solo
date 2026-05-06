"""PDF 报表生成器"""

from pathlib import Path
from typing import Any, Optional
import pandas as pd
from loguru import logger

from src.report.base_generator import BaseReportGenerator


class PDFGenerator(BaseReportGenerator):
    """PDF 报表生成器
    
    使用 WeasyPrint 引擎生成 PDF 文件
    """
    
    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self.page_size = self.config.get("page_size", "A4")
        self.margin = self.config.get("margin", "20mm")
    
    def generate(
        self,
        data: pd.DataFrame,
        filename: str,
        title: str = "报表",
        header_html: Optional[str] = None,
        footer_html: Optional[str] = None,
        **kwargs
    ) -> Path:
        """生成 PDF 报表
        
        Args:
            data: 报表数据 DataFrame
            filename: 输出文件名
            title: 报表标题
            header_html: 自定义 HTML 页眉
            footer_html: 自定义 HTML 页脚
            **kwargs: 额外参数
            
        Returns:
            Path: 生成的文件路径
        """
        filename = self._ensure_extension(filename, ".pdf")
        output_file = self.output_path / filename
        
        logger.info(f"生成 PDF 报表: {output_file}")
        
        html_content = self._generate_html(data, title, header_html)
        
        try:
            from weasyprint import HTML
            
            HTML(string=html_content).write_pdf(
                output_file,
                presentational_hints=True
            )
            logger.info(f"PDF 报表生成完成: {output_file}")
        except ImportError:
            logger.error("weasyprint 未安装，请运行: pip install weasyprint")
            raise
        except Exception as e:
            logger.error(f"PDF 生成失败: {e}")
            raise
        
        return output_file
    
    def _generate_html(
        self,
        data: pd.DataFrame,
        title: str,
        header_html: Optional[str] = None
    ) -> str:
        """生成 HTML 内容"""
        if header_html is None:
            header_html = f"<h1>{title}</h1>"
        
        table_html = data.to_html(index=False, classes="report-table")
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @page {{
                    size: {self.page_size};
                    margin: {self.margin};
                }}
                body {{
                    font-family: Arial, sans-serif;
                    font-size: 12px;
                }}
                h1 {{
                    text-align: center;
                    color: #333;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f5f5f5;
                    font-weight: bold;
                }}
                tr:nth-child(even) {{
                    background-color: #fafafa;
                }}
            </style>
        </head>
        <body>
            {header_html}
            {table_html}
        </body>
        </html>
        """
        return html
