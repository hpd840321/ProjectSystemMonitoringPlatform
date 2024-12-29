#!/bin/bash

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 打印带颜色的消息
print_message() {
    echo -e "${2}${1}${NC}"
}

# 检查命令执行结果
check_result() {
    if [ $? -eq 0 ]; then
        print_message "$1 成功" "${GREEN}"
    else
        print_message "$1 失败" "${RED}"
        exit 1
    fi
}

# 运行后端测试
run_backend_tests() {
    print_message "开始运行后端测试..." "${YELLOW}"
    
    cd backend
    
    # 安装开发依赖
    pip install -r requirements-dev.txt
    check_result "安装后端依赖"
    
    # 运行单元测试并生成覆盖率报告
    pytest tests/ \
        --cov=app \
        --cov-report=term-missing \
        --cov-report=html:coverage_report \
        -v
    check_result "后端单元测试"
    
    # 检查测试覆盖率
    coverage_result=$(coverage report | grep TOTAL | awk '{print $4}' | sed 's/%//')
    if (( $(echo "$coverage_result < 85" | bc -l) )); then
        print_message "测试覆盖率($coverage_result%)低于要求的85%" "${RED}"
        exit 1
    else
        print_message "测试覆盖率: $coverage_result%" "${GREEN}"
    fi
    
    cd ..
}

# 运行前端测试
run_frontend_tests() {
    print_message "开始运行前端测试..." "${YELLOW}"
    
    cd frontend
    
    # 安装依赖
    npm install
    check_result "安装前端依赖"
    
    # 运行单元测试并生成覆盖率报告
    npm run test:unit -- --coverage
    check_result "前端单元测试"
    
    # 检查测试覆盖率
    coverage_result=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
    if (( $(echo "$coverage_result < 85" | bc -l) )); then
        print_message "测试覆盖率($coverage_result%)低于要求的85%" "${RED}"
        exit 1
    else
        print_message "测试覆盖率: $coverage_result%" "${GREEN}"
    fi
    
    cd ..
}

# 运行E2E测试
run_e2e_tests() {
    print_message "开始运行E2E测试..." "${YELLOW}"
    
    cd frontend
    
    # 启动测试服务器
    npm run serve:test &
    SERVER_PID=$!
    
    # 等待服务器启动
    sleep 10
    
    # 运行E2E测试
    npm run test:e2e
    E2E_RESULT=$?
    
    # 关闭测试服务器
    kill $SERVER_PID
    
    if [ $E2E_RESULT -eq 0 ]; then
        print_message "E2E测试成功" "${GREEN}"
    else
        print_message "E2E测试失败" "${RED}"
        exit 1
    fi
    
    cd ..
}

# 主函数
main() {
    # 清理之前的测试结果
    rm -rf backend/coverage_report frontend/coverage
    
    # 运行所有测试
    run_backend_tests
    run_frontend_tests
    run_e2e_tests
    
    print_message "所有测试完成!" "${GREEN}"
}

# 执行主函数
main 