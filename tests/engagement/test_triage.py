import pytest

from shopee_marketing_ai.engagement.triage import needs_escalation


@pytest.mark.parametrize(
    "message",
    [
        "Can I get a refund for this order? It's the wrong size.",
        "This item arrived broken and I want a replacement.",
        "I'm going to file a complaint with Shopee support.",
        "This looks like a scam, I want my money back.",
    ],
)
def test_needs_escalation_true_for_sensitive_messages(message):
    assert needs_escalation(message) is True


@pytest.mark.parametrize(
    "message",
    [
        "What colors does this come in?",
        "Does this ship to Cebu?",
        "How long is the warranty?",
    ],
)
def test_needs_escalation_false_for_benign_questions(message):
    assert needs_escalation(message) is False
