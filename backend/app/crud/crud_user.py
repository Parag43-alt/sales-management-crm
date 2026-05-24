from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.get(User, user_id)

def create_user(db: Session, user_in: UserCreate) -> User:
    # Schema se raw password hata kar hashed password save karenge
    db_obj = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role if user_in.role else "sales_rep",
        is_active=user_in.is_active if user_in.is_active is not None else True,
        territory=user_in.territory,
        sales_target=user_in.sales_target if user_in.sales_target is not None else 0.0
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
