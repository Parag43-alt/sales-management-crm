from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

# Shared properties
class CustomerBase(BaseModel):
    company_name: str
    contact_name: str
    email: EmailStr
    phone: Optional[str] = None
    segment: Optional[str] = None
    satisfaction_score: Optional[float] = None
    account_plan: Optional[str] = None

# Properties to receive on customer creation
class CustomerCreate(CustomerBase):
    pass

# Properties to receive on customer update
class CustomerUpdate(BaseModel):
    company_name: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    segment: Optional[str] = None
    satisfaction_score: Optional[float] = None
    account_plan: Optional[str] = None
    owner_id: Optional[int] = None

# Properties to return to client
class CustomerResponse(CustomerBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
