#!/usr/bin/env node
/**
 * PharmaCos Insight - Content Pipeline Runner
 * 运行采集 → 格式化 → 发布的完整流程
 *
 * Usage:
 *   node scripts/pipeline/run.js                   # 运行制药板块采集
 *   node scripts/pipeline/run.js --dry-run          # 预览模式，不实际发布
 *   node scripts/pipeline/run.js --source=fda       # 只运行FDA采集器
 *   node scripts/pipeline/run.js --source=ema       # 只运行EMA采集器
 *   node scripts/pipeline/run.js --source=pubmed    # 只运行PubMed采集器
 *   node scripts/pipeline/run.js --export           # 只导出文件，不上传VPS
 */

const path = require('path');
const fs = require('fs');
const { formatBatch } = require('./formatter');
const { publish, toArticleText } = require('./publisher');

// 解析命令行参数
const args = process.argv.slice(2);
const dryRun = args.includes('--dry-run');
const exportOnly = args.includes('--export');
const sourceFilter = args.find(a => a.startsWith('--source='))?.split('=')[1];

async function main() {
  console.log('='.repeat(60));
  console.log(`PharmaCos Insight 内容采集管道`);
  console.log(`运行时间: ${new Date().toISOString()}`);
  console.log(`模式: ${dryRun ? '预览(DRY RUN)' : exportOnly ? '仅导出' : '正式运行'}`);
  console.log('='.repeat(60));

  const allArticles = [];
  const collectors = [];

  // 选择采集器
  if (!sourceFilter || sourceFilter === 'fda') {
    collectors.push({ name: 'FDA', fn: require('./collectors/fda').collect });
  }
  if (!sourceFilter || sourceFilter === 'ema') {
    collectors.push({ name: 'EMA', fn: require('./collectors/ema').collect });
  }
  if (!sourceFilter || sourceFilter === 'pubmed') {
    collectors.push({ name: 'PubMed', fn: require('./collectors/pubmed').collect });
  }

  // 执行采集（逐个采集器运行，节省内存）
  for (const collector of collectors) {
    console.log(`\n--- 运行 ${collector.name} 采集器 ---`);
    try {
      const articles = await collector.fn();
      allArticles.push(...articles);
      console.log(`${collector.name}: 采集到 ${articles.length} 篇文章`);
    } catch (e) {
      console.error(`${collector.name} 采集失败:`, e.message);
    }
  }

  if (allArticles.length === 0) {
    console.log('\n没有采集到任何文章，退出');
    process.exit(0);
  }

  // 格式化
  console.log(`\n--- 格式化 ${allArticles.length} 篇文章 ---`);
  const formatted = formatBatch(allArticles);
  console.log(`格式化完成: ${formatted.length} 篇有效文章`);

  // 导出模式：只保存文件
  if (exportOnly) {
    const outPath = path.join(__dirname, '..', '..', 'content', `pipeline_${new Date().toISOString().slice(0, 10)}.txt`);
    fs.writeFileSync(outPath, toArticleText(formatted), 'utf8');
    console.log(`\n已导出到: ${outPath}`);
    formatted.forEach(a => console.log(`  ${a.slug} → ${a.category}`));
    process.exit(0);
  }

  // 发布到VPS
  console.log(`\n--- 发布到VPS ---`);
  const result = await publish(formatted, { dryRun });

  console.log('\n' + '='.repeat(60));
  console.log(`运行完成`);
  console.log(`  采集: ${allArticles.length} 篇`);
  console.log(`  格式化: ${formatted.length} 篇`);
  console.log(`  导入: ${result.imported} 篇`);
  console.log(`  跳过: ${result.skipped} 篇`);
  if (result.preview) console.log(`  预览: ${result.preview} 篇`);
  console.log('='.repeat(60));
}

main().catch(e => {
  console.error('管道运行失败:', e);
  process.exit(1);
});
