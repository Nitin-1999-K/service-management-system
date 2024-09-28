from sqlalchemy.orm import Session
from schemas import CustomerCreate, CustomerUpdate
from models import Customer as CustomerModel


def addCustomer(db: Session, customer: CustomerCreate):
    db.add(CustomerModel(**customer.model_dump()))
    db.commit()


def getCustomerById(db: Session, customer_id: int):
    customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    return customer


def updateCustomerDetails(db: Session, customer: CustomerModel, customer_update: CustomerUpdate):
    for key, value in customer_update.model_dump(exclude_unset=True).items():
       setattr(customer, key, value)
    db.commit()