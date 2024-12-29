import pytest

async def test_create_audit_log(client, admin_token):
    """测试创建审计日志"""
    response = await client.post(
        "/api/v1/audit-logs",
        json={
            "action": "user.login",
            "resource": "auth",
            "resource_id": "user_123",
            "details": {
                "ip": "127.0.0.1",
                "user_agent": "Mozilla/5.0"
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

async def test_search_audit_logs(client, admin_token):
    """测试搜索审计日志"""
    response = await client.post(
        "/api/v1/audit-logs/search",
        json={
            "action": "user.login",
            "start_time": "2024-01-01T00:00:00Z",
            "end_time": "2024-01-02T00:00:00Z",
            "limit": 100
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "logs" in data

async def test_export_audit_logs(client, admin_token):
    """测试导出审计日志"""
    response = await client.get(
        "/api/v1/audit-logs/export",
        params={
            "format": "csv",
            "start_time": "2024-01-01T00:00:00Z",
            "end_time": "2024-01-02T00:00:00Z"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv" 