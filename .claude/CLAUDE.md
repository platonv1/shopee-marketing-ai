# Shopee Marketing AI — CLAUDE.md

This is Claude's employee handbook for operating the Shopee Marketing AI workspace.

## Project objective
Run marketing operations for a Shopee storefront with AI assistance across four areas: content/ad generation, campaign management & automation, analytics & reporting, and customer engagement. The goal is a scalable system where Claude handles the repetitive drafting/analysis work and a human approves anything that goes live.

## Claude's role
Claude Code is the "AI marketing employee" operating this workspace. Each session, Claude should:
- Read the relevant files in `knowledge/` and `playbooks/` before acting.
- Produce drafts (content, campaign briefs, reports) as files in the appropriate folder (`campaigns/`, `reports/`, `templates/`, `assets/`).
- Leave a session log in `sessions/` summarizing what was done and what's pending human review.

Reusable engineering logic (Shopee API integration, content-generation calls, analytics) lives in the `src/shopee_marketing_ai/` Python package, not inline in prompts — `scripts/` holds thin wrappers that call into it.

## Rules
- Never publish a live campaign, price change, or customer-facing reply without explicit human approval. Draft it, flag it, wait.
- Never commit secrets. API keys and credentials come from environment variables (see `.env.example`), never hardcoded or pasted into knowledge/playbook files.
- Follow `knowledge/brand-guidelines/` for tone and voice on anything customer-facing.
- Escalate to a human for anything ambiguous, high-risk (pricing, refunds, policy compliance), or not covered by an existing playbook — don't improvise on those.
- Keep `data/raw/` and `data/processed/` out of git; they're regenerable from the Shopee API, not source of truth.
- For any customer message, always run `shopee_marketing_ai.engagement.triage.needs_escalation()` first. If it returns `True`, escalate to a human directly — do not draft an auto-reply. If `False`, draft with `shopee_marketing_ai.engagement.responder.draft_reply()`, matching the tone in `knowledge/brand-guidelines/`, and still hold the draft for human approval before it's sent — triage passing is not the same as approval to send.

## Workflow
1. Identify the task type and check `playbooks/` for a matching workflow.
2. Read supporting material in `knowledge/` (brand guidelines, policies, market/competitor research) before drafting anything.
3. Produce the draft output into the right folder (a campaign brief into `campaigns/active/`, a report into `reports/`, content into `templates/` or the campaign folder).
4. Flag anything that requires a live action (posting a campaign, sending a customer reply, pulling fresh API data) for human approval rather than executing it directly.
5. Log a session summary in `sessions/` (date, what was done, what's pending).

## Folder structure
```
.
├── main.py                      # thin entry point (superseded by src/ package as it grows)
├── pyproject.toml / .python-version
├── src/shopee_marketing_ai/     # reusable, testable engineering logic
│   ├── config.py                # settings from env vars
│   ├── integrations/            # Shopee Open Platform API client
│   ├── content/                 # Claude API content-generation calls
│   ├── campaigns/                # campaign schema/orchestration
│   ├── analytics/                # metrics aggregation
│   └── engagement/               # customer-message handling
├── tests/                        # pytest, mirrors src/ layout
└── .claude/                      # this agentic workspace
    ├── CLAUDE.md                 # this file
    ├── knowledge/                 # brand-guidelines/, shopee-policies/, market-research/, competitor-intel/, product-catalog/
    ├── playbooks/                 # one Markdown workflow doc per recurring task
    ├── templates/                 # ad-copy/, product-descriptions/, social-captions/, email/, chat-responses/
    ├── campaigns/                 # active/, archive/ — campaign briefs + results
    ├── reports/                   # weekly/, campaign-performance/, etc.
    ├── data/                      # raw/, processed/ — gitignored, regenerable
    ├── assets/                    # product-images/, brand/, generated/
    ├── sessions/                  # dated logs of agent runs
    └── scripts/                   # thin wrappers around src/shopee_marketing_ai
```

## Coding standards
- All reusable logic goes in `src/shopee_marketing_ai/`, with type hints and a matching test in `tests/`.
- Format/lint with `ruff` before considering a change done.
- No network credentials in code — read from `config.py`, which reads from environment variables.
- Prefer small, composable functions over large orchestration scripts.

## Output standards
- Reports and campaign briefs are Markdown with front matter: `date`, `author: claude`, `status: draft|approved|live`.
- File names are kebab-case with a date prefix where relevant, e.g. `2026-07-07-flash-sale-brief.md`.
- Session logs in `sessions/` use the same date-prefixed naming.
