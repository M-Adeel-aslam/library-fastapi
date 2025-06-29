from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class CreateUser(BaseModel):
    username : str
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id:int
    username : str
    email : EmailStr

    class Config():
        orm_mode = True

# Works
class WorksIn(BaseModel):
    title:str
    description:Optional[str]=None
    content:str

class WorksOut(WorksIn):
    id:int
    artist_id:int
    created_at:datetime
    updated_at:datetime
    class Config():
        orm_mode = True
# update

class updateWork(BaseModel):
    title:str
    description:Optional[str]=None
    content:str

class updateWorkOut(updateWork):
    id:int
    artist_id:int
    created_at:datetime
    updated_at:datetime
    class Config():
        orm_mode = True

# support
class SupportIn(BaseModel):
    amount:int

class SupportOut(SupportIn):
    id:int
    work_id:int
    supporter_id:int
    supported_at:datetime

    class Config():
        orm_mode = True

# Join
class WorkDetailsOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    content: str
    created_at: datetime
    updated_at: datetime
    artist_username: str
    artist_email: str
    total_support: int

    class Config:
        orm_mode = True