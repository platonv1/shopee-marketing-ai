# Campaigns

Each campaign is a folder containing a `brief.yaml` (the `Campaign` schema from
`shopee_marketing_ai.campaigns.models`, read/written via
`shopee_marketing_ai.campaigns.storage.save_campaign`/`load_campaign`) plus any
generated content (ad copy, descriptions, captions) drafted for it.

- `active/<campaign-name>/brief.yaml` — campaigns that are draft, scheduled, or live
- `archive/<campaign-name>/brief.yaml` — campaigns that have ended; move the folder
  here once a campaign's `end_time` has passed

A campaign's `status` field (`draft` → `scheduled` → `live` → `archived`) tracks
where it is in the approval/launch lifecycle — see the rules in `../CLAUDE.md`:
nothing moves to `live` without explicit human approval.
