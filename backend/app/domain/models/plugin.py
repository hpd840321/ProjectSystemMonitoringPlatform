from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum

class PluginStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"

@dataclass
class Plugin:
    id: str
    name: str
    version: str
    description: Optional[str]
    entry_point: str
    config_schema: Dict[str, Any]
    status: PluginStatus
    created_at: datetime
    updated_at: datetime

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """验证插件配置"""
        # 实现配置验证逻辑
        pass

    def is_active(self) -> bool:
        return self.status == PluginStatus.ACTIVE 