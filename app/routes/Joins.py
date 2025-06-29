from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import schema, models
from auth import verify_current_user

router = APIRouter(
    prefix="/join",
    tags=['Join']
)

@router.get("/works/{id}/details", response_model=schema.WorkDetailsOut)
async def join(id: int, db: Session = Depends(get_db)):
    work = db.query(models.Work).filter(models.Work.id == id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")

    author = db.query(models.User).filter(models.User.id == work.artist_id).first()

    total_support = db.query(func.coalesce(func.sum(models.Support.amount), 0))\
        .filter(models.Support.work_id == id).scalar()

    return {
        "id": work.id,
        "title": work.title,
        "description": work.description,
        "content": work.content,
        "created_at": work.created_at,
        "updated_at": work.updated_at,
        "artist_username": author.username if author else None,
        "artist_email": author.email if author else None,
        "total_support": total_support
    }