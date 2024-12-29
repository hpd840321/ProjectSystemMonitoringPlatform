from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy import and_, or_, text
from sqlalchemy.orm import Session
from app.models.log import LogSource, LogParseRule, Log
from app.interface.api.v1.schemas.log import (
    LogSourceCreate, LogSourceUpdate,
    LogParseRuleCreate, LogParseRuleUpdate,
    LogEntry, LogQuery
)

class CRUDLogSource:
    def get(self, db: Session, id: int) -> Optional[LogSource]:
        return db.query(LogSource).filter(LogSource.id == id).first()

    def get_by_name(self, db: Session, name: str) -> Optional[LogSource]:
        return db.query(LogSource).filter(LogSource.name == name).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[LogSource]:
        return db.query(LogSource).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: LogSourceCreate) -> LogSource:
        db_obj = LogSource(
            name=obj_in.name,
            type=obj_in.type,
            config=obj_in.config,
            enabled=obj_in.enabled
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: LogSource, obj_in: LogSourceUpdate
    ) -> LogSource:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Optional[LogSource]:
        obj = db.query(LogSource).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

class CRUDLogParseRule:
    def get(self, db: Session, id: int) -> Optional[LogParseRule]:
        return db.query(LogParseRule).filter(LogParseRule.id == id).first()

    def get_by_name(self, db: Session, name: str) -> Optional[LogParseRule]:
        return db.query(LogParseRule).filter(LogParseRule.name == name).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[LogParseRule]:
        return db.query(LogParseRule).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: LogParseRuleCreate) -> LogParseRule:
        db_obj = LogParseRule(
            name=obj_in.name,
            pattern=obj_in.pattern,
            fields=obj_in.fields,
            sample=obj_in.sample,
            enabled=obj_in.enabled
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: LogParseRule, obj_in: LogParseRuleUpdate
    ) -> LogParseRule:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Optional[LogParseRule]:
        obj = db.query(LogParseRule).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

class CRUDLog:
    def create(self, db: Session, *, obj_in: LogEntry) -> Log:
        db_obj = Log(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def search(
        self, db: Session, *, query: LogQuery
    ) -> List[Log]:
        filters = []
        
        if query.start_time:
            filters.append(Log.timestamp >= query.start_time)
        if query.end_time:
            filters.append(Log.timestamp <= query.end_time)
        if query.source_ids:
            filters.append(Log.source_id.in_(query.source_ids))
        if query.levels:
            filters.append(Log.level.in_(query.levels))
        if query.search_text:
            filters.append(Log.message.ilike(f"%{query.search_text}%"))
        if query.field_filters:
            for field, value in query.field_filters.items():
                filters.append(
                    text(f"parsed_fields->'{field}' = '{value}'::jsonb")
                )

        base_query = db.query(Log)
        if filters:
            base_query = base_query.filter(and_(*filters))
        
        return base_query.order_by(Log.timestamp.desc())\
                        .offset(query.offset)\
                        .limit(query.limit)\
                        .all()

log_source = CRUDLogSource()
log_parse_rule = CRUDLogParseRule()
log = CRUDLog() 