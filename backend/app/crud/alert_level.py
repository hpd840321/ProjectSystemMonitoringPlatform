from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.alert_level import AlertLevel
from app.interface.api.v1.schemas.alert_level import AlertLevelCreate, AlertLevelUpdate

class CRUDAlertLevel:
    def get(self, db: Session, id: int) -> Optional[AlertLevel]:
        return db.query(AlertLevel).filter(AlertLevel.id == id).first()

    def get_by_name(self, db: Session, name: str) -> Optional[AlertLevel]:
        return db.query(AlertLevel).filter(AlertLevel.name == name).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[AlertLevel]:
        return db.query(AlertLevel).order_by(AlertLevel.priority).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: AlertLevelCreate) -> AlertLevel:
        db_obj = AlertLevel(
            name=obj_in.name,
            description=obj_in.description,
            color=obj_in.color,
            priority=obj_in.priority
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: AlertLevel, obj_in: AlertLevelUpdate
    ) -> AlertLevel:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Optional[AlertLevel]:
        obj = db.query(AlertLevel).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

alert_level = CRUDAlertLevel() 