from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Ye tere folder me 'hosho_crm.db' naam se ek local file bana dega (Best for assignment zip)
SQLALCHEMY_DATABASE_URL = "sqlite:///./hosho_crm.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Database se connect hone ka function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
