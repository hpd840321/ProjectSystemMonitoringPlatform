from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.infrastructure.tasks.agent import AgentTasks
from app.infrastructure.config import settings

class TaskScheduler:
    """任务调度器"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
    
    def start(self, agent_tasks: AgentTasks):
        """启动调度器"""
        # 添加Agent状态检查任务
        self.scheduler.add_job(
            agent_tasks.check_agent_status,
            CronTrigger(second="*/30"),  # 每30秒执行一次
            id="check_agent_status",
            replace_existing=True
        )
        
        # 添加指标清理任务
        self.scheduler.add_job(
            agent_tasks.cleanup_old_metrics,
            CronTrigger(hour="3"),  # 每天凌晨3点执行
            id="cleanup_old_metrics",
            replace_existing=True
        )
        
        # 启动调度器
        self.scheduler.start()
    
    def shutdown(self):
        """关闭调度器"""
        self.scheduler.shutdown() 