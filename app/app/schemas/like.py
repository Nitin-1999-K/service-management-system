from pydantic import BaseModel
from datetime import datetime


class LikeResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    created_datetime: datetime
