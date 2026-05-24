from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

# Shared properties
class OpportunityBase(BaseModel):
    title: str
    deal_value: float = Field(default=0.0, ge=0.0)
    stage: str = Field(default="Lead", description="Lead, Qualified, Proposal, Negotiation, Won, Lost")
    discount_requested: bool = False
    discount_approved: Optional[bool] = None
    forecast_category: str = "Pipeline"
    customer_id: int

# Properties to receive on creation
class OpportunityCreate(OpportunityBase):
    pass

# Properties to receive on update
class OpportunityUpdate(BaseModel):
    title: Optional[str] = None
    deal_value: Optional[float] = None
    stage: Optional[str] = None
    discount_requested: Optional[bool] = None
    discount_approved: Optional[bool] = None
    forecast_category: Optional[str] = None
    customer_id: Optional[int] = None
    owner_id: Optional[int] = None

# Properties to return to client
class OpportunityResponse(OpportunityBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
