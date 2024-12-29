from typing import List, Optional
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models.audit import AuditLog
from app.interface.api.v1.schemas.audit import AuditLogCreate, AuditLogFilter

class CRUDAuditLog:
    def create(self, db: Session, *, obj_in: AuditLogCreate) -> AuditLog:
        db_obj = AuditLog(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[AuditLog]:
        return db.query(AuditLog).filter(AuditLog.id == id).first()

    def get_multi(
        self,
        db: Session,
        *,
        filter_params: Optional[AuditLogFilter] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        query = db.query(AuditLog)
        
        if filter_params:
            filters = []
            if filter_params.user_id:
                filters.append(AuditLog.user_id == filter_params.user_id)
            if filter_params.username:
                filters.append(AuditLog.username.ilike(f"%{filter_params.username}%"))
            if filter_params.action:
                filters.append(AuditLog.action == filter_params.action)
            if filter_params.resource_type:
                filters.append(AuditLog.resource_type == filter_params.resource_type)
            if filter_params.resource_id:
                filters.append(AuditLog.resource_id == filter_params.resource_id)
            if filter_params.status:
                filters.append(AuditLog.status == filter_params.status)
            if filter_params.start_time:
                filters.append(AuditLog.created_at >= filter_params.start_time)
            if filter_params.end_time:
                filters.append(AuditLog.created_at <= filter_params.end_time)
            
            if filters:
                query = query.filter(and_(*filters))
        
        return query.order_by(AuditLog.created_at.desc())\
                   .offset(skip)\
                   .limit(limit)\
                   .all()

    def get_actions_summary(
        self,
        db: Session,
        *,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[dict]:
        """获取操作统计"""
        query = db.query(
            AuditLog.action,
            AuditLog.status,
            func.count(AuditLog.id).label('count')
        )
        
        if start_time:
            query = query.filter(AuditLog.created_at >= start_time)
        if end_time:
            query = query.filter(AuditLog.created_at <= end_time)
            
        return query.group_by(AuditLog.action, AuditLog.status).all()

audit_log = CRUDAuditLog() 