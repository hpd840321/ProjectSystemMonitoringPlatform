class UserNotFoundError(ValueError):
    """用户不存在异常"""
    pass

class InvalidPasswordError(ValueError):
    """密码错误异常"""
    pass

class UserAlreadyExistsError(ValueError):
    """用户已存在异常"""
    pass

class InvalidRoleError(ValueError):
    """无效角色异常"""
    pass 