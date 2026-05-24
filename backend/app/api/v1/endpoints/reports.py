from datetime import datetime
from typing import Any, Optional
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.customer import Customer
from app.models.opportunity import Opportunity
from app.models.activity import Activity
from app.services import report_generator
from app.crud import crud_analytics

router = APIRouter()

@router.get("/customers/csv", response_class=StreamingResponse)
def export_customers_csv(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Download a CSV file containing customer data.
    Respects Role-Based Access Control and Date filters.
    """
    stmt = select(Customer)
    if current_user.role not in ["sales_manager", "executive", "admin"]:
        stmt = stmt.where(Customer.owner_id == current_user.id)
        
    if start_date:
        stmt = stmt.where(Customer.created_at >= start_date)
    if end_date:
        stmt = stmt.where(Customer.created_at <= end_date)
        
    customers = db.execute(stmt).scalars().all()
    
    headers = ["ID", "Company Name", "Contact Name", "Email", "Phone", "Segment", "Created At"]
    rows = [
        [c.id, c.company_name, c.contact_name, c.email, c.phone or "N/A", c.segment or "N/A", c.created_at.strftime("%Y-%m-%d")]
        for c in customers
    ]
    
    csv_buffer = report_generator.export_to_csv(headers, rows)
    return StreamingResponse(
        csv_buffer, 
        media_type="text/csv", 
        headers={"Content-Disposition": f"attachment; filename=customers_export_{datetime.now().strftime('%Y%m%d')}.csv"}
    )

@router.get("/opportunities/csv", response_class=StreamingResponse)
def export_opportunities_csv(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Download a CSV file containing pipeline opportunities.
    """
    stmt = select(Opportunity)
    if current_user.role not in ["sales_manager", "executive", "admin"]:
        stmt = stmt.where(Opportunity.owner_id == current_user.id)
        
    if start_date:
        stmt = stmt.where(Opportunity.created_at >= start_date)
    if end_date:
        stmt = stmt.where(Opportunity.created_at <= end_date)
        
    opportunities = db.execute(stmt).scalars().all()
    
    headers = ["ID", "Title", "Deal Value", "Stage", "Forecast Category", "Created At"]
    rows = [
        [o.id, o.title, f"${o.deal_value:,.2f}", o.stage, o.forecast_category, o.created_at.strftime("%Y-%m-%d")]
        for o in opportunities
    ]
    
    csv_buffer = report_generator.export_to_csv(headers, rows)
    return StreamingResponse(
        csv_buffer, 
        media_type="text/csv", 
        headers={"Content-Disposition": f"attachment; filename=opportunities_export_{datetime.now().strftime('%Y%m%d')}.csv"}
    )

@router.get("/activities/csv", response_class=StreamingResponse)
def export_activities_csv(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Download a CSV file containing activity logs.
    """
    stmt = select(Activity)
    if current_user.role not in ["sales_manager", "executive", "admin"]:
        stmt = stmt.where(Activity.user_id == current_user.id)
        
    if start_date:
        stmt = stmt.where(Activity.created_at >= start_date)
    if end_date:
        stmt = stmt.where(Activity.created_at <= end_date)
        
    activities = db.execute(stmt).scalars().all()
    
    headers = ["ID", "Type", "Status", "Priority", "Due Date", "Created At"]
    rows = [
        [
            a.id, 
            a.activity_type, 
            a.status, 
            a.priority, 
            a.due_date.strftime("%Y-%m-%d") if a.due_date else "N/A", 
            a.created_at.strftime("%Y-%m-%d")
        ]
        for a in activities
    ]
    
    csv_buffer = report_generator.export_to_csv(headers, rows)
    return StreamingResponse(
        csv_buffer, 
        media_type="text/csv", 
        headers={"Content-Disposition": f"attachment; filename=activities_export_{datetime.now().strftime('%Y%m%d')}.csv"}
    )

@router.get("/revenue/pdf", response_class=StreamingResponse)
def export_revenue_pdf(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Generate and download a highly formatted PDF Summary for Revenue.
    Reuses existing Analytics CRUD aggregates.
    """
    owner_id = current_user.id if current_user.role not in ["sales_manager", "executive", "admin"] else None
    revenue_data = crud_analytics.get_monthly_revenue(db=db, owner_id=owner_id)
    
    headers = ["Month", "Revenue Generated"]
    rows = [[data["month"], f"${data['revenue']:,.2f}"] for data in revenue_data]
    
    pdf_buffer = report_generator.export_to_pdf("Monthly Revenue Report", headers, rows)
    return StreamingResponse(
        pdf_buffer, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename=revenue_report_{datetime.now().strftime('%Y%m%d')}.pdf"}
    )

@router.get("/pipeline/pdf", response_class=StreamingResponse)
def export_pipeline_pdf(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Generate and download a formatted PDF Summary for Pipeline Stage distribution.
    """
    owner_id = current_user.id if current_user.role not in ["sales_manager", "executive", "admin"] else None
    pipeline_data = crud_analytics.get_pipeline_distribution(db=db, owner_id=owner_id)
    
    headers = ["Pipeline Stage", "Total Deals"]
    rows = [[data["name"], str(data["value"])] for data in pipeline_data]
    
    pdf_buffer = report_generator.export_to_pdf("Pipeline Distribution Report", headers, rows)
    return StreamingResponse(
        pdf_buffer, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename=pipeline_report_{datetime.now().strftime('%Y%m%d')}.pdf"}
    )
