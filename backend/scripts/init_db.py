#!/usr/bin/env python3
"""
数据库初始化脚本
给现有 warning_letters 表加 region/country 字段，创建新表
"""
import sys
sys.path.insert(0, '/root/fda-warning-system/backend')

import sqlite3

DB_PATH = '/root/data/fda_warning.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 检查现有字段
cursor.execute("PRAGMA table_info(warning_letters)")
cols = [r[1] for r in cursor.fetchall()]
print(f"现有字段: {cols}")

# 补充缺失字段
if 'region' not in cols:
    cursor.execute("ALTER TABLE warning_letters ADD COLUMN region VARCHAR(100)")
    print("✓ 新增 region 字段")

if 'country' not in cols:
    cursor.execute("ALTER TABLE warning_letters ADD COLUMN country VARCHAR(100)")
    print("✓ 新增 country 字段")

# 创建新表
new_tables = {
    'violations': """
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            letter_id INTEGER,
            system VARCHAR(100),
            description TEXT,
            cfr_code VARCHAR(50),
            FOREIGN KEY (letter_id) REFERENCES warning_letters(id)
        )
    """,
    'ai_analysis': """
        CREATE TABLE IF NOT EXISTS ai_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            letter_id INTEGER UNIQUE,
            translation_zh TEXT,
            summary_zh TEXT,
            violation_type VARCHAR(100),
            key_findings TEXT,
            risk_level VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (letter_id) REFERENCES warning_letters(id)
        )
    """,
    'f483_observations': """
        CREATE TABLE IF NOT EXISTS f483_observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            letter_id INTEGER,
            observation_number VARCHAR(10),
            description TEXT,
            cfr_reference VARCHAR(100),
            FOREIGN KEY (letter_id) REFERENCES warning_letters(id)
        )
    """,
    'cfr_citations': """
        CREATE TABLE IF NOT EXISTS cfr_citations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            letter_id INTEGER,
            cfr_section VARCHAR(50),
            description TEXT,
            FOREIGN KEY (letter_id) REFERENCES warning_letters(id)
        )
    """,
    'push_subscriptions': """
        CREATE TABLE IF NOT EXISTS push_subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR(100),
            platform VARCHAR(20),
            keywords_filter TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    """
}

for name, sql in new_tables.items():
    cursor.execute(sql)
    print(f"✓ {name} 表就绪")

conn.commit()

# 验证
cursor.execute("SELECT COUNT(*) FROM warning_letters")
total = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM warning_letters WHERE url IS NOT NULL AND url != ''")
with_url = cursor.fetchone()[0]
print(f"\n📊 数据库状态: {total} 封信, {with_url} 条有URL")

conn.close()
print("\n✅ init_db.py 完成")
