
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

router = APIRouter()

# Register ke liye schema
class UserCreate(BaseModel):
    username: str
    password: str
    role: str

@router.post("/register")
async def register(user: UserCreate):
    # Bhai, aage chal kar yahan SQLite database me save karne ka code dalenge.
    # Abhi ke liye success message bhej rahe hain taaki UI test ho jaye.
    return {"message": "User registered successfully", "role": user.role}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Dummy token
    return {"access_token": "super_secret_dummy_token", "token_type": "bearer"}
