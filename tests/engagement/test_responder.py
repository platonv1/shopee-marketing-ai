from types import SimpleNamespace

from shopee_marketing_ai.engagement.responder import draft_reply


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


def test_draft_reply_renders_template_and_returns_generated_text(tmp_path):
    template_path = tmp_path / "order-inquiry.md"
    template_path.write_text("Customer asked: $customer_message about order $order_id.")
    client = FakeAnthropicClient("Thanks for reaching out! Your order is on the way.")

    result = draft_reply(
        client,
        template_path,
        customer_message="Where is my order?",
        order_id="SG12345",
    )

    assert result == "Thanks for reaching out! Your order is on the way."
    sent_prompt = client.messages.received_kwargs["messages"][0]["content"]
    assert sent_prompt == "Customer asked: Where is my order? about order SG12345."
