import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
import jwt

async def test_register(client):
    """测试用户注册"""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com", 
            "password": "Test123456",
            "confirm_password": "Test123456",
            "captcha": "1234"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "注册成功"

async def test_login(client):
    """测试用户登录"""
    # 先注册用户
    await client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test123456",
            "confirm_password": "Test123456", 
            "captcha": "1234"
        }
    )
    
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "Test123456",
            "captcha": "1234"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data 

async def test_get_captcha(client):
    """测试获取验证码"""
    response = await client.get("/api/v1/auth/captcha")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

async def test_verify_email(client):
    """测试邮箱验证"""
    response = await client.post(
        "/api/v1/auth/verify-email",
        json={"email": "test@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "available" in data

async def test_register_invalid_captcha(client):
    """测试无效验证码注册"""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test123456",
            "confirm_password": "Test123456",
            "captcha": "invalid"
        }
    )
    assert response.status_code == 400
    assert "验证码错误" in response.json()["detail"] 

async def test_user_registration_validation(client):
    """测试用户注册验证"""
    # 测试无效用户名
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "a",  # 太短
            "email": "test@example.com",
            "password": "Test123456"
        }
    )
    assert response.status_code == 400
    assert "username" in response.json()["errors"]

    # 测试无效邮箱
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "invalid-email",
            "password": "Test123456"
        }
    )
    assert response.status_code == 400
    assert "email" in response.json()["errors"]

    # 测试弱密码
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "weak"
        }
    )
    assert response.status_code == 400
    assert "password" in response.json()["errors"]

async def test_user_authentication(client):
    """测试用户认证"""
    # 注册用户
    await client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test123456"
        }
    )

    # 测试登录
    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "Test123456"
        }
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert "refresh_token" in login_response.json()

    # 测试无效凭据
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "wrongpass"
        }
    )
    assert response.status_code == 401

async def test_token_refresh(client):
    """测试令牌刷新"""
    # 先登录获取令牌
    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "Test123456"
        }
    )
    refresh_token = login_response.json()["refresh_token"]

    # 使用刷新令牌获取新的访问令牌
    refresh_response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json()

    # 测试过期的刷新令牌
    expired_token = jwt.encode(
        {
            "sub": "testuser",
            "exp": datetime.utcnow() - timedelta(days=1)
        },
        "secret_key",
        algorithm="HS256"
    )
    response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": expired_token}
    )
    assert response.status_code == 401

async def test_password_reset(client):
    """测试密码重置"""
    # 请求密码重置
    reset_request = await client.post(
        "/api/v1/auth/password-reset/request",
        json={"email": "test@example.com"}
    )
    assert reset_request.status_code == 200

    # 获取重置令牌（模拟邮件发送）
    reset_token = "simulated_reset_token"

    # 重置密码
    reset_response = await client.post(
        "/api/v1/auth/password-reset/confirm",
        json={
            "token": reset_token,
            "new_password": "NewTest123456"
        }
    )
    assert reset_response.status_code == 200

    # 使用新密码登录
    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "NewTest123456"
        }
    )
    assert login_response.status_code == 200

async def test_permission_management(client, admin_token):
    """测试权限管理"""
    # 创建角色
    role_response = await client.post(
        "/api/v1/roles",
        json={
            "name": "operator",
            "permissions": ["view_logs", "view_metrics"]
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert role_response.status_code == 200
    role_id = role_response.json()["id"]

    # 分配角色给用户
    assign_response = await client.post(
        "/api/v1/users/testuser/roles",
        json={"role_ids": [role_id]},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert assign_response.status_code == 200

    # 验证权限
    user_token = login_response.json()["access_token"]
    
    # 应该有权限访问日志
    logs_response = await client.get(
        "/api/v1/logs",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert logs_response.status_code == 200

    # 不应该有权限访问管理接口
    admin_response = await client.get(
        "/api/v1/admin/settings",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert admin_response.status_code == 403

async def test_session_management(client):
    """测试会话管理"""
    # 登录创建多个会话
    sessions = []
    for i in range(3):
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser",
                "password": "Test123456",
                "device_info": f"device_{i}"
            }
        )
        sessions.append(login_response.json()["session_id"])

    # 获取活跃会话列表
    sessions_response = await client.get(
        "/api/v1/auth/sessions",
        headers={"Authorization": f"Bearer {login_response.json()['access_token']}"}
    )
    assert sessions_response.status_code == 200
    assert len(sessions_response.json()) == 3

    # 终止特定会话
    revoke_response = await client.post(
        "/api/v1/auth/sessions/revoke",
        json={"session_id": sessions[0]},
        headers={"Authorization": f"Bearer {login_response.json()['access_token']}"}
    )
    assert revoke_response.status_code == 200

    # 终止所有其他会话
    revoke_all_response = await client.post(
        "/api/v1/auth/sessions/revoke-all",
        headers={"Authorization": f"Bearer {login_response.json()['access_token']}"}
    )
    assert revoke_all_response.status_code == 200

async def test_rate_limiting(client):
    """测试速率限制"""
    # 快速发送多个登录请求
    for i in range(10):
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser",
                "password": "wrongpass"
            }
        )
        if i >= 5:  # 假设限制为5次/分钟
            assert response.status_code == 429
            assert "Too many requests" in response.json()["message"]
            break 