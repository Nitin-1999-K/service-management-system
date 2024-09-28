from pydantic import BaseModel
from datetime import datetime


class TicketProgressUpdate(BaseModel):
    description: str | None = None
    initiated_datetime: datetime | None = None
    status_code: int | None = (
        None  # -1 => Cancelled 0 => Pending 1 => Initiated 2 => Completed
    )
    priority: int | None = None  # 1 => Low, 2 => Medium, 3 => High
    expected_datetime: datetime | None = None
    completed_datetime: datetime | None = None
