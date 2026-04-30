# 制药板块内容自动化方案

## 一、目标

实现制药板块内容的自动采集、加工和发布，替代人工逐篇编写。内容质量要求：排版规范、来源真实、不是一眼 AI 生成。

---

## 二、可用数据源

### 第一梯队：结构化 API（最稳定，优先使用）

| 数据源 | 类型 | 内容 | API |
|--------|------|------|-----|
| **FDA openFDA** | JSON API | 药品执法/召回、药品标签、不良事件 | `api.fda.gov/drug/` 各端点 |
| **PubMed** | JSON API | 学术文献摘要、最新研究 | `eutils.ncbi.nlm.nih.gov` |
| **EMA** | RSS | 欧洲药品管理局新闻和公告 | `ema.europa.eu/en/news.xml` |
| **PubChem** | REST API | 化合物/药物分子数据 | `pubchem.ncbi.nlm.nih.gov/rest/pug/` |

### 第二梯队：需要网页抓取

| 数据源 | 内容 | 难度 |
|--------|------|------|
| **NMPA（国家药监局）** | 药品公告、法规、GMP检查通报 | 中等，需处理 JS 渲染 |
| **FDA Warning Letters** | 483观察、警告信详情页 | 简单，HTML 可直接解析 |
| **ISPE/PDA** | 行业指南、技术文章 | 中等，部分内容需登录 |

### 第三梯队：人工筛选 + AI 加工

| 内容类型 | 来源 | AI 角色 |
|----------|------|---------|
| 法规解读 | 官方原文 | 基于原文写中文解读（不是编造） |
| 实验方法 | 文献/药典 | 整理步骤、写操作要点 |
| 案例分析 | FDA 483/Warning Letter | 提取要点、分析根因 |

---

## 三、内容分类映射

将抓取的内容自动映射到网站分类：

| 网站分类 | 内容来源 |
|----------|----------|
| `industry-news` 行业动态 | EMA RSS + FDA 新闻 + NMPA 公告 |
| `regulations` 政策法规 | FDA 新规 + NMPA 法规 + ICH 指南 |
| `gmp-practice` GMP 实务 | FDA 483 案例 + AI 解读 |
| `pharmacopoeia` 药典解读 | USP/EP/ChP 更新 + AI 分析 |
| `registration` 注册申报 | FDA ANDA/NDA 批准信息 |
| `quality-control` 质量控制 | PubMed 实验方法文献 |
| `process-validation` 工艺验证 | ISPE/PDA 文章 + AI 整理 |
| `pharma-case-studies` 案例研究 | FDA Warning Letters 深度分析 |

---

## 四、系统架构

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────┐
│  数据源采集   │ ──→ │  内容处理队列  │ ──→ │  格式化+去重  │ ──→ │ API 导入  │
│  (定时任务)   │     │  (待审核文章)  │     │  (统一排版)  │     │ (网站DB) │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────┘
     │                     │
     │                     ▼
     │              ┌──────────────┐
     └────────────→ │  AI 加工(可选) │
                    │  解读/翻译/摘要 │
                    └──────────────┘
```

### 组件拆分：

**1. 采集器（`scripts/collectors/`）**
- `fda_collector.py` — 调 openFDA API，抓取执法、标签、不良事件
- `ema_collector.py` — 解析 EMA RSS feed
- `pubmed_collector.py` — 按关键词搜索最新文献
- `nmpa_collector.py` — 抓取 NMPA 公告页（后期）

**2. 内容处理器（`scripts/processors/`）**
- `article_formatter.py` — 统一排版：中文标点、段落结构、去掉 AI 痕迹
- `deduplicator.py` — 去重：按 slug/title 查重，跳过已导入的
- `categorizer.py` — 自动分类：根据内容关键词匹配分类 slug

**3. AI 加工层（`scripts/ai/`）**
- `regulation_analyzer.py` — 法规原文 → 中文解读文章
- `case_study_writer.py` — Warning Letter 数据 → 案例分析
- `method_summarizer.py` — PubMed 摘要 → 实验方法概要

**4. 导入器（`scripts/publishers/`）**
- `article_publisher.py` — 调网站 API 导入文章（替代手动 docker exec）

**5. 调度器**
- `scheduler.py` — 定时执行：每天凌晨跑一次采集 + 处理 + 发布

---

## 五、排版规范（解决 AI 味问题）

### 问题
- 中英文标点混用（, vs ，）
- 列表堆砌，像 PPT 不像文章
- 段落太短，每段一两句话
- "综上所述"、"值得注意的是" 等 AI 套话

### 解决方案
1. **标点统一**：全部用中文标点（，。；：），英文术语/缩写除外
2. **段落长度**：每段 3-5 句，有完整论述
3. **列表限制**：一篇文章最多 2-3 个列表，其余用段落
4. **禁用词库**：维护一份 AI 常用但人不写的词，自动替换
5. **引用标注**：标注数据来源（FDA 文件编号、PubMed PMID 等）

---

## 六、实施计划

### 第一步：基础框架（1-2天）
- [ ] 搭建项目结构 `scripts/collectors/`, `processors/`, `publishers/`
- [ ] 实现 FDA openFDA 采集器（药品执法数据）
- [ ] 实现文章格式化器（排版统一）
- [ ] 实现去重逻辑

### 第二步：核心采集（1-2天）
- [ ] EMA RSS 采集器
- [ ] PubMed 文献采集器
- [ ] 自动分类器
- [ ] VPS 导入 API 端点

### 第三步：AI 加工（1天）
- [ ] 法规解读生成器（基于真实原文）
- [ ] 案例分析生成器（基于 483 数据）
- [ ] 排版后处理（去 AI 味）

### 第四步：自动化运行（1天）
- [ ] 定时任务配置
- [ ] 错误重试机制
- [ ] 运行日志

### 第五步：扩展（后期）
- [ ] NMPA 网页抓取
- [ ] 更多数据源接入
- [ ] 人工审核流程（可选）

---

## 七、效果预期

| 指标 | 现状 | 目标 |
|------|------|------|
| 制药板块文章数 | 10 篇 | 50+ 篇（1个月内） |
| 更新频率 | 手动，不定期 | 每天自动更新 2-3 篇 |
| 内容来源 | 纯 AI 生成 | 80% 真实来源 + 20% AI 加工 |
| 排版质量 | AI 味明显 | 统一规范，无法一眼看出 AI |

---

## 八、运行方式

开发在本地进行，脚本通过 API 推送到 VPS。

```bash
# 本地运行采集
cd fda-warning-system
python scripts/scheduler.py --sector pharma --dry-run  # 先预览不发布
python scripts/scheduler.py --sector pharma             # 确认后发布

# VPS 端需要新增一个 API 端点
POST /api/admin/articles/import
Body: { articles: [{title, slug, category, summary, content, access}] }
```
