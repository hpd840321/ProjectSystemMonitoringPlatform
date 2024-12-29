from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.interface.api.v1.dependencies import get_db
from app.interface.api.v1.schemas.log import (
    LogSourceCreate, LogSourceUpdate, LogSourceInDB,
    LogParseRuleCreate, LogParseRuleUpdate, LogParseRuleInDB,
    LogEntry, LogQuery
)
from app.crud import log_source, log_parse_rule, log

router = APIRouter()

# 日志源管理
@router.post("/log-sources", response_model=LogSourceInDB)
async def create_log_source(
    source_in: LogSourceCreate,
    db: Session = Depends(get_db)
):
    """创建日志源"""
    db_obj = await log_source.get_by_name(db, name=source_in.name)
    if db_obj:
        raise HTTPException(
            status_code=400,
            detail="Log source with this name already exists"
        )
    return await log_source.create(db, obj_in=source_in)

@router.get("/log-sources", response_model=List[LogSourceInDB])
async def list_log_sources(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取日志源列表"""
    return await log_source.get_multi(db, skip=skip, limit=limit)

@router.get("/log-sources/{source_id}", response_model=LogSourceInDB)
async def get_log_source(
    source_id: int,
    db: Session = Depends(get_db)
):
    """获取日志源详情"""
    db_obj = await log_source.get(db, id=source_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Log source not found")
    return db_obj

@router.put("/log-sources/{source_id}", response_model=LogSourceInDB)
async def update_log_source(
    source_id: int,
    source_in: LogSourceUpdate,
    db: Session = Depends(get_db)
):
    """更新日志源"""
    db_obj = await log_source.get(db, id=source_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Log source not found")
    return await log_source.update(db, db_obj=db_obj, obj_in=source_in)

@router.delete("/log-sources/{source_id}")
async def delete_log_source(
    source_id: int,
    db: Session = Depends(get_db)
):
    """删除日志源"""
    db_obj = await log_source.get(db, id=source_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Log source not found")
    await log_source.delete(db, id=source_id)
    return {"msg": "Log source deleted successfully"}

# 日志解析规则管理
@router.post("/log-parse-rules", response_model=LogParseRuleInDB)
async def create_log_parse_rule(
    rule_in: LogParseRuleCreate,
    db: Session = Depends(get_db)
):
    """创建日志解析规则"""
    db_obj = await log_parse_rule.get_by_name(db, name=rule_in.name)
    if db_obj:
        raise HTTPException(
            status_code=400,
            detail="Log parse rule with this name already exists"
        )
    return await log_parse_rule.create(db, obj_in=rule_in)

@router.get("/log-parse-rules", response_model=List[LogParseRuleInDB])
async def list_log_parse_rules(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取日志解析规则列表"""
    return await log_parse_rule.get_multi(db, skip=skip, limit=limit)

@router.put("/log-parse-rules/{rule_id}", response_model=LogParseRuleInDB)
async def update_log_parse_rule(
    rule_id: int,
    rule_in: LogParseRuleUpdate,
    db: Session = Depends(get_db)
):
    """更新日志解析规则"""
    db_obj = await log_parse_rule.get(db, id=rule_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Log parse rule not found")
    return await log_parse_rule.update(db, db_obj=db_obj, obj_in=rule_in)

# 日志查询
@router.post("/logs/search", response_model=List[LogEntry])
async def search_logs(
    query: LogQuery,
    db: Session = Depends(get_db)
):
    """搜索日志"""
    return await log.search(db, query=query)

@router.post("/logs", response_model=LogEntry)
async def create_log(
    log_entry: LogEntry,
    db: Session = Depends(get_db)
):
    """创建日志记录"""
    return await log.create(db, obj_in=log_entry) 