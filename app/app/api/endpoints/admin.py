from fastapi import APIRouter, Depends, HTTPException
from api import deps
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from models import User as UserModel
from schemas import UserCreate, AdminUpdateUser, CustomerCreate, AllotmentCreate
from crud import user_crud, customer_crud, ticket_crud, allotment_crud

router = APIRouter()


@router.post("/user")
def createUser(
    user_create: UserCreate,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_admin)
):
    
    if not user_create.user_type in [2,3]:
        raise HTTPException(400, "Invalid user type")

    if user_create.supervisor_id:

        db_supervisor = user_crud.getUserById(db = db, user_id = user_create.supervisor_id)

        if not db_supervisor:
            raise HTTPException(404, "Supervisor not found")
        
        if db_supervisor.user_type == 3:
            raise HTTPException(403, "Service engineer does not have the previlige to be a supervisor")
        
        if db_supervisor.user_type == 2 and user_create.user_type != 3:
            raise HTTPException(403, "Service head can only supervise a service engineer")

    db_user = user_crud.getUser(db = db, email = user_create.email, mobile_number = user_create.mobile_number)

    if db_user:
        create_credentials = {"email": user_create.email, "mobile_number": user_create.mobile_number}
        db_credentials = {"email": db_user.email, "mobile_number": db_user.mobile_number}
        for credential in create_credentials:
            if create_credentials[credential] == db_credentials[credential]:
                raise HTTPException(409, f"{credential}: {create_credentials[credential]} already exists")
            
    return user_crud.createUser(db = db, user_create = user_create)


@router.patch("/user/{user_id}") # Both service head and admin can alter their subordinate's credentials
def updateUser(
    user_id: str,
    user_update: AdminUpdateUser,
    current_user: UserModel = Depends(deps.get_current_admin),
    db: Session = Depends(deps.get_db)
):

    user = user_crud.getUserById(db = db, user_id = user_id)

    if not user:
        raise HTTPException(404, "User not found")
    
    if current_user.user_type == 2 and user.supervisor_id.casefold() != current_user.id.casefold():
        raise HTTPException(403, "Service heads can only update their subordinate's credentials")
    
    # if user_update.user_type and user_update.user_type != 2: 
    #         raise HTTPException(400, "Invalid user type")
    # First we have to change the user type and then only we can determine the supervisor permission  

    if user_update.supervisor_id: 

        if user.user_type == 1:
            raise HTTPException(403, "Admin cannot have a supervisor")

        db_supervisor = user_crud.getUserById(db = db, user_id = user_update.supervisor_id)

        if not db_supervisor:
            raise HTTPException(404, "Supervisor not found")
        
        if db_supervisor.user_type == 3:
            raise HTTPException(403, "Service engineer does not have the previlige to be a supervisor")
        
        if db_supervisor.user_type == 2 and user.user_type != 3:
            raise HTTPException(403, "Service head can only supervise a service engineer")

    db_user = user_crud.getUser(db = db, email = user_update.email, mobile_number = user_update.mobile_number)

    if db_user:
        create_credentials = {"email": user_update.email, "mobile_number": user_update.mobile_number}
        db_credentials = {"email": db_user.email, "mobile_number": db_user.mobile_number}
        for credential in create_credentials:
            if create_credentials[credential] == db_credentials[credential]:
                raise HTTPException(409, f"{credential}: {create_credentials[credential]} already exists")
                        
    return user_crud.updateUser(db = db, user = user, user_update = user_update)