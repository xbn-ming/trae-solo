#!/usr/bin/env python3
"""管道编排器

串联完整的 ETL + 报表生成流程
"""

import argparse
from datetime import datetime, timedelta
from typing import Any, Optional
import pandas as pd
from loguru import logger

from src.config import load_config
from src.extract.mysql_extractor import MySQLExtractor
from src.extract.postgres_extractor import PostgresExtractor
from src.extract.api_extractor import APIExtractor
from src.extract.file_extractor import FileExtractor
from src.clean.data_cleaner import DataCleaner
from src.transform.aggregate_transformer import AggregateTransformer
from src.transform.filter_transformer import FilterTransformer
from src.transform.join_transformer import JoinTransformer
from src.transform.format_transformer import FormatTransformer
from src.report.report_engine import ReportEngine


class PipelineOrchestrator:
    """ETL + 报表生成管道编排器"""
    
    EXTRACTORS = {
        'mysql': MySQLExtractor,
        'postgresql': PostgresExtractor,
        'api': APIExtractor,
        'file': FileExtractor,
    }
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        """初始化编排器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = load_config(config_path)
        self.data_cleaner = DataCleaner()
        self.report_engine = ReportEngine(self.config.get_all().get('output', {}))
    
    def extract_data(self, report_config: dict[str, Any], params: Optional[tuple] = None) -> pd.DataFrame:
        """执行数据提取
        
        Args:
            report_config: 报表配置
            params: 查询参数
            
        Returns:
            pd.DataFrame: 提取的数据
        """
        source_type = report_config.get('data_source', 'file')
        source_config = self.config.get(f'data_sources.{source_type}', {})
        
        extractor_class = self.EXTRACTORS.get(source_type)
        if not extractor_class:
            raise ValueError(f"不支持的数据源类型: {source_type}")
        
        extractor = extractor_class(source_config)
        
        with extractor as ext:
            query = report_config.get('query', '')
            data = ext.extract(query, params=params)
        
        return data
    
    def transform_data(self, data: pd.DataFrame, transformations: list[dict[str, Any]]) -> pd.DataFrame:
        """执行数据转换
        
        Args:
            data: 输入数据
            transformations: 转换步骤列表
            
        Returns:
            pd.DataFrame: 转换后的数据
        """
        result = data.copy()
        
        for step in transformations:
            step_type = step.get('type')
            
            if step_type == 'aggregate':
                transformer = AggregateTransformer()
                result = transformer.transform(
                    result,
                    group_by=step.get('group_by', [])
                )
            elif step_type == 'filter':
                transformer = FilterTransformer()
                result = transformer.transform(
                    result,
                    query_expr=step.get('expression')
                )
            elif step_type == 'format':
                transformer = FormatTransformer()
                result = transformer.transform(
                    result,
                    column=step.get('column'),
                    format_type=step.get('format', 'number')
                )
            elif step_type == 'clean':
                result = self.data_cleaner.clean(result, step.get('steps', []))
        
        return result
    
    def generate_reports(self, data: pd.DataFrame, report_config: dict[str, Any]) -> list:
        """生成报表
        
        Args:
            data: 报表数据
            report_config: 报表配置
            
        Returns:
            list: 生成的文件路径列表
        """
        report_name = report_config.get('name', 'report')
        output_formats = report_config.get('output_formats', ['excel'])
        
        filename = f"{report_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        output_files = self.report_engine.generate(
            data=data,
            filename=filename,
            formats=output_formats,
            title=report_name
        )
        
        return output_files
    
    def run(self, report_name: str, params: Optional[tuple] = None) -> list:
        """运行完整的报表生成流程
        
        Args:
            report_name: 报表名称
            params: 查询参数
            
        Returns:
            list: 生成的文件路径列表
        """
        logger.info(f"开始生成报表: {report_name}")
        
        report_config = self.config.get(f'reports.{report_name}')
        if not report_config:
            raise ValueError(f"未找到报表配置: {report_name}")
        
        logger.info("Step 1: 提取数据")
        data = self.extract_data(report_config, params)
        
        logger.info("Step 2: 转换数据")
        transformations = report_config.get('transformations', [])
        data = self.transform_data(data, transformations)
        
        logger.info("Step 3: 生成报表")
        output_files = self.generate_reports(data, report_config)
        
        logger.info(f"报表生成完成: {output_files}")
        return output_files


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="报表生成工具")
    parser.add_argument("--report", type=str, help="报表名称（all 表示生成所有报表）")
    parser.add_argument("--config", type=str, default="config/settings.yaml", help="配置文件路径")
    parser.add_argument("--start-date", type=str, help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str, help="结束日期 (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    orchestrator = PipelineOrchestrator(args.config)
    
    if args.report == "all":
        reports_config = orchestrator.config.get("reports", {})
        for report_name in reports_config.keys():
            orchestrator.run(report_name)
    elif args.report:
        params = None
        if args.start_date and args.end_date:
            params = (args.start_date, args.end_date)
        orchestrator.run(args.report, params)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
