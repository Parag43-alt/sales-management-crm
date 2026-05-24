from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate

def create_customer(db: Session, obj_in: CustomerCreate, owner_id: int) -> Customer:
    db_obj = Customer(
        **obj_in.model_dump(),
        owner_id=owner_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_customer(db: Session, customer_id: int) -> Optional[Customer]:
    return db.get(Customer, customer_id)

def get_customers(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None, 
    owner_id: Optional[int] = None
) -> List[Customer]:
    stmt = select(Customer)
    
    # Ownership filtering
    if owner_id is not None:
        stmt = stmt.where(Customer.owner_id == owner_id)
        
    # Search functionality across multiple columns
    if search:
        search_term = f"%{search}%"
        stmt = stmt.where(
            or_(
                Customer.company_name.ilike(search_term),
                Customer.contact_name.ilike(search_term),
                Customer.email.ilike(search_term)
            )
        )
        
    stmt = stmt.offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())

def update_customer(db: Session, db_obj: Customer, obj_in: CustomerUpdate) -> Customer:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_customer(db: Session, customer_id: int) -> Optional[Customer]:
    obj = db.get(Customer, customer_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj
