from datetime import datetime

from shopee_marketing_ai.campaigns.models import Campaign

ACTIVE_STATUSES = ("scheduled", "live")


def is_active(campaign: Campaign, now: datetime) -> bool:
    return campaign.status in ACTIVE_STATUSES and campaign.start_time <= now <= campaign.end_time
