"""
FDA Warning Letter System - FastAPI Backend
"""
from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_, func, text as sql_text
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from pathlib import Path
from functools import lru_cache
import re
import csv
import io
import json

from .database import get_db
from . import models
from . import models_new  # noqa: F401 — import to register new table models
from .routers.auth import router as auth_router
from .routers.content import router as content_router
from .routers.user_api import router as user_router

app = FastAPI(
    title="FDA Warning Letter API",
    version="2.0.0",
    description="FDA 警告信智能监控系统 API - 增强版",
)


# ─── Startup: create new tables if they don't exist ────────────
@app.on_event("startup")
def startup_create_tables():
    """Create any new tables (users, categories, articles, etc.) without touching existing ones."""
    from .models import Base, engine
    Base.metadata.create_all(bind=engine)

# CORS — 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Mount new routers ───────────────────────────────────────
app.include_router(auth_router)
app.include_router(content_router)
app.include_router(user_router)

# 简单内存缓存（生产环境建议使用 Redis）
cache = {}
CACHE_TTL = 300  # 5分钟缓存

def get_cached(key: str):
    if key in cache:
        data, timestamp = cache[key]
        if (datetime.now() - timestamp).seconds < CACHE_TTL:
            return data
        del cache[key]
    return None

def set_cached(key: str, data):
    cache[key] = (data, datetime.now())


# ─── Pydantic Schemas ────────────────────────────────────────────

class LetterBase(BaseModel):
    id: int
    fda_id: str
    company_name: str
    subject: str
    issuing_office: Optional[str] = None
    issue_date: Optional[date] = None
    country: Optional[str] = None
    region: Optional[str] = None
    status: Optional[str] = None
    url: Optional[str] = None

    class Config:
        from_attributes = True


class AIAnalysisOut(BaseModel):
    translation_zh: Optional[str] = None
    summary_zh: Optional[str] = None
    summary_en: Optional[str] = None
    violation_type: Optional[str] = None
    risk_level: Optional[str] = None
    key_findings: Optional[list] = None
    model_used: Optional[str] = None


class LetterDetail(BaseModel):
    id: int
    fda_id: str
    company_name: str
    subject: str
    issuing_office: Optional[str] = None
    posted_date: Optional[str] = None
    issue_date: Optional[str] = None
    fei_number: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    status: Optional[str] = None
    url: Optional[str] = None
    full_text: Optional[str] = None
    full_text_clean: Optional[str] = None
    closeout_date: Optional[str] = None
    response_date: Optional[str] = None
    ai_summary: Optional[str] = None
    violation_type: Optional[str] = None
    violations: Optional[list] = None
    citations: Optional[list] = None
    analysis: Optional[dict] = None

    class Config:
        from_attributes = True


class StatsOut(BaseModel):
    total: int
    with_url: int
    with_fulltext: int
    with_ai: int
    by_office: dict
    by_year: dict
    by_status: dict


# ─── API Routes ──────────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "fda-warning-api"}


class PaginatedLetters(BaseModel):
    items: list[LetterBase]
    total: int
    page: int
    page_size: int


