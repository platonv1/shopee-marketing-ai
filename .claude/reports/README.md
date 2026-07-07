# Reports

Generated with `shopee_marketing_ai.analytics.reports.render_campaign_report` (and
similar renderers as they're added), each report is Markdown with front matter
(`date`, `author: claude`, `status`) per the output standards in `../CLAUDE.md`.

- `campaign-performance/` — one report per campaign, named `<campaign-name>-<date>.md`
  (metrics from `shopee_marketing_ai.analytics.metrics.campaign_performance`)
- `weekly/` — rolled-up summaries across campaigns active in a given week, named
  `<week-start-date>-weekly-summary.md`

Reports are informational drafts (`status: draft` until a human reviews them) — see
`../playbooks/weekly-performance-report.md` for how they're produced.
