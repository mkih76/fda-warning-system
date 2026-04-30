# FDA警告信翻译系统 — Agent规则手册

> 本文件定义每个Agent的职责、输入输出、约束条件和质量标准。
> 所有Agent必须严格遵守本规则，不得擅自偏离。

---

## 📋 Agent概览

| Agent | 文件 | 职责 | 优先级 |
|-------|------|------|--------|
| **1. 原文预处理Agent** | `scripts/clean_fulltext.py` | 清洗FDA原文，移除网页残留 | 🔴 高 |
| **2. 翻译Agent** | `batch_translate_v2.py` | 将英文翻译为中文 | 🔴 高 |
| **3. 质量校验Agent** | `scripts/validate_translation.py` | 评估翻译质量并分级 | 🔴 高 |
| **4. 监控Agent** | `cron_f53bf284cfce` | 监控翻译进度和进程状态 | 🟡 中 |
| **5. 数据采集Agent** | 爬虫脚本 | 从FDA官网获取新信件 | 🟡 中 |

---

## 🧹 Agent 1：原文预处理Agent

**文件**：`scripts/clean_fulltext.py`
**输入**：`warning_letters.full_text`（原始HTML/文本）
**输出**：`warning_letters.full_text_clean`（清洗后纯文本）

### 1.1 职责

从FDA网页抓取的原文中移除所有非正文内容，保留纯法律信函正文。

### 1.2 处理规则

```
必须移除：
├── HTML标签和实体（<div>, &nbsp; 等）
├── 导航栏文字（"跳至主要内容", "Skip to main content" 等）
├── 面包屑导航（"首页 > 检查 > 合规 > 警告信"）
├── 页脚内容（"1-888-INFO-FDA", "返回顶部" 等）
├── 社交媒体链接（"在Facebook上关注FDA" 等）
└── 订阅/联系信息（"订阅FDA RSS", "Contact FDA" 等）

必须保留：
├── 信函日期（"April 15, 2026"）
├── 收件人称呼（"Dear Mr. Smith:"）
├── 正文段落（逐段保留）
├── CFR法规引用（"21 CFR 211.68"）
├── 签名块（"Sincerely, [Name]"）
└── 所有法律术语和编号
```

### 1.3 质量标准

| 检查项 | 通过标准 | 失败处理 |
|--------|----------|----------|
| 清洗率 | 移除内容 < 原文20% | 记录警告，继续处理 |
| 正文保留 | 长度 > 原文50% | 标记为异常，人工复查 |
| 空行处理 | 连续空行合并为1个 | 自动修复 |

### 1.4 错误处理

```python
# 输入为空
if not text:
    return text  # 直接返回，不报错

# 清洗后过短（<100字）
if len(cleaned) < 100:
    log.warning(f"清洗后原文过短: {len(cleaned)}字")
    return cleaned  # 仍然保存，让翻译Agent决定是否跳过
```

---

## 🌐 Agent 2：翻译Agent

**文件**：`batch_translate_v2.py`
**输入**：`warning_letters.full_text_clean`（清洗后英文）
**输出**：`ai_analysis.translation_zh`（中文翻译）

### 2.1 职责

将FDA警告信从英文逐句翻译为中文，保持原文结构和法律术语准确性。

### 2.2 翻译Prompt规范

```python
TRANSLATE_PROMPT = """你是一名专业的FDA法规文件翻译员。请严格按以下要求将FDA警告信翻译为中文：

【核心原则】
1. 逐句翻译：每一句英文原文都必须翻译为对应中文，不得遗漏
2. 禁止添加：不得添加原文没有的内容，包括：总结、概括、评价、注释、补充说明
3. 禁止省略：不得省略任何原文内容，包括法律条文引用、地址、日期、编号
4. 保留格式：保留原文的段落结构、换行位置、缩进层次
5. 保留专有名词：FDA、CGMP、21 CFR、FD&C Act等法规术语保留英文原文
6. 保留原文英文：人名、公司名、街道地址保留英文原文
7. 仅输出翻译：只输出翻译结果，不输出任何额外说明、标签或格式标记

【禁止出现的词汇】
- "总之"、"综上所述"、"概括来说"、"简而言之"
- "值得注意的是"、"需要指出"、"关键要点"、"主要发现"
- 任何原文中没有的总结性或评论性语句

请翻译以下FDA警告信正文：

"""
```

