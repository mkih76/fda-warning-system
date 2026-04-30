/**
 * FDA openFDA API Collector
 * 采集药品执法/召回、不良事件等数据 — 翻译为中文，AI分析内容标注
 */
const https = require('https');
const { translate } = require('../translator');

const FDA_BASE = 'https://api.fda.gov';

function fetchJSON(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { timeout: 15000, headers: { 'User-Agent': 'PharmaCosBot/1.0' } }, res => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error(`JSON parse error: ${e.message}`)); }
      });
    }).on('error', reject);
  });
}

function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^\w\u4e00-\u9fff]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .substring(0, 80);
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  const s = dateStr.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3');
  return s;
}

/**
 * 采集药品执法/召回数据
 */
async function collectDrugEnforcement(limit = 10) {
  const url = `${FDA_BASE}/drug/enforcement.json?search=classification:"Class+I"&sort=report_date:desc&limit=${limit}`;
  const data = await fetchJSON(url);

  if (!data.results) return [];

  const articles = [];
  for (const item of data.results) {
    const date = formatDate(item.report_date);
    const firm = item.recalling_firm || '未知企业';
    const reasonEn = item.reason_for_recall || '未说明';
    const productEn = item.product_description || '';
    const distribution = item.distribution_pattern || '';
    const quantity = item.product_quantity || '';

    // 翻译关键字段
    const [reasonZh, productZh] = await Promise.all([
      translate(reasonEn),
      translate(productEn.substring(0, 200)),
    ]);

    const title = `FDA I类药品召回：${productZh.substring(0, 60) || '未命名产品'}`;
    const slug = `fda-recall-${item.recall_number || slugify(title)}`;

    const content = `# ${title}

## 召回概况

${date ? `**报告日期**：${date}` : ''}

**召回企业**：${firm}

**产品描述**：${productZh}

${productEn !== productZh ? `**产品原文**：${productEn}` : ''}

**召回原因**：${reasonZh}

${distribution ? `**分销范围**：${distribution}` : ''}

${quantity ? `**召回数量**：${quantity}` : ''}

## 事件分析

*（以下分析由AI基于公开数据生成，仅供参考）*

本次召回属于 FDA Class I 级别，意味着使用或接触该产品有合理的可能导致严重的不良健康后果或死亡。

FDA 将药品召回分为三个等级：
- **Class I**：最严重，可能导致严重健康后果或死亡
- **Class II**：可能导致暂时或可逆的健康后果
- **Class III**：不太可能导致健康后果，但违反了 FDA 法规

本次召回的直接原因是：${reasonZh}

## 对制药企业的启示

1. 企业应建立完善的质量管理体系，定期进行内部审计
2. 原辅料和成品的质量控制是防止类似事件的关键
3. 发现质量问题后应主动召回，配合 FDA 的监管要求

> **数据来源**：FDA openFDA Drug Enforcement API（召回编号：${item.recall_number || 'N/A'}）
> **原文链接**：[FDA Enforcement Reports](https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts)`;

    articles.push({
      title,
      slug,
      category: 'industry-news',
      summary: `FDA发布I类药品召回通知：${firm}召回${productZh.substring(0, 40)}，原因为${reasonZh.substring(0, 40)}`,
      content,
      access: 'free',
      source: 'fda-openfda',
      sourceId: item.recall_number,
    });
  }

  return articles;
}

/**
 * 采集药品不良事件数据（聚合为分析文章）
 */
async function collectAdverseEvents(limit = 50) {
  const url = `${FDA_BASE}/drug/event.json?search=serious:1+AND+receivedate:[20240101+TO+*]&count=patient.drug.openfda.generic_name.exact&limit=20`;
  const data = await fetchJSON(url);

  if (!data.results) return [];

  // 聚合为Top药物不良事件分析文章
  const top = data.results.filter(r => r.count > 0).slice(0, 15);
  if (top.length === 0) return [];

  const listMarkdown = top
    .map((r, i) => `${i + 1}. **${r.term}** — ${r.count} 例报告`)
    .join('\n');

  const content = `# FDA 药物不良事件年度报告分析：高风险药物盘点

## 数据来源

*（本文由AI基于FDA公开数据自动分析生成，仅供行业参考）*

本文基于 FDA 不良事件报告系统（FAERS）数据，分析近期严重不良事件报告中的高风险药物。

## 不良事件报告数量 Top 15

${listMarkdown}

## 数据解读

FDA 不良事件报告系统（FAERS）是全球最大的药物安全数据库之一。医生、药企和患者均可提交不良事件报告。

**需要注意的几点：**
- 报告数量多不等于药物一定不安全，可能与该药的使用人群基数大有关
- 不良事件报告存在因果关系不确定的问题，部分报告可能只是时间上的巧合
- 企业在收到不良事件信号后应及时开展调查和评估

## 对质量管理人员的建议

1. 关注自家产品的不良事件信号，建立定期查询机制
2. 对比同类产品的安全信号，评估产品的相对安全性
3. 将 FAERS 数据纳入药品风险管理计划（RMP）的参考

> 数据来源：FDA FAERS（openFDA Drug Event API），统计截止至近期最新数据`;

  return [{
    title: 'FDA 药物不良事件年度报告：高风险药物 Top 15 分析',
    slug: 'fda-adverse-events-top-drugs-analysis',
    category: 'quality-control',
    summary: '基于FDA FAERS数据库分析近期严重不良事件报告中的高风险药物，为质量管理人员提供风险参考',
    content,
    access: 'free',
    source: 'fda-openfda',
    sourceId: 'faers-aggregate',
  }];
}

