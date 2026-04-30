#!/usr/bin/env python3
"""
FDA法规爬虫 - 爬取FDA法规指南信息
"""

import sqlite3
import requests
from bs4 import BeautifulSoup
import time
import logging
import re
import os
from datetime import datetime
from typing import Optional, List, Dict

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/root/fda-warning-system/logs/fda_regulation_crawler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FDARegulationCrawler:
    """FDA法规爬虫类"""
    
    def __init__(self, db_path: str = '/root/data/regulations.db'):
        """初始化爬虫"""
        self.db_path = db_path
        self.base_url = "https://www.fda.gov"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        self.request_delay = 2  # 请求间隔（秒）
        
        # 创建日志目录
        os.makedirs('/root/fda-warning-system/logs', exist_ok=True)
        
        # 初始化数据库
        self._init_database()
    
    def _init_database(self):
        """初始化数据库表结构"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 确保regulations表存在
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS regulations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    region TEXT NOT NULL,
                    publish_date DATE,
                    summary TEXT,
                    url TEXT UNIQUE,
                    pdf_url TEXT,
                    source TEXT,
                    industry TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("数据库初始化成功")
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            raise
    
    def _safe_request(self, url: str, max_retries: int = 3) -> Optional[str]:
        """安全的HTTP请求"""
        for attempt in range(max_retries):
            try:
                time.sleep(self.request_delay)
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                response.encoding = 'utf-8'
                return response.text
            except requests.RequestException as e:
                logger.warning(f"请求失败 (尝试 {attempt+1}/{max_retries}): {url} - {e}")
                if attempt == max_retries - 1:
                    return None
                time.sleep(5)
        return None
    
    def parse_date(self, date_str: str) -> Optional[str]:
        """解析日期格式"""
        if not date_str:
            return None
        
        # 美国日期格式
        patterns = [
            r'(\d{1,2})/(\d{1,2})/(\d{4})',  # MM/DD/YYYY
            r'(\d{4})-(\d{2})-(\d{2})',       # YYYY-MM-DD
            r'(\w+ \d{1,2}, \d{4})',           # Month DD, YYYY
        ]
        
        for pattern in patterns:
            match = re.search(pattern, date_str)
            if match:
                try:
                    if 'MM/DD/YYYY' in pattern or pattern == r'(\d{1,2})/(\d{1,2})/(\d{4})':
                        month, day, year = match.groups()
                        return f"{year}-{int(month):02d}-{int(day):02d}"
                    elif pattern == r'(\d{4})-(\d{2})-(\d{2})':
                        return match.group(0)
                    else:
                        # 尝试解析 "Month DD, YYYY" 格式
                        date_obj = datetime.strptime(match.group(0), '%B %d, %Y')
                        return date_obj.strftime('%Y-%m-%d')
                except:
                    continue
        
        return None
    
    def crawl_guidance_page(self) -> List[Dict]:
        """爬取FDA法规指南页面"""
        regulations = []
        
        # FDA法规指南URL
        url = f"{self.base_url}/regulatory-information/search-fda-guidance-documents"
        logger.info(f"正在爬取FDA法规指南: {url}")
        
        html = self._safe_request(url)
        if not html:
            logger.error("无法获取页面内容")
            return regulations
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # 查找法规列表
        # FDA网站通常使用views-row类
        items = soup.find_all('div', class_=re.compile(r'views-row|article|item', re.I))
        
        if not items:
            # 备用选择器
            items = soup.find_all('li', class_=re.compile(r'views-row|item', re.I))
        
        for item in items[:50]:  # 限制处理前50条
            try:
                # 提取标题和链接
                link_elem = item.find('a', href=True)
                if not link_elem:
                    continue
                
                title = link_elem.get_text(strip=True)
                href = link_elem['href']
                
                if not title or len(title) < 5:
                    continue
                
                # 转换为绝对URL
                if href.startswith('/'):
                    href = self.base_url + href
                elif not href.startswith('http'):
                    continue
                
                # 提取日期
                date_elem = item.find('span', class_=re.compile(r'date|time', re.I))
                if not date_elem:
                    date_elem = item.find('time')
                
                publish_date = None
                if date_elem:
                    publish_date = self.parse_date(date_elem.get_text(strip=True))
                
                # 提取摘要
                summary_elem = item.find('div', class_=re.compile(r'summary|description|teaser', re.I))
                if not summary_elem:
                    summary_elem = item.find('p')
                
                summary = None
                if summary_elem:
                    summary = summary_elem.get_text(strip=True)[:500]
                
                regulations.append({
                    'title': title,
                    'url': href,
                    'publish_date': publish_date,
                    'summary': summary,
                    'source': 'FDA'
                })
                
            except Exception as e:
                logger.warning(f"解析项目失败: {e}")
                continue
        
        logger.info(f"找到 {len(regulations)} 条FDA法规")
        return regulations
    
    def crawl_detail(self, regulation: Dict) -> Optional[Dict]:
        """爬取法规详情"""
        url = regulation['url']
        logger.info(f"爬取详情: {regulation['title'][:50]}...")
        
        html = self._safe_request(url)
        if not html:
            return regulation  # 返回基本信息
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取更详细的摘要
        content_elem = soup.find('div', class_=re.compile(r'field--name-body|content|article', re.I))
        if content_elem:
            full_text = content_elem.get_text(strip=True)[:1000]
            if not regulation.get('summary'):
                regulation['summary'] = full_text[:500]
        
        # 提取PDF链接
        pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$', re.I))
        if pdf_links:
            pdf_url = pdf_links[0]['href']
            if pdf_url.startswith('/'):
                pdf_url = self.base_url + pdf_url
            regulation['pdf_url'] = pdf_url
        
        return regulation
    
    def save_regulation(self, regulation: Dict) -> bool:
        """保存法规到数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO regulations 
                (title, region, publish_date, summary, url, pdf_url, source, industry, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                regulation['title'],
                '美国',  # FDA法规属于美国
                regulation.get('publish_date'),
                regulation.get('summary'),
                regulation['url'],
                regulation.get('pdf_url'),
                regulation.get('source', 'FDA'),
                '制药'  # 默认行业
            ))
            
            conn.commit()
            conn.close()
            logger.info(f"保存成功: {regulation['title'][:50]}...")
            return True
        except Exception as e:
            logger.error(f"保存失败: {regulation['title'][:50]}... - {e}")
            return False
    
    def run(self, max_items: int = 50):
        """运行爬虫"""
        logger.info("FDA法规爬虫开始运行")
        
        # 爬取列表
        regulations = self.crawl_guidance_page()
        
        # 限制数量
        regulations = regulations[:max_items]
        
        # 爬取详情并保存
        saved_count = 0
        for i, regulation in enumerate(regulations, 1):
            logger.info(f"处理 {i}/{len(regulations)}")
            
            detail = self.crawl_detail(regulation)
            if self.save_regulation(detail):
                saved_count += 1
            
            time.sleep(self.request_delay)
        
        logger.info(f"FDA法规爬虫运行完成，保存 {saved_count} 条法规")
        return saved_count


def main():
    """主函数"""
    crawler = FDARegulationCrawler()
    crawler.run(max_items=30)


if __name__ == '__main__':
    main()
