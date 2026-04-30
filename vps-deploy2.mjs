import { Client } from 'ssh2';

const conn = new Client();

const commands = [
  // Find correct paths
  'which docker 2>/dev/null || find / -name docker -type f 2>/dev/null | head -3',
  'which npm 2>/dev/null || find / -name npm -type f 2>/dev/null | head -3',
  'which node 2>/dev/null || find / -name node -type f 2>/dev/null | head -3',
  'docker --version 2>/dev/null || /usr/bin/docker --version 2>/dev/null || /usr/local/bin/docker --version 2>/dev/null',
  'export PATH=$PATH:/usr/local/bin:/usr/bin && docker-compose version 2>/dev/null || docker compose version 2>/dev/null',
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
    conn.end();
    return;
  }
  const cmd = commands[index];
  console.log(`\n[${index + 1}] $ ${cmd}`);
  conn.exec(cmd, (err, stream) => {
    if (err) { console.error(err.message); runCommands(conn, index + 1); return; }
    stream.on('data', (d) => process.stdout.write(d.toString()))
      .stderr.on('data', (d) => process.stderr.write(d.toString()))
      .on('close', () => runCommands(conn, index + 1));
  });
}
