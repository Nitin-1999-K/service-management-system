from fastapi import APIRouter, Depends, HTTPException
from api import deps
from sqlalchemy.orm import Session
from models import User as UserModel
from schemas import UserCreate, AdminUpdateUser, UserResponse, Message
from crud import user_crud, engineer_crud, head_crud

router = APIRouter()


@router.post("/users", response_model = Message, description="To create account for an employee. Only admin can create account")
def createUser(
    user_create: UserCreate,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_admin),
):

    if not user_create.user_type in [2, 3]:
        raise HTTPException(400, "Invalid user type")

    if user_create.supervisor_id:

        db_supervisor = user_crud.getUserById(db=db, user_id=user_create.supervisor_id)

        if not db_supervisor:
            raise HTTPException(404, "Supervisor not found")

        if db_supervisor.user_type == 3:
            raise HTTPException(
                403, "Service engineer does not have the previlige to be a supervisor"
            )

        if db_supervisor.user_type == 2 and user_create.user_type != 3:
            raise HTTPException(
                403, "Service head can only supervise a service engineer"
            )

    db_user = user_crud.getUser(
        db=db, email=user_create.email, mobile_number=user_create.mobile_number
    )

    if db_user:
        create_credentials = {
            "email": user_create.email,
            "mobile_number": user_create.mobile_number,
        }
        db_credentials = {
            "email": db_user.email,
            "mobile_number": db_user.mobile_number,
        }
        for credential in create_credentials:
            if create_credentials[credential] == db_credentials[credential]:
                raise HTTPException(
                    409,
                    f"{credential}: {create_credentials[credential]} already exists",
                )

    user_crud.createUser(db=db, user_create=user_create)
    return {"detail": "User created"}


@router.get("/users/type/{type_id}")
def getUsersByTypeId(
    user_type: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_admin),
):
    if not user_type in [1, 2, 3]:
        raise HTTPException(400, "Invalid user type")

    db_data = user_crud.getUsersByTypeId(db=db, user_type=user_type)
    return db_data
      
      
@router.patch("/users/{user_id}", response_model = Message, 
description="Update the details of an employee. Admins can update the supervisors of employees")  # Both service head and admin can alter their subordinate's credentials
def updateUser(
    user_id: str,
    user_update: AdminUpdateUser,
    current_user: UserModel = Depends(deps.get_current_admin),
    db: Session = Depends(deps.get_db),
):

    user = user_crud.getUserById(db=db, user_id=user_id)

    if not user:
        raise HTTPException(404, "User not found")

    if (
        current_user.user_type == 2
        and user.supervisor_id.casefold() != current_user.id.casefold()
    ):
        raise HTTPException(
            403, "Service heads can only update their subordinate's credentials"
        )

    if user_update.supervisor_id:

        if user.user_type == 1:
            raise HTTPException(403, "Admin cannot have a supervisor")

        db_supervisor = user_crud.getUserById(db=db, user_id=user_update.supervisor_id)

        if not db_supervisor:
            raise HTTPException(404, "Supervisor not found")

        if db_supervisor.user_type == 3:
            raise HTTPException(
                403, "Service engineer does not have the previlige to be a supervisor"
            )

        if db_supervisor.user_type == 2 and user.user_type != 3:
            raise HTTPException(
                403, "Service head can only supervise a service engineer"
            )

    db_user = user_crud.getUser(
        db=db, email=user_update.email, mobile_number=user_update.mobile_number
    )

    if db_user:
        create_credentials = {
            "email": user_update.email,
            "mobile_number": user_update.mobile_number,
        }
        db_credentials = {
            "email": db_user.email,
            "mobile_number": db_user.mobile_number,
        }
        for credential in create_credentials:
            if create_credentials[credential] == db_credentials[credential]:
                raise HTTPException(
                    409,
                    f"{credential}: {create_credentials[credential]} already exists",
                )

    user_crud.updateUser(db=db, user=user, user_update=user_update)
    return {"detail": "User updated"}


@router.delete("/users", response_model = Message, description="To soft delete a user account")
def deleteUser(
    user_id: str,
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_admin),
):
    user = user_crud.getUserById(db=db, user_id=user_id, status_code=1)
    if not user:
        raise HTTPException(404, "User not found")
    if user.user_type == 3:
        if engineer_crud.getPendingTickets(db = db, engineer_id = user.id):
            raise HTTPException(409, "The engineer has pending tickets")
    if user.user_type == 2:
        if head_crud.getPendingTickets(db = db, supervisor_id = user.id):
            raise HTTPException(409, "The subordinates of the head have pending tickets")
    if user.user_type == 1:
        raise HTTPException(403, "No permission to delete the admin account via this endpoint")
    user_crud.deleteUser(db = db, user = user)
    return {"detail": "user deleted"}


@router.patch("/users/recover/{user_id}", response_model = Message, description="To retreive soft deleted user account")
def recoverUser(
    user_id: str,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_admin)
):
    user = user_crud.getUserById(db=db, user_id=user_id, status_code = -1)
    if not user:
        raise HTTPException(404, f"There is no deleted account with user_id: {user_id}")
    user_crud.recoverUser(db = db, user = user)
    return {"detail": "user recovered"}