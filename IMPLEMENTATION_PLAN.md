# PharmaCos Insight 落地实施方案

## 一、现状审计结论

### 1.1 当前技术栈
| 层级 | 技术 | 状态 |
|------|------|------|
| 前端 | Vue 3 + Vite + Chart.js + Tailwind CSS | 正常运行 |
| 后端 | FastAPI + SQLAlchemy + SQLite | 正常运行，16个GET接口，无写入接口 |
| 数据库 | SQLite (/root/data/fda_warning.db) | 6张表，986条警告信数据 |
| 部署 | Docker (单容器) + Caddy 反代 | 手动部署，无CI/CD |
| 用户系统 | **无** | 全站无登录/注册功能 |
| 内容管理 | **无** | 文章硬编码或简单JSON |

### 1.2 数据库现有表
```
warning_letters    — 警告信主表 (986条)
violations         — 违规项
ai_analysis        — AI分析结果
f483_observations  — FDA 483观察项
cfr_citations      — CFR条款引用
push_subscriptions — 推送订阅
```

### 1.3 现有前端页面
```
HomeNew.vue        — 首页 (辉瑞风格)
LettersNew.vue     — 警告信列表 (搜索+筛选+分页)
LetterDetailNew.vue — 警告信详情 (AI分析+违规+CFR)
DashboardNew.vue   — 数据看板 (Chart.js图表)
Articles.vue       — 深度内容
News.vue           — 行业资讯
Regulations.vue    — 法规信息
Favorites.vue      — 收藏夹 (本地存储)
```

---

## 二、实施原则

### 2.1 核心原则
1. **渐进式改造**：每一步完成后网站都能正常运行，不存在"改到一半不能用"的状态
2. **只加不删**：新代码与旧代码并行，旧功能不删除直到新功能验证通过
3. **向后兼容**：现有 FDA 警告信功能在整个过程中保持正常
4. **本地优先**：所有改动先在本地验证，确认无误后才推送到 VPS

### 2.2 风险控制策略
| 风险 | 应对 |
|------|------|
| 改坏现有功能 | 每次改动前创建 git tag，可一键回滚 |
| SQLite 不支持复杂操作 | 新增表用 SQLite，不修改现有表结构 |
| VPS 部署失败 | 先在本地 `npm run dev` 完整测试 |
| GitHub 推送失败 | 如推送失败，用 VPS 直接 pull 或手动上传 |
| 数据丢失 | 改动前备份 SQLite 数据库文件 |

---

## 三、数据库设计（只加不改）

### 3.1 新增表结构

```sql
-- ═══ 用户系统 ═══
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nickname VARCHAR(100),
    company VARCHAR(200),
    role VARCHAR(50) DEFAULT 'free',       -- free/pro/enterprise/admin
    avatar_url VARCHAR(500),
    wechat_openid VARCHAR(100),            -- 微信登录
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login_at DATETIME,
    is_active INTEGER DEFAULT 1
);

-- ═══ 内容系统 ═══
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,            -- 中文名
    name_en VARCHAR(100),                  -- 英文名
    slug VARCHAR(100) UNIQUE NOT NULL,     -- URL 友好标识
    sector VARCHAR(50) NOT NULL,           -- pharma/cosmetics/food/general/tools
    parent_id INTEGER,                     -- 支持二级分类
    icon VARCHAR(50),
    sort_order INTEGER DEFAULT 0,
    description TEXT
);

CREATE TABLE articles (
    id INTEGER PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    slug VARCHAR(500) UNIQUE,
    content TEXT NOT NULL,                 -- Markdown 格式
    content_html TEXT,                     -- 渲染后的 HTML
    summary VARCHAR(1000),                 -- 摘要
    cover_image VARCHAR(500),             -- 封面图
    category_id INTEGER REFERENCES categories(id),
    sector VARCHAR(50),                   -- pharma/cosmetics/food/general (冗余，方便查询)
    tags TEXT,                            -- JSON 数组
    author_id INTEGER REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'draft',   -- draft/published/archived
    access_level VARCHAR(20) DEFAULT 'free', -- free/pro/enterprise
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    seo_title VARCHAR(200),
    seo_description VARCHAR(500),
    published_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ═══ 会员系统 ═══
CREATE TABLE memberships (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    plan VARCHAR(50) NOT NULL,            -- free/pro/enterprise/flagship
    started_at DATETIME NOT NULL,
    expires_at DATETIME,
    payment_method VARCHAR(50),           -- wechat/alipay
    amount_cents INTEGER,                 -- 金额（分）
    is_active INTEGER DEFAULT 1
);

-- ═══ 收藏系统（从 localStorage 迁移到数据库）═══
CREATE TABLE user_favorites (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    item_type VARCHAR(50) NOT NULL,       -- letter/article
    item_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, item_type, item_id)
);

-- ═══ 阅读历史 ═══
CREATE TABLE read_history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    article_id INTEGER REFERENCES articles(id),
    read_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    read_duration INTEGER                 -- 阅读时长（秒）
);
```

