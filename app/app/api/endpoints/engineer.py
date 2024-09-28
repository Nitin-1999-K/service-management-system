from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from crud import engineer_crud
from models import User as UserModel
from api import deps
from schemas import AllotmentResponse

router = APIRouter()


@router.get("/alloted-tickets/", response_model = list[AllotmentResponse], 
            description = "Engineers can view tickets alloted to them")
def getAllotedTickets(
    current_user: UserModel = Depends(deps.get_current_engineer),
    db: Session = Depends(deps.get_db),
):
    tickets = engineer_crud.getTickets(db=db, engineer_id=current_user.id)
    if tickets:
        return tickets
    raise HTTPException(404, "No ticket is alloted for this engineer")


@router.get("/alloted-tickets/{ticket_id}", response_model = list[AllotmentResponse], 
            description = "Engineers can view a specific ticket alloted to them where it could have been re-alloted more than one time")
def getAllotedTicket(
    ticket_id: int,
    current_user: UserModel = Depends(deps.get_current_engineer),
    db: Session = Depends(deps.get_db),
):
    ticket = engineer_crud.getTicket(
        db=db, engineer_id=current_user.id, ticket_id=ticket_id
    )
    if ticket:
        return ticket
    raise HTTPException(404, "Ticket not found")
