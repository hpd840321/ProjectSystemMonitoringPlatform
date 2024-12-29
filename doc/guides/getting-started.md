# 快速入门指南

## 系统要求

- Python 3.8+
- PostgreSQL 12+
- Redis 6+

## 安装

1. 克隆代码仓库
```bash
git clone https://github.com/your-org/ops-platform.git
cd ops-platform
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，配置数据库等信息
```

5. 初始化数据库
```bash
alembic upgrade head
```

6. 启动服务
```bash
uvicorn app.main:app --reload
```

## 基本使用

1. 创建管理员账号
```bash
python scripts/create_admin.py
```

2. 访问系统
- API文档: http://localhost:8000/docs
- 管理界面: http://localhost:8000

3. 添加服务器
- 登录系统
- 进入服务器管理页面
- 点击"添加服务器"
- 填写服务器信息并保存

4. 配置监控
- 进入监控配置页面
- 添加监控项
- 设置告警规则

5. 查看仪表盘
- 进入仪表盘页面
- 查看系统整体状况
- 查看各项监控指标

## 常见问题

1. 数据库连接失败
- 检查数据库服务是否启动
- 检查数据库连接信息是否正确
- 检查数据库用户权限

2. Agent连接失败
- 检查网络连接
- 检查Agent配置
- 检查防火墙设置

3. 告警未触发
- 检查告警规则配置
- 检查监控数据是否正常采集
- 检查通知渠道配置

## 下一步

- 阅读[完整文档](../README.md)
- 了解[系统架构](../architecture.md)
- 查看[API文档](../api/README.md)
- 参考[最佳实践](../best-practices.md) 