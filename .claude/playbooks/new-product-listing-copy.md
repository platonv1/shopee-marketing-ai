# Playbook: New Product Listing Copy

## When to use
A new product needs a Shopee listing description, ad copy, and/or a social caption drafted.

## Inputs needed
- Product name, category, price, key features, target audience
- Any flash-sale pricing (original price, sale price, discount %) if applicable
- Product data can come from `.claude/data/raw/products.json` (see `pull_shopee_data.py`) or be provided directly by the human

## Steps
1. Read `.claude/knowledge/brand-guidelines/` for tone/voice before drafting anything.
2. Pick the relevant template(s) from `.claude/templates/`:
   - `product-descriptions/standard-listing.md` — the main listing description
   - `ad-copy/shopee-flash-sale.md` — if this is a promo/flash-sale
   - `social-captions/instagram-caption.md` — if a social post is also needed
3. Render each chosen template with `shopee_marketing_ai.content.generator.render_template`, filling in the product's details.
4. Pass the rendered text as the `prompt` to `shopee_marketing_ai.content.generator.generate_content` (with an Anthropic client) to produce the draft copy.
5. Save the draft(s) as Markdown into the relevant campaign folder under `.claude/campaigns/active/<campaign-name>/`, or directly in the chat if no campaign exists yet, using the output front matter from `CLAUDE.md` (`date`, `author: claude`, `status: draft`).
6. Flag the draft for human review — do not treat generated copy as final or publish it anywhere without explicit approval, per the rules in `CLAUDE.md`.

## Output
One or more Markdown drafts (listing description, ad copy variations, social caption), each marked `status: draft` until a human approves them.
