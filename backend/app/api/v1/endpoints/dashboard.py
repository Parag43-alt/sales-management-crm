from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.core.database import get_db
from app.models.customer import Customer
from app.models.opportunity import Opportunity
from app.models.activity import Activity
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        total_customers = db.query(Customer).count()
        total_opportunities = db.query(Opportunity).count()
        total_activities = db.query(Activity).count()
        
        revenue_result = db.query(func.sum(Opportunity.expected_revenue)).filter(Opportunity.status == "Won").scalar()
        total_revenue = float(revenue_result) if revenue_result else 0.0

        won_deals = db.query(Opportunity).filter(Opportunity.status == "Won").count()
        lost_deals = db.query(Opportunity).filter(Opportunity.status == "Lost").count()
        pending_activities = db.query(Activity).filter(Activity.status == "Pending").count()

        return {
            "total_customers": total_customers,
            "total_opportunities": total_opportunities,
            "total_activities": total_activities,
            "total_revenue": total_revenue,
            "won_deals": won_deals,
            "lost_deals": lost_deals,
            "pending_activities": pending_activities
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent-activities")
def get_recent_activities(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        activities = db.query(Activity).order_by(desc(Activity.created_at)).limit(5).all()
        return [
            {
                "id": act.id,
                "type": act.type,
                "description": act.description,
                "status": act.status,
                "created_at": act.created_at
            } for act in activities
        ]
    except Exception:
        return []

@router.get("/pipeline")
def get_pipeline_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        pipeline_data = db.query(
            Opportunity.stage, func.count(Opportunity.id).label("count")
        ).group_by(Opportunity.stage).all()
        return [{"stage": row[0], "count": row[1]} for row in pipeline_data]
    except Exception:
        return []

@router.get("/revenue")
def get_revenue_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        won_revenue = db.query(func.sum(Opportunity.expected_revenue)).filter(Opportunity.status == "Won").scalar() or 0
        pipeline_revenue = db.query(func.sum(Opportunity.expected_revenue)).filter(Opportunity.status == "Open").scalar() or 0
        return {
            "won_revenue": float(won_revenue),
            "pipeline_revenue": float(pipeline_revenue)
        }
    except Exception:
        return {"won_revenue": 0.0, "pipeline_revenue": 0.0}
