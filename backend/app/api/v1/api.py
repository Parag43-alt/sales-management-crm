from fastapi import APIRouter
from app.api.v1.endpoints import auth, dashboard, notifications # notification import kiya
from app.api.v1.endpoints import analytics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
# Niche ye line zaroor daalna:
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Advanced Analytics"])
