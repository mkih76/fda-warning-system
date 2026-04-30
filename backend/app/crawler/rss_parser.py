"""
RSS解析器
负责解析RSS源，提取文章信息
"""

import re
import httpx
import asyncio
from datetime import datetime
from typing import List, Optional, Dict
from dataclasses import dataclass
import hashlib

# 尝试导入feedparser，如果没有安装则使用备用解析
try:
    import feedparser
    HAS_FEEDPARSER = True
except ImportError:
    HAS_FEEDPARSER = False
    print("⚠️  feedparser未安装，使用备用RSS解析器")
    print("   安装命令: pip install feedparser")


@dataclass
class RSSItem:
    """RSS文章数据结构"""
    title: str
    link: str
    summary: str
    content: str
    published_at: Optional[datetime]
    author: Optional[str]
    source_name: str
    source_url: str
    sector: str
    lang: str
    tags: List[str]
    image_url: Optional[str]
    content_hash: str  # 用于去重

    def to_dict(self):
        return {
            'title': self.title,
            'link': self.link,
            'summary': self.summary,
            'content': self.content,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'author': self.author,
            'source_name': self.source_name,
            'source_url': self.source_url,
            'sector': self.sector,
            'lang': self.lang,
            'tags': self.tags,
            'image_url': self.image_url,
            'content_hash': self.content_hash,
        }


