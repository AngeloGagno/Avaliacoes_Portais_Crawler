from pydantic import BaseModel
from typing import Optional
from datetime import date

class Validator_Airbnb(BaseModel):
    accommodation_id: int
    accommodation_name: str
    airbnb_account_id: Optional[int] = None
    accommodation_link: Optional[str] = None
    channel_name: Optional[str] = None
    local_status: bool
    publishment_status: str
    alert: int
    sync_alert: Optional[str] = None
    rejection_alert: bool
    warning_alert: Optional[str] = None
    review_count: Optional[float] = None
    review_value: Optional[float] = None
    cleanliness_value: Optional[float] = None
    location_value: Optional[float] = None
    truthfulness_value: Optional[float] = None
    checkin_value: Optional[float] = None
    communication_value: Optional[float] = None
    scrap_data: Optional[date] = None