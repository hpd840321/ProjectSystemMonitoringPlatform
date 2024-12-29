#!/bin/bash

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}开始运行测试...${NC}"

# 1. 环境准备
echo -e "${YELLOW}准备测试环境...${NC}"

# 检查并创建测试数据库
echo -e "${YELLOW}准备测试数据库...${NC}"
PGPASSWORD=postgres psql -U postgres -h localhost -c "DROP DATABASE IF EXISTS test_db;"
PGPASSWORD=postgres psql -U postgres -h localhost -c "CREATE DATABASE test_db;"

# 检查Redis服务
echo -e "${YELLOW}检查Redis服务...${NC}"
if ! redis-cli ping > /dev/null 2>&1; then
    echo -e "${RED}Error: Redis服务未运行${NC}"
    exit 1
fi

# 安装依赖和迁移
echo -e "${YELLOW}安装测试依赖...${NC}"
pip install -r requirements-dev.txt

echo -e "${YELLOW}运行数据库迁移...${NC}"
alembic upgrade head

# 2. 运行测试用例
echo -e "${YELLOW}开始运行测试用例...${NC}"

# 2.1 前端组件测试
echo -e "${YELLOW}运行前端组件测试...${NC}"
cd frontend && npm run test:unit && cd ..

# 2.2 后端API测试
echo -e "${YELLOW}运行后端API测试...${NC}"

# 认证与用户管理测试
echo -e "${YELLOW}运行认证与用户管理测试...${NC}"
pytest tests/api/test_auth.py -v --cov=app.interface.api.v1.auth
pytest tests/api/test_user.py -v --cov=app.interface.api.v1.user

# 租户管理测试
echo -e "${YELLOW}运行租户管理测试...${NC}"
pytest tests/api/test_tenant.py -v --cov=app.interface.api.v1.tenant
pytest tests/api/test_tenant_member.py -v --cov=app.interface.api.v1.tenant

# 权限管理测试
echo -e "${YELLOW}运行权限管理测试...${NC}"
pytest tests/api/test_permission.py -v --cov=app.interface.api.v1.permission

# 监控告警测试
echo -e "${YELLOW}运行监控告警测试...${NC}"
pytest tests/api/test_monitor.py -v --cov=app.interface.api.v1.monitor
pytest tests/api/test_alert.py -v --cov=app.interface.api.v1.alert

# 日志管理测试
echo -e "${YELLOW}运行日志管理测试...${NC}"
pytest tests/api/test_log.py -v --cov=app.interface.api.v1.log

# 系统设置测试
echo -e "${YELLOW}运行系统设置测试...${NC}"
pytest tests/api/test_settings.py -v --cov=app.interface.api.v1.settings

# 插件系统测试
echo -e "${YELLOW}运行插件系统测试...${NC}"
pytest tests/api/test_plugin.py -v --cov=app.interface.api.v1.plugin

# 备份恢复测试
echo -e "${YELLOW}运行备份恢复测试...${NC}"
pytest tests/api/test_backup.py -v --cov=app.interface.api.v1.backup

# 任务调度测试
echo -e "${YELLOW}运行任务调度测试...${NC}"
pytest tests/api/test_scheduler.py -v --cov=app.interface.api.v1.scheduler

# 审计日志测试
echo -e "${YELLOW}运行审计日志测试...${NC}"
pytest tests/api/test_audit.py -v --cov=app.interface.api.v1.audit

# API网关测试
echo -e "${YELLOW}运行API网关测试...${NC}"
pytest tests/api/test_api_gateway.py -v --cov=app.interface.api.v1.gateway

# 健康检查测试
echo -e "${YELLOW}运行健康检查测试...${NC}"
pytest tests/api/test_health.py -v --cov=app.interface.api.v1.health

# 系统资源监控测试
echo -e "${YELLOW}运行系统资源监控测试...${NC}"
pytest tests/api/test_system.py -v --cov=app.interface.api.v1.system

# WebSocket测试
echo -e "${YELLOW}运行WebSocket测试...${NC}"
pytest tests/api/test_websocket.py -v --cov=app.interface.api.v1.websocket

# 文件管理测试
echo -e "${YELLOW}运行文件管理测试...${NC}"
pytest tests/api/test_file.py -v --cov=app.interface.api.v1.file

# 数据导入导出测试
echo -e "${YELLOW}运行数据导入导出测试...${NC}"
pytest tests/api/test_data.py -v --cov=app.interface.api.v1.data

# 国际化测试
echo -e "${YELLOW}运行国际化测试...${NC}"
pytest tests/api/test_i18n.py -v --cov=app.interface.api.v1.i18n

# 主题设置测试
echo -e "${YELLOW}运行主题设置测试...${NC}"
pytest tests/api/test_theme.py -v --cov=app.interface.api.v1.theme

# 缓存机制测试
echo -e "${YELLOW}运行缓存机制测试...${NC}"
pytest tests/api/test_cache.py -v --cov=app.interface.api.v1.cache

# 搜索功能测试
echo -e "${YELLOW}运行搜索功能测试...${NC}"
pytest tests/api/test_search.py -v --cov=app.interface.api.v1.search

# 性能测试
echo -e "${YELLOW}运行性能测试...${NC}"
pytest tests/performance/test_performance.py -v

# 安全性测试
echo -e "${YELLOW}运行安全性测试...${NC}"
pytest tests/security/test_security.py -v

# 集成测试
echo -e "${YELLOW}运行集成测试...${NC}"
pytest tests/integration/test_integration.py -v

# 压力测试
echo -e "${YELLOW}运行压力测试...${NC}"
pytest tests/stress/test_stress.py -v

# 数据一致性测试
echo -e "${YELLOW}运行数据一致性测试...${NC}"
pytest tests/consistency/test_consistency.py -v

# 3. 生成测试报告
echo -e "${YELLOW}生成测试报告...${NC}"

# 后端覆盖率报告
coverage html

# 前端覆盖率报告
cd frontend && npm run coverage && cd ..

# 4. 清理环境
echo -e "${YELLOW}清理测试环境...${NC}"
PGPASSWORD=postgres psql -U postgres -h localhost -c "DROP DATABASE IF EXISTS test_db;"

# 5. 测试完成
echo -e "${GREEN}所有测试完成!${NC}"
echo -e "${YELLOW}后端测试报告: backend/htmlcov/index.html${NC}"
echo -e "${YELLOW}前端测试报告: frontend/coverage/lcov-report/index.html${NC}"

# 6. 检查测试结果
if [ $? -eq 0 ]; then
    echo -e "${GREEN}测试全部通过!${NC}"
    exit 0
else
    echo -e "${RED}测试失败!${NC}"
    exit 1
fi 