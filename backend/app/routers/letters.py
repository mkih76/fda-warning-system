"""
FDA 警告信 CRUD + 统计接口
"""
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..database import get_db
from ..models import WarningLetter, Violation, CfrCitation, AiAnalysis

router = APIRouter()


@router.get("/")
async def list_letters(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    office: str = None,
    status: str = None,
    company: str = None,
    date_from: date = None,
    date_to: date = None,
    db: AsyncSession = Depends(get_db),
):
    """分页查询警告信列表，支持多条件筛选"""
    stmt = select(WarningLetter)

    if office:
        stmt = stmt.where(WarningLetter.issuing_office == office)
    if status:
        stmt = stmt.where(WarningLetter.status == status)
    if company:
        stmt = stmt.where(WarningLetter.company_name.ilike(f"%{company}%"))
    if date_from:
        stmt = stmt.where(WarningLetter.posted_date >= date_from)
    if date_to:
        stmt = stmt.where(WarningLetter.posted_date <= date_to)

    # 总数
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar() or 0

    # 分页
    stmt = stmt.order_by(WarningLetter.posted_date.desc())\
               .offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(stmt)
    items = result.scalars().all()

    return {
        "items": [
            {
                "id": l.id,
                "fda_id": l.fda_id,
                "company_name": l.company_name,
                "subject": l.subject,
                "issuing_office": l.issuing_office,
                "posted_date": str(l.posted_date) if l.posted_date else None,
                "status": l.status,
                "fei_number": l.fei_number,
                "country": l.country,
            }
            for l in items
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.get("/{letter_id}")
async def get_letter(letter_id: int, db: AsyncSession = Depends(get_db)):
    """获取单封警告信详情（含违规、CFR引用、AI分析）"""
    stmt = (
        select(WarningLetter)
        .options(
            selectinload(WarningLetter.violations),
            selectinload(WarningLetter.citations),
            selectinload(WarningLetter.analysis),
        )
        .where(WarningLetter.id == letter_id)
    )
    result = await db.execute(stmt)
    letter = result.scalar_one_or_none()
    if not letter:
        raise HTTPException(404, detail="警告信不存在")

    return {
        "id": letter.id,
        "fda_id": letter.fda_id,
        "company_name": letter.company_name,
        "subject": letter.subject,
        "issuing_office": letter.issuing_office,
        "posted_date": str(letter.posted_date) if letter.posted_date else None,
        "issue_date": str(letter.issue_date) if letter.issue_date else None,
        "fei_number": letter.fei_number,
        "country": letter.country,
        "full_text": letter.full_text_clean or letter.full_text,
        "url": letter.url,
        "status": letter.status,
        "closeout_date": str(letter.closeout_date) if letter.closeout_date else None,
        "violations": [
            {
                "system_category": v.system_category,
                "violation_type": v.violation_type,
                "severity": v.severity,
                "description": v.description,
                "description_zh": v.description_zh,
            }
            for v in (letter.violations or [])
        ],
        "citations": [
            {"cfr_part": c.cfr_part, "cfr_section": c.cfr_section, "cfr_text": c.cfr_text}
            for c in (letter.citations or [])
        ],
        "analysis": {
            "summary_en": letter.analysis.summary_en,
            "summary_zh": letter.analysis.summary_zh,
            "key_findings": letter.analysis.key_findings,
        }
        if letter.analysis
        else None,
    }


@router.get("/company/{company_name:path}")
async def get_company_timeline(company_name: str, db: AsyncSession = Depends(get_db)):
    """查询企业全链路追踪时间线"""
    stmt = (
        select(WarningLetter)
        .where(WarningLetter.company_name.ilike(f"%{company_name}%"))
        .order_by(WarningLetter.posted_date.desc())
    )
    result = await db.execute(stmt)
    letters = result.scalars().all()

    return [
        {
            "fda_id": l.fda_id,
            "subject": l.subject,
            "posted_date": str(l.posted_date),
            "status": l.status,
            "issuing_office": l.issuing_office,
            "closeout_date": str(l.closeout_date) if l.closeout_date else None,
            "fei_number": l.fei_number,
        }
        for l in letters
    ]


@router.get("/stats/offices")
async def get_office_stats(db: AsyncSession = Depends(get_db)):
    """各签发办公室警告信数量统计"""
    stmt = (
        select(WarningLetter.issuing_office, func.count(WarningLetter.id))
        .where(WarningLetter.issuing_office.isnot(None))
        .group_by(WarningLetter.issuing_office)
        .order_by(func.count(WarningLetter.id).desc())
    )
    result = await db.execute(stmt)
    return [{"office": row[0], "count": row[1]} for row in result]


@router.get("/stats/timeline")
async def get_timeline_stats(year: int = None, db: AsyncSession = Depends(get_db)):
    """年度时间线统计"""
    stmt = select(
        func.strftime("%Y", WarningLetter.posted_date).label("year"),
        func.count(WarningLetter.id).label("count"),
    )
    if year:
        stmt = stmt.where(func.strftime("%Y", WarningLetter.posted_date) == str(year))
    stmt = stmt.group_by("year").order_by("year")
    result = await db.execute(stmt)
    return [{"year": row[0], "count": row[1]} for row in result]
