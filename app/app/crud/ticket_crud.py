from sqlalchemy.orm import Session
from schemas import TicketCreate
from models import Ticket as TicketModel
from models import TicketRaiser


def raiseTicket(
    db: Session,
    ticket_create: TicketCreate,
    user_id: int | None = None
):
    db_ticket = TicketModel(**ticket_create.model_dump())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    if user_id:
        db.add(TicketRaiser(user_id = user_id, ticket_id = db_ticket.id))
    db.commit()
    return db_ticket


def getTicketById(
    db: Session, 
    ticket_id: int,
    status_codes: list[int] | None = None
):
    if status_codes:
        ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id, TicketModel.status_code.in_(status_codes)).first()
    else:
        ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    return ticket

    # cancelled => -1, pending => 0, Alloted => 1