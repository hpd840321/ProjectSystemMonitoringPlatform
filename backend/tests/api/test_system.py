import pytest
from datetime import datetime, timedelta

async def test_system_resources(client, admin_token):
    """测试系统资源监控"""
    response = await client.get(
        "/api/v1/system/resources",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "cpu" in data
    assert "memory" in data
    assert "disk" in data

async def test_process_metrics(client, admin_token):
    """测试进程指标"""
    response = await client.get(
        "/api/v1/system/processes",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 

async def test_system_info(client, admin_token):
    """测试系统信息获取"""
    response = await client.get(
        "/api/v1/system/info",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    
    # 验证系统信息字段
    required_fields = [
        "version", "uptime", "cpu_usage", 
        "memory_usage", "disk_usage", "node_count"
    ]
    for field in required_fields:
        assert field in data

async def test_system_metrics(client, admin_token):
    """测试系统指标采集"""
    # 测试不同时间范围的指标
    time_ranges = [
        ("1h", 60),    # 1小时，60个数据点
        ("6h", 180),   # 6小时，180个数据点
        ("24h", 288),  # 24小时，288个数据点
        ("7d", 168)    # 7天，168个数据点
    ]

    for range_str, expected_points in time_ranges:
        response = await client.get(
            "/api/v1/system/metrics",
            params={"range": range_str},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # 验证数据点数量
        for metric in ["cpu", "memory", "disk", "network"]:
            assert len(data[metric]["data"]) <= expected_points

async def test_system_config_management(client, admin_token):
    """测试系统配置管理"""
    # 获取当前配置
    current_config = await client.get(
        "/api/v1/system/config",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert current_config.status_code == 200

    # 更新配置
    new_config = {
        "log_level": "DEBUG",
        "metrics_retention_days": 30,
        "alert_check_interval": 60,
        "max_concurrent_tasks": 10
    }
    
    update_response = await client.put(
        "/api/v1/system/config",
        json=new_config,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert update_response.status_code == 200

    # 验证配置更新
    verify_response = await client.get(
        "/api/v1/system/config",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    updated_config = verify_response.json()
    for key, value in new_config.items():
        assert updated_config[key] == value

async def test_system_backup(client, admin_token):
    """测试系统备份功能"""
    # 创建备份
    backup_response = await client.post(
        "/api/v1/system/backup",
        json={"description": "Test backup"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert backup_response.status_code == 200
    backup_id = backup_response.json()["id"]

    # 获取备份列表
    list_response = await client.get(
        "/api/v1/system/backups",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert list_response.status_code == 200
    assert len(list_response.json()) > 0

    # 还原备份
    restore_response = await client.post(
        f"/api/v1/system/backup/{backup_id}/restore",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert restore_response.status_code == 200

async def test_system_task_management(client, admin_token):
    """测试系统任务管理"""
    # 创建定时任务
    task_response = await client.post(
        "/api/v1/system/tasks",
        json={
            "name": "Test Task",
            "type": "metric_cleanup",
            "schedule": "0 0 * * *",  # 每天零点
            "params": {
                "retention_days": 30
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert task_response.status_code == 200
    task_id = task_response.json()["id"]

    # 获取任务状态
    status_response = await client.get(
        f"/api/v1/system/tasks/{task_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert status_response.status_code == 200
    assert status_response.json()["status"] in ["pending", "running", "completed"]

async def test_system_node_management(client, admin_token):
    """测试系统节点管理"""
    # 注册新节点
    node_response = await client.post(
        "/api/v1/system/nodes",
        json={
            "hostname": "test-node-1",
            "ip": "192.168.1.100",
            "role": "worker",
            "labels": {
                "zone": "us-east",
                "env": "prod"
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert node_response.status_code == 200
    node_id = node_response.json()["id"]

    # 更新节点状态
    update_response = await client.put(
        f"/api/v1/system/nodes/{node_id}",
        json={"status": "maintenance"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert update_response.status_code == 200

    # 获取节点列表
    list_response = await client.get(
        "/api/v1/system/nodes",
        params={"role": "worker", "status": "maintenance"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert list_response.status_code == 200
    nodes = list_response.json()
    assert len(nodes) > 0
    assert nodes[0]["status"] == "maintenance"

async def test_system_health_check(client, admin_token):
    """测试系统健康检查"""
    # 执行全面健康检查
    health_response = await client.get(
        "/api/v1/system/health",
        params={"full": True},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert health_response.status_code == 200
    health_data = health_response.json()

    # 验证健康检查结果
    required_checks = [
        "database", "cache", "message_queue", 
        "storage", "external_services"
    ]
    for check in required_checks:
        assert check in health_data
        assert health_data[check]["status"] in ["healthy", "degraded", "unhealthy"]

async def test_system_maintenance_mode(client, admin_token):
    """测试系统维护模式"""
    # 启用维护模式
    enable_response = await client.post(
        "/api/v1/system/maintenance/enable",
        json={
            "reason": "Scheduled maintenance",
            "duration": "2h",
            "allow_admin_access": True
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert enable_response.status_code == 200

    # 验证普通用户无法访问
    user_response = await client.get(
        "/api/v1/system/info",
        headers={"Authorization": "Bearer user_token"}
    )
    assert user_response.status_code == 503
    assert "maintenance mode" in user_response.json()["message"]

    # 管理员可以访问
    admin_response = await client.get(
        "/api/v1/system/info",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert admin_response.status_code == 200

    # 禁用维护模式
    disable_response = await client.post(
        "/api/v1/system/maintenance/disable",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert disable_response.status_code == 200 