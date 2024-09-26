from fastapi import APIRouter, Depends, HTTPException
from api import deps
from sqlalchemy.orm import Session
from models import User as UserModel, Customer as CustomerModel
from schemas import CustomerCreate, TicketCreate
from crud import customer_crud, ticket_crud

router = APIRouter()


@router.post("/ticket")
def raiseTicket(
    ticket_create: TicketCreate,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_head)
):
    customer = customer_crud.getCustomerById(db = db, customer_id = ticket_create.customer_id)
    if not customer:
        raise HTTPException(404, "Customer not found")
    db_ticket = ticket_crud.raiseTicket(db = db, ticket_create = ticket_create, user_id = current_user.id if current_user else None)
    return db_ticket

# Customer can delete ticket only if the status is in pending condition

