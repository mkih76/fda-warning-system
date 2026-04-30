#!/bin/bash
# PharmaCos Insight - Deploy Script
# Run on VPS: cd /root/fda-warning-system && bash deploy.sh

set -e

echo "═══════════════════════════════════════"
echo "  PharmaCos Insight 部署脚本"
echo "═══════════════════════════════════════"

# Navigate to project root
cd "$(dirname "$0")"

echo ""
echo "[1/5] 拉取最新代码..."
git pull origin main

echo ""
echo "[2/5] 安装前端依赖..."
cd frontend && npm install

echo ""
echo "[3/5] 构建前端..."
npm run build
cd ..

echo ""
echo "[4/5] 安装后端依赖..."
pip install -r backend/requirements.txt

echo ""
echo "[5/5] 重启 Docker 容器..."
docker-compose down
docker-compose up -d --build

echo ""
echo "═══════════════════════════════════════"
echo "  部署完成！"
echo "═══════════════════════════════════════"

# Health check
sleep 3
echo ""
echo "健康检查:"
curl -s http://localhost:8790/api/health && echo ""

echo ""
echo "[可选] 初始化种子数据（分类+示例文章）:"
echo "  docker exec fda-warning-backend python -m backend.scripts.seed_data"
