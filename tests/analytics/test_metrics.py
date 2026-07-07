from datetime import datetime, timezone

from shopee_marketing_ai.analytics.metrics import campaign_performance
from shopee_marketing_ai.analytics.models import OrderRecord
from shopee_marketing_ai.campaigns.models import Campaign


def _campaign():
    return Campaign(
        name="July Flash Sale",
        status="live",
        start_time=datetime(2026, 7, 10, tzinfo=timezone.utc),
        end_time=datetime(2026, 7, 12, tzinfo=timezone.utc),
        discount_percent=20.0,
        product_ids=["sku-1", "sku-2"],
    )


def test_campaign_performance_sums_only_matching_orders():
    campaign = _campaign()
    orders = [
        OrderRecord(
            product_id="sku-1", quantity=2, revenue=40.0,
            timestamp=datetime(2026, 7, 11, tzinfo=timezone.utc),
        ),
        OrderRecord(
            product_id="sku-2", quantity=1, revenue=15.0,
            timestamp=datetime(2026, 7, 11, 12, tzinfo=timezone.utc),
        ),
        # outside the campaign window
        OrderRecord(
            product_id="sku-1", quantity=5, revenue=100.0,
            timestamp=datetime(2026, 7, 20, tzinfo=timezone.utc),
        ),
        # not one of the campaign's products
        OrderRecord(
            product_id="sku-3", quantity=3, revenue=30.0,
            timestamp=datetime(2026, 7, 11, tzinfo=timezone.utc),
        ),
    ]

    result = campaign_performance(campaign, orders)

    assert result == {"units_sold": 3, "revenue": 55.0}
