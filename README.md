# Shopee Marketing AI

An AI-assisted marketing system for a Shopee storefront: content/ad generation, campaign management & automation, analytics & reporting, and customer engagement.

## How this project is organized
- `src/shopee_marketing_ai/` — reusable, testable Python package: Shopee Open Platform API integration, content-generation calls, campaign orchestration, analytics.
- `.claude/` — the agentic workspace. Claude Code operates here as the "AI marketing employee," reading `knowledge/` and `playbooks/`, and producing campaign drafts, reports, and session logs. See `.claude/CLAUDE.md` for the full operating handbook.
- `tests/` — pytest suite mirroring the `src/` layout.

## Setup
```bash
uv sync
cp .env.example .env  # then fill in your API credentials
```

## Running
```bash
uv run main.py
```

See `.claude/CLAUDE.md` for how Claude operates this workspace day-to-day.
