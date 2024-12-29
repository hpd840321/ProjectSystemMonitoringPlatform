import pytest

async def test_global_search(client, admin_token):
    """测试全局搜索"""
    response = await client.post(
        "/api/v1/search",
        json={
            "query": "test",
            "types": ["users", "logs", "alerts"],
            "page": 1,
            "page_size": 10
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "results" in data

async def test_search_suggestions(client, admin_token):
    """测试搜索建议"""
    response = await client.get(
        "/api/v1/search/suggestions",
        params={"query": "te"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

async def test_search_filters(client, admin_token):
    """测试搜索过滤器"""
    response = await client.post(
        "/api/v1/search",
        json={
            "query": "error",
            "filters": {
                "date_range": {
                    "start": "2024-01-01",
                    "end": "2024-01-31"
                },
                "severity": ["high", "critical"],
                "source": ["system", "application"]
            }
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "results" in data 