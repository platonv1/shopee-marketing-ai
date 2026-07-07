from pathlib import Path
from typing import Any

from shopee_marketing_ai.content.generator import generate_content, render_template

SUPPORT_SYSTEM_PROMPT = "You are a Shopee customer support assistant."


def draft_reply(client: Any, template_path: Path, **context: str) -> str:
    prompt = render_template(template_path, **context)
    return generate_content(client, prompt, system=SUPPORT_SYSTEM_PROMPT)
