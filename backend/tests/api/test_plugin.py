import pytest
from pathlib import Path

async def test_install_plugin(client, admin_token):
    """测试安装插件"""
    # 创建测试插件文件
    plugin_file = Path(__file__).parent / "test_data" / "test_plugin.zip"
    
    with open(plugin_file, "rb") as f:
        response = await client.post(
            "/api/v1/plugins/install",
            files={"file": ("test_plugin.zip", f, "application/zip")},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test_plugin"
    assert data["status"] == "installed"

async def test_plugin_config(client, admin_token):
    """测试插件配置"""
    response = await client.put(
        "/api/v1/plugins/test_plugin/config",
        json={
            "enabled": True,
            "settings": {
                "api_key": "test_key",
                "endpoint": "http://test.com"
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

async def test_plugin_hooks(client, admin_token):
    """测试插件钩子"""
    response = await client.get(
        "/api/v1/plugins/hooks",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 