### 3.2 分类数据初始值
```sql
-- 制药板块
INSERT INTO categories (name, name_en, slug, sector, sort_order) VALUES
('行业动态', 'Industry News', 'industry-news', 'pharma', 1),
('政策法规', 'Regulations', 'regulations', 'pharma', 2),
('GMP 实务', 'GMP Practice', 'gmp-practice', 'pharma', 3),
('药典解读', 'Pharmacopoeia', 'pharmacopoeia', 'pharma', 4),
('注册申报', 'Registration', 'registration', 'pharma', 5),
('质量控制', 'Quality Control', 'quality-control', 'pharma', 6),
('工艺验证', 'Process Validation', 'process-validation', 'pharma', 7),
('案例研究', 'Case Studies', 'case-studies', 'pharma', 8),
('专家观点', 'Expert Insights', 'expert-insights', 'pharma', 9),

-- 化妆品板块
('行业动态', 'Industry News', 'cosmetics-industry', 'cosmetics', 1),
('政策法规', 'Regulations', 'cosmetics-regulations', 'cosmetics', 2),
('配方与安全', 'Formulation & Safety', 'formulation-safety', 'cosmetics', 3),
('功效评价', 'Efficacy Testing', 'efficacy-testing', 'cosmetics', 4),
('原料合规', 'Ingredient Compliance', 'ingredient-compliance', 'cosmetics', 5),
('标签与宣称', 'Labeling & Claims', 'labeling-claims', 'cosmetics', 6),
('生产质量管理', 'Manufacturing QM', 'manufacturing-qm', 'cosmetics', 7),
('市场趋势', 'Market Trends', 'cosmetics-trends', 'cosmetics', 8),

-- 食品板块
('行业动态', 'Industry News', 'food-industry', 'food', 1),
('政策法规', 'Regulations', 'food-regulations', 'food', 2),
('食品安全管理体系', 'Food Safety Management', 'food-safety-mgmt', 'food', 3),
('添加剂与新原料', 'Additives & Ingredients', 'food-additives', 'food', 4),
('标签标识', 'Labeling', 'food-labeling', 'food', 5),
('进出口合规', 'Import/Export Compliance', 'food-import-export', 'food', 6),
('营养与健康声称', 'Nutrition Claims', 'nutrition-claims', 'food', 7),
('市场趋势', 'Market Trends', 'food-trends', 'food', 8),

-- 综合板块
('GMP 全景', 'GMP Panorama', 'gmp-panorama', 'general', 1),
('药典对照', 'Pharmacopoeia Comparison', 'pharma-compare', 'general', 2),
('FDA 警告信', 'FDA Warning Letters', 'fda-warnings', 'general', 3),
('法规库', 'Regulation Library', 'regulation-library', 'general', 4),
('行业白皮书', 'White Papers', 'white-papers', 'general', 5);
```

