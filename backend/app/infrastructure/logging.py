import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from app.infrastructure.config import settings

def setup_logging():
    """配置日志"""
    # 创建日志目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 创建日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 配置文件处理器
    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10_000_000,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # 配置控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # 配置应用日志记录器
    app_logger = logging.getLogger("app")
    app_logger.setLevel(settings.LOG_LEVEL)
    
    return app_logger 