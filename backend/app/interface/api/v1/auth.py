from fastapi import APIRouter, HTTPException, Depends, Response
from app.application.user.dto import UserRegisterDTO
from app.application.user.service import UserApplicationService
from app.infrastructure.cache import cache
from app.infrastructure.captcha import captcha_generator

@router.post("/register")
async def register(
    data: UserRegisterDTO,
    user_service: UserApplicationService = Depends()
):
    """用户注册"""
    # 验证验证码
    cached_code = await cache.get(f"captcha:{data.captcha}")
    if not cached_code or cached_code != data.captcha:
        raise HTTPException(status_code=400, detail="验证码错误")
    
    # 删除验证码缓存
    await cache.delete(f"captcha:{data.captcha}")
    
    # 注册用户
    try:
        await user_service.register(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    return {"message": "注册成功"} 

@router.get("/captcha")
async def get_captcha():
    """生成验证码"""
    code, image = captcha_generator.generate()
    # 存储验证码到缓存
    await cache.set(f"captcha:{code}", code, expire=300)
    return Response(content=image, media_type="image/png")

@router.post("/verify-email")
async def verify_email(email: str):
    """验证邮箱是否可用"""
    is_available = await user_service.check_email_available(email)
    return {"available": is_available}

@router.post("/verify-username")
async def verify_username(username: str):
    """验证用户名是否可用"""
    is_available = await user_service.check_username_available(username)
    return {"available": is_available} 