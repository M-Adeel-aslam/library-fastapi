from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database import get_db
import schema, models
from auth import verify_current_user

router = APIRouter(
    prefix="/support",
    tags=['Support']
)

@router.post("/works/{id}/support", response_model=schema.SupportOut)
async def support_a_work(id:int,support_data: schema.SupportIn,current_user: dict = Depends(verify_current_user),db: Session = Depends(get_db)):
    work = db.query(models.Work).filter(models.Work.id == id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")
    new_support = models.Support(
        work_id=id,
        supporter_id=current_user['id'],
        amount=support_data.amount
    )
    db.add(new_support)
    db.commit()
    db.refresh(new_support)
    return new_support

@router.get("/works/{id}/support", response_model=List[schema.SupportOut])
async def list_supports(id: int, db: Session = Depends(get_db)):
    supports = db.query(models.Support).filter(models.Support.work_id == id).all()
    return supports

@router.get("/users/{id}/support", response_model=List[schema.SupportOut])
async def user_support_history(id: int, current_user: dict = Depends(verify_current_user), db: Session = Depends(get_db)):
    if current_user["id"] != id:
        raise HTTPException(status_code=403, detail="Not authorized to view other user's support history")

    support_history = db.query(models.Support).filter(models.Support.supporter_id == id).all()
    return support_history