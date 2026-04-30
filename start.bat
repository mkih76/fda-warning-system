@echo off
chcp 65001 >nul
title FDA 警告信系统 - 本地启动

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║           FDA 警告信智能平台 - 本地测试                   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo [步骤 1/4] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到 Python！
    echo 请先安装 Python 3.10+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python 已安装

echo.
echo [步骤 2/4] 检查 Node.js 环境...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到 Node.js！
    echo 请先安装 Node.js 18+
    echo 下载地址：https://nodejs.org/
    pause
    exit /b 1
)
echo ✅ Node.js 已安装

echo.
echo [步骤 3/4] 启动后端服务...
echo 正在启动后端，请稍候...
cd backend

:: 创建虚拟环境（如果不存在）
if not exist ".venv" (
    echo 创建 Python 虚拟环境...
    python -m venv .venv
)

:: 激活虚拟环境
call .venv\Scripts\activate.bat

:: 安装依赖（如果需要）
if not exist ".venv\Lib\site-packages\fastapi" (
    echo 安装 Python 依赖（首次运行需要几分钟）...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
)

:: 创建数据目录
if not exist "..\data" mkdir "..\data"

:: 启动后端（新窗口）
echo 启动后端服务...
start "FDA 后端服务" cmd /k "cd /d %cd% && .venv\Scripts\activate.bat && uvicorn app.main:app --reload --host 0.0.0.0 --port 8790"

:: 等待后端启动
echo 等待后端服务启动...
timeout /t 5 /nobreak >nul

cd ..

echo.
echo [步骤 4/4] 启动前端服务...
cd frontend

:: 安装依赖（如果需要）
if not exist "node_modules" (
    echo 安装前端依赖（首次运行需要几分钟）...
    npm install
)

:: 启动前端（新窗口）
echo 启动前端服务...
start "FDA 前端服务" cmd /k "cd /d %cd% && npm run dev"

cd ..

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                    ✅ 启动完成！                          ║
echo ╠════════════════════════════════════════════════════════════╣
echo ║                                                            ║
echo ║   🌐 网站地址：http://localhost:5173                      ║
echo ║                                                            ║
echo ║   📊 后端 API：http://localhost:8790                      ║
echo ║   📖 API 文档：http://localhost:8790/docs                 ║
echo ║                                                            ║
echo ║   💡 提示：                                               ║
echo ║   - 两个命令行窗口会自动打开                               ║
echo ║   - 关闭这两个窗口即可停止服务                             ║
echo ║   - 首次启动会自动安装依赖，请耐心等待                     ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo 正在打开浏览器...
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo.
echo 按任意键退出此窗口（服务会继续运行）...
pause >nul
