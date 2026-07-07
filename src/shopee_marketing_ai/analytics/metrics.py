from shopee_marketing_ai.analytics.models import OrderRecord
from shopee_marketing_ai.campaigns.models import Campaign


def campaign_performance(campaign: Campaign, orders: list[OrderRecord]) -> dict:
    matching = [
        order
        for order in orders
        if order.product_id in campaign.product_ids
        and campaign.start_time <= order.timestamp <= campaign.end_time
    ]
    return {
        "units_sold": sum(order.quantity for order in matching),
        "revenue": sum(order.revenue for order in matching),
    }
