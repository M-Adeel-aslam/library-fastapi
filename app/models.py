from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, unique=True, nullable=False)

    works = relationship("Work", back_populates="artist")
    supports = relationship("Support", back_populates="supporter")


class Work(Base):
    __tablename__ = "works"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    content = Column(String, nullable=False)
    artist_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    artist = relationship("User", back_populates="works")
    supports = relationship("Support", back_populates="work")

class Support(Base):
    __tablename__ = "supports"
    id = Column(Integer, primary_key=True, index=True)
    work_id = Column(Integer, ForeignKey('works.id'))
    supporter_id = Column(Integer, ForeignKey('users.id'))  # <-- renamed from support_id
    amount = Column(Integer, nullable=False)
    supported_at = Column(DateTime, default=datetime.utcnow, nullable=True)

    work= relationship("Work", back_populates="supports")
    supporter = relationship("User", back_populates="supports")