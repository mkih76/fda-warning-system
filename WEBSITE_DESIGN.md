# FDA 警告信智能平台 - 网站设计方案

> 基于现有系统的全面优化与扩展规划

---

## 📋 项目概述

### 项目定位
面向中国制药、化妆品、食品行业的 **FDA 警告信智能分析平台**，提供警告信翻译、AI 分析、行业法规、数据可视化等功能。

### 核心价值
- 实时监控 FDA 警告信动态
- AI 驱动的智能分析与翻译
- 行业合规风险预警
- 数据可视化决策支持

### 目标用户
- 制药企业合规部门
- 食品/化妆品企业质量管理人员
- 法规咨询机构
- 行业研究人员

---

## 🏗️ 架构设计

### 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    用户访问层 (User Access)                   │
├─────────────────────────────────────────────────────────────┤
│  移动端 Web    │    PC Web    │    API 调用    │    微信小程序  │
└───────┬────────┴──────┬───────┴──────┬────────┴───────┬──────┘
        │               │              │                │
        ▼               ▼              ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                 Cloudflare CDN + WAF                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  DDoS 防护   │  │  SSL/TLS    │  │  缓存加速    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              前端服务层 (Frontend Layer)                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Cloudflare Pages (Vue 3 SPA)                │  │
│  │  - 静态资源托管                                        │  │
│  │  - 自动部署 (GitHub Actions)                          │  │
│  │  - 边缘缓存                                          │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ API 请求
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              API 网关层 (API Gateway)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Cloudflare Workers (轻量代理)               │  │
│  │  - 请求路由                                          │  │
│  │  - 速率限制                                          │  │
│  │  - 请求/响应转换                                     │  │
│  │  - 简单逻辑处理                                      │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              后端服务层 (Backend Layer) - VPS                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   FastAPI     │  │   Celery     │  │   Redis      │      │
│  │   主服务      │  │   任务队列    │  │   缓存       │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │                │
│         ▼                 ▼                 ▼                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                 核心业务逻辑                           │  │
│  │  - 警告信 CRUD                                       │  │
│  │  - AI 分析流水线                                      │  │
│  │  - 数据同步调度                                       │  │
│  │  - 用户认证                                          │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              数据存储层 (Data Layer)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   SQLite     │  │   Redis      │  │   R2/S3      │      │
│  │   主数据库    │  │   缓存+队列  │  │   文件存储    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              外部服务层 (External Services)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  FDA 官网    │  │  NVIDIA NIM  │  │  RSS 源      │      │
│  │  数据源      │  │  AI 服务     │  │  新闻聚合     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 UI/UX 设计规范

### 设计原则
1. **简洁专业** - 医疗/法规行业需要严谨感
2. **信息层次清晰** - 数据密度高，需要良好的视觉引导
3. **响应式优先** - 支持多端访问
4. **无障碍设计** - 符合 WCAG 2.1 AA 标准

### 色彩系统

```css
:root {
  /* 主色系 - 专业医疗蓝 */
  --primary-50: #eff6ff;
  --primary-100: #dbeafe;
  --primary-500: #3b82f6;
  --primary-600: #2563eb;
  --primary-700: #1d4ed8;

  /* 辅助色 */
  --success: #10b981;      /* 成功/已关闭 */
  --warning: #f59e0b;      /* 警告/中风险 */
  --danger: #ef4444;       /* 错误/高风险 */
  --info: #06b6d4;         /* 信息 */

  /* 中性色 */
  --gray-50: #f8fafc;
  --gray-100: #f1f5f9;
  --gray-200: #e2e8f0;
  --gray-300: #cbd5e1;
  --gray-400: #94a3b8;
  --gray-500: #64748b;
  --gray-600: #475569;
  --gray-700: #334155;
  --gray-800: #1e293b;
  --gray-900: #0f172a;

  /* 暗色模式 */
  --dark-bg: #0f172a;
  --dark-surface: #1e293b;
  --dark-text: #e2e8f0;
}
```

