from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.db import create_test_user, create_test_tenant
from tests.config import TEST_DATA

async def init_test_data(db: AsyncSession):
    """初始化测试数据"""
    # 创建管理员用户
    admin = await create_test_user(
        db,
        username=TEST_DATA["admin"]["username"],
        is_admin=True
    )
    
    # 创建普通用户
    user = await create_test_user(
        db,
        username=TEST_DATA["user"]["username"]
    )
    
    # 创建测试租户
    tenant = await create_test_tenant(
        db,
        name=TEST_DATA["tenant"]["name"]
    )
    
    return {
        "admin": admin,
        "user": user,
        "tenant": tenant
    } 