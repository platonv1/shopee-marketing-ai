from datetime import datetime, timezone

from shopee_marketing_ai.campaigns.models import Campaign
from shopee_marketing_ai.campaigns.storage import load_campaign, save_campaign


def test_save_and_load_campaign_round_trip(tmp_path):
    campaign = Campaign(
        name="July Flash Sale",
        status="scheduled",
        start_time=datetime(2026, 7, 10, tzinfo=timezone.utc),
        end_time=datetime(2026, 7, 12, tzinfo=timezone.utc),
        discount_percent=20.0,
        product_ids=["sku-1", "sku-2"],
    )
    path = tmp_path / "active" / "july-flash-sale" / "brief.yaml"

    save_campaign(campaign, path)
    loaded = load_campaign(path)

    assert loaded == campaign
