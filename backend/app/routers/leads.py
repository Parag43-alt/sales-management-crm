from fastapi import APIRouter

router = APIRouter()

# Dono raaste open kar diye taaki 307 Redirect na aaye
@router.get("")
@router.get("/")
async def get_leads():
    return [
        {"id": 1001, "name": "TechVision Inc", "email": "hello@techvision.com", "status": "New", "priority": "High", "source": "Website"},
        {"id": 1002, "name": "Alpha Solutions", "email": "sales@alpha.com", "status": "Qualified", "priority": "Medium", "source": "Referral"}
    ]