@app.get("/api/letters", response_model=PaginatedLetters)
def list_letters(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    office: Optional[str] = None,
    country: Optional[str] = None,
    year: Optional[int] = None,
    status: Optional[str] = None,
    violation_type: Optional[str] = None,
    risk_level: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(models.WarningLetter)

    if search:
        q = q.filter(
            or_(
                models.WarningLetter.company_name.ilike(f"%{search}%"),
                models.WarningLetter.subject.ilike(f"%{search}%"),
            )
        )
    if office:
        q = q.filter(models.WarningLetter.issuing_office == office)
    if country:
        q = q.filter(models.WarningLetter.country == country)
    if year:
        q = q.filter(func.substr(models.WarningLetter.issue_date, 1, 4) == str(year))
    if status:
        q = q.filter(models.WarningLetter.status == status)
    
    # 高级筛选：违规类型（通过JOIN ai_analysis表）
    if violation_type:
        q = q.join(models.AIAnalysis, models.WarningLetter.id == models.AIAnalysis.letter_id)
        q = q.filter(models.AIAnalysis.violation_type == violation_type)
    
    # 高级筛选：风险等级（通过JOIN ai_analysis表）
    if risk_level:
        if not violation_type:  # 如果还没JOIN
            q = q.join(models.AIAnalysis, models.WarningLetter.id == models.AIAnalysis.letter_id)
        q = q.filter(models.AIAnalysis.risk_level == risk_level)
    
    # 高级筛选：日期范围
    if date_from:
        q = q.filter(models.WarningLetter.issue_date >= date_from)
    if date_to:
        q = q.filter(models.WarningLetter.issue_date <= date_to)

    total = q.count()
    letters = (
        q.order_by(desc(models.WarningLetter.issue_date))
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return PaginatedLetters(items=letters, total=total, page=page, page_size=page_size)


@app.get("/api/letters/{letter_id}")
def get_letter(letter_id: int, db: Session = Depends(get_db)):
    """获取单封警告信详情（含违规、CFR引用、AI分析），支持从全文自动解析"""
    letter = db.query(models.WarningLetter).filter(
        models.WarningLetter.id == letter_id
    ).first()
    if not letter:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Letter not found")

    # 1. AI 分析
    ai = db.query(models.AIAnalysis).filter(
        models.AIAnalysis.letter_id == letter_id
    ).first()
    analysis_out = None
    if ai:
        analysis_out = {
            "summary_zh": ai.summary_zh,
            "summary_en": getattr(ai, 'summary_en', None),
            "translation_zh": getattr(ai, 'translation_zh', None),
            "violation_type": ai.violation_type,
            "risk_level": getattr(ai, 'risk_level', None),
            "key_findings": getattr(ai, 'key_findings', None),
            "model_used": getattr(ai, 'model_used', None),
        }

    # 2. 违规分类（优先用数据库，没有则从全文解析）
    violations = []
    viol_rows = db.execute(
        sql_text("SELECT * FROM violations WHERE warning_letter_id = :lid")
        .bindparams(lid=letter_id)
    ).fetchall()
    if viol_rows:
        for v in viol_rows:
            violations.append({
                "system_category": v._mapping.get('system_category'),
                "violation_type": v._mapping.get('violation_type'),
                "severity": v._mapping.get('severity', 'major'),
                "description": v._mapping.get('description'),
                "description_zh": v._mapping.get('description_zh'),
            })

    # 3. CFR 引用（优先用数据库，没有则从全文解析）
    citations = []
    cfr_rows = db.execute(
        sql_text("SELECT * FROM cfr_citations WHERE warning_letter_id = :lid")
        .bindparams(lid=letter_id)
    ).fetchall()
    if cfr_rows:
        for c in cfr_rows:
            citations.append({
                "cfr_part": c._mapping.get('cfr_part'),
                "cfr_section": c._mapping.get('cfr_section'),
                "cfr_text": c._mapping.get('description'),
            })

    # 4. 如果 DB 没有，自动从 full_text 解析
    if not violations or not citations:
        text = letter.full_text or ""
        # 解析 CFR 条款: 21 CFR Part.Section
        if not citations:
            cfr_pattern = re.compile(r'21\s+C\.?F\.?R\.?\s+(?:Part\s+)?(\d+)[.\s](\d+)', re.IGNORECASE)
            found_cfrs = set()
            for m in cfr_pattern.finditer(text):
                part, section = m.group(1), m.group(2)
                cfr_key = f"{part}.{section}"
                if cfr_key not in found_cfrs:
                    found_cfrs.add(cfr_key)
                    citations.append({
                        "cfr_part": part,
                        "cfr_section": cfr_key,
                        "cfr_text": None,
                    })
            # 也匹配 "21 CFR § 820" 这种格式
            cfr_pattern2 = re.compile(r'21\s+CFR\s+[§\s]+(\d+\.?\d*[a-z]?)', re.IGNORECASE)
            for m in cfr_pattern2.finditer(text):
                cfr_key = m.group(1).rstrip('.')
                if cfr_key not in found_cfrs:
                    found_cfrs.add(cfr_key)
                    citations.append({
                        "cfr_part": cfr_key.split('.')[0] if '.' in cfr_key else cfr_key,
                        "cfr_section": cfr_key,
                        "cfr_text": None,
                    })

        # 从 subject 和全文推断违规类型
        if not violations:
            subject = (letter.subject or "").upper()
            text_upper = text.upper()
            detected_violations = []

            # CGMP六大系统关键词
            cGMP_systems = {
                "Quality System": ["QUALITY SYSTEM", "QUALITY UNIT", "QA", "QUALITY CONTROL", "QUALITY MANAGEMENT"],
                "Production System": ["PRODUCTION", "MANUFACTURING PROCESS", "PROCESS CONTROL", "PRODUCTION RECORD"],
                "Facility and Equipment": ["FACILITY", "EQUIPMENT", "MAINTENANCE", "SANITATION", "CLEANING"],
                "Materials System": ["MATERIAL", "COMPONENT", "RAW MATERIAL", "INCOMING", "WAREHOUSE", "STORAGE"],
                "Personnel": ["PERSONNEL", "TRAINING", "HYGIENE", "EMPLOYEE"],
                "Production and Process Controls": ["PROCESS VALIDATION", "PROCESS CONTROL", "PRODUCTION AND PROCESS CONTROL"],
            }
            for system, keywords in cGMP_systems.items():
                for kw in keywords:
                    if kw in text_upper:
                        detected_violations.append({
                            "system_category": system,
                            "violation_type": "CGMP Violation",
                            "severity": "major",
                            "description": f"发现涉及 {system} 的违规内容（关键词: {kw}）",
                            "description_zh": None,
                        })
                        break

            # 标签/假药/劣药
            if any(k in subject for k in ["MISBRANDED", "UNAPPROVED", "ADULTERATED"]):
                detected_violations.append({
                    "system_category": "Labeling & Marketing",
                    "violation_type": "Misbranded/Unapproved",
                    "severity": "critical",
                    "description": subject,
                    "description_zh": None,
                })
            violations.extend(detected_violations[:5])

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
        "region": letter.region,
        "status": letter.status,
        "url": letter.url,
        "full_text": letter.full_text,
        "full_text_clean": getattr(letter, 'full_text_clean', None),
        "closeout_date": str(letter.closeout_date) if letter.closeout_date else None,
        "response_date": str(letter.response_date) if letter.response_date else None,
        "ai_summary": analysis_out["summary_zh"] if analysis_out else None,
        "violation_type": analysis_out["violation_type"] if analysis_out else None,
        "violations": violations,
        "citations": citations,
        "analysis": analysis_out,
    }


@app.get("/api/letters/{letter_id}/ai", response_model=AIAnalysisOut)
def get_letter_ai(letter_id: int, db: Session = Depends(get_db)):
    ai = db.query(models.AIAnalysis).filter(
        models.AIAnalysis.letter_id == letter_id
    ).first()
    if not ai:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="AI analysis not found")
    return AIAnalysisOut.model_validate(ai)


