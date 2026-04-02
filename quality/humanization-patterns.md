# Humanization Patterns — 24 Anti-AI Rules

> Applied by /broker-writer during HUMANIZE step.
> Checked by /broker-checker during Humanization Check.
> Source: AI detection research, ForexBrokers/BrokerChooser analysis, ZeroGPT/GPTZero findings.

---

## Category A: Generic Transitions (AVOID — replace or remove)

1. **"Furthermore"** → remove or replace with specific connector tied to content
2. **"Moreover"** → remove
3. **"It's worth noting that"** → remove (just state the fact)
4. **"In addition"** → remove or merge sentences
5. **"Additionally"** → remove
6. **"Notably"** → remove
7. **"Importantly"** → remove (let reader decide importance)

## Category B: AI Summary Formulas (AVOID)

8. **"In conclusion, {X} offers a comprehensive..."** → free narrative, no formula
9. **"Overall, {X} is a great/excellent choice for..."** → specific recommendation with reasons
10. **"{X} stands out as..."** → specific facts instead
11. **"Whether you're a beginner or experienced..."** → pick one audience per section
12. **"With its robust/comprehensive/cutting-edge..."** → replace with specific metrics

## Category C: Adjective Lists (AVOID)

13. **Triple/quad adjectives:** "robust, comprehensive, and cutting-edge" → one concrete fact
14. **Superlatives without evidence:** "best-in-class", "industry-leading" → specific ranking or metric
15. **Vague qualifiers:** "very", "extremely", "highly" → concrete numbers

## Category D: Sentence Structure (APPLY)

16. **Vary length:** alternate short (5-8 words) and long (20-30 words) sentences
17. **Start differently:** not every sentence with subject-verb. Use "But", "Still", questions, fragments
18. **Imperfections:** occasional conversational tone, parenthetical asides, minor style quirks
19. **Contractions:** use "don't", "it's", "won't" naturally (not in every sentence)

## Category E: Data Specificity (APPLY)

20. **Numbers from input.json:** "low fees" → "EUR/USD spread from 0.6 pips, no commission on standard account"
21. **Comparisons with data:** "competitive pricing" → "0.6 pips vs Saxo Bank's 0.8 pips"
22. **Regulatory specifics:** "well-regulated" → "FCA-regulated (license #195355), Tier 1"

## Category F: Expert Voice (APPLY in Expert Take)

23. **First-person:** "I tested...", "In my experience...", "What impressed me..."
24. **Specific experience:** "After 3 months trading forex on IG's proprietary platform, I found..." — not generic praise
