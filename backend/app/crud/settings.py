from typing import List, Optional, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.settings import SystemSetting, UserPreference
from app.interface.api.v1.schemas.settings import (
    SystemSettingCreate,
    SystemSettingUpdate,
    UserPreferenceCreate,
    UserPreferenceUpdate
)

class CRUDSystemSetting:
    def get(self, db: Session, id: int) -> Optional[SystemSetting]:
        return db.query(SystemSetting).filter(SystemSetting.id == id).first()

    def get_by_key(
        self, db: Session, *, category: str, key: str
    ) -> Optional[SystemSetting]:
        return db.query(SystemSetting).filter(
            and_(
                SystemSetting.category == category,
                SystemSetting.key == key
            )
        ).first()

    def get_by_category(
        self, db: Session, *, category: str
    ) -> List[SystemSetting]:
        return db.query(SystemSetting)\
                .filter(SystemSetting.category == category)\
                .all()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[SystemSetting]:
        return db.query(SystemSetting).offset(skip).limit(limit).all()

    def create(
        self, db: Session, *, obj_in: SystemSettingCreate
    ) -> SystemSetting:
        db_obj = SystemSetting(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: SystemSetting, obj_in: SystemSettingUpdate
    ) -> SystemSetting:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_settings_dict(
        self, db: Session, *, category: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取设置字典"""
        query = db.query(SystemSetting)
        if category:
            query = query.filter(SystemSetting.category == category)
        
        settings = {}
        for setting in query.all():
            if setting.category not in settings:
                settings[setting.category] = {}
            settings[setting.category][setting.key] = setting.value
        return settings

class CRUDUserPreference:
    def get(
        self, db: Session, *, user_id: int, key: str
    ) -> Optional[UserPreference]:
        return db.query(UserPreference).filter(
            and_(
                UserPreference.user_id == user_id,
                UserPreference.key == key
            )
        ).first()

    def get_multi_by_user(
        self, db: Session, *, user_id: int
    ) -> List[UserPreference]:
        return db.query(UserPreference)\
                .filter(UserPreference.user_id == user_id)\
                .all()

    def create(
        self, db: Session, *, obj_in: UserPreferenceCreate
    ) -> UserPreference:
        db_obj = UserPreference(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: UserPreference, obj_in: UserPreferenceUpdate
    ) -> UserPreference:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(
        self, db: Session, *, user_id: int, key: str
    ) -> Optional[UserPreference]:
        obj = self.get(db, user_id=user_id, key=key)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def get_preferences_dict(
        self, db: Session, *, user_id: int
    ) -> Dict[str, Any]:
        """获取用户偏好设置字典"""
        preferences = {}
        for pref in self.get_multi_by_user(db, user_id=user_id):
            preferences[pref.key] = pref.value
        return preferences

system_setting = CRUDSystemSetting()
user_preference = CRUDUserPreference() 