from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_customers():
    # Ye dummy data hai taaki tera frontend table test ho sake
    return [
        {"id": 101, "name": "Acme Corp", "email": "contact@acme.com", "status": "Active"},
        {"id": 102, "name": "Global Tech", "email": "info@globaltech.com", "status": "Lead"},
        {"id": 103, "name": "Stark Industries", "email": "tony@stark.com", "status": "Active"}
    ]
