"""
PharmaCos Insight - New Database Models
These tables are ADDITIVE — they do NOT modify existing tables.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime


# Import the existing Base from models.py to use the same metadata
from .models import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nickname = Column(String(100))
    company = Column(String(200))
    role = Column(String(50), default='free')  # free/pro/enterprise/admin
    avatar_url = Column(String(500))
    wechat_openid = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime)
    is_active = Column(Integer, default=1)

    # Relationships
    memberships = relationship('Membership', back_populates='user')
    favorites = relationship('UserFavorite', back_populates='user')


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)       # 中文名
    name_en = Column(String(100))                     # 英文名
    slug = Column(String(100), unique=True, nullable=False)
    sector = Column(String(50), nullable=False)       # pharma/cosmetics/food/general/tools
    parent_id = Column(Integer)                       # 支持二级分类
    icon = Column(String(50))
    sort_order = Column(Integer, default=0)
    description = Column(Text)

    articles = relationship('Article', back_populates='category')


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    slug = Column(String(500), unique=True)
    content = Column(Text, nullable=False)            # Markdown 格式
    content_html = Column(Text)                       # 渲染后的 HTML
    summary = Column(String(1000))
    cover_image = Column(String(500))
    category_id = Column(Integer, ForeignKey('categories.id'))
    sector = Column(String(50))                       # pharma/cosmetics/food/general (冗余)
    tags = Column(Text)                               # JSON 数组字符串
    author_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String(20), default='draft')      # draft/published/archived
    access_level = Column(String(20), default='free') # free/pro/enterprise
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    is_headline = Column(Integer, default=0)          # 是否为头条新闻 0/1
    hot_score = Column(Integer, default=0)            # 热度分
    seo_title = Column(String(200))
    seo_description = Column(String(500))
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # RSS相关字段
    source_type = Column(String(20), default='manual')  # manual/rss/ai_generated
    source_name = Column(String(100))                    # 来源名称（如"FDA新闻"）
    source_url = Column(String(500))                     # RSS源URL
    original_url = Column(String(500))                   # 原文链接
    language = Column(String(10), default='zh')          # 语言代码
    content_hash = Column(String(32))                    # 内容hash（用于去重）

    # Relationships
    category = relationship('Category', back_populates='articles')
    author = relationship('User')


class Membership(Base):
    __tablename__ = 'memberships'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    plan = Column(String(50), nullable=False)         # free/pro/enterprise/flagship
    started_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime)
    payment_method = Column(String(50))               # wechat/alipay
    amount_cents = Column(Integer)                    # 金额（分）
    is_active = Column(Integer, default=1)

    user = relationship('User', back_populates='memberships')


class UserFavorite(Base):
    __tablename__ = 'user_favorites'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    item_type = Column(String(50), nullable=False)    # letter/article
    item_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='favorites')

    __table_args__ = (
        UniqueConstraint('user_id', 'item_type', 'item_id', name='uq_user_favorite'),
    )


class ReadHistory(Base):
    __tablename__ = 'read_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    article_id = Column(Integer, ForeignKey('articles.id'))
    read_at = Column(DateTime, default=datetime.utcnow)
    read_duration = Column(Integer)                   # 阅读时长（秒）


class Subscription(Base):
    """邮件订阅"""
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100))
    sectors = Column(Text)  # JSON数组: ["pharma", "cosmetics", "food"]
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_notified_at = Column(DateTime)


# 给Article添加is_headline字段
# 注意：这个字段需要在数据库迁移时添加
# ALTER TABLE articles ADD COLUMN is_headline BOOLEAN DEFAULT false;