---

## 四、分阶段实施计划

### Phase 1：基础设施搭建（前端路由重构 + 后端骨架）
**工期：3-4天 | 风险：低 | 影响：仅前端**

#### 1.1 前端路由重构
**目标：** 建立新的导航结构，旧页面保留，新页面搭骨架

```
新增/修改文件：
├── frontend/src/router/index.js          — 新增路由
├── frontend/src/components/Navbar.vue     — 更新导航结构
├── frontend/src/views/                   — 新增页面骨架
│   ├── pharma/PharmaHome.vue             — 制药板块首页
│   ├── pharma/PharmaArticleList.vue      — 制药文章列表
│   ├── pharma/PharmaArticleDetail.vue    — 制药文章详情
│   ├── cosmetics/CosmeticsHome.vue       — 化妆品板块首页
│   ├── cosmetics/CosmeticsArticleList.vue
│   ├── cosmetics/CosmeticsArticleDetail.vue
│   ├── food/FoodHome.vue                 — 食品板块首页
│   ├── food/FoodArticleList.vue
│   ├── food/FoodArticleDetail.vue
│   ├── general/GeneralHome.vue           — 综合板块首页
│   ├── tools/ToolsHome.vue               — 工具集首页
│   └── about/AboutHome.vue               — 关于页面
```

**路由设计：**
```javascript
// 新增路由（旧路由保持不变）
{ path: '/pharma', component: PharmaHome },
{ path: '/pharma/:category', component: PharmaArticleList },
{ path: '/pharma/article/:slug', component: PharmaArticleDetail },
{ path: '/cosmetics', component: CosmeticsHome },
{ path: '/cosmetics/:category', component: CosmeticsArticleList },
{ path: '/cosmetics/article/:slug', component: CosmeticsArticleDetail },
{ path: '/food', component: FoodHome },
{ path: '/food/:category', component: FoodArticleList },
{ path: '/food/article/:slug', component: FoodArticleDetail },
{ path: '/general', component: GeneralHome },
{ path: '/tools', component: ToolsHome },
{ path: '/about', component: AboutHome },
// 旧路由保持不动，通过 /general/fda-warnings 访问
```

**验证标准：**
- [ ] 所有新路由可正常访问（骨架页面显示）
- [ ] 旧路由（/letters, /dashboard 等）完全不受影响
- [ ] 导航栏显示新的板块入口
- [ ] 移动端导航正常

#### 1.2 后端数据库扩展
**目标：** 新增表，不修改旧表

```python
# backend/app/models_new.py（新文件，不修改 models.py）
# 包含 User, Category, Article, Membership, UserFavorite, ReadHistory
```

**验证标准：**
- [ ] 新表创建成功，旧表无变化
- [ ] 旧 API 全部正常响应
- [ ] 数据库文件大小合理增长

---

### Phase 2：后端 API 开发（内容管理 + 用户系统）
**工期：5-7天 | 风险：中 | 影响：仅后端，不影响前端**

#### 2.1 内容管理 API
```python
# backend/app/routers/content.py（新文件）

# 分类
GET  /api/categories                    — 获取分类树
GET  /api/categories/{slug}             — 获取分类详情

# 文章
GET  /api/content/articles              — 文章列表（支持 sector/category/tag 筛选 + 分页）
GET  /api/content/articles/{slug}       — 文章详情（按 slug）
POST /api/content/articles              — 创建文章（需管理员权限）
PUT  /api/content/articles/{id}         — 更新文章
DELETE /api/content/articles/{id}       — 删除文章

# 首页聚合
GET  /api/content/home                  — 首页所需的所有数据（各板块最新文章）
GET  /api/content/sector/{sector}       — 单个板块首页数据
```

