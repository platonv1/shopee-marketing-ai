from datetime import datetime, timezone

from shopee_marketing_ai.analytics.reports import render_campaign_report
from shopee_marketing_ai.campaigns.models import Campaign


def test_render_campaign_report_includes_front_matter_and_metrics():
    campaign = Campaign(
        name="July Flash Sale",
        status="live",
        start_time=datetime(2026, 7, 10, tzinfo=timezone.utc),
        end_time=datetime(2026, 7, 12, tzinfo=timezone.utc),
        discount_percent=20.0,
        product_ids=["sku-1", "sku-2"],
    )
    metrics = {"units_sold": 3, "revenue": 55.0}

    report = render_campaign_report(
        campaign, metrics, generated_at=datetime(2026, 7, 13, tzinfo=timezone.utc)
    )

    assert "date: 2026-07-13" in report
    assert "author: claude" in report
    assert "status: draft" in report
    assert "July Flash Sale" in report
    assert "Units sold: 3" in report
    assert "Revenue: $55.00" in report
