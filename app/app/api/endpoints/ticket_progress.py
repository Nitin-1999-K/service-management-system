from fastapi import HTTPException, Depends, Body
from crud import ticket_progress_crud, ticket_crud
from sqlalchemy.orm import Session
from models import User as UserModel
from fastapi import APIRouter
from api import deps
from schemas import TicketProgressUpdate, Message

router = APIRouter()


@router.post("/", response_model = Message, 
             description="Ticket Progress section will be auto-generated once the engineer marks the ticket allotment status as 'departed'")
def engineerDepart(
    ticket_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user),
):
    
    ticket = ticket_crud.getTicketById(db = db, ticket_id= ticket_id, status_codes=[0,1])

    if not ticket:
        raise HTTPException(404, "Ticket not found")
    
    if ticket.status_code == 0:
        raise HTTPException(400, "Ticket is currently not alloted to any engineer")

    latest_allotment = ticket.ticket_allotment[-1]


    if (
        current_user.user_type == 3
        and latest_allotment.engineer.id.casefold() != current_user.id.casefold()
    ):
        raise HTTPException(403, "Ticket does not belong to the current engineer")

    if (
        current_user.user_type == 2
        and latest_allotment.engineer.supervisor_id.casefold() != current_user.id.casefold()
    ):
        raise HTTPException(
            403, "Ticket does not come under the authority of current service head"
        )

    if latest_allotment.status_code == 1:
        raise HTTPException(409, "Engineer already departed")

    if latest_allotment.status_code == 2:
        raise HTTPException(409, "Ticket transferred to another service engineer")

    if latest_allotment.status_code == 3:
        raise HTTPException(409, "This ticket is released by service head / admin")

    ticket_progress_crud.engineerDepart(db=db, allotment=latest_allotment)
    return {"detail": "Progress generated"}


@router.delete("/", response_model = Message,
               description="Service engineer can cancel the ticket after reaching site if the ticket does not come under company policies")
def cancelTicketProgress(
    ticket_id: int,
    current_user: UserModel = Depends(deps.get_current_user),
    description: str = Body(),
    db: Session = Depends(deps.get_db),
):
    
    ticket = ticket_crud.getTicketById(db = db, ticket_id= ticket_id, status_codes=[0,1])

    if not ticket:
        raise HTTPException(404, "Ticket not found")
    
    if ticket.status_code == 0:
        raise HTTPException(400, "Ticket is currently not alloted to any engineer")

    if ticket.ticket_allotment[-1].status_code == -1:
        raise HTTPException(400, "Ticket cancelled")

    if ticket.ticket_allotment[-1].status_code == 0:
        raise HTTPException(400, "Service engineer not yet departed")

    ticket_progress = ticket.ticket_allotment[-1].ticket_progress

    if (
        current_user.user_type == 3
        and current_user.id.casefold()
        != ticket_progress.ticket_allotment.engineer.id.casefold()
    ):
        raise HTTPException(
            403, "This ticket is not managed by current service engineer"
        )

    if (
        current_user.user_type == 2
        and current_user.id.casefold()
        != ticket_progress.ticket_allotment.engineer.supervisor_id.casefold()
    ):
        raise HTTPException(
            403, "This ticket is not under the control of current service head"
        )

    ticket_progress_crud.cancelTicketProgress(
        db=db,
        ticket_progress=ticket_progress,
        description=description,
        user_id=current_user.id,
    )
    return {"detail": "Ticket cancelled"}


@router.patch("/", response_model = Message,
              description="Service engineer can add description to the ticket issue after reaching the site")
def updateTicketProgress(
    ticket_id: int,
    ticket_progress_update: TicketProgressUpdate,
    current_user: UserModel = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):

    ticket = ticket_crud.getTicketById(db = db, ticket_id= ticket_id, status_codes=[0,1])

    if not ticket:
        raise HTTPException(404, "Ticket not found")
    
    if ticket.status_code == 0:
        raise HTTPException(400, "Ticket is currently not alloted to any engineer")

    if ticket.ticket_allotment[-1].status_code == -1:
        raise HTTPException(400, "Ticket cancelled")

    if ticket.ticket_allotment[-1].status_code == 0:
        raise HTTPException(400, "Service engineer not yet departed")

    ticket_progress = ticket.ticket_allotment[-1].ticket_progress

    if ticket_progress.status_code == -1:
        raise HTTPException(400, "Ticket already cancelled")

    if ticket_progress.status_code == 1:
        raise HTTPException(400, "Ticket already marked as completed")

    if (
        current_user.user_type == 3
        and ticket_progress.ticket_allotment.engineer.id.casefold()
        != current_user.id.casefold()
    ):
        raise HTTPException(
            403, "Ticket does not belong to the current service engineer"
        )

    if (
        current_user.user_type == 2
        and ticket_progress.ticket_allotment.engineer.supervisor_id.casefold()
        != current_user.id.casefold()
    ):
        raise HTTPException(
            403, "Ticket does not come under the authority of current service engineer"
        )

    ticket_progress_crud.updateTicketProgress(
        db=db,
        ticket_progress=ticket_progress,
        ticket_progress_update=ticket_progress_update,
    )

    return {"detail": "Progress updated"}