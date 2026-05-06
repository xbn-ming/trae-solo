"""数据提取器测试"""

import pytest
from pathlib import Path
import pandas as pd
from src.extract.file_extractor import FileExtractor


@pytest.fixture
def file_extractor_config():
    """提供文件提取器配置"""
    return {
        'base_path': './data/raw',
        'supported_formats': ['csv', 'excel', 'json', 'parquet']
    }


@pytest.fixture
def sample_csv_file(tmp_path):
    """创建示例 CSV 文件"""
    csv_content = """date,product,amount,quantity
2024-01-01,A,100.50,10
2024-01-02,B,200.30,20
2024-01-03,A,150.75,15
"""
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(csv_content, encoding='utf-8')
    return csv_file


def test_extract_csv(file_extractor_config, sample_csv_file, tmp_path):
    """测试从 CSV 文件提取数据"""
    file_extractor_config['base_path'] = str(tmp_path)
    extractor = FileExtractor(file_extractor_config)
    extractor.connect()
    
    try:
        data = extractor.extract(sample_csv_file.name)
        
        assert isinstance(data, pd.DataFrame)
        assert len(data) == 3
        assert list(data.columns) == ['date', 'product', 'amount', 'quantity']
    finally:
        extractor.disconnect()


def test_extract_nonexistent_file(file_extractor_config, tmp_path):
    """测试提取不存在的文件"""
    file_extractor_config['base_path'] = str(tmp_path)
    extractor = FileExtractor(file_extractor_config)
    extractor.connect()
    
    try:
        with pytest.raises(FileNotFoundError):
            extractor.extract("nonexistent.csv")
    finally:
        extractor.disconnect()


def test_extract_unsupported_format(file_extractor_config, tmp_path):
    """测试提取不支持的格式"""
    unsupported_file = tmp_path / "test.txt"
    unsupported_file.write_text("test content", encoding='utf-8')
    
    file_extractor_config['base_path'] = str(tmp_path)
    extractor = FileExtractor(file_extractor_config)
    extractor.connect()
    
    try:
        with pytest.raises(ValueError, match="不支持的文件格式"):
            extractor.extract("test.txt")
    finally:
        extractor.disconnect()
