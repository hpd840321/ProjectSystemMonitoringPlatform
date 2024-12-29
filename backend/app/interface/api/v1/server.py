from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.interface.api.v1.dependencies import get_db
from app.interface.api.v1.schemas.server import (
    ServerCreate, ServerUpdate, ServerInDB,
    ServerGroupCreate, ServerGroupInDB
)

router = APIRouter()

@router.post("/servers", response_model=ServerInDB)
async def create_server(
    server: ServerCreate,
    db: Session = Depends(get_db)
):
    """创建服务器"""
    db_server = await crud.server.create(db, obj_in=server)
    return db_server

@router.get("/servers", response_model=List[ServerInDB])
async def list_servers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取服务器列表"""
    servers = await crud.server.get_multi(db, skip=skip, limit=limit)
    return servers

@router.get("/servers/{server_id}", response_model=ServerInDB)
async def get_server(
    server_id: int,
    db: Session = Depends(get_db)
):
    """获取服务器详情"""
    server = await crud.server.get(db, id=server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server

@router.put("/servers/{server_id}", response_model=ServerInDB)
async def update_server(
    server_id: int,
    server: ServerUpdate,
    db: Session = Depends(get_db)
):
    """更新服务器信息"""
    db_server = await crud.server.get(db, id=server_id)
    if not db_server:
        raise HTTPException(status_code=404, detail="Server not found")
    server = await crud.server.update(db, db_obj=db_server, obj_in=server)
    return server

@router.post("/server-groups", response_model=ServerGroupInDB)
async def create_server_group(
    group: ServerGroupCreate,
    db: Session = Depends(get_db)
):
    """创建服务器分组"""
    return await crud.server_group.create(db, obj_in=group)

@router.get("/server-groups", response_model=List[ServerGroupInDB])
async def list_server_groups(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取服务器分组列表"""
    return await crud.server_group.get_multi(db, skip=skip, limit=limit)

@router.post("/server-groups/{group_id}/servers/{server_id}")
async def add_server_to_group(
    group_id: int,
    server_id: int,
    db: Session = Depends(get_db)
):
    """添加服务器到分组"""
    group = await crud.server_group.add_server_to_group(
        db, group_id=group_id, server_id=server_id
    )
    if not group:
        raise HTTPException(
            status_code=404,
            detail="Server or group not found"
        )
    return {"msg": "Server added to group successfully"}

@router.delete("/server-groups/{group_id}/servers/{server_id}")
async def remove_server_from_group(
    group_id: int,
    server_id: int,
    db: Session = Depends(get_db)
):
    """从分组中移除服务器"""
    group = await crud.server_group.remove_server_from_group(
        db, group_id=group_id, server_id=server_id
    )
    if not group:
        raise HTTPException(
            status_code=404,
            detail="Server or group not found"
        )
    return {"msg": "Server removed from group successfully"}

@router.post("/servers/batch")
async def batch_operation(
    operation: str,
    server_ids: List[int],
    db: Session = Depends(get_db)
):
    """服务器批量操作"""
    if operation not in ["start", "stop", "restart"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid operation"
        )
    
    results = []
    for server_id in server_ids:
        server = await crud.server.get(db, id=server_id)
        if server:
            # 执行具体操作
            result = await execute_server_operation(server, operation)
            results.append({
                "server_id": server_id,
                "success": result
            })
    
    return results 