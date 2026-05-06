"""转换器测试"""

import pandas as pd
import pytest
from src.transform.aggregate_transformer import AggregateTransformer
from src.transform.filter_transformer import FilterTransformer
from src.transform.format_transformer import FormatTransformer


@pytest.fixture
def sample_df():
    """提供测试用 DataFrame"""
    return pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=10),
        'category': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C'],
        'amount': [100.50, 200.30, 150.75, 300.00, 250.60, 180.90, 320.40, 210.80, 160.20, 290.50],
        'quantity': [10, 20, 15, 30, 25, 18, 32, 21, 16, 29]
    })


class TestAggregateTransformer:
    """聚合转换器测试"""
    
    def test_basic_aggregation(self, sample_df):
        """测试基本聚合"""
        transformer = AggregateTransformer()
        result = transformer.transform(
            sample_df,
            group_by=['category'],
            aggregations={'amount': 'sum', 'quantity': 'mean'}
        )
        
        assert len(result) == 3
        assert 'category' in result.columns
        assert 'amount' in result.columns
        assert 'quantity' in result.columns
    
    def test_empty_group_by(self, sample_df):
        """测试空分组"""
        transformer = AggregateTransformer()
        result = transformer.transform(sample_df, group_by=[])
        
        pd.testing.assert_frame_equal(result, sample_df)


class TestFilterTransformer:
    """过滤转换器测试"""
    
    def test_query_filter(self, sample_df):
        """测试 query 过滤"""
        transformer = FilterTransformer()
        result = transformer.transform(
            sample_df,
            query_expr="amount > 200"
        )
        
        assert len(result) < len(sample_df)
        assert all(result['amount'] > 200)
    
    def test_callable_filter(self, sample_df):
        """测试函数过滤"""
        transformer = FilterTransformer()
        result = transformer.transform(
            sample_df,
            condition=lambda df: df['quantity'] >= 20
        )
        
        assert all(result['quantity'] >= 20)
    
    def test_no_filter(self, sample_df):
        """测试无过滤条件"""
        transformer = FilterTransformer()
        result = transformer.transform(sample_df)
        
        pd.testing.assert_frame_equal(result, sample_df)


class TestFormatTransformer:
    """格式转换器测试"""
    
    def test_currency_format(self, sample_df):
        """测试货币格式"""
        transformer = FormatTransformer()
        result = transformer.transform(
            sample_df,
            column='amount',
            format_type='currency'
        )
        
        assert result['amount'].iloc[0].startswith('¥')
    
    def test_invalid_column(self, sample_df):
        """测试无效列名"""
        transformer = FormatTransformer()
        
        with pytest.raises(ValueError, match="列 'invalid' 不存在"):
            transformer.transform(
                sample_df,
                column='invalid',
                format_type='currency'
            )
    
    def test_invalid_format(self, sample_df):
        """测试无效格式类型"""
        transformer = FormatTransformer()
        
        with pytest.raises(ValueError, match="不支持的格式类型"):
            transformer.transform(
                sample_df,
                column='amount',
                format_type='invalid'
            )
