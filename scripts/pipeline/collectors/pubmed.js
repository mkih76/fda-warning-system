/**
 * PubMed API Collector
 * 采集制药相关学术文献
 */
const https = require('https');

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
    label: 'GMP实务',
  },
  {
    category: 'quality-control',
    terms: ['HPLC pharmaceutical analysis', 'pharmaceutical quality control method'],
    label: '质量控制',
  },
  {
    category: 'process-validation',
    terms: ['pharmaceutical process validation', 'sterile drug manufacturing validation'],
    label: '工艺验证',
  },
  {
    category: 'pharmacopoeia',
    terms: ['pharmacopoeia monograph update', 'USP EP pharmaceutical standard'],
    label: '药典解读',
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

function translateTitle(title) {
  // 简单的标题处理，保留英文原标题，加中文说明
  return title;
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

          const title = paper.title;
          const slug = `pubmed-${paper.uid}`;
          const authors = (paper.authors || []).map(a => a.name).slice(0, 5).join(', ');
          const journal = paper.fulljournalname || paper.source || '';
          const pubDate = paper.pubdate || '';
          const doi = paper.elocationid || '';

          const summary = title.length > 120 ? title.substring(0, 120) + '...' : title;

          const content = `# ${title}

## 文献信息

| 项目 | 内容 |
|------|------|
| **作者** | ${authors} |
| **期刊** | ${journal} |
| **发表日期** | ${pubDate} |
| **PMID** | ${paper.uid} |
| ${doi ? `**DOI** | ${doi} |` : ''}

## 摘要

${paper.title}

本文献涉及 ${query.label} 领域，收录于 PubMed 数据库（PMID: ${paper.uid}）。

## 对行业从业者的参考价值

本文献为制药行业${query.label}相关的研究论文，可作为以下用途的参考资料：
- 质量管理体系的持续改进
- 培训材料和知识更新
- 合规策略的制定依据

> 数据来源：PubMed / NCBI（PMID: ${paper.uid}）
> 原文可通过 PubMed 获取：https://pubmed.ncbi.nlm.nih.gov/${paper.uid}/`;

          articles.push({
            title: `${query.label}前沿：${title.substring(0, 60)}`,
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
      console.error(`[PubMed] 搜索 "${query.label}" 失败:`, e.message);
    }
  }

  console.log(`[PubMed] 获取 ${articles.length} 篇文献`);
  return articles;
}

module.exports = { collect };
