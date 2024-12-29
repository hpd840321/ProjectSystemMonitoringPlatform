from typing import List, Optional, Set
from sqlalchemy.orm import Session
from app.models.permission import Permission, Role
from app.models.user import User
from app.interface.api.v1.schemas.permission import (
    PermissionCreate,
    PermissionUpdate,
    RoleCreate,
    RoleUpdate
)

class CRUDPermission:
    def get(self, db: Session, id: int) -> Optional[Permission]:
        return db.query(Permission).filter(Permission.id == id).first()

    def get_by_code(self, db: Session, code: str) -> Optional[Permission]:
        return db.query(Permission).filter(Permission.code == code).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Permission]:
        return db.query(Permission).offset(skip).limit(limit).all()

    def get_by_module(self, db: Session, module: str) -> List[Permission]:
        return db.query(Permission).filter(Permission.module == module).all()

    def create(self, db: Session, *, obj_in: PermissionCreate) -> Permission:
        db_obj = Permission(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Permission, obj_in: PermissionUpdate
    ) -> Permission:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDRole:
    def get(self, db: Session, id: int) -> Optional[Role]:
        return db.query(Role).filter(Role.id == id).first()

    def get_by_name(self, db: Session, name: str) -> Optional[Role]:
        return db.query(Role).filter(Role.name == name).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Role]:
        return db.query(Role).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: RoleCreate) -> Role:
        # 创建角色
        db_obj = Role(
            name=obj_in.name,
            description=obj_in.description,
            is_system=obj_in.is_system
        )
        
        # 添加权限
        if obj_in.permission_ids:
            permissions = db.query(Permission)\
                           .filter(Permission.id.in_(obj_in.permission_ids))\
                           .all()
            db_obj.permissions = permissions
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Role, obj_in: RoleUpdate
    ) -> Role:
        # 更新基本信息
        update_data = obj_in.dict(exclude={'permission_ids'})
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        # 更新权限
        if obj_in.permission_ids is not None:
            permissions = db.query(Permission)\
                           .filter(Permission.id.in_(obj_in.permission_ids))\
                           .all()
            db_obj.permissions = permissions
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Optional[Role]:
        obj = db.query(Role).get(id)
        if obj and not obj.is_system:  # 不允许删除系统角色
            db.delete(obj)
            db.commit()
        return obj

    def assign_users(
        self, db: Session, *, role_id: int, user_ids: List[int]
    ) -> Role:
        """为角色分配用户"""
        role = self.get(db, id=role_id)
        if not role:
            return None
            
        users = db.query(User).filter(User.id.in_(user_ids)).all()
        role.users = users
        
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

    def get_user_roles(
        self, db: Session, *, user_id: int
    ) -> List[Role]:
        """获取用户的所有角色"""
        user = db.query(User).get(user_id)
        if not user:
            return []
        return user.roles

    def get_user_permissions(
        self, db: Session, *, user_id: int
    ) -> Set[str]:
        """获取用户的所有权限代码"""
        user = db.query(User).get(user_id)
        if not user:
            return set()
            
        if user.is_superuser:
            return {p.code for p in db.query(Permission).all()}
            
        permissions = set()
        for role in user.roles:
            permissions.update(p.code for p in role.permissions)
        return permissions

permission = CRUDPermission()
role = CRUDRole() 