/**
 * 采集药品召回趋势（聚合分析）
 */
async function collectRecallTrends() {
  const url = `${FDA_BASE}/drug/enforcement.json?search=report_date:[20240101+TO+*]&count=classification.exact&limit=10`;
  const data = await fetchJSON(url);

  if (!data.results) return [];

  const byClass = {};
  data.results.forEach(r => { byClass[r.term] = r.count; });
  const total = Object.values(byClass).reduce((a, b) => a + b, 0);

  const content = `# FDA 药品召回趋势分析：${new Date().getFullYear()}年数据回顾

*（本文由AI基于FDA公开数据自动分析生成，仅供行业参考）*

## 召回分级统计

| 召回等级 | 数量 | 占比 | 风险程度 |
|---------|------|------|---------|
| Class I（严重） | ${byClass['Class I'] || 0} | ${((byClass['Class I'] || 0) / total * 100).toFixed(1)}% | 使用或接触可能导致严重伤害或死亡 |
| Class II（中等） | ${byClass['Class II'] || 0} | ${((byClass['Class II'] || 0) / total * 100).toFixed(1)}% | 可能导致暂时或可逆的健康后果 |
| Class III（轻微） | ${byClass['Class III'] || 0} | ${((byClass['Class III'] || 0) / total * 100).toFixed(1)}% | 不太可能导致健康后果 |

总计：${total} 起药品召回事件

## 主要召回原因分析

根据 FDA 执法数据，药品召回的主要原因通常包括：
- **cGMP 违规**：生产过程不符合现行药品生产质量管理规范
- **标签错误**：药品标签信息与实际成分不符
- **交叉污染**：生产设施中不同产品之间的交叉污染
- **稳定性问题**：药品在有效期内质量不达标
- **微生物污染**：无菌产品或非无菌产品的微生物超标

## 启示

药品召回不仅是企业面临的监管风险，更是对患者安全的直接威胁。质量管理体系的有效运行是预防召回的核心。企业应重视偏差管理、CAPA系统和变更控制，从源头降低召回风险。

> **数据来源**：FDA openFDA Drug Enforcement API
> **原文链接**：[FDA Drug Enforcement Reports](https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts)`;

  return [{
    title: `FDA 药品召回趋势分析：${new Date().getFullYear()}年数据回顾`,
    slug: `fda-drug-recall-trends-${new Date().getFullYear()}`,
    category: 'pharma-case-studies',
    summary: `基于FDA执法数据分析${new Date().getFullYear()}年药品召回的分级统计和主要召回原因`,
    content,
    access: 'free',
    source: 'fda-openfda',
    sourceId: 'enforcement-aggregate',
  }];
}

/**
 * 主采集函数
 */
async function collect() {
  const allArticles = [];

  try {
    console.log('[FDA] 采集药品执法/召回数据...');
    const recalls = await collectDrugEnforcement(5);
    allArticles.push(...recalls);
    console.log(`[FDA] 获取 ${recalls.length} 篇召回文章`);
  } catch (e) {
    console.error('[FDA] 召回采集失败:', e.message);
  }

  try {
    console.log('[FDA] 采集不良事件数据...');
    const events = await collectAdverseEvents();
    allArticles.push(...events);
    console.log(`[FDA] 获取 ${events.length} 篇不良事件分析`);
  } catch (e) {
    console.error('[FDA] 不良事件采集失败:', e.message);
  }

  try {
    console.log('[FDA] 采集召回趋势...');
    const trends = await collectRecallTrends();
    allArticles.push(...trends);
    console.log(`[FDA] 获取 ${trends.length} 篇趋势分析`);
  } catch (e) {
    console.error('[FDA] 趋势采集失败:', e.message);
  }

  return allArticles;
}

module.exports = { collect };
