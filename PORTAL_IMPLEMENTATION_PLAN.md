# 资讯门户数据落地方案

## 总体架构

```
数据源层          采集层           存储层          API层          展示层
─────────────────────────────────────────────────────────────────────
FDA官网    ─┐
NMPA官网   ─┤    RSS聚合器  ─┐
行业网站   ─┤    (Phase 2)   │
           │                 ↓
           │    爬虫系统    ─┤    PostgreSQL/    ─┐
           ├    (Phase 1)   │    SQLite           │    REST API    →    资讯门户
           │                 ↓                     ├    /api/portal      (Vue前端)
           │    内容表      ─┘                     │
           │    (现有)                              │
           │                                        │
AI模型     ─┤    AI生成器   ─┐                     │
(Google/   │    (Phase 3)   ↓                     │
NVIDIA)    └──────────────→ 内容队列  ────────────┘
```

## 实施阶段

### Phase 1: 现有数据快速落地 (1-2天)
**目标：** 门户页面立即可用，数据来自现有数据库

#### 后端任务：
- [ ] 创建 `/api/portal/headlines` - 获取置顶文章
- [ ] 创建 `/api/portal/industry/{sector}` - 获取各行业最新动态
- [ ] 创建 `/api/portal/hot` - 热门文章排行
- [ ] 创建 `/api/portal/stats` - 统计数据
- [ ] 创建 `/api/portal/subscribe` - 订阅功能（存储邮箱）

#### 前端任务：
- [ ] 修改PortalHome.vue，调用真实API
- [ ] 移除静态示例数据
- [ ] 添加loading状态
- [ ] 实现订阅表单提交
- [ ] 添加错误处理和fallback

#### 数据库：
- [ ] 创建subscriptions表（存储订阅邮箱）
- [ ] 给articles表添加is_headline字段（标记头条）
- [ ] 给articles表添加view_count字段（统计浏览量）

---

### Phase 2: RSS聚合系统 (3-5天)
**目标：** 自动聚合行业新闻，保持内容新鲜

#### 数据源配置：
```python
RSS_SOURCES = {
    'pharma': [
        {'name': 'NMPA公告', 'url': 'https://www.nmpa.gov.cn/rss.xml', 'type': 'official'},
        {'name': 'FDA药品新闻', 'url': 'https://www.fda.gov/about-fda/contact-fda/stay-informed/rss/drugs/rss.xml', 'type': 'official'},
        {'name': '医药经济报', 'url': '...', 'type': 'industry'},
    ],
    'cosmetics': [
        {'name': 'FDA化妆品', 'url': '...', 'type': 'official'},
        {'name': '中国化妆品', 'url': '...', 'type': 'industry'},
    ],
    'food': [
        {'name': '食品安全网', 'url': '...', 'type': 'industry'},
        {'name': 'FDA食品', 'url': '...', 'type': 'official'},
    ]
}
```

#### 后端任务：
- [ ] 创建RSS解析器 (`app/crawler/rss_parser.py`)
- [ ] 创建RSS调度器（每日定时拉取）
- [ ] 创建去重机制（基于URL）
- [ ] 创建自动分类逻辑
- [ ] 创建内容清洗（HTML→纯文本）
- [ ] 存入articles表

#### 定时任务：
```python
# 每天凌晨2点执行
scheduler.add_job(sync_rss_feeds, 'cron', hour=2)
scheduler.add_job(calculate_hot_articles, 'cron', hour=3)
```

---

### Phase 3: AI内容生成 (5-7天)
**目标：** 自动生成高质量的行业资讯翻译

#### AI模型配置：
```python
AI_MODELS = {
    'primary': {
        'provider': 'nvidia',
        'model': 'deepseek-ai/deepseek-v4-flash',
        'api_key': 'nvapi-xxx',
        'use_for': ['translation', 'summary']
    },
    'secondary': {
        'provider': 'google',
        'model': 'gemma-3-4b-it',
        'api_key': 'AIzaSyxxx',
        'use_for': ['classification', 'tags']
    }
}
```

#### AI生成流程：
```
英文原文 → AI翻译 → AI改写 → AI生成摘要 → AI打标签 → 人工审核(可选) → 发布
```

#### 后端任务：
- [ ] 创建AI调用封装 (`app/ai/content_generator.py`)
- [ ] 创建翻译pipeline
- [ ] 创建审核队列
- [ ] 创建发布工作流
- [ ] 添加质量评估机制

