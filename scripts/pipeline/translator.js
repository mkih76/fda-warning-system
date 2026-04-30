/**
 * Translation Utility
 * 将英文内容翻译为中文（用于EMA/PubMed等英文源）
 * 使用MyMemory免费翻译API（无需API Key）
 */
const https = require('https');
const http = require('http');

/**
 * HTTP GET 请求
 */
function httpGet(url, timeout = 15000) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? https : http;
    mod.get(url, { timeout, headers: { 'User-Agent': 'Mozilla/5.0' } }, res => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

/**
 * MyMemory翻译API（免费，每日5000字限制）
 */
async function translateViaMyMemory(text, from = 'en', to = 'zh-CN') {
  if (!text || text.trim().length === 0) return text;

  // MyMemory语言代码
  const langMap = { 'en': 'en', 'zh-CN': 'zh-CN' };
  const sl = langMap[from] || from;
  const tl = langMap[to] || to;

  const encoded = encodeURIComponent(text);
  const url = `https://api.mymemory.translated.net/get?q=${encoded}&langpair=${sl}|${tl}`;

  try {
    const data = await httpGet(url);
    const result = JSON.parse(data);
    if (result.responseStatus === 200 && result.responseData?.translatedText) {
      return result.responseData.translatedText;
    }
    console.warn('[翻译] MyMemory返回异常:', result.responseStatus);
    return text;
  } catch (e) {
    console.warn('[翻译] MyMemory请求失败:', e.message);
    return text;
  }
}

/**
 * Google Translate备用端点
 */
async function translateViaGoogle(text, from = 'en', to = 'zh-CN') {
  if (!text || text.trim().length === 0) return text;

  const encoded = encodeURIComponent(text);
  const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${from}&tl=${to}&dt=t&q=${encoded}`;

  try {
    const data = await httpGet(url);
    const result = JSON.parse(data);
    const translated = result[0].map(item => item[0]).join('');
    return translated;
  } catch (e) {
    return null;
  }
}

/**
 * 翻译文本，带备用端点
 */
async function translate(text, from = 'en', to = 'zh-CN') {
  if (!text || text.trim().length === 0) return '';

  // 短文本直接翻译
  if (text.length < 1000) {
    const result = await translateViaMyMemory(text, from, to);
    if (result !== text) return result;
    // 备用
    const google = await translateViaGoogle(text, from, to);
    return google || result;
  }

  // 长文本按段落分段翻译
  const paragraphs = text.split(/\n\n+/);
  const translated = [];

  for (const para of paragraphs) {
    if (para.trim().length === 0) {
      translated.push('');
      continue;
    }
    const result = await translateViaMyMemory(para, from, to);
    translated.push(result);
    // 避免请求过快
    await new Promise(r => setTimeout(r, 300));
  }

  return translated.join('\n\n');
}

/**
 * 翻译文章对象的各个字段
 */
async function translateArticle(article) {
  console.log(`[翻译] 翻译文章: ${article.title?.substring(0, 40)}...`);

  const translated = { ...article };

  if (article.title) {
    translated.title = await translate(article.title);
  }

  if (article.summary) {
    translated.summary = await translate(article.summary);
  }

  if (article.content) {
    translated.content = await translateMarkdown(article.content);
  }

  console.log(`[翻译] 完成: ${translated.title?.substring(0, 40)}`);
  return translated;
}

/**
 * 翻译Markdown内容，保留格式标记
 */
async function translateMarkdown(md) {
  const lines = md.split('\n');
  const result = [];
  let buffer = [];

  async function flushBuffer() {
    if (buffer.length === 0) return;
    const text = buffer.join('\n');
    const translated = await translate(text);
    result.push(translated);
    buffer = [];
  }

  for (const line of lines) {
    const trimmed = line.trim();

    // 表格行
    if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
      await flushBuffer();
      if (/^\|[\s\-:|]+\|$/.test(trimmed)) {
        result.push(line);
        continue;
      }
      const cells = trimmed.slice(1, -1).split('|').map(c => c.trim());
      const translatedCells = [];
      for (const cell of cells) {
        const clean = cell.replace(/\*\*/g, '');
        const t = await translate(clean);
        translatedCells.push(cell.includes('**') ? `**${t}**` : t);
      }
      result.push('| ' + translatedCells.join(' | ') + ' |');
      continue;
    }

    // 标题行
    const headingMatch = trimmed.match(/^(#{1,6})\s+(.+)$/);
    if (headingMatch) {
      await flushBuffer();
      const prefix = headingMatch[1];
      const cleanText = headingMatch[2].replace(/\*\*/g, '').replace(/`/g, '');
      const translated = await translate(cleanText);
      result.push(`${prefix} ${translated}`);
      continue;
    }

    // 引用行
    if (trimmed.startsWith('>')) {
      await flushBuffer();
      const quoteText = trimmed.replace(/^>\s*/, '');
      if (quoteText.trim()) {
        const t = await translate(quoteText);
        result.push(`> ${t}`);
      } else {
        result.push(line);
      }
      continue;
    }

    // 列表项
    const listMatch = trimmed.match(/^([-*•]|\d+[.)])\s+(.+)$/);
    if (listMatch) {
      await flushBuffer();
      const marker = listMatch[1];
      const text = listMatch[2];
      const cleanText = text.replace(/\*\*/g, '');
      const translated = await translate(cleanText);
      let finalText = translated;
      if (text.includes('**') && !translated.includes('**')) {
        finalText = `**${translated}**`;
      }
      result.push(`${marker} ${finalText}`);
      continue;
    }

    // 空行
    if (!trimmed) {
      await flushBuffer();
      result.push('');
      continue;
    }

    // 普通段落
    buffer.push(line);
  }

  await flushBuffer();
  return result.join('\n');
}

module.exports = { translate, translateArticle, translateMarkdown };