### 字体系统

```css
/* 中文优先的字体栈 */
--font-sans: 'Inter', 'Noto Sans SC', -apple-system, BlinkMacSystemFont,
             'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;

/* 等宽字体（代码、FDA ID） */
--font-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas,
             'Liberation Mono', Menlo, monospace;
```

### 间距系统（8px 网格）

```css
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-5: 1.25rem;  /* 20px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
--space-10: 2.5rem;  /* 40px */
--space-12: 3rem;    /* 48px */
--space-16: 4rem;    /* 64px */
```

### 圆角规范

```css
--radius-sm: 0.375rem;  /* 6px - 按钮、标签 */
--radius-md: 0.5rem;    /* 8px - 输入框 */
--radius-lg: 0.75rem;   /* 12px - 卡片 */
--radius-xl: 1rem;      /* 16px - 模态框 */
--radius-full: 9999px;  /* 圆形 */
```

### 阴影系统

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
             0 2px 4px -2px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
             0 4px 6px -4px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
             0 8px 10px -6px rgba(0, 0, 0, 0.1);
```

---

## 📱 页面设计

### 1. 首页 (Home)

**设计目标**: 快速传达价值，引导用户探索

**布局结构**:
```
┌─────────────────────────────────────────┐
│              Hero Section                │
│  ┌─────────────────────────────────────┐│
│  │  背景图片 + 渐变遮罩                ││
│  │  标题: FDA 警告信智能平台           ││
│  │  副标题: AI 驱动的合规监控          ││
│  │  CTA: 开始探索 / 查看数据          ││
│  └─────────────────────────────────────┘│
├─────────────────────────────────────────┤
│           统计数据栏                     │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │
│  │ 986 │ │ 100%│ │ 24h │ │ AI  │     │
│  │警告信│ │翻译 │ │同步 │ │分析 │     │
│  └─────┘ └─────┘ └─────┘ └─────┘     │
├─────────────────────────────────────────┤
│           核心功能展示                   │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│  │ 实时同步 │ │ AI翻译  │ │ 智能分类 │  │
│  └─────────┘ └─────────┘ └─────────┘  │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│  │ 风险预警 │ │ 全文检索 │ │ 数据看板 │  │
│  └─────────┘ └─────────┘ └─────────┘  │
├─────────────────────────────────────────┤
│           工作流程展示                   │
│  采集 → AI处理 → 洞察呈现              │
├─────────────────────────────────────────┤
│           最新动态                       │
│  行业新闻 + 趋势分析                    │
├─────────────────────────────────────────┤
│           CTA 区域                      │
│  立即开始 / 查看数据看板                │
└─────────────────────────────────────────┘
```

**关键交互**:
- Hero 区域视差滚动
- 统计数字动态计数
- 功能卡片 hover 动画
- 最新动态轮播

---

### 2. 警告信列表页 (Letters)

**设计目标**: 高效浏览、精准筛选、快速定位

**布局结构**:
```
┌─────────────────────────────────────────┐
│  页头                                    │
│  ┌──────────────────┐ ┌───────────────┐│
│  │ 标题 + 副标题     │ │ 共 N 条记录   ││
│  └──────────────────┘ │ 导出 CSV      ││
│                       └───────────────┘│
├─────────────────────────────────────────┤
│  搜索与筛选栏                           │
│  ┌─────────────────────────────────────┐│
│  │ 🔍 搜索公司名、FDA ID...           ││
│  └─────────────────────────────────────┘│
│  ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│  │全部办公室│ │全部状态  │ │搜索     │  │
│  └─────────┘ └─────────┘ └─────────┘  │
│  ┌─────────┐ ┌─────────┐ ┌────────┐  │
│  │违规类型  │ │风险等级  │ │日期范围│  │
│  └─────────┘ └─────────┘ └────────┘  │
├─────────────────────────────────────────┤
│  信件卡片网格                           │
│  ┌─────────────┐ ┌─────────────┐      │
│  │ 状态标签     │ │ 状态标签     │      │
│  │ ❤️ 收藏     │ │ ❤️ 收藏     │      │
│  │             │ │             │      │
│  │ 公司名称     │ │ 公司名称     │      │
│  │ 摘要预览     │ │ 摘要预览     │      │
│  │             │ │             │      │
│  │ 日期 办公室  │ │ 日期 办公室  │      │
│  └─────────────┘ └─────────────┘      │
│  ┌─────────────┐ ┌─────────────┐      │
│  │     ...     │ │     ...     │      │
│  └─────────────┘ └─────────────┘      │
├─────────────────────────────────────────┤
│  分页                                    │
│  显示第 1-20 条，共 986 条              │
│  [<] [1] [2] [3] ... [50] [>]          │
└─────────────────────────────────────────┘
```

**关键特性**:
- 搜索建议（自动完成）
- 高级筛选面板（可折叠）
- 无限滚动 / 分页切换
- 批量收藏/导出
- 骨架屏加载

---

### 3. 警告信详情页 (LetterDetail)

**设计目标**: 信息全面、阅读舒适、快速理解

**布局结构**:
```
┌─────────────────────────────────────────┐
│  面包屑导航                             │
│  首页 > 警告信 > 详情                   │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐│
│  │           信件头部信息               ││
│  │  公司名称 (大标题)                   ││
│  │  FDA ID: xxx-xxxxxx                 ││
│  │  ┌──────┐ ┌──────┐ ┌──────┐       ││
│  │  │状态   │ │国家   │ │日期   │       ││
│  │  └──────┘ └──────┘ └──────┘       ││
│  │  办公室: CDER / CDRH / ...         ││
│  └─────────────────────────────────────┘│
├─────────────────────────────────────────┤
│  ┌──────────────┐ ┌──────────────┐     │
│  │              │ │              │     │
│  │   AI 分析    │ │   违规项     │     │
│  │   ───────    │ │   ───────    │     │
│  │   摘要       │ │   列表       │     │
│  │   风险等级   │ │   严重程度   │     │
│  │   违规类型   │ │              │     │
│  │              │ │              │     │
│  └──────────────┘ └──────────────┘     │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐│
│  │           CFR 引用                   ││
│  │  21 CFR 211.22 - 质量体系           ││
│  │  21 CFR 211.68 - 自动化设备         ││
│  └─────────────────────────────────────┘│
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐│
│  │           完整译文                   ││
│  │  [可折叠/展开]                       ││
│  │  长文本内容...                       ││
│  └─────────────────────────────────────┘│
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐│
│  │           原文链接                   ││
│  │  查看 FDA 原文 →                    ││
│  └─────────────────────────────────────┘│
├─────────────────────────────────────────┤
│  相关警告信推荐                         │
│  [卡片] [卡片] [卡片]                   │
└─────────────────────────────────────────┘
```

**关键交互**:
- AI 分析卡片可展开/折叠
- 违规项颜色编码（高/中/低风险）
- 锚点导航（快速跳转）
- 阅读进度条

---

### 4. 数据看板 (Dashboard)

**设计目标**: 数据可视化、趋势洞察、决策支持

**布局结构**:
```
┌─────────────────────────────────────────┐
│  页头                                    │
│  数据看板                                │
│  数据更新至 2024 年                      │
├─────────────────────────────────────────┤
│  指标卡片（2x2 网格）                   │
│  ┌─────────┐ ┌─────────┐               │
│  │  986    │ │  234    │               │
│  │ 警告信  │ │ 活跃中  │               │
│  └─────────┘ └─────────┘               │
│  ┌─────────┐ ┌─────────┐               │
│  │  752    │ │  12     │               │
│  │ 已关闭  │ │ 办公室  │               │
│  └─────────┘ └─────────┘               │
├─────────────────────────────────────────┤
│  图表行 1                               │
│  ┌──────────────────┐ ┌──────────────┐│
│  │                  │ │              ││
│  │   年度发布趋势   │ │  状态分布    ││
│  │   (柱状图/折线)  │ │  (环形图)    ││
│  │                  │ │              ││
│  └──────────────────┘ └──────────────┘│
├─────────────────────────────────────────┤
│  图表行 2                               │
│  ┌──────────────────┐ ┌──────────────┐│
│  │                  │ │              ││
│  │   签发办公室排名 │ │  国家分布    ││
│  │   (水平柱状图)   │ │  (饼图)      ││
│  │                  │ │              ││
│  └──────────────────┘ └──────────────┘│
├─────────────────────────────────────────┤
│  图表行 3                               │
│  ┌─────────────────────────────────────┐│
│  │           月度趋势 (面积图)         ││
│  │   近 12 个月的警告信数量变化        ││
│  └─────────────────────────────────────┘│
├─────────────────────────────────────────┤
│  高风险企业表格                         │
│  ┌─────┬─────┬─────┬─────┬─────┐     │
│  │排名 │公司 │国家 │数量 │风险 │     │
│  ├─────┼─────┼─────┼─────┼─────┤     │
│  │ 1   │ xxx │ CN  │ 5   │ 高  │     │
│  │ 2   │ xxx │ IN  │ 3   │ 高  │     │
│  └─────┴─────┴─────┴─────┴─────┘     │
└─────────────────────────────────────────┘
```

**图表库**: Chart.js / ECharts
**交互特性**:
- 图表联动（点击筛选）
- 时间范围选择
- 数据导出（PNG/CSV）
- 暗色模式适配

---

## 🔧 技术实现

### 前端技术栈

```json
{
  "framework": "Vue 3.4+",
  "buildTool": "Vite 5",
  "router": "Vue Router 4",
  "state": "Composables (Pinia if needed)",
  "ui": "Tailwind CSS 3",
  "charts": "Chart.js 4",
  "icons": "Heroicons",
  "http": "Axios",
  "date": "date-fns",
  "animation": "Framer Motion (optional)"
}
```

### 组件设计

```
src/
├── components/
│   ├── common/
│   │   ├── AppHeader.vue          # 全局头部
│   │   ├── AppFooter.vue          # 全局底部
│   │   ├── LoadingSpinner.vue     # 加载动画
│   │   ├── SkeletonLoader.vue     # 骨架屏
│   │   ├── EmptyState.vue         # 空状态
│   │   ├── ErrorBoundary.vue      # 错误边界
│   │   └── BackToTop.vue          # 回到顶部
│   │
│   ├── ui/
│   │   ├── BaseButton.vue         # 基础按钮
│   │   ├── BaseInput.vue          # 基础输入框
│   │   ├── BaseSelect.vue         # 基础下拉框
│   │   ├── BaseModal.vue          # 模态框
│   │   ├── BaseCard.vue           # 卡片
│   │   ├── BaseBadge.vue          # 徽章
│   │   ├── BaseTooltip.vue        # 提示
│   │   └── BasePagination.vue     # 分页
│   │
│   ├── business/
│   │   ├── LetterCard.vue         # 警告信卡片
│   │   ├── LetterDetail.vue       # 警告信详情
│   │   ├── AIAnalysisCard.vue     # AI 分析卡片
│   │   ├── ViolationList.vue      # 违规项列表
│   │   ├── CFRReferences.vue      # CFR 引用
│   │   ├── SearchBar.vue          # 搜索框
│   │   ├── SearchSuggestions.vue  # 搜索建议
│   │   ├── FilterPanel.vue        # 筛选面板
│   │   └── ExportButton.vue       # 导出按钮
│   │
│   └── charts/
│       ├── TrendChart.vue         # 趋势图
│       ├── PieChart.vue           # 饼图
│       ├── BarChart.vue           # 柱状图
│       └── TimelineChart.vue      # 时间线
│
├── composables/
│   ├── useDarkMode.js             # 暗色模式
│   ├── useFavorites.js            # 收藏功能
│   ├── useSearch.js               # 搜索逻辑
│   ├── usePagination.js           # 分页逻辑
│   ├── useExport.js               # 导出功能
│   └── useApi.js                  # API 封装
│
├── views/
│   ├── Home.vue                   # 首页
│   ├── Letters.vue                # 列表页
│   ├── LetterDetail.vue           # 详情页
│   ├── Dashboard.vue              # 看板页
│   ├── Favorites.vue              # 收藏页
│   ├── Articles.vue               # 文章页
│   ├── Regulations.vue            # 法规页
│   └── News.vue                   # 资讯页
│
└── styles/
    ├── variables.css              # CSS 变量
    ├── base.css                   # 基础样式
    ├── utilities.css              # 工具类
    └── animations.css             # 动画
