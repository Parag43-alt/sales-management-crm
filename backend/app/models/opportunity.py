from typing import Optional
from sqlalchemy import String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Opportunity(Base):
    __tablename__ = "opportunities"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Relationships
    customer = relationship("Customer", back_populates="opportunities")
    owner = relationship("User", back_populates="opportunities")
