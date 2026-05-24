from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class DateRangeFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
