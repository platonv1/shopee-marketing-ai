from datetime import datetime, timezone

from shopee_marketing_ai.campaigns.models import Campaign


def test_campaign_defaults_to_draft_status():
    campaign = Campaign(
        name="July Flash Sale",
        start_time=datetime(2026, 7, 10, tzinfo=timezone.utc),
        end_time=datetime(2026, 7, 12, tzinfo=timezone.utc),
        discount_percent=20.0,
        product_ids=["sku-1", "sku-2"],
    )

    assert campaign.status == "draft"
