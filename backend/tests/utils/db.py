from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.tenant import Tenant

async def create_test_user(
    db: AsyncSession,
    username: str = "testuser",
    is_admin: bool = False
) -> User:
    """创建测试用户"""
    user = User(
        username=username,
        email=f"{username}@example.com",
        is_admin=is_admin
    )
    user.set_password("Test123456")
    db.add(user)
    await db.commit()
    return user

async def create_test_tenant(
    db: AsyncSession,
    name: str = "Test Tenant"
) -> Tenant:
    """创建测试租户"""
    tenant = Tenant(
        name=name,
        code=name.lower().replace(" ", "_")
    )
    db.add(tenant)
    await db.commit()
    return tenant 