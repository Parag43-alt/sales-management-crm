from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.opportunity import Opportunity
from app.schemas.opportunity import OpportunityCreate, OpportunityUpdate

def create_opportunity(db: Session, obj_in: OpportunityCreate, owner_id: int) -> Opportunity:
    db_obj = Opportunity(
        **obj_in.model_dump(),
        owner_id=owner_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_opportunity(db: Session, opportunity_id: int) -> Optional[Opportunity]:
    return db.get(Opportunity, opportunity_id)

def get_opportunities(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    stage: Optional[str] = None,
    customer_id: Optional[int] = None,
    owner_id: Optional[int] = None
) -> List[Opportunity]:
    stmt = select(Opportunity)
    
    # Ownership filtering (RBAC)
    if owner_id is not None:
        stmt = stmt.where(Opportunity.owner_id == owner_id)
        
    # Pipeline Stage filtering
    if stage:
        stmt = stmt.where(Opportunity.stage == stage)
        
    # Customer specific opportunities
    if customer_id:
        stmt = stmt.where(Opportunity.customer_id == customer_id)
        
    stmt = stmt.offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())

def update_opportunity(db: Session, db_obj: Opportunity, obj_in: OpportunityUpdate) -> Opportunity:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_opportunity(db: Session, opportunity_id: int) -> Optional[Opportunity]:
    obj = db.get(Opportunity, opportunity_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj
