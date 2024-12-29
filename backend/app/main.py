from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.scheduler import TaskScheduler
from app.infrastructure.tasks.agent import AgentTasks
from app.interface.api.middleware import AuditMiddleware
from app.infrastructure.persistence.database import engine, Base
from app.interface.api.v1 import router as api_router
from app.interface.api.middleware import exception_handler
from app.infrastructure.logging import setup_logging
from .interface.ws import ws_router
from .interface.api.middlewares.rate_limit import rate_limit_middleware
from .interface.api.middlewares.auth import auth_middleware
from .interface.api.middlewares.audit import audit_middleware
from .infrastructure.tasks.monitor import MonitorTasks
from .infrastructure.tasks.agent import AgentStatusChecker
from .interface.api.v1.dependencies import get_agent_service
from .infrastructure.tasks.agent_metrics import AgentMetricsAggregator
from app.infrastructure.log.service import LogService
from app.infrastructure.storage.executor import StoragePolicyExecutor
from app.infrastructure.backup.executor import BackupExecutor
from app.interface.api.middlewares.tenant import TenantMiddleware
from app.interface.api.v1.tenant import router as tenant_router
from app.infrastructure.gateway.core import gateway
from app.infrastructure.gateway.plugins.auth import (
    AuthPlugin,
    RateLimitPlugin,
    LoggingPlugin
)
import asyncio

# 配置日志
logger = setup_logging()

# 创建FastAPI应用
app = FastAPI(title="Server Monitor")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置审计日志
audit_service = get_audit_service()
app.add_middleware(AuditMiddleware, audit_service=audit_service)

# 注册异常处理器
app.middleware("http")(exception_handler)

# 注册中间件(按顺序)
app.middleware("http")(rate_limit_middleware)  # 限流最先处理
app.middleware("http")(exception_handler)      # 异常处理其次
app.middleware("http")(auth_middleware)        # 认证中间件
app.middleware("http")(audit_middleware)       # 审计日志最后

# 注册路由
app.include_router(api_router, prefix="/api/v1")
app.include_router(ws_router)  # WebSocket路由
app.include_router(
    tenant_router,
    prefix="/api/v1",
    tags=["tenants"]
)

# 创建数据库表
@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 启动定时任务
scheduler = TaskScheduler()

@app.on_event("startup")
async def start_scheduler():
    # 初始化Agent任务
    agent_tasks = AgentTasks(get_agent_service())
    scheduler.start(agent_tasks)

@app.on_event("shutdown")
async def shutdown_scheduler():
    scheduler.shutdown()

# 启动后台任务
@app.on_event("startup")
async def startup_event():
    monitor_tasks = MonitorTasks()
    asyncio.create_task(monitor_tasks.start())
    # 启动Agent状态检查
    service = await get_agent_service()
    checker = AgentStatusChecker(service)
    asyncio.create_task(checker.run())
    
    # 启动指标聚合任务
    aggregator = AgentMetricsAggregator(service)
    asyncio.create_task(aggregator.run())
    
    # 启动日志服务
    asyncio.create_task(start_log_service())

@app.on_event("shutdown")
async def shutdown_event():
    # 清理资源
    pass 

async def start_log_service():
    """启动日志服务"""
    db = SessionLocal()
    try:
        service = LogService(db)
        await service.start()
    finally:
        db.close() 

# 创建存储策略执行器实例
storage_executor = StoragePolicyExecutor()

@app.on_event("startup")
async def start_storage_executor():
    """启动存储策略执行器"""
    asyncio.create_task(storage_executor.start())

@app.on_event("shutdown")
async def stop_storage_executor():
    """停止存储策略执行器"""
    storage_executor.stop() 

# 创建备份执行器实例
backup_executor = BackupExecutor()

@app.on_event("startup")
async def start_backup_executor():
    """启动备份执行器"""
    asyncio.create_task(backup_executor.start())

@app.on_event("shutdown")
async def stop_backup_executor():
    """停止备份执行器"""
    backup_executor.stop() 

# 在应用程序创建后添加中间件
app.add_middleware(TenantMiddleware) 

# 注册网关插件
gateway.register_plugin("auth", AuthPlugin())
gateway.register_plugin("rate_limit", RateLimitPlugin(rate_limit=100))
gateway.register_plugin("logging", LoggingPlugin())

# 添加网关中间件
@app.middleware("http")
async def gateway_middleware(request: Request, call_next):
    # 检查是否是网关路由
    if request.url.path.startswith("/gateway/"):
        return await gateway.handle_request(request)
    return await call_next(request) 