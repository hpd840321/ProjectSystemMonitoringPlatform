import pytest

async def test_update_system_settings(client, admin_token):
    """测试更新系统设置"""
    response = await client.put(
        "/api/v1/settings/system",
        json={
            "site_name": "Test System",
            "logo_url": "http://example.com/logo.png",
            "allow_registration": True
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

async def test_backup_settings(client, admin_token):
    """测试备份设置"""
    response = await client.post(
        "/api/v1/settings/backup",
        json={
            "backup_path": "/data/backups",
            "retention_days": 7,
            "schedule": "0 0 * * *"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200 