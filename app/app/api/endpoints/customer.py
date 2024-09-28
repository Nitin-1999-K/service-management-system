from fastapi import APIRouter, Depends, HTTPException
from api import deps
from sqlalchemy.orm import Session
from models import User as UserModel
from schemas import CustomerCreate, TicketCreate, CustomerUpdate, CustomerResponse, Message
from crud import customer_crud
from api.endpoints import ticket

router = APIRouter()


@router.post("/", response_model = Message, description = "Admin and service heads can add new customer")
def addCustomer(
    customer: CustomerCreate,
    db: Session = Depends(deps.get_db),
    user: UserModel = Depends(deps.get_current_head),
):
    customer_crud.addCustomer(db=db, customer=customer)
    return {"detail": "Customer Added"}


@router.post("/ticket", response_model = Message)
def raiseTicket(ticket_create: TicketCreate, db: Session = Depends(deps.get_db)):
    ticket.raiseTicket(db=db, ticket_create=ticket_create, current_user=None)
    return {"detail": "Ticket Raised"}


@router.get("/", response_model = CustomerResponse, description = "Admin and service heads can view customer details")
def viewCustomerDetails(
    customer_id: int,
    db: Session = Depends(deps.get_db),
    user: UserModel = Depends(deps.get_current_head)
):
    customer = customer_crud.getCustomerById(db = db, customer_id=customer_id)
    if not customer:
        raise HTTPException(404, "Customer not found")
    return customer


@router.patch("/", response_model = Message, description = "Admin and service heads can update customer details")
def updateCustomerDetails(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: Session = Depends(deps.get_db),
    user: UserModel = Depends(deps.get_current_head)
):
    customer = customer_crud.getCustomerById(db = db, customer_id=customer_id)
    if not customer:
        raise HTTPException(404, "Customer not found")
    customer_crud.updateCustomerDetails(db = db, customer = customer, customer_update = customer_update)
    return {"detail": "Details updated"}