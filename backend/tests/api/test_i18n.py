import pytest

async def test_get_translations(client):
    """测试获取翻译文本"""
    response = await client.get(
        "/api/v1/i18n/translations",
        params={"lang": "zh-CN"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "messages" in data
    assert isinstance(data["messages"], dict)

async def test_supported_languages(client):
    """测试支持的语言列表"""
    response = await client.get("/api/v1/i18n/languages")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert {"code": "zh-CN", "name": "简体中文"} in data

async def test_custom_translations(client, admin_token):
    """测试自定义翻译"""
    response = await client.post(
        "/api/v1/i18n/translations",
        json={
            "lang": "zh-CN",
            "translations": {
                "custom.key": "自定义文本"
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200 