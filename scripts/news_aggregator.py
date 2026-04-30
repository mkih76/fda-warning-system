#!/usr/bin/env python3
"""
行业资讯RSS聚合系统 - 聚合制药/化妆品/食品行业新闻
"""

import sqlite3
import feedparser
import time
import logging
import os
import hashlib
from datetime import datetime
from typing import List, Dict, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/root/fda-warning-system/logs/news_aggregator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class NewsAggregator:
    """行业资讯聚合类"""
    
    def __init__(self, db_path: str = '/root/data/news.db'):
        """初始化聚合器"""
        self.db_path = db_path
        
        # RSS订阅源
        self.feeds = {
            'fda_news': {
                'name': 'FDA News',
                'url': 'https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/press-releases/rss.xml',
                'category': '国际动态',
                'industry': '制药'
            },
            'fda_safety': {
                'name': 'FDA Safety Alerts',
                'url': 'https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/drug-safety/rss.xml',
                'category': '法规信息',
                'industry': '制药'
            },
            'fda_recalls': {
                'name': 'FDA Recalls',
                'url': 'https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/recalls/rss.xml',
                'category': '行业资讯',
                'industry': '制药'
            }
        }
        
        # 创建日志目录
        os.makedirs('/root/fda-warning-system/logs', exist_ok=True)
        
        # 初始化数据库
        self._init_database()
    
    def _init_database(self):
        """初始化数据库表结构"""
        try:
            # 确保数据目录存在
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 创建news表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    source TEXT NOT NULL,
                    source_url TEXT UNIQUE,
                    publish_date DATE,
                    category TEXT,
                    industry TEXT,
                    summary TEXT,
                    content TEXT,
                    content_hash TEXT,
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_news_source ON news(source)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_news_category ON news(category)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_news_publish_date ON news(publish_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_news_content_hash ON news(content_hash)')
            
            # 创建crawl_log表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS crawl_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feed_name TEXT NOT NULL,
                    crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    items_found INTEGER DEFAULT 0,
                    items_saved INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'success',
                    error_message TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("数据库初始化成功")
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            raise
    
    def generate_content_hash(self, title: str, url: str) -> str:
        """生成内容哈希用于去重"""
        content = f"{title}{url}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def parse_date(self, date_str: str) -> Optional[str]:
        """解析日期格式"""
        if not date_str:
            return None
        
        # 尝试多种日期格式
        from email.utils import parsedate_to_datetime
        from dateutil import parser as date_parser
        
        try:
            # 尝试RFC 2822格式
            dt = parsedate_to_datetime(date_str)
            return dt.strftime('%Y-%m-%d')
        except:
            pass
        
        try:
            # 尝试dateutil解析
            dt = date_parser.parse(date_str)
            return dt.strftime('%Y-%m-%d')
        except:
            pass
        
        return None
    
    def fetch_feed(self, feed_name: str, feed_config: Dict) -> List[Dict]:
        """获取单个RSS源"""
        news_items = []
        
        try:
            logger.info(f"正在获取RSS源: {feed_config['name']}")
            
            feed = feedparser.parse(feed_config['url'])
            
            if feed.bozo and not feed.entries:
                logger.warning(f"RSS源解析警告: {feed.bozo_exception}")
                return news_items
            
            for entry in feed.entries:
                try:
                    title = entry.get('title', '').strip()
                    link = entry.get('link', '').strip()
                    
                    if not title or not link:
                        continue
                    
                    # 解析日期
                    publish_date = None
                    if hasattr(entry, 'published'):
                        publish_date = self.parse_date(entry.published)
                    elif hasattr(entry, 'updated'):
                        publish_date = self.parse_date(entry.updated)
                    
                    # 提取摘要
                    summary = entry.get('summary', '')
                    if summary:
                        # 清理HTML标签
                        from bs4 import BeautifulSoup
                        summary = BeautifulSoup(summary, 'html.parser').get_text(strip=True)[:500]
                    
                    # 生成内容哈希
                    content_hash = self.generate_content_hash(title, link)
                    
                    news_items.append({
                        'title': title,
                        'source': feed_config['name'],
                        'source_url': link,
                        'publish_date': publish_date,
                        'category': feed_config['category'],
                        'industry': feed_config['industry'],
                        'summary': summary,
                        'content_hash': content_hash
                    })
                    
                except Exception as e:
                    logger.warning(f"解析RSS条目失败: {e}")
                    continue
            
            logger.info(f"从 {feed_config['name']} 获取 {len(news_items)} 条新闻")
            
        except Exception as e:
            logger.error(f"获取RSS源失败 {feed_config['name']}: {e}")
        
        return news_items
    
    def save_news(self, news: Dict) -> bool:
        """保存新闻到数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查是否已存在（使用content_hash去重）
            cursor.execute(
                'SELECT id FROM news WHERE content_hash = ?',
                (news['content_hash'],)
            )
            if cursor.fetchone():
                conn.close()
                return False  # 已存在，跳过
            
            cursor.execute('''
                INSERT INTO news 
                (title, source, source_url, publish_date, category, industry, summary, content_hash, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                news['title'],
                news['source'],
                news['source_url'],
                news.get('publish_date'),
                news.get('category'),
                news.get('industry'),
                news.get('summary'),
                news['content_hash']
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"保存新闻失败: {news['title'][:50]}... - {e}")
            return False
    
    def log_crawl(self, feed_name: str, items_found: int, items_saved: int, status: str = 'success', error_message: str = None):
        """记录爬取日志"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO crawl_log (feed_name, items_found, items_saved, status, error_message)
                VALUES (?, ?, ?, ?, ?)
            ''', (feed_name, items_found, items_saved, status, error_message))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"记录爬取日志失败: {e}")
    
    def fetch_all(self) -> int:
        """获取所有订阅源"""
        total_saved = 0
        
        for feed_name, feed_config in self.feeds.items():
            try:
                # 获取新闻
                news_items = self.fetch_feed(feed_name, feed_config)
                items_found = len(news_items)
                items_saved = 0
                
                # 保存新闻
                for news in news_items:
                    if self.save_news(news):
                        items_saved += 1
                    time.sleep(0.1)  # 短暂延迟
                
                total_saved += items_saved
                
                # 记录日志
                self.log_crawl(feed_name, items_found, items_saved)
                
                logger.info(f"{feed_config['name']}: 找到 {items_found} 条，保存 {items_saved} 条")
                
                # 请求间隔
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"处理 {feed_name} 失败: {e}")
                self.log_crawl(feed_name, 0, 0, 'error', str(e))
        
        logger.info(f"所有RSS源处理完成，共保存 {total_saved} 条新闻")
        return total_saved
    
    def get_latest_news(self, limit: int = 10, category: str = None) -> List[Dict]:
        """获取最新新闻"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = '''
                SELECT id, title, source, publish_date, category, industry, summary
                FROM news
            '''
            params = []
            
            if category:
                query += ' WHERE category = ?'
                params.append(category)
            
            query += ' ORDER BY publish_date DESC, created_at DESC LIMIT ?'
            params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            conn.close()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"获取最新新闻失败: {e}")
            return []
    
    def get_news_stats(self) -> Dict:
        """获取新闻统计"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 总数
            cursor.execute('SELECT COUNT(*) FROM news')
            total = cursor.fetchone()[0]
            
            # 按来源统计
            cursor.execute('''
                SELECT source, COUNT(*) as count
                FROM news
                GROUP BY source
                ORDER BY count DESC
            ''')
            by_source = cursor.fetchall()
            
            # 按分类统计
            cursor.execute('''
                SELECT category, COUNT(*) as count
                FROM news
                GROUP BY category
                ORDER BY count DESC
            ''')
            by_category = cursor.fetchall()
            
            # 今日新增
            cursor.execute('''
                SELECT COUNT(*) FROM news
                WHERE DATE(created_at) = DATE('now')
            ''')
            today_new = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total': total,
                'by_source': by_source,
                'by_category': by_category,
                'today_new': today_new
            }
            
        except Exception as e:
            logger.error(f"获取统计失败: {e}")
            return {}


def main():
    """主函数"""
    aggregator = NewsAggregator()
    
    # 获取所有新闻
    total = aggregator.fetch_all()
    
    # 打印统计
    stats = aggregator.get_news_stats()
    print(f"\n=== 新闻统计 ===")
    print(f"总数: {stats.get('total', 0)}")
    print(f"今日新增: {stats.get('today_new', 0)}")
    print(f"\n按来源:")
    for source, count in stats.get('by_source', []):
        print(f"  {source}: {count}")
    print(f"\n按分类:")
    for category, count in stats.get('by_category', []):
        print(f"  {category}: {count}")


if __name__ == '__main__':
    main()
