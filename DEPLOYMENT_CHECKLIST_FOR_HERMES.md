# 资讯门户部署清单（给Hermes）

## 📋 部署任务

请按顺序执行以下任务：

### 1️⃣ 同步代码（5分钟）
- [ ] 从本地上传代码到VPS
- [ ] 解压到 `/root/fda-warning-system/`

### 2️⃣ 数据库迁移（2分钟）
```bash
# 备份
cp /root/data/fda_warning.db /root/data/fda_warning.db.bak

# 执行迁移
sqlite3 /root/data/fda_warning.db < /root/fda-warning-system/scripts/portal_migration.sql

# 验证
sqlite3 /root/data/fda_warning.db "SELECT COUNT(*) FROM articles WHERE is_headline=1;"
```

### 3️⃣ 重启后端（1分钟）
```bash
cd /root/fda-warning-system/backend
docker restart fda-warning-backend
# 或者
pkill -f uvicorn && nohup uvicorn app.main:app --host 0.0.0.0 --port 8790 --reload &

# 验证API
curl http://localhost:8790/api/portal/headlines
```

### 4️⃣ 重新构建前端（2分钟）
```bash
cd /root/fda-warning-system/frontend
npm install
npm run build
```

### 5️⃣ 配置Nginx（3分钟）

```nginx
server {
    listen 80;
    server_name _;

    # API代理
    location /api/ {
        proxy_pass http://127.0.0.1:8790/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 120s;
    }

    # 前端静态文件
    location / {
        root /root/fda-warning-system/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

```bash
# 测试配置
nginx -t

# 重载
nginx -s reload
```

### 6️⃣ 测试验证（2分钟）

浏览器访问：
- [ ] http://IP/#/ （原首页）
- [ ] http://IP/#/portal （门户页面）

测试API：
```bash
curl http://IP/api/portal/headlines | head -20
curl -X POST http://IP/api/portal/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'
```

---

## ✅ 完成标志

全部打勾即为部署成功：

- [ ] 原首页正常显示（Hero大图）
- [ ] 门户页面正常显示（资讯布局）
- [ ] 导航栏有"资讯门户"入口
- [ ] FDA警告信列表显示数据
- [ ] 订阅功能可以提交
- [ ] 没有500错误

---

## 🐛 如果出错

### 错误1：API 404
```bash
# 检查main.py
grep "portal" /root/fda-warning-system/backend/app/main.py

# 重启后端
docker restart fda-warning-backend
```

### 错误2：数据库字段不存在
```bash
# 重新执行迁移
sqlite3 /root/data/fda_warning.db < /root/fda-warning-system/scripts/portal_migration.sql
```

### 错误3：前端白屏
```bash
# 查看浏览器控制台（F12）
# 检查Network请求是否成功
# 重新构建前端
cd /root/fda-warning-system/frontend && npm run build
```

---

## 📞 部署完成后

请回复以下信息：

```
✅ 部署完成
- 访问地址：http://xxx.xxx.xxx.xxx
- 门户页面：http://xxx.xxx.xxx.xxx/#/portal
- API测试：正常/异常
- 订阅测试：正常/异常
- 备注：xxx
```

有问题随时联系！

---

**预计时间：15分钟**
**难度：⭐⭐（简单）**
**优先级：🔴 高**
