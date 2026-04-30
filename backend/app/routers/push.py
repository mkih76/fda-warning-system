"""
FDA 警告信 Telegram 推送订阅接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from ..database import get_db
from ..models import PushSubscription

router = APIRouter()


class SubscribeRequest(BaseModel):
    chat_id: str
    filters: dict = None


@router.post("/subscribe")
async def subscribe(req: SubscribeRequest, db: AsyncSession = Depends(get_db)):
    """Telegram 推送订阅"""
    stmt = select(PushSubscription).where(PushSubscription.chat_id == req.chat_id)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()
    if existing:
        existing.active = True
        if req.filters:
            existing.filters = req.filters
        return {"message": "订阅已更新", "chat_id": req.chat_id}

    sub = PushSubscription(chat_id=req.chat_id, filters=req.filters)
    db.add(sub)
    await db.flush()
    return {"message": "订阅成功", "id": sub.id, "chat_id": req.chat_id}


@router.delete("/subscribe/{chat_id}")
async def unsubscribe(chat_id: str, db: AsyncSession = Depends(get_db)):
    """取消推送订阅"""
    stmt = select(PushSubscription).where(PushSubscription.chat_id == chat_id)
    result = await db.execute(stmt)
    sub = result.scalar_one_or_none()
    if not sub:
        raise HTTPException(404, detail="未找到订阅")
    sub.active = False
    return {"message": "已取消订阅", "chat_id": chat_id}


@router.get("/subscribe/{chat_id}")
async def get_subscription(chat_id: str, db: AsyncSession = Depends(get_db)):
    """查询订阅状态"""
    stmt = select(PushSubscription).where(PushSubscription.chat_id == chat_id)
    result = await db.execute(stmt)
    sub = result.scalar_one_or_none()
    if not sub:
        return {"subscribed": False}
    return {
        "subscribed": sub.active,
        "chat_id": sub.chat_id,
        "filters": sub.filters,
        "created_at": str(sub.created_at),
    }
