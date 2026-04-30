"""
FDA 警告信全文搜索接口
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import WarningLetter

router = APIRouter()


@router.get("/")
async def search_letters(
    q: str = Query(..., min_length=1),
    field: str = Query("all", regex="^(all|company|subject|full_text|cfr)$"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """搜索警告信，支持多字段"""
    stmt = select(WarningLetter)
    like_pattern = f"%{q}%"

    if field == "company":
        stmt = stmt.where(WarningLetter.company_name.ilike(like_pattern))
    elif field == "subject":
        stmt = stmt.where(WarningLetter.subject.ilike(like_pattern))
    elif field == "full_text":
        stmt = stmt.where(WarningLetter.full_text_clean.ilike(like_pattern))
    elif field == "cfr":
        from ..models import CfrCitation
        stmt = (
            select(WarningLetter)
            .join(CfrCitation)
            .where(CfrCitation.cfr_section.ilike(like_pattern))
        )
    else:
        stmt = stmt.where(
            or_(
                WarningLetter.company_name.ilike(like_pattern),
                WarningLetter.subject.ilike(like_pattern),
                WarningLetter.full_text_clean.ilike(like_pattern),
            )
        )

    from sqlalchemy import func
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar() or 0

    stmt = stmt.order_by(WarningLetter.posted_date.desc())\
               .offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(stmt)
    items = result.scalars().all()

    return {
        "items": [
            {
                "id": l.id,
                "company_name": l.company_name,
                "subject": l.subject,
                "issuing_office": l.issuing_office,
                "posted_date": str(l.posted_date) if l.posted_date else None,
                "status": l.status,
            }
            for l in items
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
        "query": q,
    }
