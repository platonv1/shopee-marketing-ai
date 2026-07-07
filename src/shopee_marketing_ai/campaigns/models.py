from datetime import datetime
from typing import Literal

from pydantic import BaseModel

CampaignStatus = Literal["draft", "scheduled", "live", "archived"]


class Campaign(BaseModel):
    name: str
    status: CampaignStatus = "draft"
    start_time: datetime
    end_time: datetime
    discount_percent: float
    product_ids: list[str]
    notes: str = ""
