-- ==============================================
-- 资讯门户数据库迁移脚本
-- 执行时间：2026-05-01
-- ==============================================

-- 1. 创建subscriptions表（邮件订阅）
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    sectors TEXT,  -- JSON数组: ["pharma", "cosmetics", "food"]
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_notified_at TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_subscriptions_email ON subscriptions(email);
CREATE INDEX IF NOT EXISTS idx_subscriptions_active ON subscriptions(is_active);

-- 2. 给articles表添加新字段
-- 注意：SQLite不支持ALTER TABLE ADD COLUMN IF NOT EXISTS
-- 如果字段已存在，会报错，可以忽略

-- 添加is_headline字段
ALTER TABLE articles ADD COLUMN is_headline INTEGER DEFAULT 0;

-- 添加hot_score字段
ALTER TABLE articles ADD COLUMN hot_score INTEGER DEFAULT 0;

-- 3. 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_articles_is_headline ON articles(is_headline);
CREATE INDEX IF NOT EXISTS idx_articles_hot_score ON articles(hot_score);
CREATE INDEX IF NOT EXISTS idx_articles_sector_status ON articles(sector, status);
CREATE INDEX IF NOT EXISTS idx_articles_published_at ON articles(published_at);

-- 4. 更新现有文章的hot_score（基于view_count和发布时间）
UPDATE articles
SET hot_score = (
    CASE
        WHEN view_count IS NULL OR view_count = 0 THEN 0
        WHEN view_count < 100 THEN view_count
        WHEN view_count < 1000 THEN 100 + (view_count / 10)
        WHEN view_count < 10000 THEN 200 + (view_count / 100)
        ELSE 300 + (view_count / 1000)
    END
)
WHERE status = 'published';

-- 5. 标记一些热门文章为头条（选择view_count最高的）
UPDATE articles
SET is_headline = 1
WHERE id IN (
    SELECT id
    FROM articles
    WHERE status = 'published'
    ORDER BY view_count DESC, published_at DESC
    LIMIT 5
);

-- 6. 创建视图：门户首页头条
CREATE VIEW IF NOT EXISTS portal_headlines AS
SELECT
    id,
    title,
    summary,
    sector,
    published_at,
    cover_image,
    view_count,
    is_headline
FROM articles
WHERE status = 'published'
    AND is_headline = 1
ORDER BY published_at DESC
LIMIT 3;

-- 7. 创建视图：各行业最新动态
CREATE VIEW IF NOT EXISTS portal_industry_news AS
SELECT
    id,
    title,
    summary,
    sector,
    published_at,
    category_id,
    ROW_NUMBER() OVER (PARTITION BY sector ORDER BY published_at DESC) as rn
FROM articles
WHERE status = 'published'
    AND sector IN ('pharma', 'cosmetics', 'food');

-- 8. 创建视图：热门文章排行
CREATE VIEW IF NOT EXISTS portal_hot_articles AS
SELECT
    id,
    title,
    sector,
    view_count,
    hot_score,
    published_at
FROM articles
WHERE status = 'published'
    AND published_at >= datetime('now', '-30 days')
ORDER BY hot_score DESC, view_count DESC
LIMIT 100;

-- ==============================================
-- 迁移完成
-- ==============================================

-- 验证迁移结果
SELECT 'subscriptions' as table_name, COUNT(*) as count FROM subscriptions
UNION ALL
SELECT 'articles with is_headline', COUNT(*) FROM articles WHERE is_headline = 1
UNION ALL
SELECT 'articles with hot_score', COUNT(*) FROM articles WHERE hot_score > 0;
