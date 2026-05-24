from typing import Optional, List
from sqlalchemy import String, ForeignKey, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    # ... baki fields ...
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="customers")
    opportunities = relationship("Opportunity", back_populates="customer")
    activities = relationship("Activity", back_populates="customer")
