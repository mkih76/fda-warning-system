module.exports = {
  vps: {
    host: '23.94.206.159',
    port: 22,
    username: 'root',
    password: 'Cmh@13579',
  },
  // AI禁用词：这些词组在格式化时会被替换
  bannedPhrases: [
    '综上所述', '值得注意的是', '总而言之', '不难发现', '由此可见',
    '众所周知', '毋庸置疑', '事实上', '具体而言', '换言之',
    '需要指出的是', '必须强调', '显而易见', '毫无疑问',
    'In conclusion', 'It is worth noting', 'Notably',
    'It goes without saying', 'As we all know',
  ],
  // 标点替换：英文标点 → 中文标点（在中文语境中）
  punctuationMap: {
    ',': '，', ';': '；', ':': '：', '?': '？', '!': '！',
  },
};
