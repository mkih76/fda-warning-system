#!/usr/bin/env python3
"""
NMPA法规爬虫系统
爬取国家药品监督管理局(NMPA)的法规公告信息
Author: Hermes Agent
Date: 2026-04-30
"""

import sqlite3
import requests
import time
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from bs4 import BeautifulSoup
import json
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 数据库路径
DB_PATH = "/root/data/regulations.db"

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
}

# 请求间隔(秒)
MIN_DELAY = 2
MAX_DELAY = 5


def init_database():
    """初始化法规数据库表"""
    import os
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建法规信息表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS regulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            title_cn TEXT,
            publish_date DATE,
            department TEXT,
            category TEXT,
            content TEXT,
            content_text TEXT,
            url TEXT UNIQUE,
            attachment_url TEXT,
            view_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_publish_date ON regulations(publish_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON regulations(category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_title ON regulations(title)')
    
    # 创建爬取记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crawl_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status TEXT,
            error_message TEXT,
            crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info(f"数据库初始化完成: {DB_PATH}")


def get_random_delay():
    """获取随机延迟时间"""
    import random
    return random.uniform(MIN_DELAY, MAX_DELAY)


def fetch_page(url: str, retry: int = 3) -> Optional[str]:
    """获取网页内容，带重试机制"""
    for attempt in range(retry):
        try:
            response = requests.get(url, headers=HEADERS, timeout=30)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                return response.text
            else:
                logger.warning(f"请求失败 {url}: HTTP {response.status_code}, 重试 {attempt+1}/{retry}")
        except Exception as e:
            logger.warning(f"请求异常 {url}: {e}, 重试 {attempt+1}/{retry}")
        
        if attempt < retry - 1:
            time.sleep(get_random_delay())
    
    return None


def parse_list_page(html: str) -> List[Dict]:
    """
    解析列表页，提取法规条目
    返回: [{'title': '标题', 'url': '链接', 'date': '发布日期'}, ...]
    """
    soup = BeautifulSoup(html, 'html.parser')
    items = []
    
    # NMPA公告列表常见结构
    # 查找列表项 - 多种选择器适配
    list_selectors = [
        'ul.list li',
        'div.list ul li',
        'div.news-list li',
        'div.content-list li',
        'table tbody tr',
        '.news_list li',
        '.list-item',
        'li.news-item'
    ]
    
    list_items = []
    for selector in list_selectors:
        list_items = soup.select(selector)
        if list_items:
            break
    
    if not list_items:
        # 尝试查找包含链接和日期的元素
        list_items = soup.find_all('li')
    
    for item in list_items:
        # 提取标题和链接
        link = item.find('a')
        if not link:
            continue
        
        title = link.get_text(strip=True)
        url = link.get('href', '')
        
        if not title or not url:
            continue
        
        # 处理相对链接
        if url.startswith('/'):
            url = 'https://www.nmpa.gov.cn' + url
        elif url.startswith('./'):
            url = 'https://www.nmpa.gov.cn' + url[1:]
        elif not url.startswith('http'):
            url = 'https://www.nmpa.gov.cn/' + url
        
        # 提取日期
        date_text = ''
        # 查找日期元素
        date_selectors = [
            'span.date',
            'span.time',
            '.date',
            '.time',
            '.pub-date',
            '.publish-time',
            'span[class*="date"]',
            'span[class*="time"]'
        ]
        
        for selector in date_selectors:
            date_elem = item.select_one(selector)
            if date_elem:
                date_text = date_elem.get_text(strip=True)
                break
        
        if not date_text:
            # 尝试在文本中查找日期
            text = item.get_text()
            date_match = re.search(r'(\d{4}[年/-]\d{1,2}[月/-]\d{1,2})', text)
            if date_match:
                date_text = date_match.group(1)
        
        # 解析日期格式
        publish_date = None
        if date_text:
            # 多种日期格式转换
            date_text_clean = re.sub(r'[年月]', '-', date_text)
            date_text_clean = re.sub(r'日$', '', date_text_clean)
            
            try:
                # 尝试解析 YYYY-MM-DD
                match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', date_text_clean)
                if match:
                    publish_date = f"{match.group(1)}-{int(match.group(2)):02d}-{int(match.group(3)):02d}"
            except:
                pass
        
        items.append({
            'title': title,
            'url': url,
            'date': publish_date,
            'raw_date': date_text
        })
    
    return items


def parse_detail_page(html: str, url: str) -> Dict:
    """
    解析详情页，提取法规完整内容
    返回: {'title': '标题', 'content': '正文内容', 'publish_date': '发布日期', ...}
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # 提取标题
    title = ''
    title_selectors = ['h1', '.article-title', '.title', '.news-title', '.detail-title', 'h2']
    for selector in title_selectors:
        elem = soup.select_one(selector)
        if elem:
            title = elem.get_text(strip=True)
            break
    
    if not title:
        title_elem = soup.find('title')
        if title_elem:
            title = title_elem.get_text(strip=True)
            # 移除后缀
            title = re.sub(r'[-|_]\s*国家药品监督管理局.*$', '', title)
    
    # 提取发布日期
    publish_date = ''
    date_selectors = [
        '.article-date',
        '.news-date',
        '.publish-time',
        '.date',
        '.time',
        'span[class*="date"]',
        'div[class*="date"]'
    ]
    
    for selector in date_selectors:
        elem = soup.select_one(selector)
        if elem:
            date_text = elem.get_text(strip=True)
            match = re.search(r'(\d{4}[年/-]\d{1,2}[月/-]\d{1,2})', date_text)
            if match:
                publish_date = match.group(1)
                break
    
    # 清理日期格式
    if publish_date:
        publish_date = re.sub(r'[年月]', '-', publish_date)
        publish_date = re.sub(r'日$', '', publish_date)
        try:
            dt = datetime.strptime(publish_date, '%Y-%m-%d')
            publish_date = dt.strftime('%Y-%m-%d')
        except:
            pass
    
    # 提取正文内容
    content = ''
    content_selectors = [
        '.article-content',
        '.news-content',
        '.detail-content',
        '.content',
        '#content',
        '.TRS_Editor',
        '.TRS_PreAppend',
        'div.article',
        'div.content'
    ]
    
    for selector in content_selectors:
        elem = soup.select_one(selector)
        if elem:
            content = str(elem)
            break
    
    if not content:
        # 尝试获取body中的主要内容
        main = soup.find('main')
        if main:
            content = str(main)
        else:
            # 获取所有段落
            paragraphs = soup.find_all('p')
            if paragraphs:
                content = ''.join(str(p) for p in paragraphs)
    
    # 清理HTML内容，保留文本
    content_text = ''
    if content:
        soup_content = BeautifulSoup(content, 'html.parser')
        # 移除脚本和样式
        for script in soup_content(['script', 'style', 'iframe', 'nav', 'footer', 'header']):
            script.decompose()
        content_text = soup_content.get_text()
        # 清理多余空白
        content_text = re.sub(r'\n\s*\n', '\n\n', content_text)
        content_text = content_text.strip()
    
    # 提取附件
    attachment_url = ''
    attachment_selectors = ['a[href$=".pdf"]', 'a[href$=".doc"]', 'a[href$=".docx"]', 'a.download']
    for selector in attachment_selectors:
        links = soup.select(selector)
        if links:
            attachment_url = links[0].get('href', '')
            if attachment_url.startswith('/'):
                attachment_url = 'https://www.nmpa.gov.cn' + attachment_url
            break
    
    return {
        'title': title,
        'content': content,
        'content_text': content_text,
        'publish_date': publish_date,
        'attachment_url': attachment_url
    }


def save_regulation(conn, regulation: Dict) -> bool:
    """
    保存法规信息到数据库
    返回: 是否保存成功
    """
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO regulations 
            (title, publish_date, content, content_text, url, attachment_url, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (
            regulation.get('title'),
            regulation.get('publish_date'),
            regulation.get('content'),
            regulation.get('content_text'),
            regulation.get('url'),
            regulation.get('attachment_url')
        ))
        
        return True
    except Exception as e:
        logger.error(f"保存失败 {regulation.get('url')}: {e}")
        return False


def log_crawl(conn, url: str, status: str, error: str = None):
    """记录爬取日志"""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO crawl_log (url, status, error_message)
        VALUES (?, ?, ?)
    ''', (url, status, error))


def crawl_nmpa(max_pages: int = 5):
    """
    主爬取函数
    max_pages: 最大爬取页数，默认5页
    """
    # 初始化数据库
    init_database()
    
    conn = sqlite3.connect(DB_PATH)
    base_url = 'https://www.nmpa.gov.cn/xxgk/ggtg/'
    
    # 收集所有需要爬取的URL
    all_items = []
    
    # 爬取列表页
    for page in range(1, max_pages + 1):
        logger.info(f"正在爬取第 {page} 页...")
        
        # 构建分页URL
        if page == 1:
            page_url = base_url
        else:
            # NMPA分页格式
            page_url = f"{base_url}index_{page}.html"
        
        html = fetch_page(page_url)
        if not html:
            logger.warning(f"无法获取第 {page} 页: {page_url}")
            continue
        
        items = parse_list_page(html)
        logger.info(f"第 {page} 页获取到 {len(items)} 条法规")
        all_items.extend(items)
        
        # 请求间隔
        time.sleep(get_random_delay())
    
    logger.info(f"共获取到 {len(all_items)} 条法规链接")
    
    # 爬取详情页
    success_count = 0
    fail_count = 0
    
    for idx, item in enumerate(all_items, 1):
        url = item['url']
        title = item['title']
        
        logger.info(f"正在爬取 [{idx}/{len(all_items)}]: {title[:50]}...")
        
        # 检查是否已爬取过
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM regulations WHERE url = ?', (url,))
        if cursor.fetchone():
            logger.info(f"  已存在，跳过: {url}")
            continue
        
        # 获取详情页
        html = fetch_page(url)
        if not html:
            logger.warning(f"  获取详情页失败: {url}")
            log_crawl(conn, url, 'failed', '获取详情页失败')
            fail_count += 1
            continue
        
        # 解析详情页
        detail = parse_detail_page(html, url)
        
        # 合并数据
        regulation = {
            'title': detail['title'] or title,
            'publish_date': detail['publish_date'] or item.get('date'),
            'content': detail['content'],
            'content_text': detail['content_text'],
            'url': url,
            'attachment_url': detail.get('attachment_url')
        }
        
        # 保存到数据库
        if save_regulation(conn, regulation):
            conn.commit()
            success_count += 1
            logger.info(f"  ✓ 保存成功: {regulation['title'][:50]}...")
        else:
            fail_count += 1
            logger.error(f"  ✗ 保存失败: {title}")
        
        # 请求间隔
        delay = get_random_delay()
        logger.debug(f"  等待 {delay:.1f} 秒...")
        time.sleep(delay)
    
    conn.close()
    
    logger.info(f"\n爬取完成! 成功: {success_count}, 失败: {fail_count}")
    return success_count, fail_count


def test_connection():
    """测试NMPA网站连接"""
    try:
        response = requests.get('https://www.nmpa.gov.cn', headers=HEADERS, timeout=10)
        if response.status_code == 200:
            logger.info("NMPA网站连接正常")
            return True
        else:
            logger.warning(f"NMPA网站返回状态码: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"NMPA网站连接失败: {e}")
        return False


def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("NMPA法规爬虫系统启动")
    logger.info("=" * 50)
    
    # 测试连接
    if not test_connection():
        logger.error("无法连接到NMPA网站，请检查网络")
        return
    
    # 开始爬取
    try:
        success, fail = crawl_nmpa(max_pages=5)
        logger.info(f"\n爬虫执行完成，成功: {success}, 失败: {fail}")
    except KeyboardInterrupt:
        logger.info("用户中断爬虫")
    except Exception as e:
        logger.error(f"爬虫执行异常: {e}", exc_info=True)


if __name__ == '__main__':
    main()
