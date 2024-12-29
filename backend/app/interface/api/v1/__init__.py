from fastapi import APIRouter
from .user import router as user_router
from .project import router as project_router
from .agent import router as agent_router
from .alert import router as alert_router
from .backup import router as backup_router
from .ws import router as ws_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["用户管理"])
router.include_router(project_router, prefix="/projects", tags=["项目管理"])
router.include_router(agent_router, prefix="/agents", tags=["Agent管理"])
router.include_router(alert_router, prefix="/alerts", tags=["告警管理"])
router.include_router(backup_router, prefix="/backups", tags=["备份管理"])
router.include_router(ws_router, tags=["WebSocket"]) 