from datetime import datetime

from pydantic import BaseModel


class OrderRecord(BaseModel):
    product_id: str
    quantity: int
    revenue: float
    timestamp: datetime
