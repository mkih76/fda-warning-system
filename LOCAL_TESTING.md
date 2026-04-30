# FDA 警告信系统 - 本地测试指南

## 📋 前置要求

### 必需软件
- **Node.js** 18+ (推荐 20+)
- **Python** 3.10+
- **npm** 或 **yarn**
- **Git**

### 检查版本
```bash
node --version    # 应该 >= 18.0.0
python --version  # 应该 >= 3.10
npm --version     # 应该 >= 9.0.0
git --version     # 任意版本
```

---

## 🚀 快速开始

### 方式一：分别启动（推荐）

#### 1. 克隆项目
```bash
git clone https://github.com/mkih76/fda-warning-system.git
cd fda-warning-system
```

#### 2. 启动后端

**Windows:**
```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 创建数据目录
mkdir ..\data

# 启动后端服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8790
```

**Mac/Linux:**
```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建数据目录
mkdir -p ../data

# 启动后端服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8790
```

后端启动后会显示：
```
INFO:     Uvicorn running on http://0.0.0.0:8790 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

#### 3. 启动前端（新终端窗口）

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端启动后会显示：
```
  VITE v5.x.x  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.x.x:5173/
```

#### 4. 访问网站

打开浏览器访问：**http://localhost:5173**

---

### 方式二：使用 Docker（更简单）

#### 1. 克隆项目
```bash
git clone https://github.com/mkih76/fda-warning-system.git
cd fda-warning-system
```

#### 2. 启动服务
```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f
```

#### 3. 访问网站
- **前端**: http://localhost:5173 (需要单独启动前端)
- **后端 API**: http://localhost:8790

---

## 🔧 详细步骤

### 步骤 1：安装后端依赖

```bash
cd backend

# 创建虚拟环境（推荐）
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# 升级 pip
pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt
```

**常见问题：**

如果 pip 安装慢，使用国内镜像：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 步骤 2：配置后端

后端会自动创建 SQLite 数据库，无需额外配置。

**环境变量（可选）：**
```bash
# 设置 API 密钥（用于 AI 分析功能）
export NVIDIA_API_KEY="your-nvidia-api-key"
export CF_API_KEY="your-cloudflare-api-key"

# Windows PowerShell:
$env:NVIDIA_API_KEY="your-nvidia-api-key"
$env:CF_API_KEY="your-cloudflare-api-key"
```

### 步骤 3：启动后端

```bash
# 确保在 backend 目录下，且虚拟环境已激活
cd backend

# 启动开发服务器（带热重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8790

# 或者指定更详细的日志
uvicorn app.main:app --reload --host 0.0.0.0 --port 8790 --log-level debug
```

**验证后端启动：**
```bash
# 测试健康检查接口
curl http://localhost:8790/api/health

# 应该返回：
# {"status":"ok","service":"fda-warning-api"}
```

**API 文档：**
- Swagger UI: http://localhost:8790/docs
- ReDoc: http://localhost:8790/redoc

### 步骤 4：安装前端依赖

```bash
# 新开一个终端窗口
cd frontend

# 安装依赖
npm install

# 如果 npm 慢，使用国内镜像
npm config set registry https://registry.npmmirror.com
npm install
```

### 步骤 5：配置前端

前端会自动连接后端 API（默认 http://localhost:8790）。

**如需修改 API 地址：**

创建 `.env.local` 文件：
```bash
# frontend/.env.local
VITE_API_BASE_URL=http://localhost:8790
```

### 步骤 6：启动前端

```bash
cd frontend

# 启动开发服务器
npm run dev

# 或者指定端口
npm run dev -- --port 5173
```

**访问地址：**
- 本地: http://localhost:5173
- 局域网: http://你的IP:5173

---

## 🧪 测试功能

### 1. 测试首页
- 访问 http://localhost:5173
- 检查 Hero Section 是否显示
- 测试导航链接
- 测试暗色模式切换

### 2. 测试列表页
- 访问 http://localhost:5173/#/letters
- 测试搜索功能
- 测试筛选器
- 测试收藏功能
- 测试 CSV 导出

### 3. 测试详情页
- 点击任意警告信卡片
- 检查 AI 分析是否显示
- 测试收藏按钮
- 测试返回按钮

### 4. 测试数据看板
- 访问 http://localhost:5173/#/dashboard
- 检查图表是否渲染
- 测试图表交互

### 5. 测试收藏功能
- 收藏几封警告信
- 访问 http://localhost:5173/#/favorites
- 检查收藏列表

---

## 🐛 常见问题

### 1. Python 虚拟环境问题

**问题**: `python -m venv .venv` 失败
**解决**:
```bash
# Windows
python -m venv .venv --clear

# 或者使用 conda
conda create -n fda python=3.10
conda activate fda
```

### 2. pip 安装依赖失败

**问题**: 网络超时
**解决**:
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或者阿里云镜像
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### 3. 端口被占用

**问题**: `Address already in use`
**解决**:
```bash
# 查找占用端口的进程
# Windows
netstat -ano | findstr :8790
# 杀掉进程
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :8790
kill -9 <PID>

# 或者使用其他端口
uvicorn app.main:app --reload --port 8791
```

然后修改前端 API 地址：
```bash
# frontend/.env.local
VITE_API_BASE_URL=http://localhost:8791
```

### 4. npm install 失败

**问题**: 网络问题
**解决**:
```bash
# 使用国内镜像
npm config set registry https://registry.npmmirror.com

# 清除缓存
npm cache clean --force

