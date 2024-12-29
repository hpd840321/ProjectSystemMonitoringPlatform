from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.quota import ProjectQuota, ResourceUsage
from app.interface.api.v1.schemas.quota import QuotaCreate, QuotaUpdate

class CRUDQuota:
    def get(self, db: Session, id: int) -> Optional[ProjectQuota]:
        return db.query(ProjectQuota).filter(ProjectQuota.id == id).first()

    def get_by_project_and_type(
        self, db: Session, *, project_id: int, resource_type: str
    ) -> Optional[ProjectQuota]:
        return db.query(ProjectQuota).filter(
            and_(
                ProjectQuota.project_id == project_id,
                ProjectQuota.resource_type == resource_type
            )
        ).first()

    def get_multi_by_project(
        self, db: Session, *, project_id: int
    ) -> List[ProjectQuota]:
        return db.query(ProjectQuota).filter(
            ProjectQuota.project_id == project_id
        ).all()

    def create(self, db: Session, *, obj_in: QuotaCreate) -> ProjectQuota:
        db_obj = ProjectQuota(
            project_id=obj_in.project_id,
            resource_type=obj_in.resource_type,
            quota_limit=obj_in.quota_limit,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: ProjectQuota, obj_in: QuotaUpdate
    ) -> ProjectQuota:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def check_quota(
        self, db: Session, *, project_id: int, resource_type: str, amount: int
    ) -> bool:
        """检查资源使用是否超出配额"""
        quota = self.get_by_project_and_type(
            db, project_id=project_id, resource_type=resource_type
        )
        if not quota:
            return False
        return quota.used_amount + amount <= quota.quota_limit

    def record_usage(
        self, db: Session, *, project_id: int, resource_type: str, 
        amount: int, operation: str
    ) -> ResourceUsage:
        """记录资源使用情况"""
        usage = ResourceUsage(
            project_id=project_id,
            resource_type=resource_type,
            amount=amount,
            operation=operation
        )
        db.add(usage)
        
        # 更新配额使用量
        quota = self.get_by_project_and_type(
            db, project_id=project_id, resource_type=resource_type
        )
        if quota:
            if operation == "increase":
                quota.used_amount += amount
            elif operation == "decrease":
                quota.used_amount = max(0, quota.used_amount - amount)
            db.add(quota)
            
        db.commit()
        return usage

quota = CRUDQuota() 