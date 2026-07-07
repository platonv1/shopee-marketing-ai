import hashlib
import hmac
import time
from collections.abc import Callable

import httpx

BASE_URL = "https://partner.shopeemobile.com"
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 1.0


class ShopeeClient:
    def __init__(
        self,
        *,
        partner_id: str,
        partner_key: str,
        shop_id: str,
        access_token: str = "",
        base_url: str = BASE_URL,
        transport: httpx.BaseTransport | None = None,
        max_retries: int = MAX_RETRIES,
        min_request_interval: float = 0.0,
        sleep_fn: Callable[[float], None] = time.sleep,
        now_fn: Callable[[], float] = time.monotonic,
    ):
        if max_retries < 1:
            raise ValueError("max_retries must be at least 1")
        self.partner_id = partner_id
        self.partner_key = partner_key
        self.shop_id = shop_id
        self.access_token = access_token
        self.max_retries = max_retries
        self.min_request_interval = min_request_interval
        self._sleep = sleep_fn
        self._now = now_fn
        self._last_request_time: float | None = None
        self._client = httpx.Client(base_url=base_url, transport=transport)

    def _rate_limit(self) -> None:
        now = self._now()
        if self._last_request_time is not None:
            elapsed = now - self._last_request_time
            if elapsed < self.min_request_interval:
                self._sleep(self.min_request_interval - elapsed)
        self._last_request_time = now

    def _sign(self, path: str, timestamp: int) -> str:
        base_string = f"{self.partner_id}{path}{timestamp}{self.access_token}{self.shop_id}"
        return hmac.new(self.partner_key.encode(), base_string.encode(), hashlib.sha256).hexdigest()

    def get(self, path: str, params: dict) -> dict:
        self._rate_limit()
        timestamp = int(time.time())
        request_params = {
            **params,
            "partner_id": self.partner_id,
            "shop_id": self.shop_id,
            "timestamp": timestamp,
            "sign": self._sign(path, timestamp),
        }
        for attempt in range(1, self.max_retries + 1):
            response = self._client.get(path, params=request_params)
            if response.status_code < 500:
                response.raise_for_status()
                return response.json()
            if attempt == self.max_retries:
                response.raise_for_status()
            self._sleep(RETRY_BACKOFF_SECONDS)

    def get_products(self, *, page_size: int = 50, offset: int = 0) -> dict:
        return self.get(
            "/api/v2/product/get_item_list",
            params={"page_size": page_size, "offset": offset, "item_status": "NORMAL"},
        )
