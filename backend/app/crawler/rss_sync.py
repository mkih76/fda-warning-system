"""
RSS同步服务
负责将RSS数据同步到数据库
"""

import asyncio
from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import AsyncSessionLocal
from ..models_new import Article, Category
from .rss_parser import fetch_rss_feeds, RSSItem
from .rss_config import (
    get_enabled_sources,
    SYNC_CONFIG,
    CONTENT_FILTERS,
    CATEGORY_RULES,
)


class RSSSyncService:
    """RSS同步服务"""

    def __init__(self, config: dict = None):
        self.config = config or SYNC_CONFIG

    async def sync_all(self, sector: str = None) -> dict:
        """同步所有RSS源"""
        print(f"\n{'='*60}")
        print(f"📡 RSS同步开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        stats = {
            'total_fetched': 0,
            'total_saved': 0,
            'total_skipped': 0,
            'errors': 0,
            'by_sector': {},
        }

        try:
            # 1. 获取RSS数据
            items = await fetch_rss_feeds(sector, self.config)
            stats['total_fetched'] = len(items)

            if not items:
                print("⚠️  没有获取到任何数据")
                return stats

            # 2. 保存到数据库
            async with AsyncSessionLocal() as session:
                for item in items:
                    try:
                        saved = await self._save_article(session, item)
                        if saved:
                            stats['total_saved'] += 1
                            sector_key = item.sector
                            stats['by_sector'][sector_key] = stats['by_sector'].get(sector_key, 0) + 1
                        else:
                            stats['total_skipped'] += 1
                    except Exception as e:
                        print(f"❌ 保存失败 {item.title[:30]}: {e}")
                        stats['errors'] += 1

                # 3. 提交事务
                await session.commit()

        except Exception as e:
            print(f"❌ 同步过程出错: {e}")
            stats['errors'] += 1

        # 4. 打印统计
        self._print_stats(stats)

        return stats

    async def _save_article(self, session: AsyncSession, item: RSSItem) -> bool:
        """保存单篇文章到数据库"""
        # 检查是否已存在（基于链接）
        existing = await session.execute(
            select(Article).where(Article.slug == self._generate_slug(item.link))
        )
        if existing.scalar_one_or_none():
            return False

        # 检查是否已存在（基于标题相似度）
        similar = await session.execute(
            select(Article).where(
                and_(
                    Article.title == item.title,
                    Article.sector == item.sector,
                )
            )
        )
        if similar.scalar_one_or_none():
            return False

        # 内容过滤
        if not self._passes_filters(item):
            return False

        # 自动分类
        category_id = await self._auto_categorize(session, item)

        # 创建文章
        article = Article(
            title=item.title,
            slug=self._generate_slug(item.link),
            content=item.content or item.summary,
            content_html=None,  # 可以后续渲染
            summary=item.summary,
            cover_image=item.image_url,
            category_id=category_id,
            sector=item.sector,
            tags=','.join(item.tags) if item.tags else None,
            author_id=None,  # RSS来源没有作者
            status='published',
            access_level='free',
            view_count=0,
            like_count=0,
            is_headline=0,
            hot_score=0,
            seo_title=item.title[:200],
            seo_description=item.summary[:500],
            published_at=item.published_at or datetime.now(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            # RSS特有字段（需要在模型中添加）
            # source_name=item.source_name,
            # source_url=item.source_url,
            # original_url=item.link,
            # language=item.lang,
        )

        session.add(article)

        print(f"  💾 保存: {item.title[:50]}...")

        return True

    def _passes_filters(self, item: RSSItem) -> bool:
        """检查是否通过内容过滤"""
        filters = CONTENT_FILTERS

        # 标题长度
        if len(item.title) < filters.get('min_title_length', 10):
            return False

        # 内容长度（如果有内容）
        content = item.content or item.summary
        if content and len(content) < filters.get('min_content_length', 50):
            return False

        # 排除关键词
        for keyword in filters.get('exclude_keywords', []):
            if keyword.lower() in item.title.lower():
                return False

        return True

    async def _auto_categorize(self, session: AsyncSession, item: RSSItem) -> Optional[int]:
        """自动分类"""
        sector_rules = CATEGORY_RULES.get(item.sector, {})

        # 基于关键词匹配
        for category_name, keywords in sector_rules.items():
            for keyword in keywords:
                if keyword.lower() in item.title.lower() or keyword.lower() in (item.content or '').lower():
                    # 查找或创建分类
                    category = await self._get_or_create_category(
                        session,
                        name=category_name,
                        sector=item.sector,
                    )
                    return category.id

        # 默认返回None（无分类）
        return None

    async def _get_or_create_category(
        self,
        session: AsyncSession,
        name: str,
        sector: str,
    ) -> Category:
        """获取或创建分类"""
        # 查找现有分类
        result = await session.execute(
            select(Category).where(
                and_(
                    Category.name == name,
                    Category.sector == sector,
                )
            )
        )
        category = result.scalar_one_or_none()

        if category:
            return category

        # 创建新分类
        category = Category(
            name=name,
            name_en=name,  # 暂时用中文名
            slug=self._generate_slug(f"{sector}-{name}"),
            sector=sector,
            parent_id=None,
            icon=None,
            sort_order=0,
            description=f"由RSS自动创建的分类：{name}",
        )
        session.add(category)
        await session.flush()  # 获取ID

        return category

    def _generate_slug(self, text: str) -> str:
        """生成URL友好的slug"""
        import re
        import hashlib

        # 移除特殊字符
        slug = re.sub(r'[^\w\s-]', '', text.lower())
        # 替换空格为连字符
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')
        # 限制长度
        slug = slug[:100]
        # 添加hash后缀确保唯一性
        hash_suffix = hashlib.md5(text.encode()).hexdigest()[:8]
        slug = f"{slug}-{hash_suffix}"

        return slug

    def _print_stats(self, stats: dict):
        """打印统计信息"""
        print(f"\n{'='*60}")
        print(f"📊 RSS同步完成统计")
        print(f"{'='*60}")
        print(f"📥 获取文章数: {stats['total_fetched']}")
        print(f"💾 保存文章数: {stats['total_saved']}")
        print(f"⏭️  跳过文章数: {stats['total_skipped']}")
        print(f"❌ 错误数量:   {stats['errors']}")
        print(f"\n📈 各行业统计:")
        for sector, count in stats.get('by_sector', {}).items():
            print(f"  {sector}: {count} 篇")
        print(f"{'='*60}\n")


# 定时任务入口
async def run_rss_sync(sector: str = None):
    """运行RSS同步（定时任务调用）"""
    service = RSSSyncService()
    stats = await service.sync_all(sector)
    return stats


# CLI入口
if __name__ == '__main__':
    import sys

    async def main():
        # 解析命令行参数
        sector = sys.argv[1] if len(sys.argv) > 1 else None

        if sector and sector not in ['pharma', 'cosmetics', 'food']:
            print(f"❌ 无效的sector: {sector}")
            print("   可选值: pharma, cosmetics, food")
            sys.exit(1)

        # 运行同步
        stats = await run_rss_sync(sector)

        # 返回退出码
        if stats['errors'] > 0:
            sys.exit(1)
        sys.exit(0)

    asyncio.run(main())