### 2.3 模型使用规则

```python
# 模型优先级（按翻译质量排序）
MODEL_PRIORITY = [
    'deepseek-ai/deepseek-v4-pro',      # 最高优先级
    'deepseek-ai/deepseek-v4-flash',     # 次高优先级
    'meta/llama-3.3-70b-instruct',       # 第三优先级
    'nvidia/llama-3.1-nemotron-70b-instruct',
    'nvidia/llama-3.3-nemotron-super-49b-v1',
    'nvidia/llama-3.1-nemotron-ultra-253b-v1',
    'mistralai/mistral-large-3-675b-instruct-2512',
    'qwen/qwen3.5-122b-a10b',
]

# API Key轮询规则
# - 每次请求使用不同的Key（循环轮询）
# - 遇到429/401错误时，切换到下一个Key
# - 所有Key都失败时，等待60秒后重试

# 模型切换规则
# - 单次请求超时（30秒）→ 切换到下一个模型
# - 返回空结果 → 切换到下一个模型
# - 返回错误 → 记录日志，切换到下一个模型
```

### 2.4 处理流程

```python
def translate_one(text, max_retries=4):
    """
    翻译单封信件
    
    流程：
    1. 截取前10000字（NVIDIA NIM上下文限制）
    2. 拼接翻译Prompt
    3. 调用API（带重试）
    4. 返回翻译结果
    
    返回：(translation, model_name) 或 (None, None)
    """
    
    # 截断处理
    if len(text) > 10000:
        text = text[:10000] + '\n\n[...文本过长已截断...]'
    
    prompt = TRANSLATE_PROMPT + text
    
    for attempt in range(max_retries):
        model = get_model()  # 轮询获取模型
        api_key = get_key()  # 轮询获取Key
        
        try:
            # 调用API
            result = call_nvidia_api(model, api_key, prompt)
            
            # 验证结果
            if result and len(result) > 100:
                return result, model
            else:
                log.warning(f"翻译结果过短: {len(result) if result else 0}字")
                continue
                
        except TimeoutError:
            log.warning(f"翻译超时: model={model}, attempt={attempt}")
            continue
            
        except APIError as e:
            if e.status == 429:  # Rate limit
                time.sleep(5)
                continue
            elif e.status == 401:  # Auth error
                log.error(f"API Key无效: {api_key[:20]}...")
                continue
            else:
                log.error(f"API错误: {e}")
                continue
    
    return None, None  # 所有重试失败
```

### 2.5 质量控制规则

```python
# 翻译后立即校验
score, issues = validate_translation(translation, original)

# 质量阈值
if score < 60:
    # 评分太低，标记但仍保存（允许后续人工重翻）
    log.warning(f"翻译质量过低: {score}分 ({grade})")
    stats['low_quality'] += 1

# 保存到数据库
save_to_db(letter_id, translation, model)
```

### 2.6 并发控制

```python
# 线程配置
MAX_WORKERS = 5  # 最大并发数

# 数据库写入锁
db_lock = threading.Lock()

def save_to_db(letter_id, translation, model):
    with db_lock:
        conn = sqlite3.connect(DB)
        conn.execute(
            'UPDATE ai_analysis SET translation_zh = ?, model_used = ? WHERE warning_letter_id = ?',
            (translation, model, letter_id)
        )
        conn.commit()
        conn.close()
```

### 2.7 错误处理

```python
# 进程级错误处理
try:
    main()
except KeyboardInterrupt:
    log.info("用户中断，正在保存进度...")
    save_progress()
    sys.exit(0)
except Exception as e:
    log.error(f"未预期错误: {e}", exc_info=True)
    sys.exit(1)

# 单封信件错误处理（不影响其他信件）
try:
    result = process_one(row)
except Exception as e:
    log.error(f"处理信件失败: {row[1]} - {e}")
    stats['error'] += 1
    continue  # 继续处理下一封
```

---

## ✅ Agent 3：质量校验Agent

**文件**：`scripts/validate_translation.py`
**输入**：`(zh_text, en_text)` 中文翻译和英文原文
**输出**：`(score, issues)` 评分和问题列表

