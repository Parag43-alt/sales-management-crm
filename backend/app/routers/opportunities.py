from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_opportunities():
    return [
        {"id": 201, "customer": "Acme Corp", "amount": "$12,500", "stage": "Negotiation"},
        {"id": 202, "customer": "Global Tech", "amount": "$8,000", "stage": "Proposal Sent"},
        {"id": 203, "customer": "Stark Industries", "amount": "$45,000", "stage": "Closed Won"}
    ]