#### 2.2 用户认证 API
```python
# backend/app/routers/auth.py（新文件）

POST /api/auth/register                 — 注册（邮箱+密码）
POST /api/auth/login                    — 登录（返回 JWT）
POST /api/auth/refresh                  — 刷新 token
GET  /api/auth/me                       — 获取当前用户信息
PUT  /api/auth/me                       — 更新个人信息
POST /api/auth/forgot-password          — 忘记密码（发邮件）
```

#### 2.3 用户功能 API
```python
# backend/app/routers/user.py（新文件）

GET    /api/user/favorites              — 获取收藏列表
POST   /api/user/favorites              — 添加收藏
DELETE /api/user/favorites/{id}         — 取消收藏
GET    /api/user/history                — 阅读历史
GET    /api/user/membership             — 会员信息
```

**依赖安装：**
```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

**验证标准：**
- [ ] 注册 → 登录 → 获取用户信息 完整流程正常
- [ ] JWT token 签发和验证正确
- [ ] 文章 CRUD 正常工作
- [ ] 旧的 FDA 相关 API 完全不受影响
- [ ] 管理员/普通用户权限区分正确

---

### Phase 3：前端内容页面开发
**工期：5-7天 | 风险：低 | 影响：仅新增页面**

#### 3.1 板块首页（三个板块结构相同，内容不同）
每个板块首页采用「辉瑞风格」的双栏布局：
- Hero Banner（板块主题图 + 板块介绍）
- 最新文章列表（左侧图文，右侧文字 — 辉瑞双栏模式）
- 分类入口卡片
- 板块数据统计

#### 3.2 文章列表页
- 筛选面板（分类、标签、时间范围）
- 搜索栏
- 文章卡片（标题 + 摘要 + 分类标签 + 发布时间 + 阅读量）
- 分页

#### 3.3 文章详情页
- 面包屑导航
- 文章正文（Markdown 渲染，支持代码块、表格、图片）
- 右侧 TOC（目录）
- 相关文章推荐
- 底部上/下一篇导航

#### 3.4 综合板块
- GMP 全景（跨行业 GMP 对照表，可交互）
- 药典对照（ChP/USP/EP/JP 方法差异，可搜索）
- FDA 警告信入口（跳转到现有 /letters 页面）
- 法规库（法规列表，按行业×地区×主题筛选）

**验证标准：**
- [ ] 三个板块首页各自展示正确的分类和文章
- [ ] 文章列表筛选、搜索、分页正常
- [ ] 文章详情页 Markdown 渲染正确，TOC 可点击跳转
- [ ] 旧页面（/letters, /dashboard 等）完全不受影响
- [ ] 移动端响应式正常

---

### Phase 4：用户系统前端
**工期：3-4天 | 风险：低**

#### 4.1 新增页面
```
views/auth/Login.vue          — 登录页
views/auth/Register.vue       — 注册页
views/auth/ForgotPassword.vue — 忘记密码
views/user/Profile.vue        — 个人中心
views/user/MyFavorites.vue    — 我的收藏（替代旧的 Favorites.vue）
views/user/ReadHistory.vue    — 阅读历史
views/user/Membership.vue     — 会员中心
```

#### 4.2 新增 composable
```javascript
// composables/useAuth.js
// - user (ref)
// - isLoggedIn (computed)
// - isAdmin (computed)
// - login(email, password)
// - register(email, password, nickname)
// - logout()
// - refreshToken()

