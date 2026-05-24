from typing import List, Optional
from pydantic import BaseModel

# 1. Main Dashboard KPIs
class KPIDashboard(BaseModel):
    total_customers: int
    total_opportunities: int
    total_activities: int
    total_revenue_won: float
    active_pipeline_value: float
    win_rate_percentage: float

# 2. Generic Chart Data format for Recharts (BarChart, PieChart)
class ChartDataPoint(BaseModel):
    name: str
    value: float

# 3. Monthly Revenue Trend
class MonthlyRevenue(BaseModel):
    month: str
    revenue: float

# 4. Sales Rep Performance 
class RepPerformance(BaseModel):
    rep_name: str
    total_deals_assigned: int
    won_deals: int
    revenue_generated: float
    conversion_rate: float
