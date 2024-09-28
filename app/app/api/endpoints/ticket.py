from fastapi import APIRouter, Depends, HTTPException, Body
from api import deps
from sqlalchemy.orm import Session
from models import User as UserModel
from schemas import TicketCreate, Message
from crud import customer_crud, ticket_crud

router = APIRouter()


@router.post("/ticket", response_model = Message, description="Service engineer and admin can raise ticket for the customer")
def raiseTicket(
    ticket_create: TicketCreate,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_head),
):
    customer = customer_crud.getCustomerById(
        db=db, customer_id=ticket_create.customer_id
    )
    if not customer:
        raise HTTPException(404, "Customer not found")
    ticket_crud.raiseTicket(
        db=db,
        ticket_create=ticket_create,
        user_id=current_user.id if current_user else None,
    )
    return {"detail": "Ticket Raised"}


@router.delete("/ticket", response_model = Message, 
               description="Service engineer and admin can cancel tickets if the engineer didn't depart yet")
def cancelTicket(
    ticket_id: int,
    description: str = Body(),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_head),
):
    ticket = ticket_crud.getTicketById(db=db, ticket_id=ticket_id, status_codes=[0, 1])
    if not ticket:
        raise HTTPException(404, "Ticket not found")
    if ticket.status_code == 1:
        if (
            current_user.user_type == 2
            and ticket.ticket_allotment[-1].engineer.supervisor_id.casefold() != current_user.id.casefold()
        ):
            raise HTTPException(403, "Ticket is not under the control of current head")
        if ticket.ticket_allotment[-1].status_code == 1:
            raise HTTPException(403, "Service engineer already departed")
    ticket_crud.cancelTicket(
        db=db, ticket=ticket, user_id=current_user.id, description=description
    )
    return {"detail": "Ticket cancelled"}
# Update ticket