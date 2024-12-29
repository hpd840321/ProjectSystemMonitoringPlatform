#!/bin/bash

# 运行测试
pytest tests/ -v --cov=app --cov-report=term-missing 