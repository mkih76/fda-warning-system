# 资讯门户部署指南

## 📦 Phase 1 已完成的内容

### ✅ 后端（FastAPI）
- [x] `/api/portal/headlines` - 头条新闻API
- [x] `/api/portal/industry/{sector}` - 各行业动态API
- [x] `/api/portal/hot` - 热门文章排行API
- [x] `/api/portal/stats` - 统计数据API
- [x] `/api/portal/subscribe` - 邮件订阅API
- [x] 数据库模型（Subscription表，Article新字段）

### ✅ 前端（Vue 3）
- [x] 门户页面调用真实API
- [x] Loading状态
- [x] 订阅功能完整实现
- [x] 错误处理和静态fallback

### ✅ 数据库
- [x] 迁移脚本（portal_migration.sql）
- [x] 新表：subscriptions
- [x] 新字段：articles.is_headline, articles.hot_score
- [x] 索引优化

---

## 🚀 部署步骤

### 第一步：同步代码到VPS

在本地打包代码：

```bash
# 打包修改过的文件
cd C:/Users/22975/fda-warning-system
tar -czf portal-update.tar.gz \
  backend/app/routers/portal.py \
  backend/app/models_new.py \
  backend/app/main.py \
  frontend/src/views/PortalHome.vue \
  frontend/src/components/Navbar.vue \
  frontend/src/router/index.js \
  scripts/portal_migration.sql
```

上传到VPS：

```bash
scp portal-update.tar.gz root@你的VPS_IP:/root/
```

在VPS上解压：

```bash
cd /root/fda-warning-system
tar -xzf /root/portal-update.tar.gz
```

---

### 第二步：执行数据库迁移

```bash
# 进入项目目录
cd /root/fda-warning-system

# 备份现有数据库
cp /root/data/fda_warning.db /root/data/fda_warning.db.backup_$(date +%Y%m%d)

# 执行迁移脚本
sqlite3 /root/data/fda_warning.db < scripts/portal_migration.sql
```

验证迁移结果：

```bash
sqlite3 /root/data/fda_warning.db << 'EOF'
SELECT 'subscriptions表' as item, COUNT(*) as count FROM subscriptions
UNION ALL
SELECT '头条文章数', COUNT(*) FROM articles WHERE is_headline = 1
UNION ALL
SELECT '带hot_score的文章', COUNT(*) FROM articles WHERE hot_score > 0;
EOF
```

预期输出：
```
subscriptions表|0
头条文章数|5
带hot_score的文章|XXX
```

---

### 第三步：重启后端服务

```bash
# 进入backend目录
cd /root/fda-warning-system/backend

# 如果使用systemd服务
sudo systemctl restart fda-backend

# 或者直接重启Docker
docker restart fda-warning-backend

# 或者手动重启uvicorn
pkill -f uvicorn
nohup uvicorn app.main:app --host 0.0.0.0 --port 8790 --reload > /tmp/backend.log 2>&1 &
```

验证后端启动：

```bash
# 测试portal API
curl http://localhost:8790/api/portal/headlines | python3 -m json.tool

curl http://localhost:8790/api/portal/industry/pharma | python3 -m json.tool

curl http://localhost:8790/api/portal/hot | python3 -m json.tool
```

---

### 第四步：重新构建前端

```bash
# 进入frontend目录
cd /root/fda-warning-system/frontend

# 安装依赖（如果有新依赖）
npm install

# 构建生产版本
npm run build

# 验证构建
ls -la dist/
```

---

### 第五步：配置Nginx（如果需要）

如果前端和API不在同一个域名，需要配置代理。

