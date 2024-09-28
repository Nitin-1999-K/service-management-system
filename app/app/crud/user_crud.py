from sqlalchemy import or_
from sqlalchemy.orm import Session
from models import User as UserModel
from schemas import UserCreate, AdminUpdateUser
from core import security


def createUser(db: Session, user_create: UserCreate):
    hashed_password = security.hash_password(user_create.password)

    db_user = UserModel(
        **user_create.model_dump(exclude=("password")),
        hashed_password=hashed_password,
        db=db
    )
    db.add(db_user)
    db.commit()
    # db.refresh(db_user)
    # return db_user


def getUser(
    db: Session,
    email: str,
    mobile_number: str,
):
    user = db.query(UserModel).filter(or_(UserModel.email == email, UserModel.mobile_number == mobile_number)).first()
    return user


def getUserById(
    db: Session,
    user_id: str,
    status_code: int | None = None,
    supervisor_id: str | None = None,
):
    if status_code == None:
        if supervisor_id == None:
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
        else:
            user = (
                db.query(UserModel)
                .filter(
                    UserModel.id == user_id, UserModel.supervisor_id == supervisor_id
                )
                .first()
            )
    else:
        if supervisor_id == None:
            user = (
                db.query(UserModel)
                .filter(UserModel.id == user_id, UserModel.status_code == status_code)
                .first()
            )
        else:
            user = (
                db.query(UserModel)
                .filter(
                    UserModel.id == user_id,
                    UserModel.status_code == status_code,
                    UserModel.supervisor_id == supervisor_id,
                )
                .first()
            )
    return user


def getUsers(
    db: Session, supervisor_id: str | None = None, status_codes: list[int] | None = None
):
    if supervisor_id == None:
        if status_codes:
            return (
                db.query(UserModel)
                .filter(
                    UserModel.supervisor_id == supervisor_id,
                    UserModel.status_code.in_(status_codes),
                )
                .all()
            )
        else:
            return (
                db.query(UserModel)
                .filter(UserModel.supervisor_id == supervisor_id)
                .all()
            )
    else:
        if status_codes:
            return (
                db.query(UserModel)
                .filter(UserModel.status_code.in_(status_codes))
                .all()
            )
        else:
            return db.query(UserModel).all()


def getUsersByTypeId(db: Session, user_type: int):
    return db.query(UserModel).filter(UserModel.user_type == user_type).all()


def updateUser(user_update: AdminUpdateUser, db: Session, user: UserModel):
    for key, value in user_update.model_dump(
        exclude_unset=True, exclude=["password"]
    ).items():
        setattr(user, key, value)
    if user_update.password:
        user.hashed_password = security.hash_password(user_update.password)
    db.commit()
    # db.refresh(user)
    return user


def deleteUser(db: Session, user: UserModel):
    user.status_code = -1
    db.commit()


def recoverUser(db: Session, user: UserModel):
    user.status_code = 1
    db.commit()