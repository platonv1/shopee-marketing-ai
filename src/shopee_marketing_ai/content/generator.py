from pathlib import Path
from string import Template
from typing import Any

DEFAULT_MODEL = "claude-sonnet-5"
DEFAULT_MAX_TOKENS = 1024


def render_template(template_path: Path, **context: str) -> str:
    template_text = template_path.read_text()
    return Template(template_text).substitute(**context)


def generate_content(
    client: Any,
    prompt: str,
    *,
    system: str = "",
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