```

---

## 🚀 部署方案

### 方案 A: Cloudflare Pages + VPS（推荐）

**架构**:
```
Cloudflare Pages (前端)
       ↓
Cloudflare Workers (API 代理)
       ↓
VPS (后端 API + 数据库)
```

**优势**:
- ✅ 全球 CDN，访问速度快
- ✅ 自动 HTTPS
- ✅ DDoS 防护
- ✅ 前端自动部署
- ✅ 成本低（Pages 免费）

**实施步骤**:

1. **配置前端环境变量**
```bash
# .env.production
VITE_API_BASE_URL=https://api.fda.19990419.top
```

2. **创建 Cloudflare Worker 代理**
```javascript
// worker.js
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // API 请求转发到 VPS
    if (url.pathname.startsWith('/api')) {
      const apiUrl = `https://your-vps-ip:8790${url.pathname}${url.search}`;
      return fetch(apiUrl, {
        method: request.method,
        headers: request.headers,
        body: request.body,
      });
    }

    // 静态资源请求 Pages
    return env.ASSETS.fetch(request);
  }
};
```

3. **配置 GitHub Actions 自动部署**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: cd frontend && npm ci

      - name: Build
        run: cd frontend && npm run build
        env:
          VITE_API_BASE_URL: ${{ secrets.API_BASE_URL }}

      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: fda-warning-system
          directory: frontend/dist
```

