from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from api.deps import get_db
from crud import user_crud
from core import security
from api import deps
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post("/token", description = "To log-in")
def createAccessToken(db: Session = Depends(deps.get_db), user: OAuth2PasswordRequestForm = Depends()):

    db_user = user_crud.getUserById(db = db, user_id = user.username) # Empolyees will enter their ID's in the username section
    
    if not db_user:
        raise HTTPException(status_code=404, detail = "User not found")
    
    if db_user.status_code == -1:
        raise HTTPException(status_code=404, detail = "User not found")
    
    if not security.authenticate(user.password, db_user.hashed_password):
        raise HTTPException(status_code= 401, detail = "Incorrect Password")
    
    token = security.create_access_token(db_user.id)
    return {"access_token": token,"token_type": "bearer"}