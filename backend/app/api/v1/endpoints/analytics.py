from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, extract
from typing import Dict, Any
from datetime import datetime, timedelta

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.opportunity import Opportunity
from app.models.activity import Activity
from app.models.customer import Customer

router = APIRouter()

@router.get("/advanced-metrics")
def get_advanced_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # 1. Funnel Data
        funnel_stages = ["Lead", "Qualification", "Proposal", "Negotiation", "Won", "Lost"]
        funnel_data = []
        for stage in funnel_stages:
            count = db.query(Opportunity).filter(Opportunity.stage == stage).count()
            funnel_data.append({"name": stage, "value": count})

        # 2. Monthly Revenue Trends (Last 6 Months Mock/Actual Logic)
        # Using a simple aggregation grouped by month
        trends = []
        for i in range(5, -1, -1):
            target_month = datetime.now() - timedelta(days=30*i)
            month_name = target_month.strftime("%b")
            
            # Sum expected revenue for WON deals in that month
            revenue = db.query(func.sum(Opportunity.expected_revenue)).filter(
                Opportunity.status == "Won",
                extract('month', Opportunity.created_at) == target_month.month,
                extract('year', Opportunity.created_at) == target_month.year
            ).scalar() or 0
            
            trends.append({"month": month_name, "revenue": float(revenue)})

        # 3. Activity Distribution
        activity_types = db.query(Activity.type, func.count(Activity.id)).group_by(Activity.type).all()
        activity_data = [{"name": act[0], "value": act[1]} for act in activity_types]
        if not activity_data:
             activity_data = [{"name": "No Data", "value": 1}] # Fallback for pie chart

        # 4. Team Performance (Dummy mapping for UI layout, maps to current user)
        won_deals = db.query(Opportunity).filter(Opportunity.status == "Won").count()
        team_data = [
            {"name": current_user.full_name or "You", "deals": won_deals, "target": current_user.sales_target or 100000}
        ]

        return {
            "funnel": funnel_data,
            "trends": trends,
            "activities": activity_data,
            "team": team_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