4. **VPS 后端部署**
```bash
# docker-compose.yml 已配置
docker-compose up -d

# 配置 Caddy 反向代理
# Caddyfile
api.fda.19990419.top {
    reverse_proxy localhost:8790
}
```

**成本估算**:
- Cloudflare Pages: 免费（每月 500 次构建）
- Cloudflare Workers: 免费（每日 10 万请求）
- VPS: $5-10/月（Hetzner/Contabo）
- 域名: $10/年
- **总计**: ~$5-10/月

---

### 方案 B: 全 VPS 部署（当前方案）

**架构**:
```
VPS (Nginx/Caddy + FastAPI + 静态文件)
```

**优势**:
- ✅ 简单直接
- ✅ 完全控制
- ✅ 无外部依赖

**劣势**:
- ❌ 单点故障
- ❌ 访问速度受地域限制
- ❌ 需要手动维护 SSL

**优化建议**:
```bash
# 1. 启用 Nginx 缓存
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g;

# 2. 启用 Gzip 压缩
gzip on;
gzip_types text/plain application/json application/javascript text/css;

# 3. 配置 HTTP/2
listen 443 ssl http2;

# 4. 设置静态资源缓存
location ~* \.(js|css|png|jpg|ico)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

---

### 方案 C: Serverless 全托管

**架构**:
```
Cloudflare Pages (前端)
       ↓
