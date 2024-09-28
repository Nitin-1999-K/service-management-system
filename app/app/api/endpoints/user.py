from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from api import deps
from models import User as UserModel
from crud import user_crud
from schemas import UserResponse

router = APIRouter()


@router.get("/{user_id}", response_model= UserResponse, description= "To view a specific user. Service engineer can only view his subordinate")
def getUser(
    user_id: str,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_head),
):

    if current_user.user_type == 1:
        user = user_crud.getUserById(db=db, user_id=user_id)
    else:
        user = user_crud.getUserById(db=db, user_id=user_id, supervisor_id=current_user.id)
    if user:
        return user
    raise HTTPException(404, "No users found")


@router.get("/", response_model= list[UserResponse], description= "To view all users. Service engineer can only view his subordinates")
def getUsers(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_head),
):
    if current_user.user_type == 1:
        users = user_crud.getUsers(db=db)
    else:
        users = user_crud.getUsers(db=db, supervisor_id=current_user.id)

    if users:
        return users
    raise HTTPException(404, "No users found")
