import pytest

async def test_dynamic_config_update(client, admin_token):
    """测试动态配置更新"""
    response = await client.put(
        "/api/v1/config/runtime",
        json={
            "log_level": "DEBUG",
            "max_connections": 1000,
            "cache_ttl": 3600
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    
    # 验证配置已生效
    config_response = await client.get(
        "/api/v1/config/current",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert config_response.json()["log_level"] == "DEBUG"

async def test_config_validation(client, admin_token):
    """测试配置验证"""
    # 测试无效配置
    response = await client.put(
        "/api/v1/config/runtime",
        json={
            "log_level": "INVALID",
            "max_connections": -1
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 400
    
    # 测试配置依赖关系
    response = await client.put(
        "/api/v1/config/runtime",
        json={
            "min_connections": 100,
            "max_connections": 50  # 违反 min <= max 规则
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 400 

async def test_config_history(client, admin_token):
    """测试配置历史记录"""
    # 多次更新配置
    for i in range(3):
        await client.put(
            "/api/v1/config/runtime",
            json={"log_level": f"DEBUG_{i}"},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
    
    # 获取配置历史
    history_response = await client.get(
        "/api/v1/config/history",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert history_response.status_code == 200
    assert len(history_response.json()) >= 3

async def test_config_rollback(client, admin_token):
    """测试配置回滚"""
    # 获取当前配置版本
    current_response = await client.get(
        "/api/v1/config/current",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    current_version = current_response.json()["version"]
    
    # 执行回滚
    rollback_response = await client.post(
        f"/api/v1/config/rollback/{current_version}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert rollback_response.status_code == 200 

async def test_config_import_export(client, admin_token):
    """测试配置导入导出"""
    # 导出配置
    export_response = await client.get(
        "/api/v1/config/export",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert export_response.status_code == 200
    config_data = export_response.json()
    
    # 修改配置
    config_data["settings"]["new_key"] = "new_value"
    
    # 导入配置
    import_response = await client.post(
        "/api/v1/config/import",
        json=config_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert import_response.status_code == 200

async def test_config_templates(client, admin_token):
    """测试配置模板"""
    # 创建配置模板
    template_response = await client.post(
        "/api/v1/config/templates",
        json={
            "name": "Development",
            "description": "Development environment settings",
            "settings": {
                "log_level": "DEBUG",
                "debug_mode": True,
                "cache_ttl": 60
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert template_response.status_code == 200
    
    # 应用模板
    apply_response = await client.post(
        "/api/v1/config/apply-template",
        json={"template_name": "Development"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert apply_response.status_code == 200 