Cloudflare Workers (API)
       ↓
Supabase (数据库 + Auth)
       ↓
Cloudflare R2 (文件存储)
```

**优势**:
- ✅ 无需 VPS
- ✅ 自动扩缩容
- ✅ 按量付费

**劣势**:
- ❌ 需要重写后端
- ❌ 学习曲线陡峭
- ❌ 供应商锁定

**不适合原因**:
- Python 后端无法运行
- 爬虫/AI 任务会超时
- SQLite 需要迁移

---

## 🔒 安全设计

### 1. 前端安全

```javascript
// XSS 防护
// 使用 Vue 的模板语法（自动转义）
<p>{{ userInput }}</p>

// CSP 配置
// Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'

// 敏感信息不暴露
// API Key 存储在后端环境变量
```

### 2. 后端安全

```python
# 1. CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://fda.19990419.top"],  # 不要用 *
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# 2. 速率限制
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# 3. 输入验证
from pydantic import BaseModel, validator

class SearchQuery(BaseModel):
    q: str
    
    @validator('q')
    def sanitize_query(cls, v):
        # 移除特殊字符
        return re.sub(r'[<>"\']', '', v)

# 4. SQL 注入防护（SQLAlchemy 已处理）
# 使用参数化查询，不要拼接 SQL
```

### 3. API Key 管理

```bash
# 环境变量存储（不要硬编码！）
export NVIDIA_API_KEY="your-key-here"
export CF_API_KEY="your-key-here"

