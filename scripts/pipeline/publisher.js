/**
 * Article Publisher
 * 将文章推送到VPS：生成文件 → SSH上传 → 执行导入
 */
const { Client } = require('ssh2');
const fs = require('fs');
const path = require('path');
const config = require('./config');

/**
 * 将文章列表转为 ---ARTICLE--- 格式文本
 */
function toArticleText(articles) {
  return articles.map(a => {
    return `---ARTICLE---
TITLE: ${a.title}
SLUG: ${a.slug}
CATEGORY: ${a.category}
SUMMARY: ${a.summary}
ACCESS: ${a.access || 'free'}
CONTENT:
${a.content}
---END---`;
  }).join('\n\n');
}

/**
 * 通过SSH在VPS上执行命令
 */
function sshExec(command) {
  return new Promise((resolve, reject) => {
    const conn = new Client();
    conn.on('ready', () => {
      conn.exec(command, (err, stream) => {
        if (err) { conn.end(); reject(err); return; }
        let out = '', errOut = '';
        stream.on('data', d => out += d);
        stream.stderr.on('data', d => errOut += d);
        stream.on('close', (code) => {
          conn.end();
          resolve({ stdout: out, stderr: errOut, code });
        });
      });
    });
    conn.on('error', reject);
    connectSSH(conn);
  });
}

function connectSSH(conn) {
  conn.connect(config.vps);
}

/**
 * 通过SSH上传文件内容并执行命令
 * 使用base64编码避免stdin挂起问题
 */
function sshUploadAndExec(fileContent, remotePath, command) {
  return new Promise((resolve, reject) => {
    const conn = new Client();
    conn.on('ready', () => {
      const b64 = Buffer.from(fileContent, 'utf8').toString('base64');
      const cmd = `echo '${b64}' | base64 -d > ${remotePath} && ${command}`;
      conn.exec(cmd, (err, stream) => {
        if (err) { conn.end(); reject(err); return; }
        let out = '', errOut = '';
        stream.on('data', d => out += d);
        stream.stderr.on('data', d => errOut += d);
        stream.on('close', (code) => {
          conn.end();
          resolve({ stdout: out, stderr: errOut, code });
        });
      });
    });
    conn.on('error', reject);
    connectSSH(conn);
  });
}

/**
 * 获取VPS数据库中已有的slug列表
 */
async function getExistingSlugs() {
  const script = `import sys
sys.path.insert(0, '/root/fda-warning-system/backend')
from app.models import SessionLocal
from app.models_new import Article
db = SessionLocal()
articles = db.query(Article.slug).all()
for a in articles:
    print(a[0])
db.close()`;

  const remotePath = '/tmp/pipeline_check.py';
  const result = await sshUploadAndExec(
    script,
    remotePath,
    `/root/fda-warning-system/.venv/bin/python ${remotePath}`
  );

  const slugs = result.stdout.split('\n').map(s => s.trim()).filter(Boolean);
  return new Set(slugs);
}

/**
 * 发布文章到VPS
 * @param {Array} articles - 格式化后的文章列表
 * @param {Object} options - { dryRun: boolean }
 */
async function publish(articles, options = {}) {
  const { dryRun = false } = options;

  if (articles.length === 0) {
    console.log('[发布] 没有新文章需要发布');
    return { imported: 0, skipped: 0 };
  }

  // 获取已有的slug，去重
  console.log('[发布] 检查VPS数据库已有文章...');
  const existing = await getExistingSlugs();
  console.log(`[发布] VPS已有 ${existing.size} 篇文章`);

  const newArticles = articles.filter(a => !existing.has(a.slug));
  const skipped = articles.length - newArticles.length;

  if (newArticles.length === 0) {
    console.log(`[发布] 全部 ${articles.length} 篇已存在，无需导入`);
    return { imported: 0, skipped };
  }

  console.log(`[发布] ${newArticles.length} 篇新文章待导入，${skipped} 篇跳过`);

  if (dryRun) {
    console.log('[发布] DRY RUN 模式，不实际导入');
    newArticles.forEach(a => console.log(`  [预览] ${a.title} → ${a.category}`));
    return { imported: 0, skipped, preview: newArticles.length };
  }

  // 生成导入文件内容
  const text = toArticleText(newArticles);
  const remotePath = '/tmp/pipeline_import.txt';
  const importCmd = `cd /root/fda-warning-system && .venv/bin/python -m backend.scripts.import_articles ${remotePath}`;

  console.log(`[发布] 上传 ${newArticles.length} 篇文章到VPS...`);
  const result = await sshUploadAndExec(text, remotePath, importCmd);

  console.log('[发布] 导入结果:');
  console.log(result.stdout);
  if (result.stderr) console.log('警告:', result.stderr);

  // 清理临时文件
  sshExec(`rm -f /tmp/pipeline_import.txt /tmp/pipeline_check.py`).catch(() => {});

  return {
    imported: newArticles.length - (result.stdout.match(/Skipping/g) || []).length,
    skipped: skipped + (result.stdout.match(/Skipping/g) || []).length,
  };
}

module.exports = { publish, getExistingSlugs, toArticleText };
