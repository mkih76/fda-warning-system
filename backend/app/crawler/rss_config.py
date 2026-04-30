"""
RSS数据源配置
包含所有行业的RSS订阅源
"""

# RSS数据源配置
# type: official（官方）/ industry（行业媒体）/ blog（博客）
# lang: zh（中文）/ en（英文）- 用于判断是否需要翻译
RSS_SOURCES = {
    'pharma': [
        # ===== 官方源 =====
        {
            'name': 'NMPA公告',
            'url': 'https://www.nmpa.gov.cn/yaopin/ypgtg/index.html',
            'type': 'official',
            'lang': 'zh',
            'enabled': True,
            'parser': 'nmpa',  # 特殊解析器
            'priority': 1,
        },
        {
            'name': 'FDA药品新闻',
            'url': 'https://www.fda.gov/about-fda/contact-fda/stay-informed/rss/rss-feeds-drugs/rss.xml',
            'type': 'official',
            'lang': 'en',
            'enabled': True,
            'parser': 'rss',
            'priority': 1,
        },
        {
            'name': 'FDA生物制品',
            'url': 'https://www.fda.gov/about-fda/contact-fda/stay-informed/rss/rss-feeds-biologics/rss.xml',
            'type': 'official',
            'lang': 'en',
            'enabled': True,
            'parser': 'rss',
            'priority': 2,
        },
        {
            'name': 'EMA新闻',
            'url': 'https://www.ema.europa.eu/en/news/rss',
            'type': 'official',
            'lang': 'en',
            'enabled': True,
            'parser': 'rss',
            'priority': 2,
        },

        # ===== 行业媒体 =====
        {
            'name': '医药经济报',
            'url': 'http://www.yyjjb.com/rss.xml',
            'type': 'industry',
            'lang': 'zh',
            'enabled': True,
            'parser': 'rss',
            'priority': 3,
        },
        {
            'name': '药明康德',
            'url': 'https://www.wuxibiologics.com/news/rss',
            'type': 'industry',
            'lang': 'zh',
            'enabled': False,  # 需要确认RSS地址
            'parser': 'rss',
            'priority': 3,
        },
        {
            'name': 'Endpoints News',
            'url': 'https://endpts.com/feed/',
            'type': 'industry',
            'lang': 'en',
            'enabled': True,
            'parser': 'rss',
            'priority': 4,
        },
        {
            'name': 'Fierce Pharma',
            'url': 'https://www.fiercepharma.com/rss/xml',
            'type': 'industry',
            'lang': 'en',
            'enabled': True,
            'parser': 'rss',
            'priority': 4,
        },
    ],

    'cosmetics': [
        # ===== 官方源 =====
        {
            'name': 'FDA化妆品',
            'url': 'https://www.fda.gov/cosmetics/rss',
            'type': 'official',
            'lang': 'en',
            'enabled': True,
            'parser': 'rss',
            'priority': 1,
        },
        {
            'name': '欧盟SCCS',
            'url': 'https://ec.europa.eu/health/scientific_committees/rss',
            'type': 'official',
            'lang': 'en',
            'enabled': True,
            'parser': 'rss',
            'priority': 2,
        },
        {
            'name': 'NMPA化妆品',
            'url': 'https://www.nmpa.gov.cn/hzhp/index.html',
            'type': 'official',
            'lang': 'zh',
            'enabled': True,
            'parser': 'nmpa',
            'priority': 1,
        },

        # ===== 行业媒体 =====
        {
            'name': '中国化妆品',
            'url': 'http://www.cnfc.org.cn/rss',
            'type': 'industry',
            'lang': 'zh',
            'enabled': False,  # 需要确认
            'parser': 'rss',
            'priority': 3,
        },
        {
            'name': 'Cosmetics Design',
            'url': 'https://www.cosmeticsdesign.com/rss',
            'type': 'industry',
            'lang': 'en',
            'enabled': True,
            'parser': 'rss',
            'priority': 4,
        },
        {
            'name': 'Cosmetics Business',
            'url': 'https://www.cosmeticsbusiness.com/rss',
            'type': 'industry',
            'lang': 'en',
            'enabled': True,
            'parser': 'rss',
            'priority': 4,
        },
    ],

    'food': [
        # ===== 官方源 =====
        {
            'name': 'FDA食品安全',
            'url': 'https://www.fda.gov/food/rss',
            'type': 'official',
            'lang': 'en',
            'enabled': True,
            'parser': 'rss',
            'priority': 1,
        },
        {
            'name': '食品安全网',
            'url': 'http://www.foodmate.net/rss',
            'type': 'industry',
            'lang': 'zh',
            'enabled': True,
            'parser': 'rss',
            'priority': 1,
        },
        {
            'name': '市场监管总局',
            'url': 'https://www.samr.gov.cn/rss',
            'type': 'official',
            'lang': 'zh',
            'enabled': False,  # 需要确认
            'parser': 'rss',
            'priority': 1,
        },

        # ===== 行业媒体 =====
        {
            'name': 'Food Navigator',
            'url': 'https://www.foodnavigator.com/rss',
            'type': 'industry',
            'lang': 'en',
            'enabled': True,
            'parser': 'rss',
            'priority': 3,
        },
        {
            'name': 'Food Safety News',
            'url': 'https://www.foodsafetynews.com/feed/',
            'type': 'industry',
            'lang': 'en',
            'enabled': True,
            'parser': 'rss',
            'priority': 3,
        },
        {
            'name': 'Food Engineering Mag',
            'url': 'https://www.foodengineeringmag.com/rss',
            'type': 'industry',
            'lang': 'en',
            'enabled': True,
            'parser': 'rss',
            'priority': 4,
        },
    ],

    'general': [
        # ===== 综合 =====
        {
            'name': 'WHO新闻',
            'url': 'https://www.who.int/rss-feeds/news-english.xml',
            'type': 'official',
            'lang': 'en',
            'enabled': True,
            'parser': 'rss',
            'priority': 2,
        },
    ]
}