# Docker secrets（生产环境）
docker secret create nvidia_key ./nvidia_key.txt
```

### 4. HTTPS 配置

```bash
# Caddy 自动 HTTPS
api.fda.19990419.top {
    # 自动获取 Let's Encrypt 证书
    reverse_proxy localhost:8790
}

# 或 Nginx + Certbot
sudo certbot --nginx -d api.fda.19990419.top
```

---

## 📊 性能优化

### 1. 前端优化

```javascript
// 1. 代码分割
const Letters = () => import('./views/Letters.vue')
const Dashboard = () => import('./views/Dashboard.vue')

// 2. 图片懒加载
<img loading="lazy" src="..." />

// 3. 虚拟滚动（大数据列表）
import { VirtualList } from 'vue-virtual-list'

// 4. 预加载关键资源
<link rel="preload" href="/api/stats" as="fetch" crossorigin>

// 5. Service Worker 缓存
// vite-plugin-pwa 自动生成
```

### 2. 后端优化

```python
# 1. 数据库索引
class WarningLetter(Base):
    __tablename__ = 'warning_letters'
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String, index=True)  # 添加索引
    issue_date = Column(String, index=True)
    status = Column(String, index=True)

# 2. 查询优化
# 避免 N+1 查询
letters = db.query(WarningLetter).options(
    joinedload(WarningLetter.ai_analysis)
).all()

# 3. 缓存策略
from functools import lru_cache

@lru_cache(maxsize=100)
def get_stats():
    # 缓存统计结果
    pass

# 4. 异步任务
from celery import Celery

celery_app = Celery('tasks', broker='redis://localhost:6379')

@celery_app.task
def analyze_letter(letter_id):
    # 耗时的 AI 分析
    pass
```

### 3. CDN 配置

```javascript
// Cloudflare 缓存规则
// 1. 静态资源缓存 1 年
Cache-Control: public, max-age=31536000, immutable

// 2. API 响应缓存 5 分钟
Cache-Control: public, max-age=300

