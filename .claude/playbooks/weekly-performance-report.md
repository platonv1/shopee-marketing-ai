# Playbook: Weekly Performance Report

## When to use
On a regular cadence (e.g. weekly) or when asked, to summarize how campaigns performed.

## Inputs needed
- Order/sales records for the period (`shopee_marketing_ai.analytics.models.OrderRecord`: `product_id`, `quantity`, `revenue`, `timestamp`). Note: there is no Shopee order-data API integration yet (only `get_products` exists in `shopee_marketing_ai.integrations.shopee_api`) — until that's built, get order data from a manual export or ask the human for it.
- The campaigns to report on: read each `brief.yaml` under `.claude/campaigns/active/` (and any in `.claude/campaigns/archive/` that ended during the period) via `shopee_marketing_ai.campaigns.storage.load_campaign`.

## Steps
1. For each campaign in scope, compute its metrics with `shopee_marketing_ai.analytics.metrics.campaign_performance(campaign, orders)`.
2. Render each campaign's metrics with `shopee_marketing_ai.analytics.reports.render_campaign_report`, and save the result to `.claude/reports/campaign-performance/<campaign-name>-<date>.md`.
3. If summarizing a whole week across multiple campaigns, sum the per-campaign `units_sold`/`revenue` results and write a short Markdown summary (same front-matter convention: `date`, `author: claude`, `status: draft`) to `.claude/reports/weekly/<week-start-date>-weekly-summary.md`.
4. Present the report(s) to the human — these are informational drafts (`status: draft`), not live actions, but should still be reviewed before being shared or acted on.

## Output
One Markdown report per campaign in `.claude/reports/campaign-performance/`, and optionally a rolled-up weekly summary in `.claude/reports/weekly/`.
