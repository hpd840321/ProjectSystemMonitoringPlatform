from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.backup import BackupConfig, BackupRecord
from app.interface.api.v1.schemas.backup import (
    BackupConfigCreate,
    BackupConfigUpdate,
    BackupRecordCreate
)

class CRUDBackupConfig:
    def get(self, db: Session, id: int) -> Optional[BackupConfig]:
        return db.query(BackupConfig).filter(BackupConfig.id == id).first()

    def get_by_name(self, db: Session, name: str) -> Optional[BackupConfig]:
        return db.query(BackupConfig).filter(BackupConfig.name == name).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[BackupConfig]:
        return db.query(BackupConfig).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: BackupConfigCreate) -> BackupConfig:
        db_obj = BackupConfig(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: BackupConfig, obj_in: BackupConfigUpdate
    ) -> BackupConfig:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Optional[BackupConfig]:
        obj = db.query(BackupConfig).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def create_record(
        self, db: Session, *, obj_in: BackupRecordCreate
    ) -> BackupRecord:
        db_obj = BackupRecord(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_records(
        self, db: Session, *, config_id: int, skip: int = 0, limit: int = 100
    ) -> List[BackupRecord]:
        return db.query(BackupRecord)\
                .filter(BackupRecord.config_id == config_id)\
                .order_by(BackupRecord.created_at.desc())\
                .offset(skip)\
                .limit(limit)\
                .all()

backup_config = CRUDBackupConfig() 