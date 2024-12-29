import pytest
import jwt
from datetime import datetime, timedelta

async def test_sql_injection(client):
    """测试SQL注入防护"""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "' OR '1'='1",
            "password": "' OR '1'='1"
        }
    )
    assert response.status_code == 401

async def test_xss_protection(client, admin_token):
    """测试XSS防护"""
    script_content = "<script>alert('xss')</script>"
    response = await client.post(
        "/api/v1/users",
        json={
            "username": script_content,
            "email": "test@example.com"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 400

async def test_csrf_protection(client, normal_token):
    """测试CSRF防护"""
    # 不带CSRF token的请求应该失败
    response = await client.post(
        "/api/v1/users/me/password",
        json={
            "old_password": "old",
            "new_password": "new"
        },
        headers={
            "Authorization": f"Bearer {normal_token}",
            "X-CSRF-Token": None
        }
    )
    assert response.status_code == 403

async def test_rate_limiting(client):
    """测试请求限流"""
    # 连续发送多个请求
    for _ in range(10):
        await client.post("/api/v1/auth/login", 
            json={
                "username": "test",
                "password": "test"
            }
        )
    
    # 第11个请求应该被限流
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "test",
            "password": "test"
        }
    )
    assert response.status_code == 429 