import pytest
import json
from pathlib import Path

async def test_export_data(client, admin_token):
    """测试数据导出"""
    response = await client.post(
        "/api/v1/data/export",
        json={
            "type": "users",
            "format": "json",
            "filters": {
                "created_after": "2024-01-01"
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, list)

async def test_import_data(client, admin_token):
    """测试数据导入"""
    test_data = [
        {
            "username": "import_test",
            "email": "import@test.com",
            "role": "user"
        }
    ]
    
    response = await client.post(
        "/api/v1/data/import",
        json={
            "type": "users",
            "format": "json",
            "data": test_data
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["imported_count"] == 1

async def test_data_validation(client, admin_token):
    """测试数据验证"""
    invalid_data = [
        {
            "username": "test",  # 用户名太短
            "email": "invalid_email",  # 无效邮箱
            "role": "invalid_role"  # 无效角色
        }
    ]
    
    response = await client.post(
        "/api/v1/data/import",
        json={
            "type": "users",
            "format": "json",
            "data": invalid_data
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 400
    data = response.json()
    assert "validation_errors" in data 