# 开发指南

## 开发环境设置

1. 克隆代码库
```bash
git clone https://github.com/your-org/project-name.git
cd project-name
```

2. 安装依赖
```bash
# 后端依赖
cd backend
pip install -r requirements.txt

# 前端依赖
cd frontend
npm install
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件配置数据库等信息
```

4. 初始化数据库
```bash
cd backend
alembic upgrade head
```

5. 启动开发服务器
```bash
# 后端服务
cd backend
uvicorn app.main:app --reload

# 前端服务
cd frontend
npm run dev
```

## 代码规范

### Python 代码规范
- 遵循 PEP 8 规范
- 使用 Black 进行代码格式化
- 使用 isort 进行导入排序
- 使用 mypy 进行类型检查

### TypeScript/Vue 代码规范
- 遵循 Vue 3 组合式 API 风格指南
- 使用 ESLint + Prettier 进行代码格式化
- 使用 TypeScript 严格模式

## 提交规范

1. 分支命名
- feature/xxx: 新功能
- fix/xxx: 修复问题
- docs/xxx: 文档更新
- refactor/xxx: 代码重构

2. 提交信息格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

类型(type):
- feat: 新功能
- fix: 修复
- docs: 文档
- style: 格式
- refactor: 重构
- test: 测试
- chore: 构建

## 测试规范

1. 后端测试
- 使用 pytest 编写单元测试
- 测试覆盖率要求 > 80%
- 运行测试: `pytest`

2. 前端测试
- 使用 Vitest 编写单元测试
- 使用 Cypress 编写 E2E 测试
- 运行测试: `npm run test`

## 发布流程

1. 版本号规范
- 遵循语义化版本 2.0.0
- 格式: Major.Minor.Patch

2. 发布步骤
- 更新版本号
- 生成更新日志
- 创建发布标签
- 部署新版本 