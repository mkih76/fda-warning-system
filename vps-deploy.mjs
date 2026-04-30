import { Client } from 'ssh2';

const conn = new Client();

const commands = [
  'cd /root/fda-warning-system && git pull origin main',
  'cd /root/fda-warning-system/frontend && npm install && npm run build',
  'cd /root/fda-warning-system && pip install -r backend/requirements.txt',
  'cd /root/fda-warning-system && docker-compose down && docker-compose up -d --build',
  'sleep 5 && docker exec fda-warning-backend python -m backend.scripts.seed_data',
  // Import articles
  'docker cp /root/fda-warning-system/content/pharma_articles.txt fda-warning-backend:/tmp/',
  'docker exec fda-warning-backend python -m backend.scripts.import_articles /tmp/articles_pharma.txt',
  'docker cp /root/fda-warning-system/content/cosmetics_articles.txt fda-warning-backend:/tmp/',
  'docker exec fda-warning-backend python -m backend.scripts.import_articles /tmp/articles_cosmetics.txt',
  'docker cp /root/fda-warning-system/content/food_articles.txt fda-warning-backend:/tmp/',
  'docker exec fda-warning-backend python -m backend.scripts.import_articles /tmp/articles_food.txt',
  // Verify
  'curl -s http://localhost:8790/api/health',
  'curl -s http://localhost:8790/api/content/articles?page_size=3',
];

conn.on('ready', () => {
  console.log('SSH connected!');
  runCommands(conn, 0);
}).on('error', (err) => {
  console.error('SSH error:', err.message);
}).connect({
  host: '23.94.206.159',
  port: 22,
  username: 'root',
  password: 'Cmh@13579',
  readyTimeout: 15000,
});

function runCommands(conn, index) {
  if (index >= commands.length) {
    console.log('\n✅ All commands completed!');
    conn.end();
    return;
  }

  const cmd = commands[index];
  console.log(`\n[${index + 1}/${commands.length}] Running: ${cmd}`);

  conn.exec(cmd, (err, stream) => {
    if (err) {
      console.error('Error:', err.message);
      runCommands(conn, index + 1);
      return;
    }

    let output = '';
    stream.on('data', (data) => {
      const text = data.toString();
      process.stdout.write(text);
      output += text;
    }).stderr.on('data', (data) => {
      process.stderr.write(data.toString());
    }).on('close', (code) => {
      if (code !== 0 && !cmd.includes('curl')) {
        console.log(`(exit code: ${code})`);
      }
      runCommands(conn, index + 1);
    });
  });
}
