from sqlalchemy import or_
from sqlalchemy.orm import Session
from models import User as UserModel
from schemas import UserCreate, AdminUpdateUser
from sqlalchemy.exc import IntegrityError
from core import security


def getUserById(
    db: Session,
    user_id: str,
    status_code: int | None = None
):
    if status_code == None:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
    else:
        user = db.query(UserModel).filter(UserModel.id == user_id, UserModel.status_code == status_code).first()
    return user


def getUser(
    db: Session,
    email: str,
    mobile_number: str,
):
    user = db.query(UserModel).filter(or_(UserModel.email == email, UserModel.mobile_number == mobile_number)).first()
    return user


def createUser(db: Session, user_create: UserCreate):
    hashed_password = security.hash_password(user_create.password)

    db_user = UserModel(
        **user_create.model_dump(exclude=("password")),
        hashed_password=hashed_password,
        db = db
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def updateUser(user_update: AdminUpdateUser, db: Session, user: UserModel):
    for key, value in user_update.model_dump(exclude_unset=True, exclude=["password"]).items():
        setattr(user, key, value)
    if user_update.password:
        user.hashed_password = security.hash_password(user_update.password)
    db.commit()
    db.refresh(user)
    return user

