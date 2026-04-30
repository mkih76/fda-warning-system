#!/usr/bin/env python3
"""
PharmaCos Insight - Batch Article Import Script
Parses articles from a text file and inserts them into the database.

Usage:
  1. Save articles text to articles_input.txt (in the ---ARTICLE--- format)
  2. Run: python -m backend.scripts.import_articles articles_input.txt
  3. Or on VPS: docker cp articles_input.txt fda-warning-backend:/tmp/
                docker exec fda-warning-backend python -m backend.scripts.import_articles /tmp/articles_input.txt
"""
import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import SessionLocal, Base, engine
from app.models_new import Article, Category
from datetime import datetime

Base.metadata.create_all(bind=engine)


def parse_articles(text):
    """Parse articles from the ---ARTICLE--- ... ---END--- format."""
    articles = []
    blocks = re.split(r'---ARTICLE---', text)
    for block in blocks:
        if '---END---' not in block:
            continue
        block = block.split('---END---')[0].strip()

        article = {}
        # Extract fields
        for field in ['TITLE', 'SLUG', 'CATEGORY', 'SUMMARY', 'ACCESS']:
            match = re.search(rf'^{field}:\s*(.+)$', block, re.MULTILINE)
            if match:
                article[field.lower()] = match.group(1).strip()

        # Extract content (everything after CONTENT:)
        content_match = re.search(r'CONTENT:\s*\n(.*)', block, re.DOTALL)
        if content_match:
            article['content'] = content_match.group(1).strip()

        if article.get('title') and article.get('content'):
            articles.append(article)

    return articles


def import_articles(filepath, sector=None):
    """Import articles from file into database."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    articles = parse_articles(text)
    if not articles:
        print("No articles found in the input file.")
        return

    db = SessionLocal()
    imported = 0
    skipped = 0

    for art in articles:
        slug = art.get('slug', '')
        # Check if already exists
        existing = db.query(Article).filter(Article.slug == slug).first()
        if existing:
            print(f"  = Skipping (exists): {art.get('title', '?')}")
            skipped += 1
            continue

        # Find category
        cat_slug = art.get('category', '')
        cat = db.query(Category).filter(Category.slug == cat_slug).first()

        # Determine sector from category
        art_sector = sector
        if cat:
            art_sector = cat.sector
        elif not art_sector:
            # Try to guess from category slug
            if 'cosmetic' in cat_slug or 'formulation' in cat_slug or 'efficacy' in cat_slug or 'ingredient' in cat_slug or 'labeling-claims' in cat_slug or 'manufacturing' in cat_slug:
                art_sector = 'cosmetics'
            elif 'food' in cat_slug or 'haccp' in cat_slug or 'nutrition' in cat_slug:
                art_sector = 'food'
            else:
                art_sector = 'pharma'

        article = Article(
            title=art.get('title', ''),
            slug=slug,
            content=art.get('content', ''),
            summary=art.get('summary', ''),
            sector=art_sector,
            category_id=cat.id if cat else None,
            access_level=art.get('access', 'free'),
            status='published',
            published_at=datetime.utcnow(),
            view_count=0,
            like_count=0,
        )
        db.add(article)
        imported += 1
        print(f"  + Imported: {art.get('title', '?')} [{art_sector}]")

    db.commit()
    db.close()

    print(f"\nDone: {imported} imported, {skipped} skipped")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python -m backend.scripts.import_articles <filepath> [sector]")
        print("  sector: pharma, cosmetics, food (optional, auto-detected from category)")
        sys.exit(1)

    filepath = sys.argv[1]
    sector = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)

    import_articles(filepath, sector)
