import pytest
import asyncio
from httpx import AsyncClient
from app.main import app
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="session")
async def admin_token():
    # 生成管理员token用于测试
    return "test_admin_token"

@pytest.fixture(autouse=True)
async def setup_db():
    # 创建测试数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 清理测试数据
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) 