# 删除 node_modules 重试
rm -rf node_modules package-lock.json
npm install
```

### 5. 前端无法连接后端

**问题**: CORS 错误或连接失败
**检查**:
1. 后端是否运行：http://localhost:8790/api/health
2. 前端配置是否正确：检查 `.env.local`
3. 浏览器控制台错误信息

**解决**:
```bash
# 确保后端启动
curl http://localhost:8790/api/health

# 检查前端配置
cat frontend/.env.local

# 重启前端
cd frontend
npm run dev
```

### 6. 数据库问题

**问题**: 表不存在
**解决**:
```bash
# 删除旧数据库
rm -f data/fda_warning.db

# 重启后端，会自动创建新数据库
cd backend
uvicorn app.main:app --reload --port 8790
```

### 7. 图表不显示

**问题**: Chart.js 错误
**解决**:
```bash
# 清除浏览器缓存
# 或者强制刷新
Ctrl + Shift + R (Windows/Linux)
Cmd + Shift + R (Mac)
```

---

## 📦 项目结构

```
fda-warning-system/
├── backend/              # 后端 (FastAPI)
│   ├── app/
│   │   ├── main.py      # API 入口
│   │   ├── models.py    # 数据模型
│   │   ├── database.py  # 数据库配置
│   │   └── routers/     # API 路由
│   ├── requirements.txt # Python 依赖
│   └── .venv/           # 虚拟环境（自动生成）
│
├── frontend/             # 前端 (Vue 3)
│   ├── src/
│   │   ├── views/       # 页面组件
│   │   ├── components/  # 通用组件
│   │   ├── composables/ # 组合式函数
│   │   ├── styles/      # 样式文件
│   │   └── router/      # 路由配置
│   ├── package.json     # npm 依赖
│   └── dist/            # 构建产物（自动生成）
│
├── data/                 # 数据目录
│   └── fda_warning.db   # SQLite 数据库（自动生成）
│
└── docker-compose.yml    # Docker 配置
```

---

## 🔨 开发命令

### 后端命令

```bash
# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8790

# 运行测试
python -m pytest

# 代码格式化
black app/
isort app/

# 类型检查
mypy app/
```

### 前端命令

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview

# 代码检查
npm run lint

# 代码格式化
npm run format
```

---

## 🌐 API 端点

### 基础 API

- `GET /api/health` - 健康检查
- `GET /api/stats` - 统计数据
- `GET /api/letters` - 警告信列表
- `GET /api/letters/:id` - 警告信详情
- `GET /api/offices` - 办公室列表
- `GET /api/violation-types` - 违规类型
- `GET /api/search/suggestions` - 搜索建议
- `GET /api/letters/export/csv` - 导出 CSV

### Dashboard API

- `GET /api/dashboard/summary` - 摘要统计
- `GET /api/dashboard/monthly` - 月度数据
- `GET /api/dashboard/top-companies` - 高风险企业

### 文章 API

- `GET /api/articles` - 文章列表
- `GET /api/articles/:id` - 文章详情

---

## 🎯 快速测试清单

- [ ] 后端启动成功（http://localhost:8790/api/health 返回 ok）
- [ ] 前端启动成功（http://localhost:5173 可访问）
- [ ] 首页显示正常（Hero、功能、统计数据）
- [ ] 列表页加载数据（显示警告信卡片）
- [ ] 搜索功能正常（输入关键词搜索）
- [ ] 筛选功能正常（选择办公室、状态等）
- [ ] 详情页显示正常（AI 分析、违规项、译文）
- [ ] 收藏功能正常（点击收藏、查看收藏列表）
- [ ] 数据看板正常（图表渲染）
- [ ] 暗色模式正常（切换主题）
- [ ] 响应式正常（调整浏览器窗口大小）
- [ ] CSV 导出正常（点击导出按钮）

---

## 🚀 部署到生产环境

测试完成后，可以部署到 VPS：

```bash
# 1. 构建前端
cd frontend
npm run build

# 2. 部署到 VPS
./deploy.sh

# 或者手动部署
scp -r dist/* user@your-vps:/root/fda-warning-system/frontend/
ssh user@your-vps "cd /root/fda-warning-system && docker-compose restart"
```

---

## 📞 获取帮助

如果遇到问题：

1. **查看日志**：
   - 后端：终端输出
   - 前端：浏览器控制台 (F12)

2. **检查端口**：
   ```bash
   # Windows
   netstat -ano | findstr :8790
   netstat -ano | findstr :5173
   
   # Mac/Linux
   lsof -i :8790
   lsof -i :5173
   ```

3. **重启服务**：
   ```bash
   # 停止所有服务
   Ctrl + C (在运行服务的终端)
   
   # 重新启动
   cd backend && uvicorn app.main:app --reload --port 8790
   cd frontend && npm run dev
   ```

4. **清除缓存**：
   ```bash
   # 后端
   rm -f data/fda_warning.db
   
   # 前端
   cd frontend
   rm -rf node_modules dist .vite
   npm install
   npm run dev
   ```

---

## ✨ 提示

1. **热重载**：开发模式下，修改代码会自动重新加载
2. **API 文档**：访问 http://localhost:8790/docs 查看完整 API 文档
3. **数据库**：SQLite 数据库文件在 `data/fda_warning.db`
4. **日志**：后端日志会显示在终端，前端错误在浏览器控制台
5. **网络**：确保 8790 和 5173 端口未被占用

---

**祝你测试顺利！** 🎉
