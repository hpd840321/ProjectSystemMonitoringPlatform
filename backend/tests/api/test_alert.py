import pytest
from datetime import datetime, timedelta

async def test_create_alert_rule(client, admin_token):
    """测试创建告警规则"""
    response = await client.post(
        "/api/v1/alert-rules",
        json={
            "name": "High CPU Usage",
            "monitor_id": 1,
            "condition": {
                "operator": ">",
                "threshold": 80
            },
            "duration": 300,
            "severity": "critical"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "High CPU Usage"

async def test_alert_notification(client, admin_token):
    """测试告警通知"""
    response = await client.post(
        "/api/v1/alert-channels",
        json={
            "name": "Email Channel",
            "type": "email",
            "config": {
                "recipients": ["admin@example.com"]
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200 

async def test_alert_rule_conditions(client, admin_token):
    """测试告警规则条件"""
    response = await client.post(
        "/api/v1/alert-rules",
        json={
            "name": "Complex Alert",
            "monitor_id": 1,
            "conditions": [
                {
                    "metric": "cpu_usage",
                    "operator": ">",
                    "threshold": 80,
                    "duration": "5m"
                },
                {
                    "metric": "memory_usage",
                    "operator": ">",
                    "threshold": 90,
                    "duration": "5m"
                }
            ],
            "logic": "AND",
            "severity": "critical"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

async def test_alert_notification_channels(client, admin_token):
    """测试告警通知渠道"""
    # 创建邮件通知渠道
    email_channel = await client.post(
        "/api/v1/alert-channels",
        json={
            "type": "email",
            "name": "Email Channel",
            "config": {
                "recipients": ["admin@example.com"]
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert email_channel.status_code == 200

    # 创建Webhook通知渠道
    webhook_channel = await client.post(
        "/api/v1/alert-channels",
        json={
            "type": "webhook",
            "name": "Webhook Channel",
            "config": {
                "url": "http://example.com/webhook",
                "method": "POST"
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert webhook_channel.status_code == 200

async def test_alert_templates(client, admin_token):
    """测试告警模板"""
    response = await client.post(
        "/api/v1/alert-templates",
        json={
            "name": "Custom Template",
            "content": """
            告警级别: ${severity}
            告警时间: ${timestamp}
            告警详情: ${message}
            监控指标: ${metric}
            当前值: ${value}
            阈值: ${threshold}
            """,
            "format": "markdown"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

async def test_alert_aggregation(client, admin_token):
    """测试告警聚合"""
    response = await client.post(
        "/api/v1/alert-rules",
        json={
            "name": "Aggregated Alert",
            "monitor_id": 1,
            "condition": {
                "metric": "error_count",
                "operator": ">",
                "threshold": 10,
                "window": "5m",
                "aggregation": "sum"
            },
            "severity": "warning"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200 

async def test_alert_rule_dependencies(client, admin_token):
    """测试告警规则依赖关系"""
    # 创建父级告警规则
    parent_response = await client.post(
        "/api/v1/alert-rules",
        json={
            "name": "Parent Alert",
            "monitor_id": 1,
            "condition": {"metric": "service_status", "operator": "==", "value": "down"},
            "severity": "critical"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    parent_id = parent_response.json()["id"]

    # 创建依赖的子告警规则
    child_response = await client.post(
        "/api/v1/alert-rules",
        json={
            "name": "Child Alert",
            "monitor_id": 2,
            "condition": {"metric": "error_rate", "operator": ">", "threshold": 5},
            "severity": "warning",
            "dependencies": [parent_id],
            "suppress_if_parent_active": True
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert child_response.status_code == 200

async def test_alert_maintenance_window(client, admin_token):
    """测试告警维护窗口"""
    response = await client.post(
        "/api/v1/maintenance-windows",
        json={
            "name": "Weekly Maintenance",
            "schedule": "0 0 * * 0",  # 每周日零点
            "duration": "2h",
            "affected_rules": ["all"],
            "suppress_alerts": True
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200 

async def test_alert_rule_update(client, admin_token):
    """测试告警规则更新"""
    # 创建规则
    create_response = await client.post(
        "/api/v1/alert-rules",
        json={
            "name": "Test Alert",
            "monitor_id": 1,
            "condition": {"operator": ">", "threshold": 80},
            "severity": "warning"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    rule_id = create_response.json()["id"]

    # 更新规则
    update_response = await client.put(
        f"/api/v1/alert-rules/{rule_id}",
        json={
            "name": "Updated Alert",
            "condition": {"operator": ">", "threshold": 90},
            "severity": "critical"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Alert"

async def test_alert_escalation(client, admin_token):
    """测试告警升级"""
    response = await client.post(
        "/api/v1/alert-rules",
        json={
            "name": "Escalating Alert",
            "monitor_id": 1,
            "condition": {"operator": ">", "threshold": 80},
            "severity": "warning",
            "escalation": {
                "conditions": [
                    {
                        "duration": "10m",
                        "new_severity": "critical"
                    },
                    {
                        "duration": "30m",
                        "new_severity": "emergency"
                    }
                ],
                "notify_channels": ["email", "sms"]
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

async def test_alert_silence(client, admin_token):
    """测试告警静默"""
    # 创建静默规则
    silence_response = await client.post(
        "/api/v1/alert-silences",
        json={
            "name": "Test Silence",
            "start_time": "2024-01-01T00:00:00Z",
            "end_time": "2024-01-02T00:00:00Z",
            "matchers": [
                {"name": "severity", "value": "warning"},
                {"name": "service", "value": "test-service"}
            ]
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert silence_response.status_code == 200

    # 验证静默效果
    alert_response = await client.post(
        "/api/v1/alerts",
        json={
            "severity": "warning",
            "service": "test-service",
            "message": "Test alert"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert alert_response.json()["status"] == "silenced" 

async def test_alert_rule_batch_operations(client, admin_token):
    """测试告警规则批量操作"""
    # 批量创建规则
    rules = [
        {
            "name": f"Test Alert {i}",
            "monitor_id": 1,
            "condition": {"operator": ">", "threshold": 80 + i},
            "severity": "warning"
        }
        for i in range(3)
    ]
    
    create_response = await client.post(
        "/api/v1/alert-rules/batch",
        json={"rules": rules},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert create_response.status_code == 200
    rule_ids = [r["id"] for r in create_response.json()]
    
    # 批量启用/禁用
    toggle_response = await client.put(
        "/api/v1/alert-rules/batch/toggle",
        json={
            "rule_ids": rule_ids,
            "enabled": False
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert toggle_response.status_code == 200
    
    # 批量删除
    delete_response = await client.delete(
        "/api/v1/alert-rules/batch",
        json={"rule_ids": rule_ids},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert delete_response.status_code == 200

async def test_alert_rule_inheritance(client, admin_token):
    """测试告警规则继承"""
    # 创建模板规则
    template_response = await client.post(
        "/api/v1/alert-templates",
        json={
            "name": "CPU Alert Template",
            "condition": {"metric": "cpu_usage", "operator": ">", "threshold": 80},
            "severity": "warning",
            "notify_channels": ["email"]
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    template_id = template_response.json()["id"]
    
    # 基于模板创建规则
    rule_response = await client.post(
        "/api/v1/alert-rules",
        json={
            "name": "Production CPU Alert",
            "template_id": template_id,
            "override": {
                "severity": "critical",
                "threshold": 90
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert rule_response.status_code == 200

async def test_alert_rule_tags(client, admin_token):
    """测试告警规则标签"""
    response = await client.post(
        "/api/v1/alert-rules",
        json={
            "name": "Tagged Alert",
            "monitor_id": 1,
            "condition": {"operator": ">", "threshold": 80},
            "severity": "warning",
            "tags": {
                "environment": "production",
                "service": "api",
                "team": "backend"
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    
    # 按标签查询
    query_response = await client.get(
        "/api/v1/alert-rules",
        params={
            "tags": ["environment=production", "team=backend"]
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert query_response.status_code == 200
    assert len(query_response.json()) > 0 

async def test_alert_rule_lifecycle_management(client, admin_token):
    """测试告警规则生命周期管理"""
    # 创建规则
    create_response = await client.post(
        "/api/v1/alert-rules",
        json={
            "name": "Test Rule",
            "condition": {"metric": "cpu_usage", "operator": ">", "threshold": 80},
            "severity": "warning"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert create_response.status_code == 200
    rule_id = create_response.json()["id"]

    # 更新规则
    update_response = await client.put(
        f"/api/v1/alert-rules/{rule_id}",
        json={"severity": "critical"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert update_response.status_code == 200

    # 启用/禁用规则
    toggle_response = await client.put(
        f"/api/v1/alert-rules/{rule_id}/toggle",
        json={"enabled": False},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert toggle_response.status_code == 200

    # 删除规则
    delete_response = await client.delete(
        f"/api/v1/alert-rules/{rule_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert delete_response.status_code == 200

async def test_alert_rule_evaluation(client, admin_token):
    """测试告警规则评估"""
    # 创建复杂条件规则
    rule_response = await client.post(
        "/api/v1/alert-rules",
        json={
            "name": "Complex Rule",
            "conditions": [
                {
                    "metric": "cpu_usage",
                    "operator": ">",
                    "threshold": 80,
                    "duration": "5m"
                },
                {
                    "metric": "memory_usage",
                    "operator": ">",
                    "threshold": 90,
                    "duration": "5m"
                }
            ],
            "logic": "AND",
            "severity": "critical"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert rule_response.status_code == 200
    rule_id = rule_response.json()["id"]

    # 测试规则评估
    evaluation_response = await client.post(
        f"/api/v1/alert-rules/{rule_id}/evaluate",
        json={
            "metrics": {
                "cpu_usage": 85,
                "memory_usage": 95
            },
            "timestamp": "2024-01-01T00:00:00Z"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert evaluation_response.status_code == 200
    assert evaluation_response.json()["triggered"] == True

async def test_alert_notification_delivery(client, admin_token):
    """测试告警通知发送"""
    # 创建通知渠道
    channels = [
        {
            "type": "email",
            "name": "Email Channel",
            "config": {
                "recipients": ["admin@example.com"]
            }
        },
        {
            "type": "webhook",
            "name": "Webhook Channel",
            "config": {
                "url": "http://example.com/webhook",
                "method": "POST"
            }
        },
        {
            "type": "sms",
            "name": "SMS Channel",
            "config": {
                "phone_numbers": ["+1234567890"]
            }
        }
    ]

    channel_ids = []
    for channel in channels:
        response = await client.post(
            "/api/v1/alert-channels",
            json=channel,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        channel_ids.append(response.json()["id"])

    # 测试通知发送
    notification_response = await client.post(
        "/api/v1/alerts/notify",
        json={
            "alert": {
                "id": "test-alert",
                "name": "Test Alert",
                "severity": "critical",
                "message": "Test alert message"
            },
            "channel_ids": channel_ids
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert notification_response.status_code == 200

async def test_alert_aggregation_and_deduplication(client, admin_token):
    """测试告警聚合和去重"""
    # 创建相似告警
    alerts = [
        {
            "name": "CPU Alert",
            "service": "web-server",
            "severity": "warning",
            "message": f"CPU usage high on web-server-{i}"
        }
        for i in range(5)
    ]

    for alert in alerts:
        response = await client.post(
            "/api/v1/alerts",
            json=alert,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200

    # 获取聚合后的告警
    aggregated_response = await client.get(
        "/api/v1/alerts/aggregated",
        params={"group_by": ["service", "severity"]},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert aggregated_response.status_code == 200
    aggregated_alerts = aggregated_response.json()
    assert len(aggregated_alerts) == 1  # 应该被聚合为一个告警组

async def test_alert_maintenance_windows(client, admin_token):
    """测试告警维护窗口"""
    # 创建维护窗口
    window_response = await client.post(
        "/api/v1/maintenance-windows",
        json={
            "name": "Weekly Maintenance",
            "schedule": "0 0 * * 0",  # 每周日零点
            "duration": "2h",
            "affected_services": ["web-server", "database"],
            "suppress_alerts": True
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert window_response.status_code == 200
    window_id = window_response.json()["id"]

    # 验证维护窗口期间的告警抑制
    alert_response = await client.post(
        "/api/v1/alerts",
        json={
            "service": "web-server",
            "severity": "critical",
            "message": "Test alert during maintenance"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert alert_response.status_code == 200
    assert alert_response.json()["status"] == "suppressed" 