from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_activities():
    return [
        {"id": 301, "type": "Call", "description": "Discussed pricing with Acme", "date": "2026-05-24"},
        {"id": 302, "type": "Email", "description": "Sent proposal to Global Tech", "date": "2026-05-23"},
        {"id": 303, "type": "Meeting", "description": "Finalized contract with Stark", "date": "2026-05-22"}
    ]
