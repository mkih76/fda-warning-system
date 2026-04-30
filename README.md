# FDA 警告信智能平台

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

一个面向中国制药、化妆品、食品行业的 FDA 警告信智能分析平台。基于 Vue 3 + FastAPI 构建，提供 FDA 警告信翻译、行业法规、新闻聚合、AI 分析和数据可视化功能。

🌐 **在线演示**: https://fda.19990419.top

## ✨ 核心功能

- **警告信数据库**: 986 封 FDA 警告信，100% 翻译为中文
- **AI 智能分析**: 自动提取违规类型、CFR 引用、风险等级
- **数据可视化**: 年度趋势、签发办公室排名、状态分布
- **行业法规**: NMPA/FDA 法规信息聚合
- **行业资讯**: RSS 新闻聚合，40+ 篇行业文章
- **深度内容**: 合规指南、案例研究、趋势分析

## 🏗️ 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite + Chart.js |
| 后端 | FastAPI + SQLAlchemy + SQLite |
| AI | NVIDIA NIM + Cloudflare Workers AI |
| 部署 | Caddy + Cloudflare CDN |

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- npm 或 yarn

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/mkih76/fda-warning-system.git
cd fda-warning-system

# 2. 后端设置
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. 前端设置
cd ../frontend
npm install

# 4. 启动开发服务器
# 终端 1: 后端
cd backend
uvicorn app.main:app --reload --port 8790

# 终端 2: 前端
cd frontend
npm run dev
```

访问 http://localhost:5173

## 📁 项目结构

```
fda-warning-system/
├── backend/              # FastAPI 后端
│   ├── app/
│   │   ├── main.py      # API 入口
│   │   ├── models.py    # 数据模型
│   │   └── static/      # 前端构建产物
│   └── requirements.txt
├── frontend/             # Vue 3 前端
│   ├── src/
│   │   ├── views/       # 页面组件
│   │   ├── components/  # 通用组件
│   │   └── router/      # 路由配置
│   └── package.json
├── content/              # 深度内容文章
│   ├── analysis/        # 深度分析
│   ├── guides/          # 合规指南
│   └── cases/           # 案例研究
├── scripts/              # 工具脚本
│   ├── backup.sh        # 数据备份
│   ├── xlsx_sync.py     # FDA 数据同步
│   └── news_aggregator.py
└── docs/                 # 项目文档
```

## 📊 数据统计

| 指标 | 数量 |
|------|------|
| FDA 警告信 | 986 |
| AI 分析报告 | 984 |
| CFR 引用 | 1,277 |
| 违规分类 | 831 |
| 高风险企业 | 11 |
| 行业资讯 | 40+ |
| 深度文章 | 13 |

## 🔧 配置说明

### 环境变量

```bash
# 可选：AI 服务配置
NVIDIA_API_KEY=your_nvidia_key
CF_API_KEY=your_cloudflare_key
```

### 数据库

默认使用 SQLite，数据库文件位于 `data/` 目录。首次运行会自动创建。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [FDA](https://www.fda.gov/) - 警告信数据来源
- [Vue.js](https://vuejs.org/) - 前端框架
- [FastAPI](https://fastapi.tiangolo.com/) - 后端框架
- [Cloudflare](https://www.cloudflare.com/) - CDN 和 AI 服务
