from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.scheduler import TaskScheduler
from app.infrastructure.tasks.agent import AgentTasks
from app.interface.api.middleware import AuditMiddleware
from app.infrastructure.persistence.database import engine, Base
from app.interface.api.v1 import router as api_router
from app.interface.api.middleware import exception_handler
from app.infrastructure.logging import setup_logging

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

# 注册API路由
app.include_router(api_router, prefix="/api/v1")

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