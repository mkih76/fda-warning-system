/**
 * Article Formatter
 * 统一排版：中文标点、去AI味、格式规范
 */
const config = require('./config');

/**
 * 统一中文标点（在中文语境中）
 */
function fixPunctuation(text) {
  let result = text;

  // 在中文字符之间的英文标点替换为中文标点
  for (const [en, cn] of Object.entries(config.punctuationMap)) {
    // 匹配：中文字符 + 英文标点 + 空格或中文字符
    const regex = new RegExp(`([\\u4e00-\\u9fff])\\s*${en.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\s*`, 'g');
    result = result.replace(regex, `$1${cn}`);
  }

  // 修复：英文括号在中文中 → 中文括号
  result = result.replace(/（/g, '（').replace(/）/g, '）');

  return result;
}

/**
 * 去除AI常用套话
 */
function removeAIPhrases(text) {
  let result = text;
  for (const phrase of config.bannedPhrases) {
    // 替换句首的AI套话（带标点或冒号）
    const regex = new RegExp(`${phrase}[，,：:。.]\\s*`, 'g');
    result = result.replace(regex, '');
  }
  return result;
}

/**
 * 限制列表密度：如果列表太多，合并部分为段落
 */
function limitLists(text) {
  const lines = text.split('\n');
  let listCount = 0;
  let inList = false;
  const result = [];

  for (const line of lines) {
    const isListItem = /^[\s]*[-*•]\s/.test(line) || /^[\s]*\d+[.)]\s/.test(line);

    if (isListItem && !inList) {
      listCount++;
      inList = true;
    } else if (!isListItem) {
      inList = false;
    }

    result.push(line);
  }

  // 如果列表超过5个，不做额外处理（内容本身就需要列表）
  return result.join('\n');
}

/**
 * 确保段落之间有合适的间距
 */
function fixParagraphs(text) {
  // 多个空行 → 两个换行
  let result = text.replace(/\n{3,}/g, '\n\n');
  // 确保标题前后有空行
  result = result.replace(/([^\n])\n(#{1,3}\s)/g, '$1\n\n$2');
  result = result.replace(/(#{1,3}\s[^\n]+)\n([^\n#])/g, '$1\n\n$2');
  return result;
}

/**
 * 验证slug格式
 */
function validateSlug(slug) {
  return slug
    .toLowerCase()
    .replace(/[^a-z0-9\u4e00-\u9fff-]/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
    .substring(0, 100);
}

/**
 * 主格式化函数
 */
function format(article) {
  let content = article.content;

  // 1. 修复标点
  content = fixPunctuation(content);

  // 2. 去AI套话
  content = removeAIPhrases(content);

  // 3. 修复段落间距
  content = fixParagraphs(content);

  // 4. 限制列表
  content = limitLists(content);

  // 5. 验证slug
  const slug = validateSlug(article.slug);

  return {
    ...article,
    slug,
    content: content.trim(),
    summary: fixPunctuation(article.summary || '').substring(0, 200),
    title: fixPunctuation(article.title || ''),
  };
}

/**
 * 批量格式化
 */
function formatBatch(articles) {
  return articles.map(format).filter(a => a.title && a.content && a.slug);
}

module.exports = { format, formatBatch };