**方案A：前后端同域名（推荐）**

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 或 _ (接受所有域名)

    # API请求代理到后端
    location /api/ {
        proxy_pass http://127.0.0.1:8790/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 超时设置（AI生成可能需要较长时间）
        proxy_connect_timeout 60s;
        proxy_read_timeout 120s;
        proxy_send_timeout 60s;
    }

    # 前端静态文件
    location / {
        root /root/fda-warning-system/frontend/dist;
        try_files $uri $uri/ /index.html;

        # 缓存静态资源
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # 禁止访问隐藏文件
    location ~ /\. {
        deny all;
    }
}
```

**方案B：前后端分离域名**

前端：https://www.your-domain.com → CF Pages 或 静态托管
后端：https://api.your-domain.com → VPS

前端需要修改API地址：

```javascript
// frontend/src/views/PortalHome.vue
const API = 'https://api.your-domain.com'  // 替换为实际API域名
```

---

### 第六步：申请SSL证书（可选但推荐）

```bash
# 安装Certbot
apt update && apt install -y certbot python3-certbot-nginx

# 申请证书
certbot --nginx -d your-domain.com

# 自动续期测试
certbot renew --dry-run
```

---

### 第七步：测试完整功能

#### 1. 测试首页访问
```bash
# 浏览器访问
http://your-domain.com/#/          # 原首页
http://your-domain.com/#/portal    # 资讯门户
```

#### 2. 测试API
```bash
# 头条新闻
curl http://your-domain.com/api/portal/headlines

# 行业动态
curl http://your-domain.com/api/portal/industry/pharma
curl http://your-domain.com/api/portal/industry/cosmetics
curl http://your-domain.com/api/portal/industry/food

# 热门文章
curl http://your-domain.com/api/portal/hot

# 统计数据
curl http://your-domain.com/api/portal/stats

# 订阅测试
curl -X POST http://your-domain.com/api/portal/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"测试用户","sectors":["pharma","cosmetics","food"]}'
```

#### 3. 测试前端功能
- [ ] 首页正常显示
- [ ] 导航栏显示"资讯门户"入口
- [ ] 门户页面加载无报错
- [ ] 头条新闻显示（可能需要先有published的文章）
- [ ] 三个行业动态显示（fallback静态数据）
- [ ] FDA警告信列表显示
- [ ] 热门文章排行显示
- [ ] 订阅功能可以提交
- [ ] 移动端适配正常

---

## 🔧 后续优化（Phase 2 & 3）

### Phase 2：RSS聚合（3-5天）

创建RSS数据源配置：

```python
# backend/app/crawler/rss_config.py
RSS_SOURCES = {
    'pharma': [
        {'name': 'NMPA', 'url': 'https://www.nmpa.gov.cn/.../rss.xml', 'enabled': True},
        {'name': 'FDA药品', 'url': 'https://www.fda.gov/.../rss.xml', 'enabled': True},
    ],
    'cosmetics': [
        {'name': 'FDA化妆品', 'url': '...', 'enabled': True},
    ],
    'food': [
        {'name': '食品安全网', 'url': '...', 'enabled': True},
    ]
}
```

执行：
```bash
# 让Hermes创建RSS解析器
# 或者手动创建：backend/app/crawler/rss_parser.py

# 添加定时任务
# 编辑 /etc/crontab 或使用 APScheduler
0 2 * * * cd /root/fda-warning-system/backend && python -m app.crawler.rss_sync
```

### Phase 3：AI内容生成（5-7天）

配置AI模型：

```bash
# 设置环境变量
export NVIDIA_API_KEY="nvapi-xxx"
export GOOGLE_API_KEY="AIzaSyxxx"

# 或者写入.env文件
cat > /root/fda-warning-system/backend/.env << 'EOF'
NVIDIA_API_KEY=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
GOOGLE_API_KEY=AIzaSyChMbP0SCwAC12Tb1y9JtluqP2191dx1oc
EOF
```

创建AI生成任务：
```bash
# 让Hermes创建：backend/app/ai/content_generator.py

# 测试AI生成
cd /root/fda-warning-system/backend
python -c "
from app.ai.content_generator import generate_fda_summary
result = generate_fda_summary('某药企警告信原文...')
print(result)
"
```

---

## 📊 监控与维护

### 日志查看

```bash
# 后端日志
tail -f /tmp/backend.log

# 或者Docker日志
docker logs -f fda-warning-backend

# Nginx日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 数据库维护

