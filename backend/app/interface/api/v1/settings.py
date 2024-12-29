from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.interface.api.v1.dependencies import get_db, get_current_user
from app.interface.api.v1.schemas.settings import (
    SystemSettingCreate,
    SystemSettingUpdate,
    SystemSettingInDB,
    UserPreferenceCreate,
    UserPreferenceUpdate,
    UserPreferenceInDB,
    SMTPConfig,
    PasswordPolicy,
    SessionConfig
)
from app.crud import system_setting, user_preference
from app.models.user import User

router = APIRouter()

# 系统设置接口
@router.get("/system-settings", response_model=Dict[str, Dict[str, Any]])
async def get_system_settings(
    category: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取系统设置"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await system_setting.get_settings_dict(db, category=category)

@router.get("/system-settings/{category}/{key}", response_model=SystemSettingInDB)
async def get_system_setting(
    category: str,
    key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取特定系统设置"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_obj = await system_setting.get_by_key(db, category=category, key=key)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Setting not found")
    return db_obj

@router.put("/system-settings/{category}/{key}", response_model=SystemSettingInDB)
async def update_system_setting(
    category: str,
    key: str,
    setting_in: SystemSettingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新系统设置"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_obj = await system_setting.get_by_key(db, category=category, key=key)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Setting not found")
    
    return await system_setting.update(db, db_obj=db_obj, obj_in=setting_in)

# 用户偏好设置接口
@router.get("/user-preferences", response_model=Dict[str, Any])
async def get_user_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的偏好设置"""
    return await user_preference.get_preferences_dict(db, user_id=current_user.id)

@router.put("/user-preferences/{key}", response_model=UserPreferenceInDB)
async def update_user_preference(
    key: str,
    preference_in: UserPreferenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新用户偏好设置"""
    db_obj = await user_preference.get(db, user_id=current_user.id, key=key)
    if db_obj:
        return await user_preference.update(db, db_obj=db_obj, obj_in=preference_in)
    
    # 如果不存在则创建
    return await user_preference.create(
        db,
        obj_in=UserPreferenceCreate(
            user_id=current_user.id,
            key=key,
            value=preference_in.value
        )
    )

@router.delete("/user-preferences/{key}")
async def delete_user_preference(
    key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除用户偏好设置"""
    await user_preference.delete(db, user_id=current_user.id, key=key)
    return {"msg": "Preference deleted successfully"}

# 特定设置验证接口
@router.post("/system-settings/validate/smtp")
async def validate_smtp_config(
    config: SMTPConfig,
    current_user: User = Depends(get_current_user)
):
    """验证SMTP配置"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # TODO: 实现SMTP连接测试
    return {"msg": "SMTP configuration is valid"}

@router.post("/system-settings/validate/password-policy")
async def validate_password_policy(
    policy: PasswordPolicy,
    current_user: User = Depends(get_current_user)
):
    """验证密码策略"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # TODO: 实现密码策略验证
    return {"msg": "Password policy is valid"} 