from shopee_marketing_ai.config import Settings


def test_settings_loads_from_env_vars(monkeypatch):
    monkeypatch.setenv("SHOPEE_PARTNER_ID", "12345")
    monkeypatch.setenv("SHOPEE_PARTNER_KEY", "secret-key")
    monkeypatch.setenv("SHOPEE_SHOP_ID", "67890")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")

    settings = Settings(_env_file=None)

    assert settings.shopee_partner_id == "12345"
    assert settings.shopee_partner_key == "secret-key"
    assert settings.shopee_shop_id == "67890"
    assert settings.anthropic_api_key == "sk-ant-test"
