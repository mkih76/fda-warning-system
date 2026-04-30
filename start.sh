#!/bin/bash

# FDA 警告信系统 - 一键启动脚本 (Mac/Linux)

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║           FDA 警告信智能平台 - 本地测试                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 检查 Python
echo -e "${BLUE}[步骤 1/4]${NC} 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误：未找到 Python3！${NC}"
    echo "请先安装 Python 3.10+"
    echo "Mac: brew install python"
    echo "Ubuntu: sudo apt install python3 python3-venv"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1)
echo -e "${GREEN}✅ Python 已安装: $PYTHON_VERSION${NC}"

# 检查 Node.js
echo ""
echo -e "${BLUE}[步骤 2/4]${NC} 检查 Node.js 环境..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ 错误：未找到 Node.js！${NC}"
    echo "请先安装 Node.js 18+"
    echo "Mac: brew install node"
    echo "Ubuntu: curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt install nodejs"
    exit 1
fi
NODE_VERSION=$(node --version)
echo -e "${GREEN}✅ Node.js 已安装: $NODE_VERSION${NC}"

# 启动后端
echo ""
echo -e "${BLUE}[步骤 3/4]${NC} 启动后端服务..."
cd backend

# 创建虚拟环境
if [ ! -d ".venv" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv .venv
fi

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
if [ ! -d ".venv/lib/python*/site-packages/fastapi" ]; then
    echo -e "${YELLOW}安装 Python 依赖（首次运行需要几分钟）...${NC}"
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
fi

# 创建数据目录
mkdir -p ../data

# 启动后端（后台运行）
echo "启动后端服务..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8790 &
BACKEND_PID=$!

# 等待后端启动
echo "等待后端服务启动..."
sleep 3

cd ..

# 启动前端
echo ""
echo -e "${BLUE}[步骤 4/4]${NC} 启动前端服务..."
cd frontend

# 安装依赖
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}安装前端依赖（首次运行需要几分钟）...${NC}"
    npm install
fi

# 启动前端
echo "启动前端服务..."
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    ✅ 启动完成！                          ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║                                                            ║"
echo "║   🌐 网站地址：http://localhost:5173                      ║"
echo "║                                                            ║"
echo "║   📊 后端 API：http://localhost:8790                      ║"
echo "║   📖 API 文档：http://localhost:8790/docs                 ║"
echo "║                                                            ║"
echo "║   💡 提示：                                               ║"
echo "║   - 服务正在后台运行                                      ║"
echo "║   - 按 Ctrl+C 停止所有服务                                ║"
echo "║   - 首次启动会自动安装依赖，请耐心等待                     ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 打开浏览器
echo -e "${BLUE}正在打开浏览器...${NC}"
sleep 2

# 根据系统打开浏览器
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open http://localhost:5173
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open http://localhost:5173
fi

# 等待用户按 Ctrl+C
echo ""
echo -e "${YELLOW}按 Ctrl+C 停止所有服务...${NC}"
trap "echo ''; echo '正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '✅ 已停止所有服务'; exit 0" INT
wait
