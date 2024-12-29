import pytest
from datetime import datetime

async def test_create_backup(client, admin_token):
    """测试创建备份"""
    response = await client.post(
        "/api/v1/backups",
        json={
            "name": f"backup_{datetime.now().strftime('%Y%m%d')}",
            "description": "Test backup",
            "include_data": True
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "backup_id" in data

async def test_restore_backup(client, admin_token):
    """测试恢复备份"""
    # 先创建备份
    backup_response = await client.post(
        "/api/v1/backups",
        json={
            "name": "test_backup",
            "description": "Test backup",
            "include_data": True
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    backup_id = backup_response.json()["backup_id"]
    
    # 执行恢复
    response = await client.post(
        f"/api/v1/backups/{backup_id}/restore",
        json={
            "restore_data": True,
            "restore_config": True
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

async def test_list_backups(client, admin_token):
    """测试获取备份列表"""
    response = await client.get(
        "/api/v1/backups",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 