// composables/useApi.js
// - 自动附加 JWT token
// - 401 时自动跳转登录
// - 统一错误处理
```

#### 4.3 导航栏更新
- 未登录：显示「登录」「注册」按钮
- 已登录：显示用户头像 + 下拉菜单（个人中心/收藏/会员/退出）
- 会员状态标识

**验证标准：**
- [ ] 注册 → 登录 → 浏览文章 → 收藏 → 查看收藏 完整流程
- [ ] Token 过期后自动跳转登录
- [ ] 未登录用户可浏览免费内容
- [ ] 旧的本地收藏功能保持兼容

---

### Phase 5：会员与付费墙
**工期：4-5天 | 风险：中**

#### 5.1 内容访问控制
```javascript
// 前端权限判断
function canAccess(article) {
  if (article.access_level === 'free') return true
  if (!isLoggedIn.value) return false  // 跳转登录
  if (article.access_level === 'pro') return user.value.role !== 'free'
  if (article.access_level === 'enterprise') return ['enterprise', 'admin'].includes(user.value.role)
  return false
}
```

#### 5.2 付费墙 UI
- 文章阅读到一定位置时显示「解锁全文」遮罩
- 引导用户升级会员
- 付费墙设计要优雅，不能让用户反感

#### 5.3 支付接入（Phase 5 可延后）
- 微信支付 Native（扫码付）
- 支付宝当面付
- 暂时可以先用「联系客服开通」的半自动方式

**验证标准：**
- [ ] 免费文章任何人可阅读
- [ ] 付费文章免费用户看到前30% + 付费墙
- [ ] Pro 会员可阅读 Pro 文章
- [ ] 非会员点击付费内容有清晰的引导

---

### Phase 6：内容填充
**工期：持续进行 | 风险：低**

#### 6.1 内容来源
| 来源 | 方式 | 优先级 |
|------|------|--------|
| AI 生成初稿 + 人工审核 | 用 Claude/GPT 生成文章框架和初稿，人工审核修改 | P0 |
| 现有内容迁移 | Articles.vue、News.vue、Regulations.vue 中的现有内容迁移 | P0 |
| 爬虫+AI 摘要 | 爬取 FDA/NMPA/EMA 官网最新动态，AI 生成中文摘要 | P1 |
| 专家撰稿 | 邀请行业专家撰写专栏（后期） | P2 |

#### 6.2 首批内容目标
每个板块至少 10 篇高质量文章上线：
- 制药：GMP 实务 3 篇 + 药典解读 2 篇 + 政策法规 3 篇 + 案例 2 篇
- 化妆品：法规解读 3 篇 + 配方安全 2 篇 + 功效评价 2 篇 + 原料合规 3 篇
- 食品：食品安全体系 3 篇 + 法规解读 3 篇 + 添加剂 2 篇 + 标签 2 篇

---

### Phase 7：测试与部署
**工期：2-3天**

#### 7.1 本地测试清单
```
功能测试：
□ 旧功能：FDA 警告信搜索、详情、看板、收藏
□ 新功能：注册、登录、文章浏览、收藏（数据库版）
□ 导航：所有链接正确、面包屑正确
□ 响应式：桌面/平板/手机三种尺寸
□ 权限：未登录/免费会员/Pro会员 的内容可见性

性能测试：
□ 首页加载时间 < 3s
□ 文章列表接口响应 < 500ms
□ 文章详情接口响应 < 300ms

安全测试：
□ SQL 注入防护（SQLAlchemy ORM 自带）
□ XSS 防护（Markdown 渲染时 sanitize）
□ JWT token 安全性
□ CORS 配置正确
□ 密码 bcrypt 加密
```

#### 7.2 部署流程
```bash
# 1. 本地构建前端
cd frontend && npm run build

# 2. 推送到 GitHub
git add -A && git commit -m "feat: PharmaCos Insight Phase X" && git push origin main

# 3. VPS 部署
ssh root@vps
cd /root/fda-warning-system
git pull origin main
cd frontend && npm install && npm run build && cd ..
# 如果有新的 Python 依赖
pip install -r backend/requirements.txt
docker-compose down && docker-compose up -d --build

# 4. 验证
curl http://localhost:8790/api/health
curl http://localhost:8790/api/content/articles
```

#### 7.3 回滚方案
```bash
# 每次部署前打 git tag
git tag -a v2.0-phase1 -m "Phase 1 snapshot"

