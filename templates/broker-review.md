# Broker Review Template — 18 Sections

> Source: ForexBrokers.com, BrokerChooser.com, NerdWallet analysis
> See: docs/research/broker-review-seo-research.md

---

## Section 1: Hero
- **H1:** {broker_name} Review {year}: Pros & Cons
- Author attribution: {expert_name}, {expert_credentials}
- Date: "Updated {month} {year}"
- Risk disclaimer: "CFDs are complex instruments and come with a high risk of losing money rapidly due to leverage. {X}% of retail investor accounts lose money when trading CFDs with this provider. You should consider whether you understand how CFDs work and whether you can afford to take the high risk of losing your money."
- Length: 50-100 words

## Section 2: Verdict Box
- Overall rating: {ratings.overall}/5 stars
- Sub-ratings table (fees, platforms, research, mobile, education, safety)
- Key metrics: min deposit, typical spread EUR/USD, total instruments
- CTA placeholder: `[CTA: Visit {broker_name}]`
- Length: 100-150 words

## Section 3: Table of Contents
- Auto-generated anchor links to all H2 sections
- No word count

## Section 4: Pros & Cons + Key Takeaways
- Pros: bullet list from {pros}
- Cons: bullet list from {cons}
- Key Takeaways: 4-6 expert bullet points summarizing the review
- Length: 150-200 words

## Section 5: Trust & Safety
- H2: "Is {broker_name} Safe?"
- Trust rating: {ratings.safety}/5
- Regulator table: name, tier (1/2/3), country, license number
- Narrative: what tier-1 regulation means, investor protection
- Source: {regulators} from input.json
- Length: 300-500 words

## Section 6: Fees & Pricing
- H2: "{broker_name} Fees"
- Spread data: EUR/USD, GBP/USD from {spreads}
- Commission: {commission_per_trade}
- Inactivity fee: {inactivity_fee}
- Comparison table: {broker_name} vs 2 competitors from {competitors}
- CTA placeholder: `[CTA: Open Account]`
- Length: 400-600 words

## Section 7: Trading Platforms + Expert Take
- H2: "Trading Platforms"
- Narrative: available platforms from {platforms}
- Feature highlights per platform
- **Expert Take blockquote:**
  > "{expert_take}" — {expert_name}, {expert_credentials}
- Length: 300-500 words

## Section 8: Mobile App
- H2: "Mobile App"
- Platform availability (iOS/Android)
- App store ratings from {platforms.mobile_app_rating_ios/android} if available
- Key features narrative
- Length: 200-300 words

## Section 9: Product Selection
- H2: "What Can You Trade?"
- Table: asset class | available | count
- From {products}: forex, stocks, ETFs, options, futures, CFDs, crypto
- Length: 200-400 words

## Section 10: Research & Education
- H2: "Research & Education"
- Rating: {ratings.research}/5 and {ratings.education}/5
- Available research tools, educational content
- Length: 200-300 words

## Section 11: Account Opening
- H2: "How to Open an Account"
- Numbered steps from {account_opening_steps} if available
- Minimum deposit: {minimum_deposit}
- Verification requirements (general)
- Length: 150-200 words

## Section 12: Competitor Comparison
- H2: "How {broker_name} Compares"
- Table: {broker_name} vs each competitor from {competitors}
- Columns: spreads, min deposit, instruments, regulators, overall rating
- Data ONLY from input.json competitors block — never invent
- Length: 200-300 words

## Section 13: Best For
- H2: "Who Is {broker_name} Best For?"
- From {best_for}: persona + reason
- Also: "Who should avoid" section
- Length: 150-250 words

## Section 14: Final Verdict
- H2: "Final Verdict"
- Free narrative summarizing the review
- NO "In conclusion, {X} offers..." formula
- Honest assessment with specific recommendations
- CTA placeholder: `[CTA: Get Started with {broker_name}]`
- Length: 200-300 words

## Section 15: Star Ratings Summary
- Consolidated table of all sub-ratings from {ratings}
- Length: 50-100 words

## Section 16: FAQ
- H2: "Frequently Asked Questions"
- ≥5 questions with answers
- Schema.org FAQPage JSON-LD
- Questions should target long-tail keywords from brief
- Length: 300-500 words

## Section 17: Methodology
- H2: "How We Test"
- Explain review methodology (account opening, testing period, criteria)
- Transparency statement
- Length: 100-200 words

## Section 18: Editorial Team
- Author: {expert_name}, {expert_credentials}
- Editor credit
- "Not financial advice" compliance disclaimer
- Length: 100-150 words
