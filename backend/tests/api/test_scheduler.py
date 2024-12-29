import pytest

async def test_create_scheduled_task(client, admin_token):
    """测试创建定时任务"""
    response = await client.post(
        "/api/v1/scheduler/tasks",
        json={
            "name": "test_task",
            "type": "backup",
            "schedule": "0 0 * * *",  # 每天凌晨执行
            "config": {
                "backup_type": "full",
                "retention_days": 7
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test_task"

async def test_task_execution(client, admin_token):
    """测试任务执行"""
    response = await client.post(
        "/api/v1/scheduler/tasks/test_task/execute",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

async def test_task_history(client, admin_token):
    """测试任务执行历史"""
    response = await client.get(
        "/api/v1/scheduler/tasks/test_task/history",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 