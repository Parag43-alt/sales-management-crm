from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

# Shared properties
class ActivityBase(BaseModel):
    activity_type: str = Field(..., description="Call, Meeting, Email, Follow-up, Demo, Task")
    notes: Optional[str] = None
    due_date: Optional[datetime] = None
    status: str = Field(default="Pending", description="Pending, In Progress, Completed, Cancelled")
    priority: str = Field(default="Medium", description="Low, Medium, High, Urgent")
    customer_id: Optional[int] = None
    opportunity_id: Optional[int] = None

# Properties to receive on creation
class ActivityCreate(ActivityBase):
    pass

# Properties to receive on update
class ActivityUpdate(BaseModel):
    activity_type: Optional[str] = None
    notes: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    customer_id: Optional[int] = None
    opportunity_id: Optional[int] = None

# Properties to return to client
class ActivityResponse(ActivityBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