class RSSParser:
    """RSS解析器类"""

    def __init__(self, config: dict = None):
        self.config = config or {}
        self.timeout = self.config.get('request_timeout', 30)
        self.user_agent = self.config.get('user_agent', 'Mozilla/5.0 (compatible; PharmaCos-RSS/1.0)')

    async def fetch_feed(self, url: str) -> Optional[str]:
        """获取RSS内容"""
        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'application/rss+xml, application/xml, text/xml',
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers, follow_redirects=True)
                response.raise_for_status()
                return response.text
        except Exception as e:
            print(f"❌ 获取RSS失败 {url}: {e}")
            return None

    def parse_feed(self, content: str, source: dict) -> List[RSSItem]:
        """解析RSS内容"""
        if HAS_FEEDPARSER:
            return self._parse_with_feedparser(content, source)
        else:
            return self._parse_with_regex(content, source)

    def _parse_with_feedparser(self, content: str, source: dict) -> List[RSSItem]:
        """使用feedparser解析"""
        items = []
        feed = feedparser.parse(content)

        for entry in feed.entries[:self.config.get('max_articles_per_source', 10)]:
            try:
                # 提取发布时间
                published_at = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_at = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published_at = datetime(*entry.updated_parsed[:6])

                # 提取内容
                content = ''
                if hasattr(entry, 'content') and entry.content:
                    content = entry.content[0].get('value', '')
                elif hasattr(entry, 'description'):
                    content = entry.description or ''
                elif hasattr(entry, 'summary'):
                    content = entry.summary or ''

                # 清理HTML标签
                content = self._clean_html(content)
                summary = self._generate_summary(content)

                # 提取图片
                image_url = None
                if hasattr(entry, 'media_content') and entry.media_content:
                    image_url = entry.media_content[0].get('url')
                elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                    image_url = entry.media_thumbnail[0].get('url')

                # 提取标签
                tags = []
                if hasattr(entry, 'tags'):
                    tags = [tag.term for tag in entry.tags if hasattr(tag, 'term')]

                # 生成内容hash（用于去重）
                content_hash = self._generate_hash(entry.get('link', '') + entry.get('title', ''))

                item = RSSItem(
                    title=entry.get('title', '').strip(),
                    link=entry.get('link', ''),
                    summary=summary,
                    content=content[:2000],  # 限制长度
                    published_at=published_at,
                    author=entry.get('author'),
                    source_name=source['name'],
                    source_url=source['url'],
                    sector=source['sector'],
                    lang=source['lang'],
                    tags=tags,
                    image_url=image_url,
                    content_hash=content_hash,
                )

                # 过滤无效项
                if self._validate_item(item):
                    items.append(item)

            except Exception as e:
                print(f"⚠️  解析条目失败: {e}")
                continue

        return items

    def _parse_with_regex(self, content: str, source: dict) -> List[RSSItem]:
        """备用正则解析器（当feedparser不可用时）"""
        items = []

        # 简单的XML解析（不完整，仅作备用）
        item_pattern = re.compile(r'<item>(.*?)</item>', re.DOTALL)
        title_pattern = re.compile(r'<title>(.*?)</title>', re.DOTALL)
        link_pattern = re.compile(r'<link>(.*?)</link>', re.DOTALL)
        desc_pattern = re.compile(r'<description>(.*?)</description>', re.DOTALL)

        for match in item_pattern.finditer(content)[:10]:
            item_content = match.group(1)

            title_match = title_pattern.search(item_content)
            link_match = link_pattern.search(item_content)
            desc_match = desc_pattern.search(item_content)

            if not title_match or not link_match:
                continue

            title = self._clean_html(title_match.group(1).strip())
            link = link_match.group(1).strip()
            description = self._clean_html(desc_match.group(1).strip()) if desc_match else ''

            content_hash = self._generate_hash(link + title)

            item = RSSItem(
                title=title,
                link=link,
                summary=self._generate_summary(description),
                content=description[:2000],
                published_at=datetime.now(),  # 无法解析时间
                author=None,
                source_name=source['name'],
                source_url=source['url'],
                sector=source['sector'],
                lang=source['lang'],
                tags=[],
                image_url=None,
                content_hash=content_hash,
            )

            if self._validate_item(item):
                items.append(item)

        return items

    def _clean_html(self, html: str) -> str:
        """清理HTML标签"""
        if not html:
            return ''

        # 移除HTML标签
        clean = re.sub(r'<[^>]+>', '', html)
        # 移除多余空白
        clean = re.sub(r'\s+', ' ', clean)
        # 移除特殊字符
        clean = re.sub(r'&nbsp;', ' ', clean)
        clean = re.sub(r'&amp;', '&', clean)
        clean = re.sub(r'&lt;', '<', clean)
        clean = re.sub(r'&gt;', '>', clean)
        clean = re.sub(r'&quot;', '"', clean)

        return clean.strip()

    def _generate_summary(self, content: str, max_length: int = 200) -> str:
        """生成摘要"""
        if not content:
            return ''

        # 截取前max_length个字符
        summary = content[:max_length]

        # 尝试在句子边界截断
        last_period = max(summary.rfind('。'), summary.rfind('.'), summary.rfind('！'), summary.rfind('？'))
        if last_period > max_length * 0.5:  # 如果截断点在50%之后
            summary = summary[:last_period + 1]
        elif len(content) > max_length:
            summary += '...'

        return summary

    def _generate_hash(self, content: str) -> str:
        """生成内容hash"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def _validate_item(self, item: RSSItem) -> bool:
        """验证文章是否有效"""
        # 标题长度检查
        if len(item.title) < 10:
            return False

        # 必须有链接
        if not item.link:
            return False

        # 排除关键词检查
        exclude_keywords = self.config.get('exclude_keywords', [])
        for keyword in exclude_keywords:
            if keyword.lower() in item.title.lower():
                return False

        return True


class FeedFetcher:
    """批量获取RSS源"""

    def __init__(self, config: dict = None):
        self.config = config or {}
        self.parser = RSSParser(config)
        self.semaphore = asyncio.Semaphore(self.config.get('concurrent_requests', 5))

    async def fetch_single(self, source: dict) -> List[RSSItem]:
        """获取单个源"""
        async with self.semaphore:
            print(f"📥 获取: {source['name']} ({source['url']})")

            content = await self.parser.fetch_feed(source['url'])
            if not content:
                return []

            items = self.parser.parse_feed(content, source)
            print(f"  ✅ 获取 {len(items)} 条: {source['name']}")

            return items

    async def fetch_all(self, sources: List[dict]) -> List[RSSItem]:
        """并发获取所有源"""
        print(f"\n🚀 开始获取 {len(sources)} 个RSS源...\n")

        tasks = [self.fetch_single(source) for source in sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 合并结果
        all_items = []
        for result in results:
            if isinstance(result, list):
                all_items.extend(result)
            elif isinstance(result, Exception):
                print(f"❌ 获取失败: {result}")

        # 去重（基于content_hash）
        seen_hashes = set()
        unique_items = []
        for item in all_items:
            if item.content_hash not in seen_hashes:
                seen_hashes.add(item.content_hash)
                unique_items.append(item)

        # 限制总数
        max_total = self.config.get('max_total_articles', 100)
        if len(unique_items) > max_total:
            unique_items = unique_items[:max_total]

        print(f"\n✅ 完成: 获取 {len(unique_items)} 条唯一文章\n")

        return unique_items


# 便捷函数
async def fetch_rss_feeds(sector: str = None, config: dict = None) -> List[RSSItem]:
    """获取RSS feeds"""
    from .rss_config import get_enabled_sources, SYNC_CONFIG

    if config is None:
        config = SYNC_CONFIG

    sources = get_enabled_sources(sector)

    if not sources:
        print(f"⚠️  没有找到{'sector' if sector else ''}的启用数据源")
        return []

    fetcher = FeedFetcher(config)
    items = await fetcher.fetch_all(sources)

    return items


# 测试用
if __name__ == '__main__':
    async def test():
        print("🧪 RSS解析器测试\n")

        # 测试单个源
        test_source = {
            'name': 'FDA药品新闻',
            'url': 'https://www.fda.gov/about-fda/contact-fda/stay-informed/rss/rss-feeds-drugs/rss.xml',
            'type': 'official',
            'lang': 'en',
            'sector': 'pharma',
            'parser': 'rss',
            'priority': 1,
        }

        parser = RSSParser({'max_articles_per_source': 5})
        items = await parser.fetch_feed(test_source['url'])

        if items:
            parsed = parser.parse_feed(items, test_source)
            print(f"\n📊 解析结果: {len(parsed)} 条\n")
            for item in parsed[:3]:
                print(f"📰 {item.title[:50]}...")
                print(f"   🔗 {item.link}")
                print(f"   📅 {item.published_at}")
                print()
        else:
            print("❌ 获取失败")

    asyncio.run(test())