@app.get("/api/stats", response_model=StatsOut)
def get_stats(db: Session = Depends(get_db)):
    total = db.query(func.count(models.WarningLetter.id)).scalar()
    with_url = db.query(func.count(models.WarningLetter.id)).filter(
        models.WarningLetter.url.isnot(None),
        models.WarningLetter.url != "",
    ).scalar()
    with_fulltext = db.query(func.count(models.WarningLetter.id)).filter(
        models.WarningLetter.full_text.isnot(None),
        models.WarningLetter.full_text != "",
    ).scalar()
    with_ai = db.query(func.count(models.AIAnalysis.id)).scalar()

    # 按办公室统计
    office_rows = db.query(
        models.WarningLetter.issuing_office,
        func.count(models.WarningLetter.id)
    ).group_by(models.WarningLetter.issuing_office).all()
    by_office = {str(k) or "未知": v for k, v in office_rows}

    # 按年份统计
    year_rows = db.query(
        func.substr(models.WarningLetter.issue_date, 1, 4).label("year"),
        func.count(models.WarningLetter.id)
    ).filter(
        models.WarningLetter.issue_date.isnot(None)
    ).group_by("year").all()
    by_year = {str(k) or "未知": v for k, v in year_rows}

    # 按状态统计
    status_rows = db.query(
        models.WarningLetter.status,
        func.count(models.WarningLetter.id)
    ).group_by(models.WarningLetter.status).all()
    by_status = {str(k) or "未知": v for k, v in status_rows}

    return StatsOut(
        total=total or 0,
        with_url=with_url or 0,
        with_fulltext=with_fulltext or 0,
        with_ai=with_ai or 0,
        by_office=by_office,
        by_year=by_year,
        by_status=by_status,
    )


