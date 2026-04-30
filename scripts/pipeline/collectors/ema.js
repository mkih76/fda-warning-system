/**
 * EMA (European Medicines Agency) RSS Collector
 * 采集欧洲药品管理局新闻
 */
const https = require('https');

const EMA_RSS = 'https://www.ema.europa.eu/en/news.xml';

function fetchURL(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { timeout: 15000, headers: { 'User-Agent': 'PharmaCosBot/1.0' } }, res => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return fetchURL(res.headers.location).then(resolve).catch(reject);
      }
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

function parseRSSItems(xml) {
  const items = [];
  const parts = xml.split('<item>');
  for (let i = 1; i < parts.length; i++) {
    const block = parts[i].split('</item>')[0];
    const get = (tag) => {
      const m = block.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)<\\/${tag}>`));
      return m ? m[1].replace(/<!\[CDATA\[|\]\]>/g, '').trim() : '';
    };
    items.push({
      title: get('title'),
      link: get('link'),
      description: get('description'),
      pubDate: get('pubDate'),
    });
  }
  return items;
}

function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^\w\u4e00-\u9fff]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .substring(0, 80);
}

function cleanHTML(html) {
  return html
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/p>/gi, '\n\n')
    .replace(/<li>/gi, '- ')
    .replace(/<\/li>/gi, '\n')
    .replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function guessCategory(title, desc) {
  const text = (title + ' ' + desc).toLowerCase();
  if (text.includes('guideline') || text.includes('regulation') || text.includes('legal'))
    return 'regulations';
  if (text.includes('safety') || text.includes('signal') || text.includes('adverse'))
    return 'quality-control';
  if (text.includes('approval') || text.includes('marketing authorisation') || text.includes('positive opinion'))
    return 'registration';
  if (text.includes('gmp') || text.includes('inspect') || text.includes('compliance'))
    return 'gmp-practice';
  return 'industry-news';
}

async function collect(limit = 10) {
  console.log('[EMA] 采集欧洲药管局新闻...');
  const xml = await fetchURL(EMA_RSS);
  const items = parseRSSItems(xml).slice(0, limit);

  const articles = items.map(item => {
    const title = `EMA：${item.title}`;
    const slug = `ema-${slugify(item.title)}`;
    const category = guessCategory(item.title, item.description);
    const desc = cleanHTML(item.description);

    const content = `# ${title}

${desc ? `${desc}` : ''}

## 背景

欧洲药品管理局（EMA）是欧盟负责药品科学评估、监督和安全监测的机构。EMA 的监管决定影响所有欧盟成员国以及欧洲经济区国家。

对于出口欧洲的中国制药企业而言，EMA 的政策动态和监管趋势值得密切关注。

> 来源：EMA 官方新闻（${item.pubDate || '日期未知'}）
> 原文链接：${item.link}`;

    return {
      title,
      slug,
      category,
      summary: desc ? desc.substring(0, 100) : `EMA发布新闻：${item.title}`,
      content,
      access: 'free',
      source: 'ema-rss',
      sourceId: slugify(item.title),
    };
  });

  console.log(`[EMA] 获取 ${articles.length} 篇新闻`);
  return articles;
}

module.exports = { collect };
