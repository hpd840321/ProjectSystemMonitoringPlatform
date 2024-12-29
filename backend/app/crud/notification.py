from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.notification import (
    NotificationChannel,
    NotificationTemplate,
    NotificationLog
)
from app.interface.api.v1.schemas.notification import (
    NotificationChannelCreate,
    NotificationChannelUpdate,
    NotificationTemplateCreate,
    NotificationTemplateUpdate,
    NotificationLogCreate
)

class CRUDNotificationChannel:
    def get(self, db: Session, id: int) -> Optional[NotificationChannel]:
        return db.query(NotificationChannel).filter(NotificationChannel.id == id).first()

    def get_by_name(self, db: Session, name: str) -> Optional[NotificationChannel]:
        return db.query(NotificationChannel)\
                .filter(NotificationChannel.name == name)\
                .first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[NotificationChannel]:
        return db.query(NotificationChannel)\
                .offset(skip)\
                .limit(limit)\
                .all()

    def get_enabled(self, db: Session) -> List[NotificationChannel]:
        """获取所有启用的通知渠道"""
        return db.query(NotificationChannel)\
                .filter(NotificationChannel.enabled == True)\
                .all()

    def create(
        self, db: Session, *, obj_in: NotificationChannelCreate
    ) -> NotificationChannel:
        db_obj = NotificationChannel(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: NotificationChannel,
        obj_in: NotificationChannelUpdate
    ) -> NotificationChannel:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Optional[NotificationChannel]:
        obj = db.query(NotificationChannel).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

class CRUDNotificationTemplate:
    def get(self, db: Session, id: int) -> Optional[NotificationTemplate]:
        return db.query(NotificationTemplate)\
                .filter(NotificationTemplate.id == id)\
                .first()

    def get_by_name(self, db: Session, name: str) -> Optional[NotificationTemplate]:
        return db.query(NotificationTemplate)\
                .filter(NotificationTemplate.name == name)\
                .first()

    def get_by_type(
        self, db: Session, type: str
    ) -> List[NotificationTemplate]:
        return db.query(NotificationTemplate)\
                .filter(NotificationTemplate.type == type)\
                .all()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[NotificationTemplate]:
        return db.query(NotificationTemplate)\
                .offset(skip)\
                .limit(limit)\
                .all()

    def create(
        self, db: Session, *, obj_in: NotificationTemplateCreate
    ) -> NotificationTemplate:
        db_obj = NotificationTemplate(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: NotificationTemplate,
        obj_in: NotificationTemplateUpdate
    ) -> NotificationTemplate:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Optional[NotificationTemplate]:
        obj = db.query(NotificationTemplate).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

class CRUDNotificationLog:
    def get(self, db: Session, id: int) -> Optional[NotificationLog]:
        return db.query(NotificationLog).filter(NotificationLog.id == id).first()

    def get_multi(
        self, db: Session, *,
        channel_id: Optional[int] = None,
        template_id: Optional[int] = None,
        event_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[NotificationLog]:
        query = db.query(NotificationLog)
        if channel_id:
            query = query.filter(NotificationLog.channel_id == channel_id)
        if template_id:
            query = query.filter(NotificationLog.template_id == template_id)
        if event_type:
            query = query.filter(NotificationLog.event_type == event_type)
        return query.order_by(NotificationLog.created_at.desc())\
                   .offset(skip)\
                   .limit(limit)\
                   .all()

    def create(
        self, db: Session, *, obj_in: NotificationLogCreate
    ) -> NotificationLog:
        db_obj = NotificationLog(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

notification_channel = CRUDNotificationChannel()
notification_template = CRUDNotificationTemplate()
notification_log = CRUDNotificationLog() 