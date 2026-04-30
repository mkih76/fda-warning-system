"""
PharmaCos Insight - Content Management API
Handles categories and articles for all sectors.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json

from ..database import get_db
from ..models_new import Article, Category, User
from .auth import get_current_user, require_user, require_admin

import re


def markdown_to_html(md_text: str) -> str:
    """Convert Markdown to HTML with proper formatting."""
    if not md_text:
        return ""

    lines = md_text.split('\n')
    html_lines = []
    in_table = False
    table_rows = []
    in_list = False
    list_type = None  # 'ul' or 'ol'
    in_blockquote = False

    def flush_list():
        nonlocal in_list, list_type
        if in_list:
            tag = list_type or 'ul'
            html_lines.append(f'</{tag}>')
            in_list = False
            list_type = None

    def flush_blockquote():
        nonlocal in_blockquote
        if in_blockquote:
            html_lines.append('</blockquote>')
            in_blockquote = False

    def flush_table():
        nonlocal in_table, table_rows
        if in_table and table_rows:
            html_lines.append('<table>')
            for i, row in enumerate(table_rows):
                cells = [c.strip() for c in row.strip('|').split('|')]
                tag = 'th' if i == 0 else 'td'
                row_tag = 'thead' if i == 0 else ('tbody' if i == 1 else '')
                if i == 0:
                    html_lines.append('<thead>')
                if i == 1:
                    html_lines.append('<tbody>')
                html_lines.append('<tr>' + ''.join(f'<{tag}>{inline_format(c)}</{tag}>' for c in cells) + '</tr>')
                if i == 0:
                    html_lines.append('</thead>')
            if len(table_rows) > 1:
                html_lines.append('</tbody>')
            html_lines.append('</table>')
            table_rows = []
            in_table = False

    def inline_format(text):
        """Handle inline Markdown: bold, italic, code, links."""
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Italic
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        # Inline code
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
        # Links
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
        # Strikethrough
        text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
        return text

    for line in lines:
        stripped = line.strip()

        # Empty line
        if not stripped:
            flush_list()
            flush_blockquote()
            flush_table()
            continue

        # Table separator line (e.g., |---|---|)
        if re.match(r'^\|[\s\-:|]+\|$', stripped):
            continue  # Skip separator

        # Table row
        if stripped.startswith('|') and stripped.endswith('|'):
            if not in_table:
                in_table = True
            table_rows.append(stripped)
            continue
        else:
            flush_table()

        # Headings
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if heading_match:
            flush_list()
            flush_blockquote()
            level = len(heading_match.group(1))
            text = inline_format(heading_match.group(2))
            html_lines.append(f'<h{level}>{text}</h{level}>')
            continue

        # Blockquote
        if stripped.startswith('>'):
            if not in_blockquote:
                in_blockquote = True
                html_lines.append('<blockquote>')
            text = inline_format(stripped.lstrip('> '))
            html_lines.append(f'<p>{text}</p>')
            continue
        elif in_blockquote:
            flush_blockquote()

        # Unordered list
        list_match = re.match(r'^[-*•]\s+(.+)$', stripped)
        if list_match:
            flush_blockquote()
            if not in_list or list_type != 'ul':
                flush_list()
                html_lines.append('<ul>')
                in_list = True
                list_type = 'ul'
            html_lines.append(f'<li>{inline_format(list_match.group(1))}</li>')
            continue

        # Ordered list
        ol_match = re.match(r'^(\d+)[.)]\s+(.+)$', stripped)
        if ol_match:
            flush_blockquote()
            if not in_list or list_type != 'ol':
                flush_list()
                html_lines.append('<ol>')
                in_list = True
                list_type = 'ol'
            html_lines.append(f'<li>{inline_format(ol_match.group(2))}</li>')
            continue

        # Regular paragraph
        flush_list()
        flush_blockquote()
        html_lines.append(f'<p>{inline_format(stripped)}</p>')

    flush_list()
    flush_blockquote()
    flush_table()

    return '\n'.join(html_lines)

router = APIRouter(prefix="/api/content", tags=["content"])


# ─── Schemas ───────────────────────────────────────────────────
class CategoryResponse(BaseModel):
    id: int
    name: str
    name_en: Optional[str]
    slug: str
    sector: str
    parent_id: Optional[int]
    sort_order: int
    description: Optional[str]

    class Config:
        from_attributes = True


class ArticleListItem(BaseModel):
    id: int
    title: str
    slug: str
    summary: Optional[str]
    sector: Optional[str]
    category_name: Optional[str] = None
    access_level: str
    view_count: int
    published_at: Optional[datetime]
    cover_image: Optional[str]

    class Config:
        from_attributes = True


class ArticleDetailResponse(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    content_html: Optional[str]
    summary: Optional[str]
    sector: Optional[str]
    category_id: Optional[int]
    category_name: Optional[str] = None
    tags: Optional[str]
    access_level: str
    view_count: int
    like_count: int
    published_at: Optional[datetime]
    author_name: Optional[str] = None
    seo_title: Optional[str]
    seo_description: Optional[str]

    class Config:
        from_attributes = True


class CreateArticleRequest(BaseModel):
    title: str
    slug: Optional[str] = None
    content: str
    summary: Optional[str] = None
    sector: str
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None
    access_level: str = "free"
    cover_image: Optional[str] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None


class UpdateArticleRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    sector: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None
    access_level: Optional[str] = None
    status: Optional[str] = None
    cover_image: Optional[str] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None


class PaginatedArticles(BaseModel):
    items: List[ArticleListItem]
    total: int
    page: int
    page_size: int


class HomeDataResponse(BaseModel):
    sectors: dict
    latest_articles: List[ArticleListItem]


# ─── Helper ────────────────────────────────────────────────────
def make_slug(title: str) -> str:
    """Generate a simple slug from title."""
    import re
    slug = title.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:200]


def article_to_list_item(article: Article, db: Session) -> dict:
    cat_name = None
    if article.category_id:
        cat = db.query(Category).filter(Category.id == article.category_id).first()
        cat_name = cat.name if cat else None
    return {
        "id": article.id,
        "title": article.title,
        "slug": article.slug,
        "summary": article.summary,
        "sector": article.sector,
        "category_name": cat_name,
        "access_level": article.access_level,
        "view_count": article.view_count,
        "published_at": article.published_at,
        "cover_image": article.cover_image,
    }


# ─── Categories ────────────────────────────────────────────────
@router.get("/categories", response_model=List[CategoryResponse])
def list_categories(
    sector: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all categories, optionally filtered by sector."""
    q = db.query(Category)
    if sector:
        q = q.filter(Category.sector == sector)
    return q.order_by(Category.sector, Category.sort_order).all()


