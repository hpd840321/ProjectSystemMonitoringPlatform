from typing import List, Dict

class ServerService:
    async def batch_update_servers(
        self,
        server_ids: List[str],
        updates: Dict
    ) -> None:
        """批量更新服务器"""
        for server_id in server_ids:
            server = await self.server_repo.get_by_id(server_id)
            if not server:
                continue
            
            # 更新服务器属性
            for key, value in updates.items():
                if hasattr(server, key):
                    setattr(server, key, value)
            
            await self.server_repo.save(server)

    async def batch_delete_servers(self, server_ids: List[str]) -> None:
        """批量删除服务器"""
        for server_id in server_ids:
            await self.server_repo.delete(server_id) 