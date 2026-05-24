from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate

def create_activity(db: Session, obj_in: ActivityCreate, user_id: int) -> Activity:
    db_obj = Activity(
        **obj_in.model_dump(),
        user_id=user_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_activity(db: Session, activity_id: int) -> Optional[Activity]:
    return db.get(Activity, activity_id)

def get_activities(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    activity_type: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    customer_id: Optional[int] = None,
    opportunity_id: Optional[int] = None,
    user_id: Optional[int] = None
) -> List[Activity]:
    stmt = select(Activity)
    
    # Ownership filtering (RBAC)
    if user_id is not None:
        stmt = stmt.where(Activity.user_id == user_id)
        
    if activity_type:
        stmt = stmt.where(Activity.activity_type == activity_type)
        
    if status:
        stmt = stmt.where(Activity.status == status)
        
    if priority:
        stmt = stmt.where(Activity.priority == priority)
        
    if customer_id:
        stmt = stmt.where(Activity.customer_id == customer_id)
        
    if opportunity_id:
        stmt = stmt.where(Activity.opportunity_id == opportunity_id)
        
    stmt = stmt.offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())

def update_activity(db: Session, db_obj: Activity, obj_in: ActivityUpdate) -> Activity:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_activity(db: Session, activity_id: int) -> Optional[Activity]:
    obj = db.get(Activity, activity_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj
