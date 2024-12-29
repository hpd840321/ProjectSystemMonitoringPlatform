import pytest
from alembic.config import Config
from alembic import command

async def test_migration_upgrade(client, admin_token):
    """测试数据库升级"""
    # 获取当前版本
    response = await client.get(
        "/api/v1/system/db-version",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    current_version = response.json()["version"]
    
    # 执行升级
    config = Config("alembic.ini")
    command.upgrade(config, "head")
    
    # 验证升级后的版本
    response = await client.get(
        "/api/v1/system/db-version",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.json()["version"] > current_version

async def test_migration_rollback(client, admin_token):
    """测试数据库回滚"""
    # 记录当前版本
    response = await client.get(
        "/api/v1/system/db-version",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    current_version = response.json()["version"]
    
    # 执行回滚
    config = Config("alembic.ini")
    command.downgrade(config, f"{current_version}-1")
    
    # 验证回滚结果
    response = await client.get(
        "/api/v1/system/db-version",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.json()["version"] < current_version 