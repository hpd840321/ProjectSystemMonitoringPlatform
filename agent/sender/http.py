import aiohttp
from .base import BaseSender

class HttpSender(BaseSender):
    def __init__(self, config: dict):
        self.server_url = config["server_url"]
        self.auth_key = config["auth_key"]
        self.retry_config = config["retry"]

    async def send(self, data: Dict[str, Any]) -> bool:
        """通过HTTP发送数据"""
        headers = {
            "Authorization": f"Bearer {self.auth_key}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    self.server_url,
                    json=data,
                    headers=headers
                ) as response:
                    return response.status == 200
            except Exception as e:
                # 处理网络异常
                return False 