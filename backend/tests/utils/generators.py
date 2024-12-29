import random
import string
from datetime import datetime, timedelta

def generate_username():
    """生成随机用户名"""
    return ''.join(random.choices(string.ascii_lowercase, k=8))

def generate_email():
    """生成随机邮箱"""
    username = generate_username()
    domain = ''.join(random.choices(string.ascii_lowercase, k=6))
    return f"{username}@{domain}.com"

def generate_password():
    """生成符合要求的随机密码"""
    lowercase = ''.join(random.choices(string.ascii_lowercase, k=4))
    uppercase = ''.join(random.choices(string.ascii_uppercase, k=2))
    digits = ''.join(random.choices(string.digits, k=2))
    return f"{lowercase}{uppercase}{digits}" 