### 3.1 职责

评估翻译质量，输出0-100分评分和A-F等级。

### 3.2 评分维度

```python
# 评分权重
SCORING = {
    'length_ratio': 30,      # 长度比检查（30分）
    'ai_markers': 25,        # AI总结词检查（25分）
    'nav_residual': 25,      # 导航残留检查（25分）
    'paragraph_consistency': 20,  # 段落一致性（20分）
}

# 额外扣分项
PENALTIES = {
    'english_ratio': 15,     # 英文比例过高（-15分）
    'min_length': 20,        # 最小长度不足（-20分）
}
```

### 3.3 检查规则

#### 规则1：长度比检查（30分）

```python
ratio = len(zh_text) / len(en_text)

# 判断标准
if ratio < 0.2:
    # 翻译严重过短（可能截断或遗漏）
    score -= 30
    issues.append(f'翻译过短: {ratio:.2f}')
    
elif ratio < 0.3:
    # 翻译偏短（可能遗漏段落）
    score -= 15
    issues.append(f'翻译偏短: {ratio:.2f}')
    
elif ratio > 0.9:
    # 翻译偏长（可能添加了内容）
    score -= 10
    issues.append(f'翻译偏长: {ratio:.2f}')

# 正常范围：0.3 ≤ ratio ≤ 0.9
```

#### 规则2：AI总结词检查（25分）

```python
AI_MARKERS = [
    '总之', '综上所述', '总结', '概括来说', '简而言之',
    '值得注意的是', '需要指出', '关键要点', '主要发现',
    '总的来说', '简单来说', '概括地说', '总结如下',
    '总而言之', '概括而言', '要而言之',
]

# 检查逻辑
found = [m for m in AI_MARKERS if m in zh_text]
if found:
    score -= 25
    issues.append(f'发现AI总结词: {", ".join(found[:5])}')
```

#### 规则3：导航残留检查（25分）

```python
NAV_MARKERS = [
    '跳至', '跳转到', '首页', '主页', '返回顶部',
    '在Facebook上', '在X上', '在Instagram上', '在LinkedIn上',
    '订阅FDA', '联系电话', '返回FDA',
]

FOOTER_MARKERS = [
    '1-888-INFO-FDA', '返回顶部', '反馈 联系FDA',
    'Follow FDA', 'Subscribe to FDA', 'Back to Top',
]

# 检查逻辑
found_nav = [m for m in NAV_MARKERS if m in zh_text]
found_footer = [m for m in FOOTER_MARKERS if m in zh_text]

if found_nav:
    score -= 15
    issues.append(f'发现导航残留: {", ".join(found_nav[:5])}')
if found_footer:
    score -= 10
    issues.append(f'发现页脚残留: {", ".join(found_footer[:3])}')
```

#### 规则4：段落一致性检查（20分）

```python
en_paras = len([p for p in en_text.split('\n\n') if p.strip()])
zh_paras = len([p for p in zh_text.split('\n\n') if p.strip()])

para_ratio = zh_paras / en_paras if en_paras > 0 else 1

if para_ratio < 0.5 or para_ratio > 2.0:
    # 段落数差异过大（可能丢失或添加段落）
    score -= 20
    issues.append(f'段落数差异过大: 英文{en_paras}段, 中文{zh_paras}段')
    
elif para_ratio < 0.7 or para_ratio > 1.5:
    # 段落数差异较大
    score -= 10
    issues.append(f'段落数差异较大: 英文{en_paras}段, 中文{zh_paras}段')
```

### 3.4 等级划分

```python
def quality_grade(score):
    """
    质量等级划分
    
    A (优秀): 90-100分 — 可直接使用
    B (良好): 80-89分 — 基本可用，轻微瑕疵
    C (合格): 70-79分 — 需人工审核
    D (较差): 60-69分 — 需要重翻
    F (不合格): <60分 — 必须重翻
    """
    if score >= 90: return 'A'
    if score >= 80: return 'B'
    if score >= 70: return 'C'
    if score >= 60: return 'D'
    return 'F'
```

---

## 📊 Agent 4：监控Agent

**文件**：Cron Job `f53bf284cfce`
**输入**：无（定时触发）
**输出**：进度报告（发送到Telegram）

