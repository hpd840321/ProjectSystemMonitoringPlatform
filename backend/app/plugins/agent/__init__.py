from typing import Dict, Any
from app.infrastructure.plugins.base_plugin import BaseAgentPlugin

# 插件注册表
PLUGIN_REGISTRY = {}

def register_plugin(name: str):
    """插件注册装饰器"""
    def wrapper(cls):
        if not issubclass(cls, BaseAgentPlugin):
            raise TypeError(f"Plugin {name} must inherit from BaseAgentPlugin")
        PLUGIN_REGISTRY[name] = cls
        return cls
    return wrapper 