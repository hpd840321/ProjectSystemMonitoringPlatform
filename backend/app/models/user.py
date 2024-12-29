from app.models.permission import user_roles

class User(Base):
    # ... 现有字段 ...

    # 添加角色关联
    roles = relationship(
        "Role",
        secondary=user_roles,
        back_populates="users"
    )

    def has_permission(self, permission_code: str) -> bool:
        """检查用户是否拥有指定权限"""
        if self.is_superuser:
            return True
        return any(
            any(p.code == permission_code for p in role.permissions)
            for role in self.roles
        )

    def has_role(self, role_name: str) -> bool:
        """检查用户是否拥有指定角色"""
        return any(role.name == role_name for role in self.roles) 