### 4.1 职责

定时检查翻译进度、进程状态、质量分布，发现异常及时告警。

### 4.2 监控指标

```python
# 必须监控的指标
METRICS = {
    # 进度指标
    'total_letters': 986,           # 总信件数
    'translated_count': 0,          # 已翻译数
    'progress_pct': 0,              # 进度百分比
    
    # 质量指标
    'grade_a': 0,                   # A级数量
    'grade_b': 0,                   # B级数量
    'grade_c': 0,                   # C级数量
    'grade_d': 0,                   # D级数量
    'grade_f': 0,                   # F级数量
    
    # 进程指标
    'process_count': 0,             # 运行中的进程数
    'process_status': '',           # 进程状态
    'cpu_usage': 0,                 # CPU使用率
    'memory_usage': 0,              # 内存使用量
    
    # API指标
    'api_calls': 0,                 # API调用次数
    'api_errors': 0,                # API错误次数
    'avg_latency': 0,               # 平均延迟
}
```

### 4.3 告警规则

```python
# 告警条件
ALERTS = {
    # 严重告警（立即通知）
    'process_count > 1': '发现重复进程！可能导致数据竞争',
    'process_status == "Z"': '进程变为僵尸状态，需要重启',
    'grade_f > 50%': 'F级翻译占比过高，需要检查翻译质量',
    
    # 警告告警（汇总通知）
    'progress_stall > 30min': '翻译进度停滞超过30分钟',
    'api_error_rate > 10%': 'API错误率超过10%',
    'grade_d > 30%': 'D级翻译占比偏高',
    
    # 信息告警（仅记录）
    'translation_complete': '翻译任务完成',
    'quality_check_complete': '质量检查完成',
}
```

### 4.4 报告格式

```markdown
# FDA警告信翻译进度报告

## 📊 翻译质量分布（{total}封）

| 等级 | 数量 | 占比 | 趋势 |
|------|------|------|------|
| **A** (优秀) | {a_count}封 | {a_pct}% | ↑ +{a_trend} |
| **B** (良好) | {b_count}封 | {b_pct}% | ↑ +{b_trend} |
| **C** (合格) | {c_count}封 | {c_pct}% | ↓ -{c_trend} |
| **D** (较差) | {d_count}封 | {d_pct}% | ↑ +{d_trend} |
| **F** (不合格) | {f_count}封 | {f_pct}% | ↓ -{f_trend} |

总问题信件：{problem_count}封（{total}封中有问题）

## ⚙️ 进程状态

- PID {pid}：{status}，状态 {state}，CPU {cpu}%，RSS {memory}MB，已运行 ~{runtime}
- ⚠️ 发现重复进程：PID {dup_pid} 也在运行

## 🔍 关键发现

1. {finding_1}
2. {finding_2}
3. {finding_3}

## 💡 建议

1. {recommendation_1}
2. {recommendation_2}
```

---

## 🔍 Agent 5：数据采集Agent

**文件**：爬虫脚本（待开发）
**输入**：FDA官网警告信列表
**输出**：`warning_letters` 表（新增记录）

### 5.1 职责

从FDA官网抓取新的警告信，补充全文内容到数据库。

### 5.2 抓取规则

```python
# 数据源
FDA_URL = "https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters"

# 抓取策略
STRATEGY = {
    # 1. 首先抓取列表页
    'list_pages': range(1, 50),  # 前50页
    
    # 2. 逐个抓取详情页
    'detail_page': True,
    
    # 3. 优先抓取缺失全文的信件
    'priority': 'missing_fulltext',
    
    # 4. 支持PDF下载
    'download_pdf': True,
    
    # 5. PDF转文本
    'pdf_to_text': True,
}
```

### 5.3 数据验证规则

```python
# 必须验证的字段
REQUIRED_FIELDS = [
    'fda_id',           # FDA编号（必须唯一）
    'posted_date',      # 发布日期（必须有效）
    'company_name',     # 公司名称（不能为空）
    'full_text',        # 全文内容（必须>100字）
]

# 可选字段
OPTIONAL_FIELDS = [
    'issue_date',       # 签发日期
    'issuing_office',   # 签发办公室
    'subject',          # 主题
    'fei_number',       # FEI编号
    'country',          # 国家
    'url',              # 原始URL
]

# 数据清洗规则
CLEANING = {
    # 移除HTML标签
    'remove_html': True,
    
    # 标准化日期格式
    'normalize_date': '%Y-%m-%d',
    
    # 去除首尾空白
    'strip_whitespace': True,
    
    # 合并连续空行
    'merge_blank_lines': True,
}
```