```bash
# 查看订阅数量
sqlite3 /root/data/fda_warning.db "SELECT COUNT(*) FROM subscriptions WHERE is_active=1;"

# 查看文章统计
sqlite3 /root/data/fda_warning.db << 'EOF'
SELECT
    sector,
    COUNT(*) as total,
    SUM(CASE WHEN is_headline=1 THEN 1 ELSE 0 END) as headlines,
    AVG(view_count) as avg_views
FROM articles
WHERE status='published'
GROUP BY sector;
EOF

# 清理过期数据（可选）
sqlite3 /root/data/fda_warning.db "DELETE FROM read_history WHERE read_at < datetime('now', '-90 days');"
```

### 备份策略

```bash
# 每日备份脚本
cat > /root/backup_fda.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/root/backups/fda_$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# 备份数据库
cp /root/data/fda_warning.db $BACKUP_DIR/

# 备份代码
tar -czf $BACKUP_DIR/code.tar.gz /root/fda-warning-system --exclude=node_modules --exclude=dist

# 清理7天前的备份
find /root/backups -name "fda_*" -mtime +7 -exec rm -rf {} \;

echo "备份完成: $BACKUP_DIR"
EOF

chmod +x /root/backup_fda.sh

# 添加定时任务（每天凌晨3点）
echo "0 3 * * * /root/backup_fda.sh >> /var/log/backup.log 2>&1" | crontab -
```

---

## 🐛 常见问题排查

### 问题1：API返回404

**原因：** portal路由未注册

**解决：**
```bash
# 检查main.py是否导入了portal_router
grep "portal_router" /root/fda-warning-system/backend/app/main.py

# 重启后端
docker restart fda-warning-backend
```

### 问题2：数据库报错 "no such column: is_headline"

**原因：** 迁移脚本未执行

**解决：**
```bash
sqlite3 /root/data/fda_warning.db < /root/fda-warning-system/scripts/portal_migration.sql
```

### 问题3：前端显示静态数据，不调用API

**原因：** API请求失败，触发了fallback

**解决：**
```bash
# 检查浏览器控制台（F12）的网络请求
# 测试API连通性
curl -v http://localhost:8790/api/portal/headlines

# 检查后端日志
tail -f /tmp/backend.log
```

### 问题4：订阅功能提交失败

**原因：** subscriptions表不存在

**解决：**
```bash
# 检查表是否存在
sqlite3 /root/data/fda_warning.db ".tables" | grep subscriptions

# 如果不存在，单独创建
sqlite3 /root/data/fda_warning.db << 'EOF'
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    sectors TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_notified_at TIMESTAMP
);
EOF
```

### 问题5：页面白屏

**原因：** JavaScript错误

**解决：**
```bash
# 打开浏览器开发者工具（F12）→ Console
# 查看具体错误信息

# 常见错误：
# 1. API地址错误 → 检查const API = ...
# 2. CORS问题 → 检查后端CORS配置
# 3. 模块未找到 → npm install
```

---

## ✅ 验收清单

部署完成后，逐项检查：

- [ ] 原首页（/#/）正常访问
- [ ] 门户页面（/#/portal）正常访问
- [ ] 导航栏显示"资讯门户"入口（蓝色高亮）
- [ ] 门户页面调用真实API（查看浏览器Network）
- [ ] FDA警告信列表显示真实数据
- [ ] 订阅功能可以正常提交
- [ ] 提交后显示成功消息
- [ ] 移动端访问正常
- [ ] 没有Console错误

---

## 📞 需要帮助？

如果遇到问题：

1. 查看日志：`tail -f /tmp/backend.log`
2. 检查API：`curl http://localhost:8790/api/portal/headlines`
3. 检查数据库：`sqlite3 /root/data/fda_warning.db`
4. 让Hermes协助排查

---

## 🎉 部署完成！

恭喜！资讯门户Phase 1已部署完成。

现在你可以：
1. ✅ 访问门户页面查看真实数据
2. ✅ 测试订阅功能
3. ✅ 开始Phase 2（RSS聚合）

下一步：让Hermes实施Phase 2 RSS聚合系统！

---

**部署时间：** 2026-05-01
**版本：** Portal Phase 1
**状态：** ✅ Ready for Production
