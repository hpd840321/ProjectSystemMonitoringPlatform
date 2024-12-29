from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.storage import StoragePolicy, StoragePolicyExecution
from app.interface.api.v1.schemas.storage import (
    StoragePolicyCreate,
    StoragePolicyUpdate
)

class CRUDStoragePolicy:
    def get(self, db: Session, id: int) -> Optional[StoragePolicy]:
        return db.query(StoragePolicy).filter(StoragePolicy.id == id).first()

    def get_by_name(self, db: Session, name: str) -> Optional[StoragePolicy]:
        return db.query(StoragePolicy).filter(StoragePolicy.name == name).first()

    def get_by_type(self, db: Session, data_type: str) -> Optional[StoragePolicy]:
        return db.query(StoragePolicy).filter(
            StoragePolicy.data_type == data_type
        ).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[StoragePolicy]:
        return db.query(StoragePolicy).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: StoragePolicyCreate) -> StoragePolicy:
        db_obj = StoragePolicy(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: StoragePolicy, obj_in: StoragePolicyUpdate
    ) -> StoragePolicy:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def record_execution(
        self, db: Session, *,
        policy_id: int,
        action_type: str,
        status: str,
        affected_rows: Optional[int] = None,
        error_message: Optional[str] = None
    ) -> StoragePolicyExecution:
        execution = StoragePolicyExecution(
            policy_id=policy_id,
            action_type=action_type,
            status=status,
            affected_rows=affected_rows,
            error_message=error_message,
            started_at=datetime.now()
        )
        if status != "running":
            execution.completed_at = datetime.now()
        
        db.add(execution)
        db.commit()
        db.refresh(execution)
        return execution

storage_policy = CRUDStoragePolicy() 