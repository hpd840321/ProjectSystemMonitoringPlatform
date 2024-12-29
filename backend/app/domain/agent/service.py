from datetime import datetime, timedelta
from typing import List, Optional, Dict
from uuid import uuid4
import hashlib
import logging
from .repository import AgentRepository, AgentVersionRepository, UpgradeTaskRepository, AgentMetricsRepository
from .aggregate import Agent, AgentVersion, UpgradeTask, AgentStatus, UpgradeTaskStatus
from .agent_metrics import MetricsQuery, MetricsResponse, HourlyMetricsResponse
from .exceptions import MetricsNotFoundError, InvalidTimeRangeError

logger = logging.getLogger(__name__)

class AgentService:
    def __init__(
        self,
        agent_repo: AgentRepository,
        version_repo: AgentVersionRepository,
        task_repo: UpgradeTaskRepository,
        metrics_repo: AgentMetricsRepository
    ):
        self.agent_repo = agent_repo
        self.version_repo = version_repo
        self.task_repo = task_repo
        self.metrics_repo = metrics_repo
    
    async def register_agent(
        self,
        server_id: str,
        version: str,
        config: Dict
    ) -> Agent:
        """注册Agent"""
        now = datetime.now()
        agent = Agent(
            id=str(uuid4()),
            server_id=server_id,
            version=version,
            status=AgentStatus.ONLINE,
            last_heartbeat=now,
            config=config,
            created_at=now,
            updated_at=now
        )
        await self.agent_repo.save(agent)
        return agent
    
    async def update_heartbeat(self, agent_id: str) -> None:
        """更新Agent心跳"""
        agent = await self.agent_repo.get_by_id(agent_id)
        if not agent:
            return
        
        agent.last_heartbeat = datetime.now()
        agent.updated_at = datetime.now()
        await self.agent_repo.save(agent)
    
    async def create_version(
        self,
        version: str,
        file_path: str,
        description: Optional[str] = None,
        is_latest: bool = True
    ) -> AgentVersion:
        """创建Agent版本"""
        # 计算文件校验和
        with open(file_path, 'rb') as f:
            checksum = hashlib.sha256(f.read()).hexdigest()
        
        now = datetime.now()
        version = AgentVersion(
            id=str(uuid4()),
            version=version,
            file_path=file_path,
            checksum=checksum,
            description=description,
            is_latest=is_latest,
            created_at=now,
            updated_at=now
        )
        await self.version_repo.save(version)
        return version
    
    async def create_upgrade_task(
        self,
        agent_id: str,
        to_version: str
    ) -> UpgradeTask:
        """创建升级任务"""
        agent = await self.agent_repo.get_by_id(agent_id)
        if not agent:
            raise ValueError("Agent not found")
        
        version = await self.version_repo.get_by_version(to_version)
        if not version:
            raise ValueError("Version not found")
        
        now = datetime.now()
        task = UpgradeTask(
            id=str(uuid4()),
            agent_id=agent_id,
            from_version=agent.version,
            to_version=to_version,
            status=UpgradeTaskStatus.PENDING,
            error=None,
            created_at=now,
            updated_at=now
        )
        await self.task_repo.save(task)
        return task
    
    async def update_task_status(
        self,
        task_id: str,
        status: UpgradeTaskStatus,
        error: Optional[str] = None
    ) -> None:
        """更新任务状态"""
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            return
        
        task.status = status
        task.error = error
        task.updated_at = datetime.now()
        await self.task_repo.save(task)
        
        # 如果升级成功,更新Agent版本
        if status == UpgradeTaskStatus.SUCCESS:
            agent = await self.agent_repo.get_by_id(task.agent_id)
            if agent:
                agent.version = task.to_version
                agent.updated_at = datetime.now()
                await self.agent_repo.save(agent) 
    
    async def get_metrics(
        self,
        agent_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[AgentMetrics]:
        """获取Agent指标"""
        # 验证时间范围
        if end_time <= start_time:
            raise InvalidTimeRangeError("结束时间必须大于开始时间")
            
        if (end_time - start_time) > timedelta(days=7):
            raise InvalidTimeRangeError("时间范围不能超过7天")
        
        try:
            metrics = await self.metrics_repo.get_metrics(
                agent_id=agent_id,
                start_time=start_time,
                end_time=end_time
            )
            
            if not metrics:
                raise MetricsNotFoundError(f"未找到Agent {agent_id} 在指定时间范围的指标数据")
            
            logger.info(
                f"Retrieved {len(metrics)} metrics for agent {agent_id} "
                f"from {start_time} to {end_time}"
            )
            return metrics
            
        except Exception as e:
            logger.error(
                f"Failed to get metrics for agent {agent_id}: {str(e)}",
                exc_info=True
            )
            raise
    
    async def get_hourly_metrics(
        self,
        agent_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[AgentMetricsHourly]:
        """获取Agent小时聚合指标"""
        # 验证时间范围
        if end_time <= start_time:
            raise InvalidTimeRangeError("结束时间必须大于开始时间")
            
        if (end_time - start_time) > timedelta(days=30):
            raise InvalidTimeRangeError("时间范围不能超过30天")
        
        try:
            metrics = await self.metrics_repo.get_hourly_metrics(
                agent_id=agent_id,
                start_time=start_time,
                end_time=end_time
            )
            
            if not metrics:
                raise MetricsNotFoundError(f"未找到Agent {agent_id} 在指定时间范围的聚合指标数据")
            
            logger.info(
                f"Retrieved {len(metrics)} hourly metrics for agent {agent_id} "
                f"from {start_time} to {end_time}"
            )
            return metrics
            
        except Exception as e:
            logger.error(
                f"Failed to get hourly metrics for agent {agent_id}: {str(e)}",
                exc_info=True
            )
            raise 