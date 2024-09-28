from sqlalchemy.orm import Session
from schemas import Allotment
from models import Ticket as TicketModel, TicketAllotment as TicketAllotmentModel


def allotTicket(
    db: Session,
    allotment: Allotment,
    allocator_id: str,
    db_ticket: TicketModel | None = None,
):
    db.add(TicketAllotmentModel(**allotment.model_dump(), allocator_id=allocator_id))
    if db_ticket:
        db_ticket.status_code = 1
    db.commit()


def getAllotmentById(
    db: Session, allotment_id: int, status_codes: list[int] | None = None
):
    if status_codes:
        allotment = (
            db.query(TicketAllotmentModel)
            .filter(
                TicketAllotmentModel.id == allotment_id,
                TicketAllotmentModel.status_code.in_(status_codes),
            )
            .first()
        )
    else:
        allotment = (
            db.query(TicketAllotmentModel)
            .filter(TicketAllotmentModel.id == allotment_id)
            .first()
        )
    return allotment


def reviseAllotment(
    db: Session,
    allotment_prev: TicketAllotmentModel,
    allotment_revise: Allotment,
    allocator_id: str,
):
    allotment_prev.status_code = 2
    allotTicket(db=db, allotment=allotment_revise, allocator_id=allocator_id)


def releaseAllotment(db: Session, allotment: TicketAllotmentModel):
    allotment.status_code = 3
    allotment.ticket.status_code = 0
    db.commit()





# def findLatestAllotment(
#     db: Session,
#     ticket_id: int,
#     status_codes: list[int] | None = None
# ):
#     if status_codes:
#         allotment = db.query(TicketAllotmentModel).filter(
#         TicketAllotmentModel.ticket_id == ticket_id,
#         TicketAllotmentModel.status_code.in_(status_codes)).order_by(TicketAllotmentModel.id.desc()).first()
#     else:
#         allotment = db.query(TicketAllotmentModel).filter(
#         TicketAllotmentModel.ticket_id == ticket_id).order_by(TicketAllotmentModel.id.desc()).first()
#     return allotment