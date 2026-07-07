#!/usr/bin/env python3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

from shopee_marketing_ai.config import Settings  # noqa: E402
from shopee_marketing_ai.data import save_json  # noqa: E402
from shopee_marketing_ai.integrations.shopee_api import ShopeeClient  # noqa: E402

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "products.json"


def main() -> None:
    settings = Settings()
    client = ShopeeClient(
        partner_id=settings.shopee_partner_id,
        partner_key=settings.shopee_partner_key,
        shop_id=settings.shopee_shop_id,
    )
    data = client.get_products()
    save_json(data, OUTPUT_PATH)
    print(f"Saved products to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