### 5.4 增量更新规则

```python
# 检查是否已存在
def check_exists(fda_id):
    """检查信件是否已存在于数据库"""
    conn = sqlite3.connect(DB)
    count = conn.execute(
        'SELECT COUNT(*) FROM warning_letters WHERE fda_id = ?', 
        (fda_id,)
    ).fetchone()[0]
    conn.close()
    return count > 0

# 增量更新逻辑
def incremental_update():
    """增量更新：只抓取新信件"""
    # 1. 获取最新信件的fda_id
    latest_id = get_latest_fda_id()
    
    # 2. 抓取列表页，直到遇到已存在的fda_id
    for page in range(1, 100):
        letters = scrape_list_page(page)
        for letter in letters:
            if letter['fda_id'] <= latest_id:
                return  # 已到达已存在的信件
            if not check_exists(letter['fda_id']):
                save_letter(letter)
```

---

## 🔄 Agent协作流程

### 5.1 完整流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                    FDA警告信翻译系统流程                          │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  数据采集     │───→│  原文预处理   │───→│  批量翻译     │
│  Agent 5     │    │  Agent 1     │    │  Agent 2     │
└──────────────┘    └──────────────┘    └──────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ warning_     │    │ full_text_   │    │ translation_ │
│ letters      │    │ clean        │    │ zh           │
└──────────────┘    └──────────────┘    └──────────────┘
                                                 │
                                                 ▼
                                        ┌──────────────┐
                                        │  质量校验     │
                                        │  Agent 3     │
                                        └──────────────┘
                                                 │
                                                 ▼
                                        ┌──────────────┐
                                        │  监控告警     │
                                        │  Agent 4     │
                                        └──────────────┘
```

### 5.2 数据流转规则

```python
# Agent间数据传递规则
DATA_FLOW = {
    # Agent 5 → Agent 1
    'agent5_to_agent1': {
        'trigger': '新信件入库',
        'data': 'warning_letters.full_text',
        'action': '触发预处理',
    },
    
    # Agent 1 → Agent 2
    'agent1_to_agent2': {
        'trigger': '预处理完成',
        'data': 'warning_letters.full_text_clean',
        'action': '加入翻译队列',
    },
    
    # Agent 2 → Agent 3
    'agent2_to_agent3': {
        'trigger': '翻译完成',
        'data': 'ai_analysis.translation_zh',
        'action': '触发质量校验',
    },
    
    # Agent 3 → Agent 4
    'agent3_to_agent4': {
        'trigger': '质量校验完成',
        'data': 'quality_score, grade',
        'action': '更新监控指标',
    },
}
```

---

## 🛡️ 安全与容错规则

### 6.1 API Key安全

```python
# API Key存储规则
API_KEY_RULES = {
    # 1. 不得硬编码在代码中
    'no_hardcode': True,
    
    # 2. 使用环境变量或加密存储
    'use_env_vars': True,
    
    # 3. Key轮询时记录使用日志
    'log_usage': True,
    
    # 4. 遇到401错误立即切换Key
    'switch_on_auth_error': True,
    
    # 5. 所有Key都失败时暂停执行
    'pause_on_all_fail': True,
}
```

### 6.2 数据库安全

```python
# 数据库操作规则
DB_RULES = {
    # 1. 所有写操作必须使用事务
    'use_transactions': True,
    
    # 2. 并发写入必须加锁
    'use_locks': True,
    
    # 3. 定期备份数据库
    'backup_interval': 'daily',
    
    # 4. 操作前验证数据完整性
    'validate_before_write': True,
    
    # 5. 记录所有写操作日志
    'log_all_writes': True,
}
```

### 6.3 进程管理规则

```python
# 进程管理规则
PROCESS_RULES = {
    # 1. 启动前检查是否已有实例运行
    'check_existing_process': True,
    
    # 2. 使用PID文件防止重复启动
    'use_pid_file': True,
    
    # 3. 支持优雅停止（SIGTERM）
    'graceful_shutdown': True,
    
    # 4. 异常退出时自动重启
    'auto_restart': True,
    
    # 5. 记录进程生命周期日志
    'log_lifecycle': True,
}
```

---

## 📝 日志规范

### 7.1 日志级别

```python
# 日志级别定义
LOG_LEVELS = {
    'DEBUG': '详细调试信息（仅开发环境）',
    'INFO': '一般信息（正常运行）',
    'WARNING': '警告信息（需要关注）',
    'ERROR': '错误信息（需要处理）',
    'CRITICAL': '严重错误（需要立即处理）',
}

