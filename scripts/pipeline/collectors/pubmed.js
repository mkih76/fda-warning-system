/**
 * PubMed API Collector
 * 采集制药学术文献 — 翻译标题为中文，保留原文链接
 */
const https = require('https');
const { translate } = require('../translator');

function fetchJSON(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { timeout: 15000, headers: { 'User-Agent': 'PharmaCosBot/1.0' } }, res => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error(`JSON parse: ${e.message}`)); }
      });
    }).on('error', reject);
  });
}

// 搜索关键词配置，按网站分类
const SEARCH_QUERIES = [
  {
    category: 'gmp-practice',
    terms: ['pharmaceutical manufacturing GMP', 'drug GMP compliance'],
    labelZh: 'GMP实务',
  },
  {
    category: 'quality-control',
    terms: ['HPLC pharmaceutical analysis', 'pharmaceutical quality control method'],
    labelZh: '质量控制',
  },
  {
    category: 'process-validation',
    terms: ['pharmaceutical process validation', 'sterile drug manufacturing validation'],
    labelZh: '工艺验证',
  },
  {
    category: 'pharmacopoeia',
    terms: ['pharmacopoeia monograph update', 'USP EP pharmaceutical standard'],
    labelZh: '药典解读',
  },
];

function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^\w\u4e00-\u9fff]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .substring(0, 80);
}

async function searchPubMed(term, maxResults = 5) {
  const encoded = encodeURIComponent(term);
  const searchUrl = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=${encoded}+AND+2024[pdat]&retmax=${maxResults}&retmode=json`;
  const search = await fetchJSON(searchUrl);
  const ids = search.esearchresult?.idlist || [];
  if (ids.length === 0) return [];

  const fetchUrl = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=${ids.join(',')}&retmode=json`;
  const summary = await fetchJSON(fetchUrl);

  return ids.map(id => summary.result?.[id]).filter(Boolean);
}

async function collect(limit = 8) {
  console.log('[PubMed] 采集制药学术文献...');
  const articles = [];
  const seen = new Set();

  for (const query of SEARCH_QUERIES) {
    try {
      for (const term of query.terms) {
        const results = await searchPubMed(term, 3);
        for (const paper of results) {
          if (!paper.title || seen.has(paper.uid)) continue;
          seen.add(paper.uid);

          const titleEn = paper.title;
          const slug = `pubmed-${paper.uid}`;
          const authors = (paper.authors || []).map(a => a.name).slice(0, 5).join(', ');
          const journal = paper.fulljournalname || paper.source || '';
          const pubDate = paper.pubdate || '';
          const doi = paper.elocationid || '';
          const pubmedUrl = `https://pubmed.ncbi.nlm.nih.gov/${paper.uid}/`;

          // 翻译标题
          console.log(`[PubMed] 翻译: ${titleEn.substring(0, 50)}...`);
          const titleZh = await translate(titleEn);

          const summary = titleZh.length > 120 ? titleZh.substring(0, 120) + '...' : titleZh;

          const content = `# ${query.labelZh}前沿：${titleZh}

## 文献信息

| 项目 | 内容 |
|------|------|
| **作者** | ${authors} |
| **期刊** | ${journal} |
| **发表日期** | ${pubDate} |
| **PMID** | ${paper.uid} |
${doi ? `| **DOI** | ${doi} |` : ''}

## 原始标题（英文）

${titleEn}

## 内容说明

*（本文献信息由AI整理翻译，标题为机器翻译，如需准确表述请参考原文）*

本文献属于${query.labelZh}领域研究论文，收录于 PubMed 数据库。

## 对行业从业者的参考价值

- 可作为质量管理体系持续改进的参考资料
- 可用于培训材料和知识更新
- 可为合规策略的制定提供依据

> **数据来源**：PubMed / NCBI
> **原文链接**：[${titleEn}](${pubmedUrl})`;

          articles.push({
            title: `${query.labelZh}前沿：${titleZh.substring(0, 60)}`,
            slug,
            category: query.category,
            summary,
            content,
            access: 'free',
            source: 'pubmed',
            sourceId: paper.uid,
          });

          if (articles.length >= limit) break;
        }
        if (articles.length >= limit) break;
      }
      if (articles.length >= limit) break;
    } catch (e) {
      console.error(`[PubMed] 搜索 "${query.labelZh}" 失败:`, e.message);
    }
  }

  console.log(`[PubMed] 获取 ${articles.length} 篇文献`);
  return articles;
}

module.exports = { collect };
