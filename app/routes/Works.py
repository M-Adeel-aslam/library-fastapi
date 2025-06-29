
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from datetime import datetime
from auth import verify_current_user
import models, schema
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/works",
    tags=['Works']
)

@router.post("/", response_model=schema.WorksOut)
async def create(work:schema.WorksIn, db:Session=Depends(get_db),
                current_user: dict = Depends(verify_current_user)):
    existing = db.query(models.Work).filter(
        models.Work.artist_id == current_user["id"],
        models.Work.title == work.title).first()
    if existing:
        raise HTTPException(status_code=400, detail="Work with this title already exits")
    user = db.query(models.User).filter(models.User.email == current_user['email']).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_work = models.Work(
        title=work.title,
        description=work.description,
        content=work.content,
        artist_id=current_user["id"],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_work)
    db.commit()
    db.refresh(new_work)
    return new_work


@router.get("/", response_model=List[schema.WorksOut])
async def view_work(current_user: dict = Depends(verify_current_user),db: Session = Depends(get_db)):
    user_work = db.query(models.Work).filter(models.Work.artist_id == current_user["id"]).all()
    if not user_work:
         raise HTTPException(status_code=404, detail="No Work found")   
    return user_work


@router.get("/{work_id}", response_model=schema.WorksOut)
async def view_by_id(work_id:int,current_user:dict=Depends(verify_current_user),db: Session = Depends(get_db)):
    work = db.query(models.Work).filter(models.Work.id == work_id,models.Work.artist_id==current_user["id"]).first()
    if not work:
         raise HTTPException(status_code=404, detail="Work not found or not authorized to view this work.")
    return work

@router.put("/update_works/{work_id}", response_model=schema.updateWorkOut)
async def update_work(work_id: int, 
                      newWork: schema.updateWork, 
                      db: Session = Depends(get_db),
                      current_user: dict = Depends(verify_current_user)):

    work = db.query(models.Work).filter(
        models.Work.id == work_id,
        models.Work.artist_id == current_user["id"]
    ).first()

    if not work:
        raise HTTPException(status_code=404, detail="Work not found or not authorized")
    work.title = newWork.title
    work.description = newWork.description
    work.content = newWork.content
    work.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(work)
    return work
      
    
@router.delete("/works/{work_id}")
async def delete_work(work_id: int,
                      current_user: dict = Depends(verify_current_user),
                      db: Session = Depends(get_db)):
    work = db.query(models.Work).filter(
        models.Work.id == work_id,
        models.Work.artist_id == current_user['id']
    ).first()

    if not work:
        raise HTTPException(status_code=404, detail="Work not found or not authorized to delete")
    db.delete(work)
    db.commit()
    return {"message": f"Work with ID {work_id} has been deleted successfully"}