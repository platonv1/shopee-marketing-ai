from datetime import datetime, timezone

from shopee_marketing_ai.analytics.models import OrderRecord


def test_order_record_holds_product_quantity_revenue_and_timestamp():
    order = OrderRecord(
        product_id="sku-1",
        quantity=2,
        revenue=40.0,
        timestamp=datetime(2026, 7, 11, tzinfo=timezone.utc),
    )

    assert order.product_id == "sku-1"
    assert order.quantity == 2
    assert order.revenue == 40.0
    assert order.timestamp == datetime(2026, 7, 11, tzinfo=timezone.utc)
