"""
FDA 警告信 LLM 分析接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import WarningLetter, AiAnalysis, CfrCitation

router = APIRouter()


@router.post("/{letter_id}/analyze")
async def trigger_analysis(letter_id: int, db: AsyncSession = Depends(get_db)):
    """触发 LLM 分析（占位，实际由爬虫触发）"""
    stmt = select(WarningLetter).where(WarningLetter.id == letter_id)
    result = await db.execute(stmt)
    letter = result.scalar_one_or_none()
    if not letter:
        raise HTTPException(404, detail="警告信不存在")
    return {"message": "分析任务已排队", "letter_id": letter_id}


@router.get("/{letter_id}")
async def get_analysis(letter_id: int, db: AsyncSession = Depends(get_db)):
    """获取单封信的 AI 分析结果"""
    stmt = select(AiAnalysis).where(AiAnalysis.warning_letter_id == letter_id)
    result = await db.execute(stmt)
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(404, detail="该信尚未分析")
    return {
        "summary_en": analysis.summary_en,
        "summary_zh": analysis.summary_zh,
        "key_findings": analysis.key_findings,
        "compliance_gap": analysis.compliance_gap,
        "model_used": analysis.model_used,
        "analyzed_at": str(analysis.analyzed_at) if analysis.analyzed_at else None,
    }


@router.get("/cfr/stats")
async def get_cfr_stats(
    year: int = None,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """CFR 条款引用热度统计"""
    stmt = (
        select(CfrCitation.cfr_section, func.count(CfrCitation.id).label("count"))
        .group_by(CfrCitation.cfr_section)
        .order_by(func.count(CfrCitation.id).desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    return [{"cfr_section": row[0], "count": row[1]} for row in result]
