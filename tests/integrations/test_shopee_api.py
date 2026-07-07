import hashlib
import hmac

import httpx
import pytest

from shopee_marketing_ai.integrations.shopee_api import ShopeeClient


def test_get_sends_request_and_returns_json_response():
    captured_requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured_requests.append(request)
        return httpx.Response(200, json={"response": {"item": []}})

    client = ShopeeClient(
        partner_id="12345",
        partner_key="secret",
        shop_id="67890",
        transport=httpx.MockTransport(handler),
    )

    result = client.get("/api/v2/product/get_item_list", params={"page_size": 50})

    assert result == {"response": {"item": []}}
    assert len(captured_requests) == 1
    request = captured_requests[0]
    assert request.url.params["partner_id"] == "12345"
    assert request.url.params["shop_id"] == "67890"
    assert request.url.params["page_size"] == "50"
    assert "sign" in request.url.params
    assert "timestamp" in request.url.params


def test_get_retries_on_server_error_then_succeeds():
    attempts = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        attempts["count"] += 1
        if attempts["count"] < 3:
            return httpx.Response(500, json={"error": "server_error"})
        return httpx.Response(200, json={"response": {"item": []}})

    client = ShopeeClient(
        partner_id="12345",
        partner_key="secret",
        shop_id="67890",
        transport=httpx.MockTransport(handler),
        sleep_fn=lambda seconds: None,
    )

    result = client.get("/api/v2/product/get_item_list", params={})

    assert result == {"response": {"item": []}}
    assert attempts["count"] == 3


def test_get_raises_after_max_retries_exhausted():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "server_error"})

    client = ShopeeClient(
        partner_id="12345",
        partner_key="secret",
        shop_id="67890",
        transport=httpx.MockTransport(handler),
        sleep_fn=lambda seconds: None,
    )

    with pytest.raises(httpx.HTTPStatusError):
        client.get("/api/v2/product/get_item_list", params={})


def test_get_enforces_minimum_interval_between_requests():
    clock = iter([100.0, 100.2, 100.9])
    sleeps = []

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"response": {}})

    client = ShopeeClient(
        partner_id="12345",
        partner_key="secret",
        shop_id="67890",
        transport=httpx.MockTransport(handler),
        min_request_interval=1.0,
        now_fn=lambda: next(clock),
        sleep_fn=lambda seconds: sleeps.append(seconds),
    )

    client.get("/api/v2/product/get_item_list", params={})
    client.get("/api/v2/product/get_item_list", params={})

    assert sleeps == [pytest.approx(0.8)]


def test_get_does_not_sleep_when_interval_already_elapsed():
    clock = iter([100.0, 101.5])
    sleeps = []

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"response": {}})

    client = ShopeeClient(
        partner_id="12345",
        partner_key="secret",
        shop_id="67890",
        transport=httpx.MockTransport(handler),
        min_request_interval=1.0,
        now_fn=lambda: next(clock),
        sleep_fn=lambda seconds: sleeps.append(seconds),
    )

    client.get("/api/v2/product/get_item_list", params={})
    client.get("/api/v2/product/get_item_list", params={})

    assert sleeps == []


def test_shopee_client_rejects_non_positive_max_retries():
    with pytest.raises(ValueError, match="max_retries"):
        ShopeeClient(
            partner_id="12345",
            partner_key="secret",
            shop_id="67890",
            max_retries=0,
        )


def test_get_products_requests_item_list_endpoint():
    captured_requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured_requests.append(request)
        return httpx.Response(200, json={"response": {"item": []}})

    client = ShopeeClient(
        partner_id="12345",
        partner_key="secret",
        shop_id="67890",
        transport=httpx.MockTransport(handler),
    )

    result = client.get_products(page_size=20, offset=40)

    assert result == {"response": {"item": []}}
    request = captured_requests[0]
    assert request.url.path == "/api/v2/product/get_item_list"
    assert request.url.params["page_size"] == "20"
    assert request.url.params["offset"] == "40"
    assert request.url.params["item_status"] == "NORMAL"


def test_sign_matches_shopee_hmac_sha256_scheme():
    client = ShopeeClient(
        partner_id="12345",
        partner_key="secret",
        shop_id="67890",
        access_token="token",
    )

    signature = client._sign("/api/v2/product/get_item_list", timestamp=1000)

    base_string = "12345/api/v2/product/get_item_list1000token67890"
    expected = hmac.new(b"secret", base_string.encode(), hashlib.sha256).hexdigest()
    assert signature == expected
