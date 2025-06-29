from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from dotenv import load_dotenv
import os

OAuthScheme = OAuth2PasswordBearer(tokenUrl="authentication/login")


load_dotenv()

EXPIRY_TOKEN_MINUTES = os.getenv("EXPIRY_TOKEN_MINUTES")
KEY = os.getenv("KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(data:dict):
    encode_data = data.copy()
    expiry = datetime.utcnow()+timedelta(minutes=EXPIRY_TOKEN_MINUTES)
    encode_data.update({"exp":expiry})
    encoded_jwt = jwt.encode(encode_data,KEY,algorithm=ALGORITHM)
    return encoded_jwt


def verify_current_user(token: str = Depends(OAuthScheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = db.query(models.User).filter(models.User.email == email).first()
        if user is None:
            raise credentials_exception
        return {"id": user.id, "email": user.email} 
    except JWTError:
        raise credentials_exception