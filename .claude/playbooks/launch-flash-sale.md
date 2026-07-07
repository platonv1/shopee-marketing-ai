# Playbook: Launch a Flash Sale Campaign

## When to use
A time-boxed discount promotion (flash sale) needs to be set up for one or more products.

## Inputs needed
- Campaign name, start/end time, discount percent, and the list of product IDs on sale
- Product details for the affected items (from `.claude/data/raw/products.json` or provided directly)

## Steps
1. Read `.claude/knowledge/brand-guidelines/` and any relevant `.claude/knowledge/shopee-policies/` notes on flash-sale rules before drafting anything.
2. Build a `Campaign` (`shopee_marketing_ai.campaigns.models.Campaign`) with `status="draft"`, the sale window (`start_time`/`end_time`), `discount_percent`, and `product_ids`.
3. Save it with `shopee_marketing_ai.campaigns.storage.save_campaign` to `.claude/campaigns/active/<campaign-name>/brief.yaml`.
4. Render `.claude/templates/ad-copy/shopee-flash-sale.md` (via `render_template`) for each product, then generate the copy with `generate_content`. Save drafts alongside the brief in the same campaign folder.
5. Present the brief and drafted copy to the human for review. Only after explicit approval:
   - Update the brief's `status` to `scheduled` (or `live` if starting immediately) with `save_campaign`.
   - Use the Shopee API integration to actually apply the discount/promotion — never call a live/write Shopee API endpoint without this approval step having happened.
6. Once `end_time` has passed (`shopee_marketing_ai.campaigns.scheduler.is_active` returns `False`), set `status="archived"` and move the campaign folder from `.claude/campaigns/active/` to `.claude/campaigns/archive/`.

## Output
A `brief.yaml` campaign file plus drafted ad copy, moving through `draft` → `scheduled`/`live` → `archived`, with human approval required before anything goes live.
