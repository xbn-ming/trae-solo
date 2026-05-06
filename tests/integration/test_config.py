"""配置加载器测试"""

import os
import pytest
from pathlib import Path
import yaml
from src.utils.config_loader import ConfigLoader


@pytest.fixture
def temp_config_file(tmp_path):
    """创建临时配置文件"""
    config_data = {
        'database': {
            'host': '${DB_HOST:localhost}',
            'port': '${DB_PORT:5432}',
            'name': '${DB_NAME:test_db}'
        },
        'app': {
            'debug': True,
            'workers': 4
        }
    }
    
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text(yaml.dump(config_data), encoding='utf-8')
    return config_file


def test_load_config(temp_config_file):
    """测试加载配置文件"""
    loader = ConfigLoader(temp_config_file)
    config = loader.get_all()
    
    assert 'database' in config
    assert 'app' in config
    assert config['app']['debug'] is True
    assert config['app']['workers'] == 4


def test_get_nested_key(temp_config_file):
    """测试获取嵌套键值"""
    loader = ConfigLoader(temp_config_file)
    
    assert loader.get('database.host') == 'localhost'
    assert loader.get('database.port') == '5432'
    assert loader.get('app.debug') is True
    assert loader.get('nonexistent', 'default') == 'default'


def test_env_var_resolution(temp_config_file):
    """测试环境变量解析"""
    os.environ['DB_HOST'] = 'production-db.example.com'
    os.environ['DB_PORT'] = '3306'
    
    try:
        loader = ConfigLoader(temp_config_file)
        
        assert loader.get('database.host') == 'production-db.example.com'
        assert loader.get('database.port') == '3306'
    finally:
        del os.environ['DB_HOST']
        del os.environ['DB_PORT']


def test_file_not_found():
    """测试配置文件不存在"""
    with pytest.raises(FileNotFoundError):
        ConfigLoader("/nonexistent/config.yaml")
