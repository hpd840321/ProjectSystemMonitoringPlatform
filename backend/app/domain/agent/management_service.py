from datetime import datetime, timedelta
from typing import List, Optional
from uuid import uuid4
import asyncio
import aiohttp
from .management import (
    AgentVersion,
    AgentStatusInfo,
    AgentUpdateTask,
    AgentStatus,
    UpdateTaskStatus
)
from .repository import AgentRepository

class AgentManagementService:
    def __init__(self, agent_repo: AgentRepository):
        self.agent_repo = agent_repo
        self._status_checker: Optional[asyncio.Task] = None
    
    async def start_status_checker(self) -> None:
        """启动状态检查器"""
        if self._status_checker:
            return
            
        self._status_checker = asyncio.create_task(self._check_agent_status())
    
    async def stop_status_checker(self) -> None:
        """停止状态检查器"""
        if self._status_checker:
            self._status_checker.cancel()
            try:
                await self._status_checker
            except asyncio.CancelledError:
                pass
            self._status_checker = None
    
    async def _check_agent_status(self) -> None:
        """检查Agent状态"""
        while True:
            try:
                # 获取所有Agent状态
                statuses = await self.agent_repo.list_agent_status()
                now = datetime.now()
                
                for status in statuses:
                    # 检查心跳超时
                    if (now - status.last_heartbeat) > timedelta(minutes=5):
                        status.status = AgentStatus.OFFLINE
                        await self.agent_repo.update_agent_status(status)
                
                await asyncio.sleep(60)  # 每分钟检查一次
            except asyncio.CancelledError:
                raise
            except Exception as e:
                print(f"Status checker error: {e}")
                await asyncio.sleep(5)
    
    async def register_version(
        self,
        version: str,
        package_url: str,
        checksum: str,
        description: Optional[str] = None
    ) -> AgentVersion:
        """注册新版本"""
        # 创建版本记录
        now = datetime.now()
        agent_version = AgentVersion(
            id=str(uuid4()),
            version=version,
            description=description,
            package_url=package_url,
            checksum=checksum,
            is_latest=True,
            created_at=now,
            updated_at=now
        )
        
        # 更新之前的最新版本
        await self.agent_repo.clear_latest_version()
        await self.agent_repo.save_version(agent_version)
        
        # 检查需要更新的Agent
        await self._schedule_updates(agent_version)
        
        return agent_version
    
    async def _schedule_updates(self, new_version: AgentVersion) -> None:
        """调度更新任务"""
        # 获取所有在线的Agent
        statuses = await self.agent_repo.list_agent_status()
        online_agents = [s for s in statuses if s.status == AgentStatus.ONLINE]
        
        for agent in online_agents:
            if agent.version != new_version.version:
                # 创建更新任务
                task = AgentUpdateTask(
                    id=str(uuid4()),
                    agent_id=agent.agent_id,
                    from_version=agent.version,
                    to_version=new_version.version,
                    status=UpdateTaskStatus.PENDING,
                    error=None,
                    started_at=None,
                    completed_at=None,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                await self.agent_repo.save_update_task(task)
    
    async def process_update_tasks(self) -> None:
        """处理更新任务"""
        while True:
            try:
                # 获取待处理的任务
                tasks = await self.agent_repo.get_pending_update_tasks()
                
                for task in tasks:
                    # 获取Agent状态
                    status = await self.agent_repo.get_agent_status(task.agent_id)
                    if not status or status.status != AgentStatus.ONLINE:
                        continue
                    
                    # 开始更新
                    task.status = UpdateTaskStatus.RUNNING
                    task.started_at = datetime.now()
                    await self.agent_repo.save_update_task(task)
                    
                    try:
                        # 发送更新命令到Agent
                        version = await self.agent_repo.get_version(task.to_version)
                        if not version:
                            raise ValueError(f"Version not found: {task.to_version}")
                        
                        success = await self._send_update_command(
                            status.agent_id,
                            version.package_url,
                            version.checksum
                        )
                        
                        if success:
                            task.status = UpdateTaskStatus.SUCCESS
                        else:
                            task.status = UpdateTaskStatus.FAILED
                            task.error = "Update command failed"
                    except Exception as e:
                        task.status = UpdateTaskStatus.FAILED
                        task.error = str(e)
                    
                    task.completed_at = datetime.now()
                    await self.agent_repo.save_update_task(task)
                
                await asyncio.sleep(30)  # 每30秒检查一次
            except asyncio.CancelledError:
                raise
            except Exception as e:
                print(f"Update processor error: {e}")
                await asyncio.sleep(5)
    
    async def _send_update_command(
        self,
        agent_id: str,
        package_url: str,
        checksum: str
    ) -> bool:
        """发送更新命令到Agent"""
        try:
            # TODO: 实现与Agent的通信
            return True
        except Exception:
            return False 