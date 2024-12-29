import asyncio
from datetime import datetime, timedelta
from typing import Optional, List
import logging
from croniter import croniter
from sqlalchemy.orm import Session

from app.crud import storage_policy
from app.models.storage import StoragePolicy
from app.infrastructure.persistence.database import SessionLocal

logger = logging.getLogger(__name__)

class StoragePolicyExecutor:
    """存储策略执行器"""
    
    def __init__(self):
        self.running = False
        self.tasks = {}
    
    async def start(self):
        """启动执行器"""
        self.running = True
        db = SessionLocal()
        try:
            # 加载所有策略
            policies = storage_policy.get_multi(db)
            for policy in policies:
                self._schedule_policy(policy)
        finally:
            db.close()
            
        # 启动调度循环
        while self.running:
            await asyncio.sleep(60)  # 每分钟检查一次
            await self._check_schedules()
    
    def stop(self):
        """停止执行器"""
        self.running = False
        for task in self.tasks.values():
            task.cancel()
    
    def _schedule_policy(self, policy: StoragePolicy):
        """调度策略执行"""
        if policy.backup_enabled and policy.backup_schedule:
            self.tasks[f"{policy.id}_backup"] = {
                "policy": policy,
                "next_run": self._get_next_run(policy.backup_schedule)
            }
    
    async def _check_schedules(self):
        """检查调度"""
        now = datetime.now()
        for task_id, task in list(self.tasks.items()):
            if now >= task["next_run"]:
                policy = task["policy"]
                # 更新下次执行时间
                self.tasks[task_id]["next_run"] = self._get_next_run(policy.backup_schedule)
                # 执行策略
                asyncio.create_task(self._execute_policy(policy))
    
    async def _execute_policy(self, policy: StoragePolicy):
        """执行存储策略"""
        db = SessionLocal()
        try:
            # 记录开始执行
            execution = await storage_policy.record_execution(
                db,
                policy_id=policy.id,
                action_type="cleanup",
                status="running"
            )
            
            try:
                # 执行数据清理
                affected_rows = await self._cleanup_data(db, policy)
                
                # 更新执行记录
                execution.status = "success"
                execution.affected_rows = affected_rows
                execution.completed_at = datetime.now()
                
            except Exception as e:
                logger.exception(f"Failed to execute storage policy {policy.id}")
                execution.status = "failed"
                execution.error_message = str(e)
                execution.completed_at = datetime.now()
            
            db.add(execution)
            db.commit()
            
        finally:
            db.close()
    
    async def _cleanup_data(self, db: Session, policy: StoragePolicy) -> int:
        """清理数据"""
        cutoff_date = datetime.now() - timedelta(days=policy.retention_days)
        affected_rows = 0
        
        if policy.data_type == "metrics":
            # 清理指标数据
            result = await db.execute(
                "DELETE FROM metrics WHERE timestamp < :cutoff",
                {"cutoff": cutoff_date}
            )
            affected_rows = result.rowcount
            
        elif policy.data_type == "logs":
            # 清理日志数据
            result = await db.execute(
                "DELETE FROM logs WHERE timestamp < :cutoff",
                {"cutoff": cutoff_date}
            )
            affected_rows = result.rowcount
            
        elif policy.data_type == "alerts":
            # 清理告警数据
            result = await db.execute(
                "DELETE FROM alerts WHERE created_at < :cutoff",
                {"cutoff": cutoff_date}
            )
            affected_rows = result.rowcount
            
        elif policy.data_type == "backups":
            # 清理备份数据
            result = await db.execute(
                "DELETE FROM backups WHERE created_at < :cutoff",
                {"cutoff": cutoff_date}
            )
            affected_rows = result.rowcount
        
        return affected_rows
    
    def _get_next_run(self, schedule: str) -> datetime:
        """获取下次执行时间"""
        cron = croniter(schedule, datetime.now())
        return cron.get_next(datetime) 