from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """应用配置"""
    # 数据库配置
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/dbname"
    
    # JWT配置
    JWT_SECRET_KEY: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 密码加密配置
    PASSWORD_SCHEMES: list = ["bcrypt"]
    
    # SMTP配置
    SMTP_HOST: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USE_TLS: bool = True
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "alerts@example.com"
    
    # 告警配置
    ALERT_CHECK_INTERVAL: int = 60  # 告警检查间隔(秒)
    ALERT_NOTIFICATION_RETRY: int = 3  # 通知重试次数
    
    # Agent配置
    AGENT_STATUS_CHECK_INTERVAL: int = 30  # Agent状态检查间隔(秒)
    AGENT_OFFLINE_THRESHOLD: int = 300  # Agent离线阈值(秒)
    AGENT_METRICS_RETENTION_DAYS: int = 7  # Agent指标保留天数
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DIR: str = "logs"
    LOG_MAX_SIZE: int = 10_000_000  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    # 备份配置
    BACKUP_DIR: str = "backups"
    BACKUP_KEEP_DAYS: int = 7  # 备份保留天数
    BACKUP_DATABASE_URL: str = "postgresql://user:pass@localhost/dbname"
    
    # 审计日志配置
    AUDIT_LOG_ENABLED: bool = True
    AUDIT_LOG_RETENTION_DAYS: int = 90
    
    # 权限配置
    SUPER_ADMIN_ROLES: list = ["admin"]
    DEFAULT_MEMBER_ROLE: str = "member"
    
    # 限流配置
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100  # 每个时间窗口允许的最大请求数
    RATE_LIMIT_WINDOW: int = 60     # 时间窗口(秒)
    
    # 监控配置
    MONITOR_CLEANUP_INTERVAL: int = 24 * 60 * 60  # 清理任务间隔(秒)
    MONITOR_AGGREGATION_INTERVAL: int = 60        # 聚合任务间隔(秒)
    MONITOR_DEFAULT_RAW_RETENTION_DAYS: int = 7   # 默认原始数据保留天数
    MONITOR_DEFAULT_AGG_RETENTION_DAYS: int = 30  # 默认聚合数据保留天数
    
    # 数据库配置
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "server_manager"
    
    # Agent配置
    AGENT_UPLOAD_DIR: str = "uploads/agents"  # Agent安装包上传目录
    AGENT_OFFLINE_THRESHOLD: int = 300  # Agent离线阈值(秒)
    AGENT_CHECK_INTERVAL: int = 60  # Agent状态检查间隔(秒)
    
    class Config:
        env_file = ".env"

settings = Settings() 