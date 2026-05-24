from fastapi import APIRouter

router = APIRouter()

@router.get("")
@router.get("/")
async def get_products():
    return [
        {"id": 501, "name": "Enterprise License", "category": "Software", "price": "4999", "stock": "Unlimited", "status": "Active"},
        {"id": 502, "name": "Cloud Server Setup", "category": "Service", "price": "1200", "stock": "N/A", "status": "Active"}
    ]
