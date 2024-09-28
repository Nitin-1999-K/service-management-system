from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import User as UserModel
from schemas import AdminUpdateUser, HeadUpdateUser, Message
from api.endpoints import admin
from api import deps

router = APIRouter()


@router.patch("/{user_id}", response_model = Message, description = "Service heads can update the details of their subordinates")  
def updateUser(
    user_id: str,
    user_update: HeadUpdateUser,
    current_user: UserModel = Depends(deps.get_current_head),
    db: Session = Depends(deps.get_db),
):
    return admin.updateUser(
        db=db,
        user_id=user_id,
        user_update=AdminUpdateUser(**user_update.model_dump(exclude_unset=True)),
        current_user=current_user,
    )
