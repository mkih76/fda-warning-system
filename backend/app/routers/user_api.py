"""
PharmaCos Insight - User Features API
Favorites, reading history, membership info.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from ..database import get_db
from ..models_new import User, UserFavorite, ReadHistory, Membership, Article
from .auth import require_user

router = APIRouter(prefix="/api/user", tags=["user"])


# ─── Schemas ───────────────────────────────────────────────────
class FavoriteRequest(BaseModel):
    item_type: str  # letter / article
    item_id: int


class FavoriteResponse(BaseModel):
    id: int
    item_type: str
    item_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MembershipResponse(BaseModel):
    plan: str
    started_at: Optional[datetime]
    expires_at: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True


class ReadHistoryItem(BaseModel):
    article_id: int
    article_title: Optional[str] = None
    article_slug: Optional[str] = None
    read_at: datetime

    class Config:
        from_attributes = True


# ─── Favorites ─────────────────────────────────────────────────
@router.get("/favorites", response_model=List[FavoriteResponse])
def list_favorites(
    item_type: Optional[str] = None,
    user: User = Depends(require_user),
    db: Session = Depends(get_db)
):
    """Get user's favorites."""
    q = db.query(UserFavorite).filter(UserFavorite.user_id == user.id)
    if item_type:
        q = q.filter(UserFavorite.item_type == item_type)
    return q.order_by(UserFavorite.created_at.desc()).all()


@router.post("/favorites")
def add_favorite(
    req: FavoriteRequest,
    user: User = Depends(require_user),
    db: Session = Depends(get_db)
):
    """Add an item to favorites."""
    existing = db.query(UserFavorite).filter(
        UserFavorite.user_id == user.id,
        UserFavorite.item_type == req.item_type,
        UserFavorite.item_id == req.item_id,
    ).first()

    if existing:
        return {"message": "已收藏", "id": existing.id}

    fav = UserFavorite(
        user_id=user.id,
        item_type=req.item_type,
        item_id=req.item_id,
    )
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return {"message": "收藏成功", "id": fav.id}


@router.delete("/favorites/{fav_id}")
def remove_favorite(
    fav_id: int,
    user: User = Depends(require_user),
    db: Session = Depends(get_db)
):
    """Remove a favorite by ID."""
    fav = db.query(UserFavorite).filter(
        UserFavorite.id == fav_id,
        UserFavorite.user_id == user.id,
    ).first()
    if not fav:
        raise HTTPException(status_code=404, detail="收藏不存在")
    db.delete(fav)
    db.commit()
    return {"message": "已取消收藏"}


# ─── Membership ────────────────────────────────────────────────
@router.get("/membership", response_model=Optional[MembershipResponse])
def get_membership(user: User = Depends(require_user), db: Session = Depends(get_db)):
    """Get current user's active membership."""
    membership = (
        db.query(Membership)
        .filter(Membership.user_id == user.id, Membership.is_active == 1)
        .order_by(Membership.expires_at.desc())
        .first()
    )
    if not membership:
        return MembershipResponse(
            plan=user.role,
            started_at=None,
            expires_at=None,
            is_active=True,
        )
    return membership


# ─── Reading History ───────────────────────────────────────────
@router.post("/history")
def add_read_history(
    article_id: int,
    user: User = Depends(require_user),
    db: Session = Depends(get_db)
):
    """Record that user read an article."""
    record = ReadHistory(
        user_id=user.id,
        article_id=article_id,
        read_at=datetime.utcnow(),
    )
    db.add(record)
    db.commit()
    return {"message": "ok"}


@router.get("/history", response_model=List[ReadHistoryItem])
def list_read_history(
    limit: int = 50,
    user: User = Depends(require_user),
    db: Session = Depends(get_db)
):
    """Get user's reading history."""
    records = (
        db.query(ReadHistory)
        .filter(ReadHistory.user_id == user.id)
        .order_by(ReadHistory.read_at.desc())
        .limit(limit)
        .all()
    )

    result = []
    for r in records:
        article = db.query(Article).filter(Article.id == r.article_id).first()
        result.append(ReadHistoryItem(
            article_id=r.article_id,
            article_title=article.title if article else None,
            article_slug=article.slug if article else None,
            read_at=r.read_at,
        ))
    return result
