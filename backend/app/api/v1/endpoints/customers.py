from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.crud import crud_customer
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse

router = APIRouter()

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    *,
    db: Session = Depends(get_db),
    customer_in: CustomerCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new customer. Automatically assigns the current user as the owner.
    """
    customer = crud_customer.create_customer(db=db, obj_in=customer_in, owner_id=current_user.id)
    return customer

@router.get("/", response_model=List[CustomerResponse])
def read_customers(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Skip records for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Limit records for pagination"),
    search: Optional[str] = Query(None, description="Search by company, contact, or email"),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieve customers.
    Sales reps see only their own customers. Managers and executives see all.
    """
    owner_id = current_user.id if current_user.role not in ["sales_manager", "executive", "admin"] else None
    customers = crud_customer.get_customers(
        db=db, skip=skip, limit=limit, search=search, owner_id=owner_id
    )
    return customers

@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get a specific customer by ID.
    """
    customer = crud_customer.get_customer(db=db, customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
        
    # Check ownership
    if current_user.role not in ["sales_manager", "executive", "admin"] and customer.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions to access this customer")
        
    return customer

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    *,
    db: Session = Depends(get_db),
    customer_id: int,
    customer_in: CustomerUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update a customer.
    """
    customer = crud_customer.get_customer(db=db, customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
        
    if current_user.role not in ["sales_manager", "executive", "admin"] and customer.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions to update this customer")
        
    customer = crud_customer.update_customer(db=db, db_obj=customer, obj_in=customer_in)
    return customer

@router.delete("/{customer_id}", response_model=CustomerResponse)
def delete_customer(
    *,
    db: Session = Depends(get_db),
    customer_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete a customer.
    """
    customer = crud_customer.get_customer(db=db, customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
        
    if current_user.role not in ["sales_manager", "executive", "admin"] and customer.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions to delete this customer")
        
    customer = crud_customer.delete_customer(db=db, customer_id=customer_id)
    return customer
