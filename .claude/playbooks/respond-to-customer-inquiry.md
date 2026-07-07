# Playbook: Respond to a Customer Inquiry

## When to use
A customer has sent a message (order question, product question, complaint, etc.) that needs a response.

## Inputs needed
- The customer's message text
- Relevant order/product context (order ID, product name) if available

## Steps
1. Run `shopee_marketing_ai.engagement.triage.needs_escalation(message)` first, always — before drafting anything.
2. **If it returns `True`** (refund, complaint, damage, legal/fraud language, etc.): do not draft a reply. Escalate directly to a human with the full message and any context. This is a hard stop, not a suggestion — see the rules in `CLAUDE.md`.
3. **If it returns `False`**: read `.claude/knowledge/brand-guidelines/` for tone, then draft a reply with `shopee_marketing_ai.engagement.responder.draft_reply()` using `.claude/templates/chat-responses/order-inquiry.md` (or another chat-responses template if more appropriate).
4. Present the drafted reply to the human for approval. Never send a reply to a real customer without that approval — triage passing only means it was safe to *draft*, not safe to *send*.

## Output
Either an escalation to a human (no draft), or a drafted reply awaiting human approval before sending.
