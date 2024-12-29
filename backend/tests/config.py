from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent

# 测试配置
TEST_CONFIG = {
    "database": {
        "url": "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db",
        "echo": True
    },
    "redis": {
        "url": "redis://localhost:6379/1"
    },
    "jwt": {
        "secret_key": "test_secret_key",
        "algorithm": "HS256",
        "access_token_expire_minutes": 30
    }
}

# 测试数据配置
TEST_DATA = {
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
        "password": "Admin123456"
    },
    "user": {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Test123456"
    },
    "tenant": {
        "name": "Test Tenant",
        "code": "test"
    }
} 