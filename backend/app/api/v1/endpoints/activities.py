from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.crud import crud_activity, crud_customer, crud_opportunity
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityResponse

router = APIRouter()

@router.post("/", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
def create_activity(
    *,
    db: Session = Depends(get_db),
    activity_in: ActivityCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Log a new activity (Call, Meeting, Task, etc.).
    """
    # Cross-validation: Check if assigned Customer exists and belongs to user
    if activity_in.customer_id:
        customer = crud_customer.get_customer(db=db, customer_id=activity_in.customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        if current_user.role not in ["sales_manager", "executive", "admin"] and customer.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not permitted to log activities for customers you do not own")
            
    # Cross-validation: Check if assigned Opportunity exists and belongs to user
    if activity_in.opportunity_id:
        opportunity = crud_opportunity.get_opportunity(db=db, opportunity_id=activity_in.opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found")
        if current_user.role not in ["sales_manager", "executive", "admin"] and opportunity.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not permitted to log activities for deals you do not own")

    activity = crud_activity.create_activity(db=db, obj_in=activity_in, user_id=current_user.id)
    return activity

@router.get("/", response_model=List[ActivityResponse])
def read_activities(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    activity_type: Optional[str] = Query(None, description="Filter by type (Call, Task, etc.)"),
    status: Optional[str] = Query(None, description="Filter by status (Pending, Completed, etc.)"),
    priority: Optional[str] = Query(None, description="Filter by priority (Low, High, etc.)"),
    customer_id: Optional[int] = Query(None, description="Filter by Customer ID"),
    opportunity_id: Optional[int] = Query(None, description="Filter by Opportunity ID"),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieve all activities with deep filtering options.
    """
    user_id = current_user.id if current_user.role not in ["sales_manager", "executive", "admin"] else None
    activities = crud_activity.get_activities(
        db=db, 
        skip=skip, 
        limit=limit, 
        activity_type=activity_type,
        status=status,
        priority=priority,
        customer_id=customer_id, 
        opportunity_id=opportunity_id,
        user_id=user_id
    )
    return activities

@router.get("/{activity_id}", response_model=ActivityResponse)
def read_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get a specific activity detail by ID.
    """
    activity = crud_activity.get_activity(db=db, activity_id=activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
        
    if current_user.role not in ["sales_manager", "executive", "admin"] and activity.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions to access this activity")
        
    return activity

@router.put("/{activity_id}", response_model=ActivityResponse)
def update_activity(
    *,
    db: Session = Depends(get_db),
    activity_id: int,
    activity_in: ActivityUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update activity details (e.g., mark as Completed, change due date).
    """
    activity = crud_activity.get_activity(db=db, activity_id=activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
        
    if current_user.role not in ["sales_manager", "executive", "admin"] and activity.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions to modify this activity")
        
    # Re-validate relationship switches if they are being updated
    if activity_in.customer_id is not None and activity_in.customer_id != activity.customer_id:
        customer = crud_customer.get_customer(db=db, customer_id=activity_in.customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Target customer not found")

    activity = crud_activity.update_activity(db=db, db_obj=activity, obj_in=activity_in)
    return activity

@router.delete("/{activity_id}", response_model=ActivityResponse)
def delete_activity(
    *,
    db: Session = Depends(get_db),
    activity_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Remove a task or activity log.
    """
    activity = crud_activity.get_activity(db=db, activity_id=activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
        
    if current_user.role not in ["sales_manager", "executive", "admin"] and activity.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions to delete this activity")
        
    activity = crud_activity.delete_activity(db=db, activity_id=activity_id)
    return activity
