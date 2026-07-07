from types import SimpleNamespace

from shopee_marketing_ai.content.generator import generate_content, render_template


def test_render_template_substitutes_variables(tmp_path):
    template_path = tmp_path / "template.md"
    template_path.write_text("Write ad copy for $product_name priced at $price.")

    result = render_template(template_path, product_name="Wireless Earbuds", price="$29.99")

    assert result == "Write ad copy for Wireless Earbuds priced at $29.99."


class FakeMessages:
    def __init__(self, response_text: str):
        self.response_text = response_text
        self.received_kwargs: dict | None = None

    def create(self, **kwargs):
        self.received_kwargs = kwargs
        return SimpleNamespace(content=[SimpleNamespace(text=self.response_text)])


class FakeAnthropicClient:
    def __init__(self, response_text: str):
        self.messages = FakeMessages(response_text)


def test_generate_content_sends_prompt_and_returns_text():
    client = FakeAnthropicClient("Grab yours before the flash sale ends!")

    result = generate_content(
        client,
        "Write ad copy for Wireless Earbuds priced at $29.99.",
        system="You are a Shopee marketing copywriter.",
    )

    assert result == "Grab yours before the flash sale ends!"
    assert client.messages.received_kwargs["messages"] == [
        {"role": "user", "content": "Write ad copy for Wireless Earbuds priced at $29.99."}
    ]
    assert client.messages.received_kwargs["system"] == "You are a Shopee marketing copywriter."
