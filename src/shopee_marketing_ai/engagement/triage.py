ESCALATION_KEYWORDS = (
    "refund",
    "complaint",
    "scam",
    "fraud",
    "broken",
    "damaged",
    "lawyer",
    "legal",
    "lawsuit",
    "chargeback",
    "money back",
)


def needs_escalation(message: str) -> bool:
    lowered = message.lower()
    return any(keyword in lowered for keyword in ESCALATION_KEYWORDS)