# 同步配置
SYNC_CONFIG = {
    'max_articles_per_source': 10,  # 每个源最多抓取10条
    'max_total_articles': 100,      # 每次同步最多100条
    'request_timeout': 30,          # 请求超时（秒）
    'retry_times': 3,               # 重试次数
    'retry_delay': 5,               # 重试间隔（秒）
    'user_agent': 'Mozilla/5.0 (compatible; PharmaCos-RSS/1.0)',
    'concurrent_requests': 5,       # 并发请求数
}


# 内容过滤规则
CONTENT_FILTERS = {
    # 最小内容长度（字符）
    'min_title_length': 10,
    'min_content_length': 50,

    # 排除的关键词（标题中包含这些词的将被过滤）
    'exclude_keywords': [
        '广告', '推广', '赞助', 'sponsored', 'advertisement',
        '招聘', '诚聘', 'vacancy', 'hiring',
    ],

    # 必须包含的关键词（至少包含一个）
    'include_keywords': [
        'FDA', 'NMPA', 'GMP', '法规', '标准', '认证',
        '安全', '质量', '合规', '监管', '检查',
        'drug', 'pharma', 'cosmetic', 'food', 'safety',
        'regulation', 'compliance', 'FDA', 'GMP',
    ],
}


# 分类规则（基于关键词自动分类到子类别）
CATEGORY_RULES = {
    'pharma': {
        'GMP法规': ['GMP', 'cGMP', '生产质量管理', 'manufacturing'],
        '注册申报': ['注册', '申报', 'approval', 'filing'],
        'ICH指南': ['ICH', '指南', 'guideline'],
        'FDA警告信': ['警告信', 'warning letter', 'FDA'],
        '行业动态': ['批准', '上市', '临床', 'approval', 'clinical'],
    },
    'cosmetics': {
        '安全评估': ['安全评估', 'safety assessment', 'SCCS'],
        '功效宣称': ['功效', 'claim', 'efficacy'],
        '原料合规': ['原料', 'ingredient', '成分'],
        'MoCRA': ['MoCRA', '不良反应', 'adverse'],
        '标签标识': ['标签', 'label', '标识'],
    },
    'food': {
        '食品安全': ['食品安全', 'food safety', '微生物', '污染物'],
        '添加剂': ['添加剂', 'additive', '防腐剂'],
        '认证标准': ['FSSC', 'ISO', 'HACCP', '认证'],
        '进出口': ['进出口', 'import', 'export', '海关'],
        '标签标识': ['标签', 'label', '标识'],
    }
}


def get_enabled_sources(sector=None):
    """获取启用的数据源"""
    sources = []
    sectors = [sector] if sector else RSS_SOURCES.keys()

    for s in sectors:
        if s in RSS_SOURCES:
            for source in RSS_SOURCES[s]:
                if source['enabled']:
                    sources.append({
                        **source,
                        'sector': s,
                    })

    # 按优先级排序
    sources.sort(key=lambda x: x['priority'])
    return sources


def get_source_count():
    """获取数据源统计"""
    stats = {}
    for sector, sources in RSS_SOURCES.items():
        enabled = sum(1 for s in sources if s['enabled'])
        total = len(sources)
        stats[sector] = {
            'enabled': enabled,
            'total': total,
        }
    return stats


if __name__ == '__main__':
    # 测试配置
    print("📊 RSS数据源配置统计：\n")

    stats = get_source_count()
    for sector, count in stats.items():
        print(f"{sector}: {count['enabled']}/{count['total']} 启用")

    print(f"\n总计: {sum(s['enabled'] for s in stats.values())} 个启用源")

    print("\n📋 启用的数据源：\n")
    sources = get_enabled_sources()
    for source in sources:
        print(f"  [{source['sector']}] {source['name']} ({source['lang']})")
