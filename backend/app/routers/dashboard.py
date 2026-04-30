"""FDA 警告信系统 — 数据看板统计接口
提供总量、状态、月度分布等聚合数据。"""

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import WarningLetter

router = APIRouter()


@router.get("/summary")
async def get_summary(db: AsyncSession = Depends(get_db)):
    """总量概览：总数、活跃数、关闭数、年份跨度"""
    total_q = select(func.count(WarningLetter.id))
    total = (await db.execute(total_q)).scalar() or 0

    active_q = select(func.count(WarningLetter.id)).where(
        WarningLetter.status == "active"
    )
    active = (await db.execute(active_q)).scalar() or 0

    closed = total - active

    min_q = select(func.min(WarningLetter.posted_date))
    max_q = select(func.max(WarningLetter.posted_date))
    min_date = (await db.execute(min_q)).scalar()
    max_date = (await db.execute(max_q)).scalar()

    # 办公室数量
    dept_q = (
        select(WarningLetter.issuing_office)
        .where(WarningLetter.issuing_office.isnot(None))
        .distinct()
    )
    depts = (await db.execute(dept_q)).scalars().all()

    return {
        "total": total,
        "active": active,
        "closed": closed,
        "min_year": str(min_date)[:4] if min_date else None,
        "max_year": str(max_date)[:4] if max_date else None,
        "office_count": len(depts),
    }


@router.get("/monthly")
async def get_monthly(year: int = None, db: AsyncSession = Depends(get_db)):
    """月发量统计（某年或全部年份的月度聚合）"""
    # 按年-月分组
    stmt = select(
        func.strftime("%Y", WarningLetter.posted_date).label("year"),
        func.strftime("%m", WarningLetter.posted_date).label("month"),
        func.count(WarningLetter.id).label("count"),
    ).where(WarningLetter.posted_date.isnot(None))

    if year:
        stmt = stmt.where(func.strftime("%Y", WarningLetter.posted_date) == str(year))

    stmt = stmt.group_by("year", "month").order_by("year", "month")
    result = await db.execute(stmt)
    rows = result.all()

    return [
        {"year": r[0], "month": r[1], "count": r[2]}
        for r in rows
        if r[0] and r[1]
    ]


@router.get("/status")
async def get_status_breakdown(db: AsyncSession = Depends(get_db)):
    """状态分布统计"""
    stmt = (
        select(
            WarningLetter.status,
            func.count(WarningLetter.id).label("count"),
        )
        .where(WarningLetter.status.isnot(None))
        .group_by(WarningLetter.status)
        .order_by(func.count(WarningLetter.id).desc())
    )
    result = await db.execute(stmt)
    return [{"status": row[0], "count": row[1]} for row in result]


@router.get("/top-companies")
async def get_top_companies(limit: int = 10, db: AsyncSession = Depends(get_db)):
    """警告信最多的企业 Top N"""
    stmt = (
        select(
            WarningLetter.company_name,
            func.count(WarningLetter.id).label("count"),
        )
        .where(WarningLetter.company_name.isnot(None))
        .group_by(WarningLetter.company_name)
        .order_by(func.count(WarningLetter.id).desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    return [{"company": row[0], "count": row[1]} for row in result]
