"""Excel 报表生成器"""

from pathlib import Path
from typing import Any, Optional
import pandas as pd
from loguru import logger

from src.report.base_generator import BaseReportGenerator


class ExcelGenerator(BaseReportGenerator):
    """Excel 报表生成器
    
    使用 xlsxwriter 引擎生成 Excel 文件
    """
    
    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self.engine = self.config.get("engine", "xlsxwriter")
        self.default_date_format = self.config.get("default_date_format", "YYYY-MM-DD")
        self.default_number_format = self.config.get("default_number_format", "#,##0.00")
    
    def generate(
        self,
        data: pd.DataFrame,
        filename: str,
        sheet_name: str = "Sheet1",
        include_index: bool = False,
        freeze_panes: Optional[tuple[int, int]] = (1, 0),
        auto_filter: bool = True,
        **kwargs
    ) -> Path:
        """生成 Excel 报表
        
        Args:
            data: 报表数据 DataFrame
            filename: 输出文件名
            sheet_name: 工作表名称
            include_index: 是否包含索引
            freeze_panes: 冻结窗格 (row, col)
            auto_filter: 是否启用自动筛选
            **kwargs: 额外参数
            
        Returns:
            Path: 生成的文件路径
        """
        filename = self._ensure_extension(filename, ".xlsx")
        output_file = self.output_path / filename
        
        logger.info(f"生成 Excel 报表: {output_file}")
        
        with pd.ExcelWriter(output_file, engine=self.engine) as writer:
            data.to_excel(
                writer,
                sheet_name=sheet_name,
                index=include_index
            )
            
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            
            # 冻结窗格
            if freeze_panes:
                worksheet.freeze_panes(*freeze_panes)
            
            # 启用自动筛选
            if auto_filter:
                worksheet.autofilter(0, 0, len(data), len(data.columns) - 1)
            
            # 设置列宽
            for idx, col in enumerate(data.columns):
                max_length = max(
                    len(str(col)),
                    data[col].astype(str).str.len().max() if len(data) > 0 else 0
                )
                adjusted_width = min(max_length + 2, 50)
                worksheet.set_column(idx, idx, adjusted_width)
        
        logger.info(f"Excel 报表生成完成: {output_file}")
        return output_file
