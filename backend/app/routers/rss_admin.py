"""
RSS管理API
用于RSS源管理、手动同步、状态监控
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from ..crawler.rss_config import get_enabled_sources, get_source_count, RSS_SOURCES
from ..crawler.rss_sync import run_rss_sync
from ..crawler.scheduler import scheduler

router = APIRouter(prefix="/rss", tags=["rss"])


# ==================== 数据模型 ====================

class RSSSource(BaseModel):
    name: str
    url: str
    type: str
    lang: str
    enabled: bool
    priority: int
    sector: str

class SyncRequest(BaseModel):
    sector: Optional[str] = None  # pharma/cosmetics/food，None表示全部

class SyncResponse(BaseModel):
    success: bool
    message: str
    task_id: Optional[str] = None

class SchedulerStatus(BaseModel):
    running: bool
    tasks: dict

class SourceStats(BaseModel):
    pharma: dict
    cosmetics: dict
    food: dict


# ==================== API端点 ====================

@router.get("/sources", response_model=List[RSSSource])
async def list_sources(sector: Optional[str] = None):
    """获取所有RSS数据源"""
    sources = get_enabled_sources(sector)

    return [
        RSSSource(
            name=s['name'],
            url=s['url'],
            type=s['type'],
            lang=s['lang'],
            enabled=s['enabled'],
            priority=s['priority'],
            sector=s['sector'],
        )
        for s in sources
    ]


@router.get("/sources/stats", response_model=SourceStats)
async def get_sources_stats():
    """获取数据源统计"""
    stats = get_source_count()
    return SourceStats(**stats)


@router.post("/sync", response_model=SyncResponse)
async def trigger_sync(
    request: SyncRequest,
    background_tasks: BackgroundTasks,
):
    """手动触发RSS同步"""
    valid_sectors = ['pharma', 'cosmetics', 'food', None]
    if request.sector and request.sector not in valid_sectors:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sector. Must be one of: {valid_sectors}"
        )

    # 在后台执行同步任务
    background_tasks.add_task(run_rss_sync, request.sector)

    sector_text = request.seector or "所有行业"
    return SyncResponse(
        success=True,
        message=f"RSS同步任务已启动: {sector_text}",
        task_id=f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
    )


@router.get("/sync/status")
async def get_sync_status():
    """获取同步任务状态"""
    return scheduler.get_status()


@router.get("/scheduler/status", response_model=SchedulerStatus)
async def get_scheduler_status():
    """获取调度器状态"""
    status = scheduler.get_status()
    return SchedulerStatus(**status)


@router.post("/scheduler/start")
async def start_scheduler():
    """启动调度器（仅在主进程）"""
    if scheduler.running:
        return {"message": "调度器已在运行"}

    # 注意：这个需要在主进程中启动
    # 通常通过独立进程运行scheduler.py
    return {
        "message": "请通过独立进程启动调度器",
        "command": "python -m app.crawler.scheduler",
    }


@router.post("/scheduler/stop")
async def stop_scheduler():
    """停止调度器"""
    if not scheduler.running:
        return {"message": "调度器未在运行"}

    scheduler.stop()
    return {"message": "调度器已停止"}


@router.get("/health")
async def rss_health_check():
    """RSS系统健康检查"""
    stats = get_source_count()

    total_enabled = sum(s['enabled'] for s in stats.values())
    total_sources = sum(s['total'] for s in stats.values())

    return {
        "status": "healthy" if total_enabled > 0 else "warning",
        "enabled_sources": total_enabled,
        "total_sources": total_sources,
        "scheduler_running": scheduler.running,
        "timestamp": datetime.now().isoformat(),
    }
