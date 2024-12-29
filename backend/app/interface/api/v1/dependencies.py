from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.infrastructure.persistence.database import get_session
from app.infrastructure.persistence.repositories.user import (
    SQLUserRepository,
    SQLProjectMemberRepository
)
from app.domain.user.service import UserService
from app.application.user.service import UserApplicationService
from ....domain.alert.service import AlertLevelService, NotificationService
from ....infrastructure.persistence.alert import (
    AlertLevelRepositoryImpl,
    NotificationChannelRepositoryImpl
)
from ....infrastructure.notification.sender import NotificationSender
from ....domain.monitor.service import MonitorService
from ....infrastructure.persistence.monitor import (
    CustomMetricRepositoryImpl,
    MetricValueRepositoryImpl,
    MetricAggregationRepositoryImpl,
    AggregatedMetricRepositoryImpl,
    RetentionPolicyRepositoryImpl
)
from ...domain.log.service import LogService
from ...infrastructure.persistence.log import (
    LogConfigRepositoryImpl,
    LogEntryRepositoryImpl
)
from ...domain.backup.service import BackupService
from ...infrastructure.persistence.backup import (
    BackupConfigRepositoryImpl,
    BackupJobRepositoryImpl
)
from ...domain.settings.service import SettingService
from ...infrastructure.persistence.settings import SettingRepositoryImpl
from ...infrastructure.database import get_db, Database
from ...infrastructure.persistence.agent import (
    AgentRepositoryImpl,
    AgentVersionRepositoryImpl,
    UpgradeTaskRepositoryImpl,
    AgentMetricsRepositoryImpl
)
from ...domain.agent.service import AgentService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_user_service(
    session: AsyncSession = Depends(get_session)
) -> UserApplicationService:
    user_repo = SQLUserRepository(session)
    member_repo = SQLProjectMemberRepository(session)
    user_service = UserService(user_repo, member_repo)
    return UserApplicationService(user_service)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserApplicationService = Depends(get_user_service)
):
    try:
        # TODO: 实现token验证
        return await service.get_current_user(token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) 

async def get_alert_level_service() -> AlertLevelService:
    db = get_database()
    repo = AlertLevelRepositoryImpl(db)
    return AlertLevelService(repo)

async def get_notification_service() -> NotificationService:
    db = get_database()
    repo = NotificationChannelRepositoryImpl(db)
    return NotificationService(repo)

async def get_notification_sender() -> NotificationSender:
    return NotificationSender() 

async def get_monitor_service() -> MonitorService:
    """获取监控服务"""
    db = get_database()
    return MonitorService(
        custom_metric_repo=CustomMetricRepositoryImpl(db),
        metric_value_repo=MetricValueRepositoryImpl(db),
        aggregation_repo=MetricAggregationRepositoryImpl(db),
        aggregated_metric_repo=AggregatedMetricRepositoryImpl(db),
        retention_policy_repo=RetentionPolicyRepositoryImpl(db)
    ) 

async def get_log_service() -> LogService:
    """获取日志服务"""
    db = get_database()
    return LogService(
        config_repo=LogConfigRepositoryImpl(db),
        entry_repo=LogEntryRepositoryImpl(db)
    ) 

async def get_backup_service() -> BackupService:
    """获取备份服务"""
    db = get_database()
    return BackupService(
        config_repo=BackupConfigRepositoryImpl(db),
        job_repo=BackupJobRepositoryImpl(db)
    ) 

async def get_settings_service() -> SettingService:
    """获取设置服务"""
    db = get_database()
    return SettingService(
        repo=SettingRepositoryImpl(db)
    ) 

async def get_agent_service(
    db: Annotated[Database, Depends(get_db)]
) -> AgentService:
    """获取Agent服务"""
    agent_repo = AgentRepositoryImpl(db)
    version_repo = AgentVersionRepositoryImpl(db)
    task_repo = UpgradeTaskRepositoryImpl(db)
    metrics_repo = AgentMetricsRepositoryImpl(db)
    return AgentService(agent_repo, version_repo, task_repo, metrics_repo) 