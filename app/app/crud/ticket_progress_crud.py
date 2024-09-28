from fastapi import Depends
from sqlalchemy.orm import Session
from models import (
    TicketProgress as TicketProgressModel,
    CancelledTicket as CancelledTicketModel,
    TicketAllotment as TicketAllotmentModel,
)
from schemas import TicketProgressUpdate
from datetime import datetime
from api import deps


def engineerDepart(db: Session, allotment: TicketAllotmentModel):
    allotment.status_code = 1
    db.add(TicketProgressModel(allotment_id=allotment.id))
    db.commit()


def getTicketProgressById(
    ticket_progress_id: int,
    status_codes: list[int] | None = None,
    db: Session = Depends(deps.get_db),
):
    if status_codes:
        ticket_progress = (
            db.query(TicketProgressModel)
            .filter(
                TicketProgressModel.id == ticket_progress_id,
                TicketProgressModel.status_code.in_(status_codes),
            )
            .first()
        )
    else:
        ticket_progress = (
            db.query(TicketProgressModel)
            .filter(TicketProgressModel.id == ticket_progress_id)
            .first()
        )
    return ticket_progress


def cancelTicketProgress(
    db: Session, ticket_progress: TicketProgressModel, description: str, user_id: str
):
    ticket_progress.status_code = -1
    ticket_progress.description = description
    ticket_id = ticket_progress.ticket_allotment.ticket.id
    db.add(
        CancelledTicketModel(
            ticket_id=ticket_id, user_id=user_id, description=description
        )
    )
    db.commit()


def updateTicketProgress(
    db: Session,
    ticket_progress: TicketProgressModel,
    ticket_progress_update: TicketProgressUpdate,
):
    for key, value in ticket_progress_update.model_dump(exclude_unset=True).items():
        setattr(ticket_progress, key, value)
    db.commit()
