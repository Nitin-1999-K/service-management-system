from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from crud import allotment_crud
from schemas import Allotment, Message
from models import User as UserModel
from api import deps
from crud import user_crud, ticket_crud


router = APIRouter()


@router.post("/allot", response_model = Message, description = "Admin can allot ticket to any engineer. Service head can only allot to their subordinates")
def allotTicket(
    allotment: Allotment,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_head),
):

    engineer = user_crud.getUserById(
        db=db, user_id=allotment.engineer_id, status_code=1
    )

    if not engineer:
        raise HTTPException(404, "Engineer not found")

    if engineer.user_type != 3:
        raise HTTPException(409, "Ticket can be alloted only to an engineer")

    if (
        current_user.user_type == 2
        and engineer.supervisor_id.casefold() != current_user.id.casefold()
    ):
        raise HTTPException(
            403, "Engineer is not under the supervision of the current user"
        )

    db_ticket = ticket_crud.getTicketById(
        db=db, ticket_id=allotment.ticket_id, status_codes=[0, 1]
    )

    if not db_ticket:
        raise HTTPException(404, "Ticket not found")

    if db_ticket.status_code == 1:
        raise HTTPException(409, "Ticket Already Alloted to an engineer")

    allotment_crud.allotTicket(
        db=db, allotment=allotment, allocator_id=current_user.id, db_ticket=db_ticket
    )
    return {"detail": "Ticket Alloted"}


@router.post("/re-allot", response_model = Message, 
             description="Admin can re-allot ticket to any engineer. Service head can only re-allot within their subordinates")
def reviseAllotment(
    allotment_revise: Allotment,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_head),
):
    db_ticket = ticket_crud.getTicketById(
        db=db, ticket_id=allotment_revise.ticket_id, status_codes=[0, 1]
    )

    if not db_ticket:
        raise HTTPException(404, "Ticket not found")

    if db_ticket.status_code == 0:
        raise HTTPException(404, "Ticket is not alloted to anyone")

    allotment_prev = db_ticket.ticket_allotment[-1]

    if (
        not allotment_prev
    ):  # This is only for double checking eventhough I already checked if ticket.status_code == 0
        raise HTTPException(404, "Ticket is not alloted to anyone")

    if (
        allotment_prev.status_code == 3
    ):  # This is only for double checking eventhough I already checked if ticket.status_code == 0
        raise HTTPException(404, "Ticket is not alloted to anyone")

    if allotment_prev.status_code == 1:
        raise HTTPException(409, "Service engineer already departed")
    
    if allotment_prev.status_code == -1:
        raise HTTPException(409, "Ticket cancelled")

    # Cancelled => -1, Pending => 0, Departed => 1, Re-assigned => 2 Released => 3

    engineer = user_crud.getUserById(
        db=db, user_id=allotment_revise.engineer_id, status_code=1
    )

    if not engineer:
        raise HTTPException(404, "Engineer not found")

    if engineer.user_type != 3:
        raise HTTPException(409, "Ticket can be alloted only to an engineer")

    if current_user.user_type == 2:

        if (
            allotment_prev.engineer.supervisor_id.casefold()
            != current_user.id.casefold()
        ):
            raise HTTPException(
                403, "This ticket is not under the control of current service head"
            )

        if engineer.supervisor_id.casefold() != current_user.id.casefold():
            raise HTTPException(
                403, "Engineer is not under the supervision of the current user"
            )

    allotment_crud.reviseAllotment(
        db=db,
        allotment_prev=allotment_prev,
        allotment_revise=allotment_revise,
        allocator_id=current_user.id,
    )

    return {"detail": "Ticket re-alloted"}


@router.patch("/release", response_model = Message, 
              description="One service head has to release a ticket for the other head to acquire it")
def releaseAllotment(
    ticket_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_head),
):

    ticket = ticket_crud.getTicketById(db = db, ticket_id= ticket_id, status_codes=[0,1])

    if not ticket:
        raise HTTPException(404, "Ticket not found")
    
    if ticket.status_code == 0:
        raise HTTPException(400, "Ticket is currently not alloted to any engineer")

    latest_allotment = ticket.ticket_allotment[-1]

    if ( # I am checking this condition before other conditions because one service head should not know the ticket status of other service heads
        current_user.user_type == 2
        and latest_allotment.engineer.supervisor_id.casefold() != current_user.id.casefold()
    ):
        raise HTTPException(
            403, "Ticket is not under the authority of current service head"
        )

    if latest_allotment.status_code == -1:
        raise HTTPException(409, "Ticket cancelled")

    if latest_allotment.status_code == 1:
        raise HTTPException(409, "Service engineer already departed")

    if latest_allotment.status_code == 2:
        raise HTTPException(409, "Ticket re-alloted to another engineer")

    if latest_allotment.status_code == 3:
        raise HTTPException(409, "Ticket allotment is already released")

    allotment_crud.releaseAllotment(db=db, allotment=latest_allotment)

    return {"detail": "Allotment released"}