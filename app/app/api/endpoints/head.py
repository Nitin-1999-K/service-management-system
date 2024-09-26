from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import User as UserModel
from schemas import AdminUpdateUser, HeadUpdateUser
from api.endpoints import admin
from api import deps

router = APIRouter()


@router.patch("/{user_id}") # Both service head and admin can alter their subordinate's credentials
def updateUser(
    user_id: str,
    user_update: HeadUpdateUser,
    current_user: UserModel = Depends(deps.get_current_head),
    db: Session = Depends(deps.get_db)
):   
    return admin.updateUser(db = db, user_id = user_id, user_update = AdminUpdateUser(**user_update.model_dump()), current_user = current_user)
