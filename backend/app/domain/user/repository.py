from abc import ABC, abstractmethod
from typing import List, Optional
from .aggregate import User, ProjectMember

class UserRepository(ABC):
    """用户仓储接口"""
    
    @abstractmethod
    async def save(self, user: User) -> None:
        """保存用户"""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """根据ID获取用户"""
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        pass

class ProjectMemberRepository(ABC):
    """项目成员仓储接口"""
    
    @abstractmethod
    async def save(self, member: ProjectMember) -> None:
        """保存项目成员"""
        pass
    
    @abstractmethod
    async def list_by_project(self, project_id: str) -> List[ProjectMember]:
        """获取项目成员列表"""
        pass
    
    @abstractmethod
    async def remove(self, project_id: str, user_id: str) -> None:
        """移除项目成员"""
        pass 