# 使用场景
LOG_USAGE = {
    'DEBUG': '变量值、API请求/响应详情',
    'INFO': '任务开始/完成、进度更新',
    'WARNING': '翻译质量低、API延迟高',
    'ERROR': 'API调用失败、数据库错误',
    'CRITICAL': '进程崩溃、数据丢失',
}
```

### 7.2 日志格式

```python
# 标准日志格式
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# 示例输出
# 2026-04-29 15:30:45 - batch_translate - INFO - 开始翻译: letter_id=179, fda_id=2026-WL-001
# 2026-04-29 15:31:12 - batch_translate - WARNING - 翻译质量低: score=55, grade=F
# 2026-04-29 15:31:15 - batch_translate - ERROR - API调用失败: 429 Rate limit exceeded
```

---

## ✅ 检查清单

### Agent 1（原文预处理）检查清单

- [ ] HTML标签已移除
- [ ] 导航栏文字已移除
- [ ] 页脚内容已移除
- [ ] 面包屑导航已移除
- [ ] 社交媒体链接已移除
- [ ] 正文段落完整保留
- [ ] 法规引用完整保留
- [ ] 签名块完整保留
- [ ] 清洗后长度 > 原文50%

### Agent 2（翻译）检查清单

- [ ] 翻译Prompt符合规范
- [ ] 模型按优先级使用
- [ ] API Key正确轮询
- [ ] 重试机制正常工作
- [ ] 翻译结果已保存到数据库
- [ ] 并发控制正常
- [ ] 错误处理正常
- [ ] 日志记录完整

### Agent 3（质量校验）检查清单

- [ ] 长度比检查正确
- [ ] AI总结词检查正确
- [ ] 导航残留检查正确
- [ ] 段落一致性检查正确
- [ ] 英文比例检查正确
- [ ] 最小长度检查正确
- [ ] 评分计算正确
- [ ] 等级划分正确

### Agent 4（监控）检查清单

- [ ] 进度指标正确采集
- [ ] 质量指标正确计算
- [ ] 进程状态正确检测
- [ ] 告警规则正确触发
- [ ] 报告格式正确生成
- [ ] 消息正确发送到Telegram

### Agent 5（数据采集）检查清单

- [ ] FDA官网可访问
- [ ] 列表页抓取正常
- [ ] 详情页抓取正常
- [ ] PDF下载正常
- [ ] PDF转文本正常
- [ ] 数据验证正常
- [ ] 增量更新正常
- [ ] 去重逻辑正常

---

## 📚 附录

### A. 常见问题处理

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 翻译质量低 | 模型不遵循指令 | 切换到更强模型（DeepSeek-v4-pro） |
| API调用失败 | Key无效或配额耗尽 | 切换到下一个Key，或等待配额重置 |
| 进程卡死 | 网络超时或死锁 | 重启进程，检查网络连接 |
| 数据库锁 | 并发写入冲突 | 加大锁等待时间，减少并发数 |
| 翻译过短 | 文本被截断 | 检查原文长度，调整截断阈值 |

### B. 性能优化建议

1. **批量处理**：将多封信件合并为单次API调用
2. **异步IO**：使用asyncio替代多线程
3. **缓存机制**：缓存已翻译的结果，避免重复翻译
4. **优先级队列**：优先处理高质量潜力的信件
5. **资源监控**：实时监控API配额和系统资源

---

*规则版本：v1.0*
*更新日期：2026-04-29*
*适用项目：FDA Warning Letter 中文翻译系统*
