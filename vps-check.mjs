import { Client } from 'ssh2';

const conn = new Client();
const commands = [
  'ps aux | grep -E "uvicorn|python|node" | grep -v grep',
  'ls /root/fda-warning-system/',
  'cat /root/fda-warning-system/.venv/bin/activate 2>/dev/null | head -5',
  'ls /root/fda-warning-system/.venv/bin/ 2>/dev/null | head -20',
  'cat /etc/systemd/system/fda*.service 2>/dev/null || systemctl list-units --type=service | grep -i fda 2>/dev/null',
  'ls /root/fda-warning-system/frontend/dist/ 2>/dev/null | head -10',
  'cat /root/fda-warning-system/frontend/package.json 2>/dev/null | head -5',
];

conn.on('ready', () => {
  console.log('SSH connected!');
  let idx = 0;
  function next() {
    if (idx >= commands.length) { conn.end(); return; }
    const cmd = commands[idx++];
    console.log(`\n$ ${cmd}`);
    conn.exec(cmd, (err, stream) => {
      if (err) { console.error(err); next(); return; }
      stream.on('data', d => process.stdout.write(d.toString()))
        .stderr.on('data', d => process.stderr.write(d.toString()))
        .on('close', () => next());
    });
  }
  next();
}).connect({ host: '23.94.206.159', port: 22, username: 'root', password: 'Cmh@13579' });
