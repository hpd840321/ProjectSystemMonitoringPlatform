from typing import Dict, Tuple
from datetime import datetime, timedelta
import time
from fastapi import Request, HTTPException
import logging
from ....infrastructure.config import settings

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self):
        # 存储每个IP的请求记录 {ip: (count, start_time)}
        self.requests: Dict[str, Tuple[int, datetime]] = {}
        
        # 配置
        self.max_requests = settings.RATE_LIMIT_REQUESTS  # 最大请求数
        self.window = settings.RATE_LIMIT_WINDOW  # 时间窗口(秒)
    
    def is_allowed(self, ip: str) -> bool:
        """检查请求是否允许"""
        now = datetime.now()
        
        # 获取IP的请求记录
        if ip in self.requests:
            count, start_time = self.requests[ip]
            
            # 检查是否在时间窗口内
            if now - start_time < timedelta(seconds=self.window):
                # 在窗口内且未超过限制
                if count < self.max_requests:
                    self.requests[ip] = (count + 1, start_time)
                    return True
                # 超过限制
                return False
            
            # 超过时间窗口,重置计数
            self.requests[ip] = (1, now)
            return True
        
        # 新IP
        self.requests[ip] = (1, now)
        return True
    
    def cleanup(self):
        """清理过期记录"""
        now = datetime.now()
        expired = []
        
        for ip, (_, start_time) in self.requests.items():
            if now - start_time > timedelta(seconds=self.window):
                expired.append(ip)
        
        for ip in expired:
            del self.requests[ip]

# 全局限流器
limiter = RateLimiter()

async def rate_limit_middleware(request: Request, call_next):
    """限流中间件"""
    if not settings.RATE_LIMIT_ENABLED:
        return await call_next(request)
    
    # 获取客户端IP
    client_ip = request.client.host
    
    # 检查是否允许请求
    if not limiter.is_allowed(client_ip):
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        raise HTTPException(
            status_code=429,
            detail="Too many requests"
        )
    
    # 定期清理过期记录
    limiter.cleanup()
    
    return await call_next(request) 