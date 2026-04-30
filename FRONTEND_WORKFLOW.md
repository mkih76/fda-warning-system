# FDA警告信系统 - 前端优化工作流

## 项目概述
将FDA警告信翻译系统前端优化为专业级合规情报平台。

## 技术栈
- **后端**: FastAPI (端口8790)
- **前端**: Vue 3 + Vite
- **数据库**: SQLite (/root/data/fda_warning.db)
- **域名**: fda.19990419.top (Cloudflare CDN)

## 当前状态
- 后端API已运行
- 基础前端已部署
- 数据库包含984封已翻译警告信

## 优化任务清单

### 1. 翻译查看器 (P0)
- [ ] 中英对照阅读界面
- [ ] 原文/译文切换按钮
- [ ] 段落高亮标记
- [ ] 关键术语标注

### 2. 高级搜索 (P0)
- [ ] 全文搜索 (支持中英文)
- [ ] 按公司名称筛选
- [ ] 按日期范围筛选
- [ ] 按违规类型筛选
- [ ] 按风险等级筛选
- [ ] 按CFR法规筛选

### 3. 公司详情页 (P1)
- [ ] 公司基本信息展示
- [ ] 违规历史列表
- [ ] 风险评级显示
- [ ] 关联警告信链接

### 4. 数据导出 (P1)
- [ ] CSV导出 (支持筛选后导出)
- [ ] PDF报告生成
- [ ] 批量下载

### 5. 仪表盘统计 (P2)
- [ ] 总览卡片 (总数、高风险数等)
- [ ] 违规类型分布图 (饼图)
- [ ] 时间趋势图 (折线图)
- [ ] 地区分布图 (地图)

## 数据库表结构

### warning_letters
```sql
id, fda_id, slug, posted_date, issue_date, company_name, 
issuing_office, subject, fei_number, country, full_text, 
full_text_clean, url, closeout_date, response_date, status
```

### ai_analysis
```sql
id, warning_letter_id, summary_en, summary_zh, key_findings, 
compliance_gap, model_used, analyzed_at, translation_zh, 
violation_type, risk_level
```

### violations
```sql
id, warning_letter_id, system_category, violation_type, 
severity, description, description_zh
```

### cfr_citations
```sql
id, warning_letter_id, cfr_part, cfr_section, cfr_text, citation_raw
```

### company_tracking
```sql
id, company_name, fei_number, event_type, event_date, 
classification, details(JSON), source_url
```

## API端点 (已有)

### 基础
- `GET /api/letters` - 获取警告信列表
- `GET /api/letters/{id}` - 获取单封信详情
- `GET /api/letters/{id}/translation` - 获取翻译

### 搜索
- `GET /api/search?q=keyword` - 全文搜索
- `GET /api/search/company?name=xxx` - 按公司搜索

### 统计
- `GET /api/stats/overview` - 总览统计
- `GET /api/stats/violations` - 违规分布
- `GET /api/stats/timeline` - 时间趋势

### 公司
- `GET /api/companies` - 公司列表
- `GET /api/companies/{name}` - 公司详情
- `GET /api/companies/{name}/letters` - 公司关联信件

## 设计规范

### 色彩
- 主色: #1a73e8 (蓝色)
- 警告: #ea4335 (红色)
- 成功: #34a853 (绿色)
- 背景: #f8f9fa (浅灰)

### 字体
- 标题: Inter, sans-serif
- 正文: system-ui, sans-serif
- 代码: JetBrains Mono, monospace

### 布局
- 响应式设计 (移动端适配)
- 侧边栏导航
- 卡片式内容展示

## 执行步骤

1. **检查现有代码结构**
   ```bash
   ls -la /root/fda-warning-system/frontend/
   cat /root/fda-warning-system/frontend/package.json
   ```

2. **安装依赖**
   ```bash
   cd /root/fda-warning-system/frontend
   npm install
   ```

3. **按优先级实现功能**
   - 先完成P0 (翻译查看器 + 高级搜索)
   - 再完成P1 (公司详情 + 数据导出)
   - 最后P2 (仪表盘)

4. **测试**
   ```bash
   npm run build
   # 检查构建是否成功
   ```

5. **部署**
   ```bash
   # 构建产物会自动同步到部署目录
   # 或手动复制到Caddy服务目录
   ```

## 注意事项
- 保持与现有后端API兼容
- 响应式设计，支持移动端
- 使用中文界面
- 代码注释使用中文
