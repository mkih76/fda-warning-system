#!/bin/bash
# FDA Warning System - 快速启动脚本

set -e

echo "=== FDA Warning System ==="

# 1. 安装后端依赖
echo "[1/4] 安装后端依赖..."
cd /root/fda-warning-system/backend
pip install -q fastapi uvicorn sqlalchemy pydantic httpx openpyxl apscheduler

# 2. 初始化数据库
echo "[2/4] 初始化数据库..."
python3 scripts/init_db.py

# 3. 启动后端
echo "[3/4] 启动 FastAPI 后端..."
nohup uvicorn backend.app.main:app --host 0.0.0.0 --port 8790 > /tmp/fda-backend.log 2>&1 &
echo "PID: $!"
sleep 3

# 4. 验证
echo "[4/4] 验证 API..."
curl -s http://localhost:8790/api/health && echo ""
curl -s http://localhost:8790/api/stats && echo ""

echo ""
echo "✅ FDA Backend 启动完成!"
echo "   API: http://localhost:8790"
echo "   健康检查: http://localhost:8790/api/health"
echo "   日志: /tmp/fda-backend.log"
