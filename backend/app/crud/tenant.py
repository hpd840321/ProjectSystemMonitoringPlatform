from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.tenant import Tenant, UserTenant
from app.interface.api.v1.schemas.tenant import (
    TenantCreate,
    TenantUpdate,
    UserTenantCreate,
    UserTenantUpdate
)

class CRUDTenant:
    def get(self, db: Session, id: int) -> Optional[Tenant]:
        return db.query(Tenant).filter(Tenant.id == id).first()

    def get_by_code(self, db: Session, code: str) -> Optional[Tenant]:
        return db.query(Tenant).filter(Tenant.code == code).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Tenant]:
        query = db.query(Tenant)
        if status:
            query = query.filter(Tenant.status == status)
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: TenantCreate) -> Tenant:
        db_obj = Tenant(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Tenant,
        obj_in: TenantUpdate
    ) -> Tenant:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Optional[Tenant]:
        obj = db.query(Tenant).get(id)
        if obj:
            # 标记为删除状态而不是真正删除
            obj.status = "deleted"
            db.add(obj)
            db.commit()
        return obj

    def get_user_tenants(
        self,
        db: Session,
        *,
        user_id: int
    ) -> List[Dict]:
        """获取用户的所有租户"""
        return db.query(UserTenant)\
                .filter(UserTenant.user_id == user_id)\
                .all()

    def add_user_to_tenant(
        self,
        db: Session,
        *,
        obj_in: UserTenantCreate
    ) -> UserTenant:
        """添加用户到租户"""
        db_obj = UserTenant(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_user_role(
        self,
        db: Session,
        *,
        user_id: int,
        tenant_id: int,
        obj_in: UserTenantUpdate
    ) -> Optional[UserTenant]:
        """更新用户在租户中的角色"""
        db_obj = db.query(UserTenant)\
                  .filter(
                      and_(
                          UserTenant.user_id == user_id,
                          UserTenant.tenant_id == tenant_id
                      )
                  )\
                  .first()
        if db_obj:
            db_obj.role = obj_in.role
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def remove_user_from_tenant(
        self,
        db: Session,
        *,
        user_id: int,
        tenant_id: int
    ) -> bool:
        """从租户中移除用户"""
        db_obj = db.query(UserTenant)\
                  .filter(
                      and_(
                          UserTenant.user_id == user_id,
                          UserTenant.tenant_id == tenant_id
                      )
                  )\
                  .first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False

    def get_tenant_stats(
        self,
        db: Session,
        *,
        tenant_id: int
    ) -> Dict:
        """获取租户统计信息"""
        tenant = self.get(db, tenant_id)
        if not tenant:
            return {}

        return {
            "total_users": len(tenant.users),
            "total_projects": len(tenant.projects),
            "total_servers": len(tenant.servers),
            "resource_usage": {
                "users_percent": (len(tenant.users) / tenant.max_users * 100
                                if tenant.max_users else 0),
                "projects_percent": (len(tenant.projects) / tenant.max_projects * 100
                                  if tenant.max_projects else 0),
                "servers_percent": (len(tenant.servers) / tenant.max_servers * 100
                                 if tenant.max_servers else 0)
            }
        }

tenant = CRUDTenant() 