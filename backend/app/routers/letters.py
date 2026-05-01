from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from ..database import get_db
from ..models import WarningLetter, AiAnalysis, Violation, CFRCitation

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
    # 主查询 + eager load ai_analysis
    stmt = select(WarningLetter).options(selectinload(WarningLetter.ai_analysis))

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
    count_stmt = select(func.count()).select_from(WarningLetter)
    if office:
        count_stmt = count_stmt.where(WarningLetter.issuing_office == office)
    if status:
        count_stmt = count_stmt.where(WarningLetter.status == status)
    if company:
        count_stmt = count_stmt.where(WarningLetter.company_name.ilike(f"%{company}%"))
    if date_from:
        count_stmt = count_stmt.where(WarningLetter.posted_date >= date_from)
    if date_to:
        count_stmt = count_stmt.where(WarningLetter.posted_date <= date_to)
    total = (await db.execute(count_stmt)).scalar() or 0

    # 分页
    stmt = stmt.order_by(WarningLetter.posted_date.desc())\
               .offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(stmt)
    letters = result.scalars().all()

    items = []
    for letter in letters:
        analysis = letter.ai_analysis
        items.append({
            "id": letter.id,
            "fda_id": letter.fda_id,
            "company_name": letter.company_name,
            "subject": letter.subject,
            "issuing_office": letter.issuing_office,
            "issue_date": str(letter.issue_date) if letter.issue_date else None,
            "posted_date": str(letter.posted_date) if letter.posted_date else None,
            "status": letter.status,
            "fei_number": letter.fei_number,
            "country": letter.country,
            "translation_zh": analysis.translation_zh if analysis else None,
            "summary_zh": analysis.summary_zh if analysis else None,
            "violation_type": analysis.violation_type if analysis else None,
            "risk_level": analysis.risk_level if analysis else None,
        })

    return {
        "items": items,
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
            selectinload(WarningLetter.cfr_citations),
            selectinload(WarningLetter.ai_analysis),
        )
        .where(WarningLetter.id == letter_id)
    )
    result = await db.execute(stmt)
    letter = result.scalars().first()

    if not letter:
        raise HTTPException(status_code=404, detail="Letter not found")

    analysis = letter.ai_analysis
    analysis_out = None
    if analysis:
        analysis_out = {
            "summary_en": analysis.summary_en,
            "summary_zh": analysis.summary_zh,
            "translation_zh": analysis.translation_zh,
            "violation_type": analysis.violation_type,
            "risk_level": analysis.risk_level,
            "key_findings": analysis.key_findings,
            "model_used": getattr(analysis, 'model_used', None),
        }

    violations_out = []
    for v in (letter.violations or []):
        violations_out.append({
            "id": v.id,
            "violation_type": v.violation_type,
            "description": v.description,
            "cfr_reference": v.cfr_reference,
            "severity": v.severity,
        })

    cfr_out = []
    for c in (letter.cfr_citations or []):
        cfr_out.append({
            "id": c.id,
            "cfr_section": c.cfr_section,
            "title": c.title,
            "description": c.description,
        })

    return {
        "id": letter.id,
        "fda_id": letter.fda_id,
        "company_name": letter.company_name,
        "subject": letter.subject,
        "issuing_office": letter.issuing_office,
        "issue_date": str(letter.issue_date) if letter.issue_date else None,
        "posted_date": str(letter.posted_date) if letter.posted_date else None,
        "fei_number": letter.fei_number,
        "country": letter.country,
        "full_text": letter.full_text,
        "full_text_clean": letter.full_text_clean,
        "url": letter.url,
        "status": letter.status,
        "region": letter.region,
        "analysis": analysis_out,
        "violations": violations_out,
        "cfr_citations": cfr_out,
    }


@router.get("/company/{company_name:path}")
async def get_company_letters(company_name: str, db: AsyncSession = Depends(get_db)):
    """获取某公司的所有警告信"""
    stmt = (
        select(WarningLetter)
        .options(selectinload(WarningLetter.ai_analysis))
        .where(WarningLetter.company_name.ilike(f"%{company_name}%"))
        .order_by(WarningLetter.posted_date.desc())
    )
    result = await db.execute(stmt)
    letters = result.scalars().all()

    items = []
    for letter in letters:
        analysis = letter.ai_analysis
        items.append({
            "id": letter.id,
            "fda_id": letter.fda_id,
            "company_name": letter.company_name,
            "subject": letter.subject,
            "issuing_office": letter.issuing_office,
            "issue_date": str(letter.issue_date) if letter.issue_date else None,
            "status": letter.status,
            "translation_zh": analysis.translation_zh if analysis else None,
            "summary_zh": analysis.summary_zh if analysis else None,
        })

    return {"items": items, "total": len(items)}


@router.get("/stats/offices")
async def get_office_stats(db: AsyncSession = Depends(get_db)):
    """各签发办公室统计"""
    stmt = (
        select(WarningLetter.issuing_office, func.count(WarningLetter.id))
        .group_by(WarningLetter.issuing_office)
        .order_by(func.count(WarningLetter.id).desc())
    )
    result = await db.execute(stmt)
    return [{"office": row[0], "count": row[1]} for row in result.all()]


@router.get("/stats/timeline")
async def get_timeline_stats(db: AsyncSession = Depends(get_db)):
    """按月统计时间线"""
    stmt = (
        select(
            func.strftime("%Y-%m", WarningLetter.posted_date).label("month"),
            func.count(WarningLetter.id)
        )
        .group_by("month")
        .order_by("month")
    )
    result = await db.execute(stmt)
    return [{"month": row[0], "count": row[1]} for row in result.all() if row[0]]