// 3. HTML 不缓存
Cache-Control: no-cache
```

---

## 🎯 SEO 优化

### 1. Meta 标签

```html
<head>
  <title>FDA 警告信智能平台 - AI 驱动的合规监控</title>
  <meta name="description" content="实时监控 FDA 警告信，AI 智能分析违规项，保障药品合规。986+ 封警告信，100% 中文翻译。" />
  <meta name="keywords" content="FDA, 警告信, 药品合规, CGMP, AI分析" />
  
  <!-- Open Graph -->
  <meta property="og:title" content="FDA 警告信智能平台" />
  <meta property="og:description" content="AI 驱动的合规监控系统" />
  <meta property="og:image" content="/og-image.png" />
  <meta property="og:url" content="https://fda.19990419.top" />
  
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
</head>
```

### 2. 结构化数据

```json
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "FDA 警告信智能平台",
  "description": "AI 驱动的 FDA 警告信分析系统",
  "url": "https://fda.19990419.top",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web"
}
```

### 3. Sitemap

```xml
<!-- public/sitemap.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://fda.19990419.top/</loc>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://fda.19990419.top/letters</loc>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://fda.19990419.top/dashboard</loc>
    <priority>0.8</priority>
  </url>
</urlset>
```

---

## 📈 监控与分析

### 1. 性能监控

```javascript
// Web Vitals 监控
import { onCLS, onFID, onLCP } from 'web-vitals'

function sendToAnalytics({ name, delta, id }) {
  // 发送到 Google Analytics 或自建服务
  gtag('event', name, {
    event_category: 'Web Vitals',
    event_label: id,
    value: Math.round(name === 'CLS' ? delta * 1000 : delta),
  })
}

onCLS(sendToAnalytics)
onFID(sendToAnalytics)
onLCP(sendToAnalytics)
```

### 2. 错误监控

```javascript
// Sentry 集成
import * as Sentry from "@sentry/vue"

Sentry.init({
  app,
  dsn: "https://xxx@sentry.io/xxx",
  integrations: [
    new Sentry.BrowserTracing(),
    new Sentry.Replay(),
  ],
  tracesSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
})
```

### 3. 用户分析

```javascript
// Google Analytics 4
// 或 Umami (开源、隐私友好)
// 或 Plausible (轻量级)

// umami 示例
<script async defer
  data-website-id="xxx"
  src="https://umami.example.com/umami.js">
</script>
```

---

## 🗺️ 未来规划

### Phase 1: 核心功能完善 (1-2 周)
- [x] 收藏系统
- [x] CSV 导出
- [x] 搜索建议
- [x] 骨架屏
- [ ] 用户认证系统
- [ ] 批量操作

### Phase 2: 内容扩展 (2-4 周)
- [ ] 法规数据库
- [ ] 案例库
- [ ] 知识图谱
- [ ] 多语言支持

### Phase 3: 智能化 (4-8 周)
- [ ] 智能问答（RAG）
- [ ] 风险预测模型
- [ ] 自动化报告生成
- [ ] 邮件/微信通知

### Phase 4: 商业化 (8-12 周)
- [ ] 会员订阅系统
- [ ] API 开放平台
- [ ] 企业定制版
- [ ] 数据服务

---

## 📝 总结

### 技术选型建议

| 层级 | 推荐方案 | 理由 |
|------|---------|------|
| **前端** | Vue 3 + Vite + Tailwind | 生态成熟，开发效率高 |
| **部署** | Cloudflare Pages | 全球 CDN，免费额度足够 |
| **后端** | FastAPI (VPS) | Python 生态，AI 集成方便 |
| **数据库** | SQLite → PostgreSQL | 未来扩展性更好 |
| **缓存** | Redis | 高性能，支持队列 |
| **监控** | Sentry + Umami | 错误追踪 + 用户分析 |

### 成本估算

**启动阶段（月）**:
- Cloudflare Pages: 免费
- VPS (2C4G): $10
- 域名: $1/月
- **总计**: ~$11/月

**增长阶段（月）**:
- Cloudflare Pro: $20
- VPS (4C8G): $20
- Sentry: 免费
- **总计**: ~$40/月

### 关键成功因素

1. **内容质量** - 翻译准确、分析专业
2. **更新及时性** - 24 小时内同步新警告信
3. **用户体验** - 快速、直观、易用
4. **数据安全** - 合规存储、隐私保护

---

**文档版本**: v2.0
**最后更新**: 2026-04-30
**作者**: Claude AI Assistant
