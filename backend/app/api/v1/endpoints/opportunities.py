from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.crud import crud_opportunity
from app.crud import crud_customer
from app.schemas.opportunity import OpportunityCreate, OpportunityUpdate, OpportunityResponse

router = APIRouter()

@router.post("/", response_model=OpportunityResponse, status_code=status.HTTP_201_CREATED)
def create_opportunity(
    *,
    db: Session = Depends(get_db),
    opportunity_in: OpportunityCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new sales opportunity. 
    Strict cross-validation ensures customer exists before attaching a pipeline deal.
    """
    customer = crud_customer.get_customer(db=db, customer_id=opportunity_in.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Associated customer not found")
        
    # Validation: A sales rep shouldn't attach deals to another rep's customer
    if current_user.role not in ["sales_manager", "executive", "admin"] and customer.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not permitted to create opportunities for customers you do not own")

    opportunity = crud_opportunity.create_opportunity(db=db, obj_in=opportunity_in, owner_id=current_user.id)
    return opportunity

@router.get("/", response_model=List[OpportunityResponse])
def read_opportunities(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    stage: Optional[str] = Query(None, description="Filter by Pipeline stage (e.g., Lead, Proposal, Won)"),
    customer_id: Optional[int] = Query(None, description="Filter by Customer ID"),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieve opportunities with dynamic pipeline tracking.
    """
    owner_id = current_user.id if current_user.role not in ["sales_manager", "executive", "admin"] else None
    opportunities = crud_opportunity.get_opportunities(
        db=db, skip=skip, limit=limit, stage=stage, customer_id=customer_id, owner_id=owner_id
    )
    return opportunities

@router.get("/{opportunity_id}", response_model=OpportunityResponse)
def read_opportunity(
    opportunity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get a specific deal detail by ID.
    """
    opportunity = crud_opportunity.get_opportunity(db=db, opportunity_id=opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
        
    if current_user.role not in ["sales_manager", "executive", "admin"] and opportunity.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions to access this pipeline item")
        
    return opportunity

@router.put("/{opportunity_id}", response_model=OpportunityResponse)
def update_opportunity(
    *,
    db: Session = Depends(get_db),
    opportunity_id: int,
    opportunity_in: OpportunityUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update opportunity details (Move pipeline stages, change deal value).
    """
    opportunity = crud_opportunity.get_opportunity(db=db, opportunity_id=opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
        
    if current_user.role not in ["sales_manager", "executive", "admin"] and opportunity.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions to modify this deal")
        
    if opportunity_in.customer_id is not None and opportunity_in.customer_id != opportunity.customer_id:
        new_customer = crud_customer.get_customer(db=db, customer_id=opportunity_in.customer_id)
        if not new_customer:
            raise HTTPException(status_code=404, detail="Target customer for deal transfer not found")

    opportunity = crud_opportunity.update_opportunity(db=db, db_obj=opportunity, obj_in=opportunity_in)
    return opportunity

@router.delete("/{opportunity_id}", response_model=OpportunityResponse)
def delete_opportunity(
    *,
    db: Session = Depends(get_db),
    opportunity_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Remove a deal from the pipeline.
    """
    opportunity = crud_opportunity.get_opportunity(db=db, opportunity_id=opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
        
    if current_user.role not in ["sales_manager", "executive", "admin"] and opportunity.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions to delete this deal")
        
    opportunity = crud_opportunity.delete_opportunity(db=db, opportunity_id=opportunity_id)
    return opportunity
