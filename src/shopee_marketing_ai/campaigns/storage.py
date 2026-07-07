from pathlib import Path

import yaml

from shopee_marketing_ai.campaigns.models import Campaign


def save_campaign(campaign: Campaign, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(campaign.model_dump(mode="json"), sort_keys=False))


def load_campaign(path: Path) -> Campaign:
    data = yaml.safe_load(path.read_text())
    return Campaign.model_validate(data)
