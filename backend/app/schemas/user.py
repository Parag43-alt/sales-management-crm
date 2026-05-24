from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[str] = "sales_rep"
    is_active: Optional[bool] = True
    territory: Optional[str] = None
    sales_target: Optional[float] = 0.0

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    territory: Optional[str] = None
    sales_target: Optional[float] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    # FIXED: Pydantic V1 ke liye ye exact syntax lagta hai
    class Config:
        orm_mode = True
