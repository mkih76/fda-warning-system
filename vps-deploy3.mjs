import { Client } from 'ssh2';

const conn = new Client();
const VENV = '/root/fda-warning-system/.venv/bin';
const NODE = '/root/.hermes/node/bin/node';
const NPM = '/root/.hermes/node/lib/node_modules/npm/bin/npm';

const commands = [
  // 1. Git pull already done, verify
  'cd /root/fda-warning-system && git log --oneline -3',

  // 2. Build frontend
  `cd /root/fda-warning-system/frontend && ${NPM} install 2>&1 | tail -5`,
  `cd /root/fda-warning-system/frontend && ${NPM} run build 2>&1 | tail -5`,

  // 3. Install new Python dependencies
  `cd /root/fda-warning-system && ${VENV}/pip install -r backend/requirements.txt 2>&1 | tail -5`,

  // 4. Restart backend service
  'systemctl restart fda-backend && sleep 3 && systemctl status fda-backend --no-pager | head -10',

  // 5. Health check
  'sleep 2 && curl -s http://localhost:8790/api/health',

  // 6. Run seed data
  `cd /root/fda-warning-system && ${VENV}/python -m backend.scripts.seed_data 2>&1`,

  // 7. Import articles
  `cd /root/fda-warning-system && ${VENV}/python -m backend.scripts.import_articles content/pharma_articles.txt 2>&1`,
  `cd /root/fda-warning-system && ${VENV}/python -m backend.scripts.import_articles content/cosmetics_articles.txt 2>&1`,
  `cd /root/fda-warning-system && ${VENV}/python -m backend.scripts.import_articles content/food_articles.txt 2>&1`,

  // 8. Final verification
  'curl -s http://localhost:8790/api/content/articles?page_size=3',
  'curl -s http://localhost:8790/api/categories | python3 -c "import sys,json; cats=json.load(sys.stdin); print(f\'Categories: {len(cats)}\')"',
];

conn.on('ready', () => {
  console.log('✅ SSH connected to VPS!\n');
  runCommands(conn, 0);
}).on('error', (err) => {
  console.error('❌ SSH error:', err.message);
}).connect({
  host: '23.94.206.159',
  port: 22,
  username: 'root',
  password: 'Cmh@13579',
  readyTimeout: 15000,
});

function runCommands(conn, index) {
  if (index >= commands.length) {
    console.log('\n🎉 部署完成！访问 https://fda.19990419.top 查看效果');
    conn.end();
    return;
  }
  const cmd = commands[index];
  const num = `[${index + 1}/${commands.length}]`;
  console.log(`${num} $ ${cmd.substring(0, 100)}${cmd.length > 100 ? '...' : ''}`);

  conn.exec(cmd, (err, stream) => {
    if (err) {
      console.error(`  Error: ${err.message}`);
      runCommands(conn, index + 1);
      return;
    }
    stream.on('data', (d) => process.stdout.write(d.toString()))
      .stderr.on('data', (d) => process.stderr.write(d.toString()))
      .on('close', (code) => {
        if (code !== 0) console.log(`  (exit: ${code})`);
        runCommands(conn, index + 1);
      });
  });
}