#### 生成内容类型：
1. **FDA警告信解读** - 翻译+深度分析
2. **法规更新速递** - NMPA/FDA新法规解读
3. **行业趋势报告** - AI分析行业数据
4. **技术前沿** - 合成生物学、AI制药等

---

### Phase 4: 高级功能 (第2-3周)
**目标：** 完善用户体验和运营功能

#### 功能列表：
- [ ] 邮件订阅系统（周报推送）
- [ ] 内容推荐算法（基于用户行为）
- [ ] 搜索功能增强（全文检索）
- [ ] 内容审核后台
- [ ] 数据统计后台
- [ ] SEO优化
- [ ] 性能优化（缓存、CDN）

---

## 技术栈

### 后端（现有）：
- FastAPI + SQLAlchemy
- APScheduler（定时任务）
- httpx（爬虫）

### 新增依赖：
```txt
# RSS解析
feedparser>=6.0

# AI调用
httpx>=0.27.0  # 已有

# 邮件发送
aiosmtplib>=3.0

# 内容处理
beautifulsoup4>=4.12.0
markdown>=3.5
```

### 前端（现有）：
- Vue 3 + Vite + Tailwind CSS

---

## 数据库设计

### 新增表：

#### 1. subscriptions（订阅）
```sql
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    sectors TEXT[],  -- 订阅的行业板块
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    last_notified_at TIMESTAMP
);
```

#### 2. content_queue（内容队列）
```sql
CREATE TABLE content_queue (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500),
    content TEXT,
    summary VARCHAR(1000),
    sector VARCHAR(50),
    tags TEXT[],
    source_url VARCHAR(500),
    source_type VARCHAR(20),  -- 'rss', 'ai_generated', 'manual'
    status VARCHAR(20) DEFAULT 'pending',  -- pending, approved, published, rejected
    ai_model VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    published_at TIMESTAMP
);
```

#### 3. 修改articles表：
```sql
ALTER TABLE articles ADD COLUMN is_headline BOOLEAN DEFAULT false;
ALTER TABLE articles ADD COLUMN view_count INTEGER DEFAULT 0;
ALTER TABLE articles ADD COLUMN hot_score FLOAT DEFAULT 0;
```

---

## 实施顺序

### Week 1:
1. ✅ Day 1-2: Phase 1 - 数据库修改 + 后端API + 前端对接
2. Day 3-4: Phase 2基础 - RSS解析器 + 几个主要源
3. Day 5: Phase 2完善 - 自动分类 + 定时任务

### Week 2:
1. Day 1-2: Phase 3基础 - AI翻译封装 + FDA新闻生成
2. Day 3-4: Phase 3完善 - 多模型支持 + 审核队列
3. Day 5: Phase 4部分 - 邮件订阅 + 统计

### Week 3:
1. 测试 + 优化 + 部署

---

## 预期效果

### Phase 1完成后：
- 门户页面展示真实数据
- FDA警告信实时更新
- 订阅功能可用

### Phase 2完成后：
- 每天自动更新20-50条行业新闻
- 覆盖制药/化妆品/食品三大板块
- 内容来源可追溯

### Phase 3完成后：
- 每天AI生成5-10条高质量解读
- FDA警告信自动翻译+分析
- 内容独特性强，SEO友好

---

## 风险与对策

### 1. RSS源不稳定
**对策：** 多源备份 + 失败重试 + 监控告警

### 2. AI生成质量不稳定
**对策：** 多模型fallback + 人工审核 + 质量评分

### 3. 内容版权问题
**对策：** 标注来源 + 改写原创 + 合理使用

### 4. 反爬限制
**对策：** 合理频率 + User-Agent + 代理池（如需要）

---

## 成本估算

### 免费资源利用：
- Google Gemma API: 免费额度
- NVIDIA DeepSeek: 免费额度
- RSS源: 免费

### 服务器成本：
- 现有VPS足够
- 数据库存储: 增长缓慢，无需额外

### 人力成本：
- Phase 1: 1-2天（我来完成）
- Phase 2-3: 可以让Hermes协助
- Phase 4: 按需迭代

---

## 开始实施

现在开始 **Phase 1: 现有数据快速落地**

### 第一步：数据库修改
### 第二步：创建后端API
### 第三步：前端对接
### 第四步：测试验证

Let's go! 🚀