@router.get("/categories/{slug}", response_model=CategoryResponse)
def get_category(slug: str, db: Session = Depends(get_db)):
    """Get a single category by slug."""
    cat = db.query(Category).filter(Category.slug == slug).first()
    if not cat:
        raise HTTPException(status_code=404, detail="分类不存在")
    return cat


# ─── Articles ──────────────────────────────────────────────────
@router.get("/articles", response_model=PaginatedArticles)
def list_articles(
    sector: Optional[str] = None,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    status: str = "published",
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List articles with filters."""
    q = db.query(Article).filter(Article.status == status)

    if sector:
        q = q.filter(Article.sector == sector)

    if category:
        cat = db.query(Category).filter(Category.slug == category).first()
        if cat:
            q = q.filter(Article.category_id == cat.id)

    if search:
        q = q.filter(
            (Article.title.ilike(f"%{search}%")) |
            (Article.summary.ilike(f"%{search}%"))
        )

    if tag:
        q = q.filter(Article.tags.ilike(f'%"{tag}"%'))

    total = q.count()
    articles = (
        q.order_by(desc(Article.published_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    items = [article_to_list_item(a, db) for a in articles]
    return PaginatedArticles(items=items, total=total, page=page, page_size=page_size)


@router.get("/articles/{slug}", response_model=ArticleDetailResponse)
def get_article(slug: str, db: Session = Depends(get_db)):
    """Get a single article by slug."""
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    # Increment view count
    article.view_count = (article.view_count or 0) + 1
    db.commit()

    cat_name = None
    if article.category_id:
        cat = db.query(Category).filter(Category.id == article.category_id).first()
        cat_name = cat.name if cat else None

    author_name = None
    if article.author_id:
        author = db.query(User).filter(User.id == article.author_id).first()
        author_name = author.nickname if author else None

    # Convert Markdown to HTML on-the-fly if content_html is missing
    content_html = article.content_html
    if not content_html and article.content:
        content_html = markdown_to_html(article.content)

    return ArticleDetailResponse(
        id=article.id,
        title=article.title,
        slug=article.slug,
        content=article.content,
        content_html=content_html,
        summary=article.summary,
        sector=article.sector,
        category_id=article.category_id,
        category_name=cat_name,
        tags=article.tags,
        access_level=article.access_level,
        view_count=article.view_count,
        like_count=article.like_count,
        published_at=article.published_at,
        author_name=author_name,
        seo_title=article.seo_title,
        seo_description=article.seo_description,
    )


# ─── Admin: Create/Update/Delete Articles ─────────────────────
@router.post("/articles", response_model=ArticleDetailResponse)
def create_article(
    req: CreateArticleRequest,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new article (admin only)."""
    slug = req.slug or make_slug(req.title)

    # Check slug uniqueness
    existing = db.query(Article).filter(Article.slug == slug).first()
    if existing:
        slug = f"{slug}-{int(datetime.utcnow().timestamp())}"

    article = Article(
        title=req.title,
        slug=slug,
        content=req.content,
        summary=req.summary,
        sector=req.sector,
        category_id=req.category_id,
        tags=json.dumps(req.tags) if req.tags else None,
        access_level=req.access_level,
        cover_image=req.cover_image,
        author_id=user.id,
        status="published",
        published_at=datetime.utcnow(),
        seo_title=req.seo_title,
        seo_description=req.seo_description,
    )
    db.add(article)
    db.commit()
    db.refresh(article)

    return ArticleDetailResponse(
        id=article.id,
        title=article.title,
        slug=article.slug,
        content=article.content,
        content_html=article.content_html,
        summary=article.summary,
        sector=article.sector,
        category_id=article.category_id,
        tags=article.tags,
        access_level=article.access_level,
        view_count=0,
        like_count=0,
        published_at=article.published_at,
        author_name=user.nickname,
    )


@router.put("/articles/{article_id}", response_model=ArticleDetailResponse)
def update_article(
    article_id: int,
    req: UpdateArticleRequest,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update an article (admin only)."""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    for field, value in req.model_dump(exclude_unset=True).items():
        if field == "tags" and value is not None:
            value = json.dumps(value)
        setattr(article, field, value)

    article.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(article)

    return ArticleDetailResponse(
        id=article.id,
        title=article.title,
        slug=article.slug,
        content=article.content,
        content_html=article.content_html,
        summary=article.summary,
        sector=article.sector,
        category_id=article.category_id,
        tags=article.tags,
        access_level=article.access_level,
        view_count=article.view_count,
        like_count=article.like_count,
        published_at=article.published_at,
    )


@router.delete("/articles/{article_id}")
def delete_article(
    article_id: int,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete an article (admin only)."""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    db.delete(article)
    db.commit()
    return {"message": "已删除"}


# ─── Home Data ─────────────────────────────────────────────────
@router.get("/home")
def get_home_data(db: Session = Depends(get_db)):
    """Get aggregated data for the homepage."""
    sectors = {}
    for sector in ["pharma", "cosmetics", "food"]:
        articles = (
            db.query(Article)
            .filter(Article.sector == sector, Article.status == "published")
            .order_by(desc(Article.published_at))
            .limit(5)
            .all()
        )
        sectors[sector] = [article_to_list_item(a, db) for a in articles]

    latest = (
        db.query(Article)
        .filter(Article.status == "published")
        .order_by(desc(Article.published_at))
        .limit(10)
        .all()
    )

    return {
        "sectors": sectors,
        "latest_articles": [article_to_list_item(a, db) for a in latest],
    }


@router.get("/sector/{sector}")
def get_sector_data(sector: str, db: Session = Depends(get_db)):
    """Get data for a sector home page."""
    categories = (
        db.query(Category)
        .filter(Category.sector == sector)
        .order_by(Category.sort_order)
        .all()
    )

    latest = (
        db.query(Article)
        .filter(Article.sector == sector, Article.status == "published")
        .order_by(desc(Article.published_at))
        .limit(10)
        .all()
    )

    return {
        "categories": [
            {"id": c.id, "name": c.name, "name_en": c.name_en, "slug": c.slug, "description": c.description}
            for c in categories
        ],
        "latest_articles": [article_to_list_item(a, db) for a in latest],
    }


# ─── Global Search (articles + FDA letters) ───────────────────
@router.get("/search")
def global_search(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Search across articles and FDA warning letters."""
    results = []

    # Search articles
    articles = (
        db.query(Article)
        .filter(
            Article.status == "published",
            (Article.title.ilike(f"%{q}%")) | (Article.summary.ilike(f"%{q}%"))
        )
        .limit(limit)
        .all()
    )
    for a in articles:
        results.append({
            "type": "article",
            "id": a.id,
            "title": a.title,
            "slug": a.slug,
            "summary": a.summary,
            "sector": a.sector,
            "url": f"/{a.sector}/article/{a.slug}",
        })

    # Search FDA warning letters
    from ..models import WarningLetter
    letters = (
        db.query(WarningLetter)
        .filter(
            (WarningLetter.company_name.ilike(f"%{q}%")) |
            (WarningLetter.subject.ilike(f"%{q}%"))
        )
        .limit(limit)
        .all()
    )
    for l in letters:
        results.append({
            "type": "letter",
            "id": l.id,
            "title": l.company_name,
            "summary": l.subject,
            "url": f"/letters/{l.id}",
        })

    return {"results": results[:limit], "total": len(results)}