@app.get("/api/offices", response_model=list[str])
def list_offices(db: Session = Depends(get_db)):
    rows = db.query(models.WarningLetter.issuing_office).filter(
        models.WarningLetter.issuing_office.isnot(None),
        models.WarningLetter.issuing_office != "",
    ).distinct().all()
    return sorted(set(r[0] for r in rows if r[0]))


@app.get("/api/violation-types")
def list_violation_types(db: Session = Depends(get_db)):
    """获取所有违规类型（用于筛选下拉框）"""
    rows = db.query(models.AIAnalysis.violation_type).filter(
        models.AIAnalysis.violation_type.isnot(None),
        models.AIAnalysis.violation_type != "",
    ).distinct().all()
    return sorted(set(r[0] for r in rows if r[0]))


# ─── Dashboard APIs ────────────────────────────────────────────────

@app.get("/api/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    total = db.query(func.count(models.WarningLetter.id)).scalar() or 0
    active = db.query(func.count(models.WarningLetter.id)).filter(
        models.WarningLetter.status == "active"
    ).scalar() or 0
    closed = db.query(func.count(models.WarningLetter.id)).filter(
        models.WarningLetter.status == "closed"
    ).scalar() or 0
    rows = db.query(
        func.min(models.WarningLetter.issue_date),
        func.max(models.WarningLetter.issue_date),
    ).filter(models.WarningLetter.issue_date.isnot(None)).first()
    year_min = str(rows[0])[:4] if rows[0] else ""
    year_max = str(rows[1])[:4] if rows[1] else ""
    office_count = db.query(func.count(func.distinct(
        models.WarningLetter.issuing_office
    ))).filter(models.WarningLetter.issuing_office.isnot(None)).scalar() or 0
    return {"total": total, "active": active, "closed": closed,
            "min_year": year_min, "max_year": year_max, "office_count": office_count}


@app.get("/api/letters/stats/timeline")
def letters_timeline(db: Session = Depends(get_db)):
    rows = db.query(
        func.substr(models.WarningLetter.issue_date, 1, 7).label("month"),
        func.count(models.WarningLetter.id)
    ).filter(
        models.WarningLetter.issue_date.isnot(None)
    ).group_by("month").order_by("month").all()
    return [{"date": r[0], "count": r[1]} for r in rows]


@app.get("/api/dashboard/monthly")
def dashboard_monthly(db: Session = Depends(get_db)):
    rows = db.query(
        func.substr(models.WarningLetter.issue_date, 1, 7).label("month"),
        func.count(models.WarningLetter.id)
    ).filter(
        models.WarningLetter.issue_date.isnot(None)
    ).group_by("month").order_by(desc("month")).limit(12).all()
    return [{"month": r[0], "count": r[1]} for r in reversed(rows)]


@app.get("/api/dashboard/top-companies")
def dashboard_top_companies(db: Session = Depends(get_db)):
    rows = db.query(
        models.WarningLetter.company_name,
        func.count(models.WarningLetter.id).label("cnt")
    ).group_by(
        models.WarningLetter.company_name
    ).order_by(desc("cnt")).limit(10).all()
    return [{"company": r[0], "count": r[1]} for r in rows]


# ─── Articles API ──────────────────────────────────────────────────

import json as json_mod

@app.get("/api/articles")
def list_articles(category: Optional[str] = None):
    """获取深度内容文章列表（分析、指南、案例）"""
    index_path = Path("/root/fda-warning-system/data/articles_index.json")
    if not index_path.exists():
        return {"items": [], "total": 0}
    
    with open(index_path, "r", encoding="utf-8") as f:
        articles = json_mod.load(f)
    
    if category:
        articles = [a for a in articles if a.get("category") == category]
    
    # 去重（同一篇文章可能有重复）
    seen = set()
    unique = []
    for a in articles:
        key = a.get("title", "")
        if key not in seen:
            seen.add(key)
            unique.append(a)
    
    return {"items": unique, "total": len(unique)}


@app.get("/api/articles/{article_id}")
def get_article(article_id: str):
    """获取单篇文章内容"""
    content_dir = Path("/root/fda-warning-system/content")
    for root, dirs, files in content_dir.walk():
        for f in files:
            if f.replace(".md", "") == article_id:
                filepath = Path(root) / f
                with open(filepath, "r", encoding="utf-8") as fp:
                    content = fp.read()
                return {"id": article_id, "content": content}
    
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Article not found")


# ─── Export API ──────────────────────────────────────────────────

@app.get("/api/letters/export/csv")
def export_letters_csv(
    search: Optional[str] = None,
    office: Optional[str] = None,
    country: Optional[str] = None,
    year: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """导出警告信为 CSV 格式"""
    q = db.query(models.WarningLetter)

    if search:
        q = q.filter(
            or_(
                models.WarningLetter.company_name.ilike(f"%{search}%"),
                models.WarningLetter.subject.ilike(f"%{search}%"),
            )
        )
    if office:
        q = q.filter(models.WarningLetter.issuing_office == office)
    if country:
        q = q.filter(models.WarningLetter.country == country)
    if year:
        q = q.filter(func.substr(models.WarningLetter.issue_date, 1, 4) == str(year))
    if status:
        q = q.filter(models.WarningLetter.status == status)

    letters = q.order_by(desc(models.WarningLetter.issue_date)).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'ID', 'FDA ID', '公司名称', '主题', '签发办公室',
        '发布日期', '国家', '状态', 'URL'
    ])

    for letter in letters:
        writer.writerow([
            letter.id,
            letter.fda_id,
            letter.company_name,
            letter.subject,
            letter.issuing_office or '',
            str(letter.issue_date) if letter.issue_date else '',
            letter.country or '',
            letter.status or '',
            letter.url or '',
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=fda_letters_{datetime.now().strftime('%Y%m%d')}.csv"}
    )


# ─── Search Suggestions API ──────────────────────────────────────

@app.get("/api/search/suggestions")
def get_search_suggestions(
    q: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
):
    """获取搜索建议（自动完成）"""
    cache_key = f"suggestions:{q}"
    cached = get_cached(cache_key)
    if cached:
        return cached

    # 搜索公司名称
    companies = db.query(models.WarningLetter.company_name).filter(
        models.WarningLetter.company_name.ilike(f"%{q}%")
    ).distinct().limit(5).all()

    # 搜索主题
    subjects = db.query(models.WarningLetter.subject).filter(
        models.WarningLetter.subject.ilike(f"%{q}%")
    ).distinct().limit(5).all()

    result = {
        "companies": [c[0] for c in companies],
        "subjects": [s[0] for s in subjects],
    }

    set_cached(cache_key, result)
    return result


# ─── Optimized Stats with Cache ─────────────────────────────────

@app.get("/api/stats/optimized")
def get_optimized_stats(db: Session = Depends(get_db)):
    """带缓存的统计信息"""
    cache_key = "stats:optimized"
    cached = get_cached(cache_key)
    if cached:
        return cached

    # 复用原有逻辑
    stats = get_stats(db)

    # 添加额外统计
    # 最近30天新增
    from datetime import timedelta
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    recent_count = db.query(func.count(models.WarningLetter.id)).filter(
        models.WarningLetter.issue_date >= thirty_days_ago
    ).scalar() or 0

    # 高风险企业数量
    high_risk_count = db.query(func.count(models.WarningLetter.id)).filter(
        models.WarningLetter.country.in_(['China', 'India'])
    ).scalar() or 0

    result = {
        **stats.dict(),
        "recent_30_days": recent_count,
        "high_risk_countries": high_risk_count,
        "cache_time": datetime.now().isoformat(),
    }

    set_cached(cache_key, result)
    return result


# ─── Serve Frontend Static Files ──────────────────────────────────

frontend_dist = Path("/root/fda-warning-system/frontend/dist")
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")

# SPA fallback: non-API routes → index.html
@app.middleware("http")
async def spa_fallback(request, call_next):
    response = await call_next(request)
    if response.status_code == 404 and not request.url.path.startswith("/api"):
        # Re-serve index.html for SPA routes
        index_path = frontend_dist / "index.html"
        if index_path.exists():
            from fastapi.responses import FileResponse
            return FileResponse(str(index_path))
    return response
