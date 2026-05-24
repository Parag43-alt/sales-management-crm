from sqlalchemy.orm import Session
from sqlalchemy import func, case, select

from app.models.customer import Customer
from app.models.opportunity import Opportunity
from app.models.activity import Activity
from app.models.user import User

def get_dashboard_kpis(db: Session, owner_id: int = None) -> dict:
    # Build base queries
    q_cust = select(func.count(Customer.id))
    q_opp = select(func.count(Opportunity.id))
    q_act = select(func.count(Activity.id))
    
    q_rev_won = select(func.sum(Opportunity.deal_value)).where(Opportunity.stage == "Won")
    q_pipe_val = select(func.sum(Opportunity.deal_value)).where(Opportunity.stage.notin_(["Won", "Lost"]))
    q_won_count = select(func.count(Opportunity.id)).where(Opportunity.stage == "Won")
    q_closed_count = select(func.count(Opportunity.id)).where(Opportunity.stage.in_(["Won", "Lost"]))

    # Apply RBAC Filtering
    if owner_id:
        q_cust = q_cust.where(Customer.owner_id == owner_id)
        q_opp = q_opp.where(Opportunity.owner_id == owner_id)
        q_act = q_act.where(Activity.user_id == owner_id)
        q_rev_won = q_rev_won.where(Opportunity.owner_id == owner_id)
        q_pipe_val = q_pipe_val.where(Opportunity.owner_id == owner_id)
        q_won_count = q_won_count.where(Opportunity.owner_id == owner_id)
        q_closed_count = q_closed_count.where(Opportunity.owner_id == owner_id)

    # Execute queries
    total_customers = db.execute(q_cust).scalar() or 0
    total_opportunities = db.execute(q_opp).scalar() or 0
    total_activities = db.execute(q_act).scalar() or 0
    total_revenue_won = db.execute(q_rev_won).scalar() or 0.0
    active_pipeline_value = db.execute(q_pipe_val).scalar() or 0.0
    
    won_count = db.execute(q_won_count).scalar() or 0
    closed_count = db.execute(q_closed_count).scalar() or 0
    
    win_rate = (won_count / closed_count * 100) if closed_count > 0 else 0.0

    return {
        "total_customers": total_customers,
        "total_opportunities": total_opportunities,
        "total_activities": total_activities,
        "total_revenue_won": total_revenue_won,
        "active_pipeline_value": active_pipeline_value,
        "win_rate_percentage": round(win_rate, 2)
    }

def get_monthly_revenue(db: Session, owner_id: int = None) -> list:
    # SQLite strftime for grouping by YYYY-MM
    stmt = select(
        func.strftime('%Y-%m', Opportunity.updated_at).label("month"),
        func.sum(Opportunity.deal_value).label("revenue")
    ).where(Opportunity.stage == "Won")
    
    if owner_id:
        stmt = stmt.where(Opportunity.owner_id == owner_id)
        
    stmt = stmt.group_by("month").order_by("month")
    
    results = db.execute(stmt).all()
    return [{"month": r.month or "Unknown", "revenue": r.revenue or 0.0} for r in results]

def get_pipeline_distribution(db: Session, owner_id: int = None) -> list:
    stmt = select(
        Opportunity.stage,
        func.count(Opportunity.id).label("count")
    )
    if owner_id:
        stmt = stmt.where(Opportunity.owner_id == owner_id)
        
    stmt = stmt.group_by(Opportunity.stage)
    
    results = db.execute(stmt).all()
    return [{"name": r.stage, "value": r.count} for r in results]

def get_activity_metrics(db: Session, owner_id: int = None) -> list:
    stmt = select(
        Activity.status,
        func.count(Activity.id).label("count")
    )
    if owner_id:
        stmt = stmt.where(Activity.user_id == owner_id)
        
    stmt = stmt.group_by(Activity.status)
    
    results = db.execute(stmt).all()
    return [{"name": r.status, "value": r.count} for r in results]

def get_rep_performance(db: Session) -> list:
    # Only Managers and Executives should typically see this, no owner_id filter needed as it compares reps
    stmt = select(
        User.full_name,
        func.count(Opportunity.id).label("total_deals"),
        func.sum(case((Opportunity.stage == "Won", 1), else_=0)).label("won_deals"),
        func.sum(case((Opportunity.stage == "Won", Opportunity.deal_value), else_=0.0)).label("revenue_generated")
    ).outerjoin(Opportunity, User.id == Opportunity.owner_id).group_by(User.id)
    
    results = db.execute(stmt).all()
    
    performance_list = []
    for r in results:
        conversion = (r.won_deals / r.total_deals * 100) if r.total_deals and r.total_deals > 0 else 0.0
        performance_list.append({
            "rep_name": r.full_name or "Unknown Rep",
            "total_deals_assigned": r.total_deals or 0,
            "won_deals": r.won_deals or 0,
            "revenue_generated": r.revenue_generated or 0.0,
            "conversion_rate": round(conversion, 2)
        })
        
    return performance_list
