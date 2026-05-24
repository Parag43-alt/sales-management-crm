from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, default="sales_rep")
    is_active = Column(Boolean, default=True)
    territory = Column(String)
    sales_target = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships - Ye saari lines hona zaroori hai
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    customers = relationship("Customer", back_populates="owner")
    activities = relationship("Activity", back_populates="user")
    opportunities = relationship("Opportunity", back_populates="owner")
