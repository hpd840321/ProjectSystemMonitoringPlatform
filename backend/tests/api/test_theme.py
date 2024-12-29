import pytest

async def test_get_theme_config(client):
    """测试获取主题配置"""
    response = await client.get("/api/v1/themes/config")
    assert response.status_code == 200
    data = response.json()
    assert "current_theme" in data
    assert "available_themes" in data

async def test_update_theme(client, admin_token):
    """测试更新主题"""
    response = await client.put(
        "/api/v1/themes/current",
        json={
            "theme": "dark",
            "config": {
                "primary_color": "#1890ff",
                "border_radius": "4px"
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

async def test_custom_theme(client, admin_token):
    """测试自定义主题"""
    response = await client.post(
        "/api/v1/themes",
        json={
            "name": "custom_theme",
            "config": {
                "primary_color": "#f5222d",
                "secondary_color": "#52c41a",
                "border_radius": "6px",
                "font_family": "Arial"
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200 