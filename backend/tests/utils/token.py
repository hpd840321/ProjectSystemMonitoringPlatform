from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

def create_test_token(user_id: str, is_admin: bool = False) -> str:
    """创建测试用token"""
    expire = datetime.utcnow() + timedelta(minutes=15)
    data = {
        "sub": user_id,
        "exp": expire,
        "is_admin": is_admin
    }
    return jwt.encode(
        data,
        settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm
    )

@pytest.fixture
def admin_token():
    """管理员token"""
    return create_test_token("admin_id", is_admin=True)

@pytest.fixture
def normal_token():
    """普通用户token"""
    return create_test_token("user_id", is_admin=False) 