from fastapi import Depends, HTTPException
from core.security import ALGORITHM
from core.config import settings
from models import User as UserModel
import jwt
from db.db import engine
from sqlalchemy.orm import Session, sessionmaker
from datetime import datetime
from core.security import oauth2_bearer


SessionLocal = sessionmaker(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_bearer)
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")

        if not user_id:
            return None

        expiry_date = payload.get("exp")
        if expiry_date and datetime.utcnow() > datetime.fromtimestamp(expiry_date):
            return None

        else:
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
        return user

    except:
        raise HTTPException(401, "Token Invalid or Expired")


def get_current_active_user(
    token: str = Depends(oauth2_bearer), 
    db: Session = Depends(get_db)
):
    user = get_current_user(db=db, token=token)
    if user.status_code == 1:
        return user
    raise HTTPException(404, "User not found")


def get_current_head(
    token: str = Depends(oauth2_bearer), 
    db: Session = Depends(get_db)
):
    user = get_current_active_user(db=db, token=token)
    if user.user_type <= 2:
        return user
    raise HTTPException(403, "User does not have enough previliges")


def get_current_admin(
    token: str = Depends(oauth2_bearer), 
    db: Session = Depends(get_db)
):
    user = get_current_active_user(db=db, token=token)
    if user.user_type == 1:
        return user
    raise HTTPException(403, "User does not have enough previliges")