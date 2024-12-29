# 服务器监控管理平台文档
Project System Monitoring Platform

## 文档目录

### 1. 用户指南
- [快速入门](guides/getting-started.md)
- [用户手册](guides/user-manual.md)
- [常见问题](guides/faq.md)

### 2. 系统设计
- [系统架构](design/architecture.md)
- [数据模型](design/data-model.md)
- [接口设计](design/api-design.md)
- [Agent设计](design/agent-design.md)

### 3. 开发文档
- [开发环境搭建](development/setup.md)
- [开发规范](development/contributing.md)
- [API文档](api/README.md)
- [后端实现评估](development/backend-implementation.md)

### 4. 运维指南
- [部署指南](operations/deployment.md)
- [监控配置](operations/monitoring.md)
- [故障处理](operations/troubleshooting.md)

## 系统概述

本系统是一个基于项目的服务器监控管理平台，提供以下核心功能：

1. 项目管理
   - 多项目支持
   - 项目资源配额
   - 项目成员管理

2. 服务器监控
   - 实时状态监控
   - 资源使用分析
   - 性能指标趋势

3. 告警管理
   - 自定义告警规则
   - 多级告警策略
   - 灵活通知方式

4. 日志管理
   - 集中日志采集
   - 日志实时分析
   - 历史日志查询

## 技术架构

- 前端：Vue 3 + TypeScript
- 后端：Python + FastAPI
- 数据库：PostgreSQL + TimescaleDB
- 消息队列：RabbitMQ
- 缓存：Redis

## 快速链接

- [API文档](api/README.md)
- [开发指南](development/contributing.md)
- [部署文档](operations/deployment.md) 