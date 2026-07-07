from datetime import datetime, timezone

from shopee_marketing_ai.campaigns.models import Campaign
from shopee_marketing_ai.campaigns.scheduler import is_active


def _campaign(status, start, end):
    return Campaign(
        name="Test Campaign",
        status=status,
        start_time=start,
        end_time=end,
        discount_percent=10.0,
        product_ids=["sku-1"],
    )


def test_is_active_true_when_scheduled_and_within_window():
    campaign = _campaign(
        "scheduled",
        datetime(2026, 7, 1, tzinfo=timezone.utc),
        datetime(2026, 7, 31, tzinfo=timezone.utc),
    )

    assert is_active(campaign, datetime(2026, 7, 15, tzinfo=timezone.utc)) is True


def test_is_active_false_before_start():
    campaign = _campaign(
        "scheduled",
        datetime(2026, 7, 10, tzinfo=timezone.utc),
        datetime(2026, 7, 31, tzinfo=timezone.utc),
    )

    assert is_active(campaign, datetime(2026, 7, 1, tzinfo=timezone.utc)) is False


def test_is_active_false_after_end():
    campaign = _campaign(
        "live",
        datetime(2026, 7, 1, tzinfo=timezone.utc),
        datetime(2026, 7, 10, tzinfo=timezone.utc),
    )

    assert is_active(campaign, datetime(2026, 7, 15, tzinfo=timezone.utc)) is False


def test_is_active_false_when_draft_status():
    campaign = _campaign(
        "draft",
        datetime(2026, 7, 1, tzinfo=timezone.utc),
        datetime(2026, 7, 31, tzinfo=timezone.utc),
    )

    assert is_active(campaign, datetime(2026, 7, 15, tzinfo=timezone.utc)) is False
