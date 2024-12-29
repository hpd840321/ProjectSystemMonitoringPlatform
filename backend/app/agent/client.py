import asyncio
import websockets
import json
import logging
from datetime import datetime
import psutil
import platform

logger = logging.getLogger(__name__)

class AgentClient:
    """Agent客户端"""
    
    def __init__(
        self,
        server_url: str,
        agent_id: str,
        heartbeat_interval: int = 30
    ):
        self.server_url = server_url
        self.agent_id = agent_id
        self.heartbeat_interval = heartbeat_interval
        self.websocket = None
    
    async def connect(self):
        """连接服务器"""
        try:
            self.websocket = await websockets.connect(
                f"{self.server_url}/ws/agents/{self.agent_id}"
            )
            logger.info("Connected to server")
            
            # 启动心跳任务
            asyncio.create_task(self.send_heartbeat())
            # 启动指标收集任务
            asyncio.create_task(self.collect_metrics())
            
            # 处理服务器消息
            while True:
                message = await self.websocket.recv()
                await self.handle_message(json.loads(message))
        
        except Exception as e:
            logger.error(f"Connection failed: {str(e)}")
            # 重试连接
            await asyncio.sleep(5)
            await self.connect()
    
    async def send_heartbeat(self):
        """发送心跳"""
        while True:
            try:
                await self.websocket.send(json.dumps({
                    "type": "heartbeat",
                    "timestamp": datetime.now().isoformat()
                }))
                await asyncio.sleep(self.heartbeat_interval)
            except Exception as e:
                logger.error(f"Failed to send heartbeat: {str(e)}")
                break
    
    async def collect_metrics(self):
        """收集系统指标"""
        while True:
            try:
                metrics = {
                    "type": "metrics",
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "cpu_percent": psutil.cpu_percent(),
                        "memory_percent": psutil.virtual_memory().percent,
                        "disk_usage": psutil.disk_usage("/").percent,
                        "network": dict(psutil.net_io_counters()._asdict())
                    }
                }
                await self.websocket.send(json.dumps(metrics))
                await asyncio.sleep(60)  # 每分钟采集一次
            except Exception as e:
                logger.error(f"Failed to collect metrics: {str(e)}")
                break
    
    async def handle_message(self, message: dict):
        """处理服务器消息"""
        msg_type = message.get("type")
        
        if msg_type == "upgrade":
            # 处理升级命令
            await self.handle_upgrade(message)
        elif msg_type == "config":
            # 处理配置更新
            await self.handle_config_update(message)
    
    async def handle_upgrade(self, message: dict):
        """处理升级命令"""
        try:
            version = message["version"]
            task_id = message["task_id"]
            
            # 下载新版本
            # 执行升级
            # 发送结果
            await self.websocket.send(json.dumps({
                "type": "upgrade_result",
                "task_id": task_id,
                "status": "success",
                "error": None
            }))
        except Exception as e:
            await self.websocket.send(json.dumps({
                "type": "upgrade_result",
                "task_id": task_id,
                "status": "failed",
                "error": str(e)
            }))
    
    async def handle_config_update(self, message: dict):
        """处理配置更新"""
        try:
            new_config = message["config"]
            # 应用新配置
            # TODO: 实现配置更新逻辑
            pass
        except Exception as e:
            logger.error(f"Failed to update config: {str(e)}")

if __name__ == "__main__":
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) != 3:
        print("Usage: python client.py <server_url> <agent_id>")
        sys.exit(1)
    
    server_url = sys.argv[1]
    agent_id = sys.argv[2]
    
    client = AgentClient(server_url, agent_id)
    asyncio.run(client.connect()) 