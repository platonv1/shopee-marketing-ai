from datetime import datetime

from shopee_marketing_ai.campaigns.models import Campaign


def render_campaign_report(campaign: Campaign, metrics: dict, *, generated_at: datetime) -> str:
    return (
        "---\n"
        f"date: {generated_at.date().isoformat()}\n"
        "author: claude\n"
        "status: draft\n"
        "---\n\n"
        f"# Campaign Performance: {campaign.name}\n\n"
        f"- Units sold: {metrics['units_sold']}\n"
        f"- Revenue: ${metrics['revenue']:.2f}\n"
    )