# 如需回滚
git checkout v2.0-phase1
cd frontend && npm run build
docker-compose restart
```

---

## 五、影响评估

### 5.1 对现有功能的影响
| 功能 | 影响 | 措施 |
|------|------|------|
| FDA 警告信搜索 | **无影响** — 旧 API 不变 | 旧路由保持 |
| 警告信详情 | **无影响** — 旧 API 不变 | 旧路由保持 |
| 数据看板 | **无影响** — 旧 API 不变 | 旧路由保持 |
| 收藏功能 | **增强** — 从 localStorage 迁移到数据库 | 保持 localStorage 兼容，登录后用数据库 |
| 行业资讯 | **迁移** — 内容迁移到新的文章系统 | 保留旧路由，逐步引导到新页面 |
| 法规信息 | **迁移** — 内容迁移到综合板块 | 保留旧路由 |
| 深度内容 | **迁移** — 内容迁移到对应板块 | 保留旧路由 |

### 5.2 性能影响
| 指标 | 当前 | 改造后预期 |
|------|------|----------|
| 首页加载 | ~1.5s | ~2s（新增板块入口组件） |
| API 响应 | ~100ms | ~150ms（新增查询） |
| 数据库大小 | ~50MB | ~60MB（新表+内容） |
| Docker 镜像 | ~200MB | ~250MB（新增 Python 依赖） |

### 5.3 向后兼容性
- 所有旧路由（`/#/letters`, `/#/dashboard` 等）继续工作
- 旧 API（`/api/letters`, `/api/stats` 等）继续工作
- 本地收藏数据在用户登录后自动迁移到数据库
- 旧页面（Home.vue, Letters.vue 等）保留但不再默认使用

---

## 六、技术债务与后续优化

### 6.1 Phase 1-4 期间的技术债务
| 债务 | 说明 | 还债时间 |
|------|------|---------|
| SQLite 限制 | 不支持 ALTER TABLE、并发写入有限 | Phase 5+ 考虑 PostgreSQL |
| 无 Redis | 缓存用内存字典，重启丢失 | Phase 5+ 加 Redis 容器 |
| Markdown 存储 | 文章内容存 Markdown，无版本控制 | 后续加版本历史表 |
| 搜索功能 | 简单 LIKE 查询，无全文索引 | 后续加 Meilisearch |

### 6.2 长期技术演进
```
Phase 8+ (远期):
├── PostgreSQL 替代 SQLite
├── Redis 缓存层
├── Meilisearch 全文搜索
├── 微信小程序
├── 邮件订阅系统（行业周报）
├── 在线培训系统
├── API 开放平台
└── 微信公众号集成
```

---

## 七、实施顺序总结

```
Phase 1 (3-4天)  → 前端路由重构 + 数据库新表
  ↓ 验证：新旧路由都正常
Phase 2 (5-7天)  → 后端 API（内容管理 + 用户认证）
  ↓ 验证：API 接口可用
Phase 3 (5-7天)  → 前端内容页面
  ↓ 验证：三个板块可浏览
Phase 4 (3-4天)  → 用户系统前端
  ↓ 验证：注册登录流程完整
Phase 5 (4-5天)  → 会员与付费墙
  ↓ 验证：权限控制正确
Phase 6 (持续)   → 内容填充
  ↓ 验证：每板块 10+ 篇文章
Phase 7 (2-3天)  → 测试与部署
  ↓ 上线
总计：约 22-30 个工作日
```

---

## 八、我会如何工作

### 每个 Phase 的工作流程：
1. **规划**：列出要改的文件清单，确认不影响旧功能
2. **实施**：逐步修改文件，每改完一个文件就本地验证
3. **验证**：运行 `npm run build`，检查编译是否通过
4. **提交**：git commit（每完成一个有意义的单元就提交）
5. **报告**：告诉你当前进度，下一步计划

### 沟通机制：
- 每个 Phase 开始前告诉你要做什么
- 遇到需要你决策的问题会主动问你
- 每个 Phase 完成后报告结果和验证情况
- 如果发现问题（即使是我自己造成的），会立即告知并修复
