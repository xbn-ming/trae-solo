"""配置加载快捷方式"""

from src.utils.config_loader import ConfigLoader

_default_config = None


def load_config(config_path: str = "config/settings.yaml") -> ConfigLoader:
    """加载配置文件的快捷函数"""
    global _default_config
    if _default_config is None:
        _default_config = ConfigLoader(config_path)
    return _default_config


def get_config() -> ConfigLoader:
    """获取已加载的配置"""
    if _default_config is None:
        return load_config()
    return _default_config
