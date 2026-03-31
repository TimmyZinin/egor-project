#!/usr/bin/env python3
"""
Expert Hunter — SCAN module.
Searches for finance expert candidates via Google site:linkedin.com queries.
Outputs raw candidate list for enrichment and scoring.

Usage:
    python3 scan.py [--niche forex|stocks|crypto|personal_finance] [--output candidates_raw.json]
"""

import json
import subprocess
import sys
import re
from datetime import datetime, timezone


QUERIES = {
    "forex": [
        'site:linkedin.com/in "CFA" "forex" ("analyst" OR "trader" OR "strategist")',
        'site:linkedin.com/in "forex" "author" ("Forbes" OR "Bloomberg" OR "CNBC")',
        'site:linkedin.com/in "forex" "certified" ("planner" OR "advisor")',
    ],
    "stocks": [
        'site:linkedin.com/in "CFA" "equity" ("analyst" OR "portfolio manager")',
        'site:linkedin.com/in "investment" "author" ("Forbes" OR "Investopedia" OR "Motley Fool")',
        'site:linkedin.com/in "stock" "CFA charterholder" ("writer" OR "contributor")',
    ],
    "crypto": [
        'site:linkedin.com/in "crypto" "CFA" ("analyst" OR "researcher")',
        'site:linkedin.com/in "blockchain" "finance" ("author" OR "contributor")',
        'site:linkedin.com/in "digital assets" ("CFA" OR "CFP") ("writer" OR "analyst")',
    ],
    "personal_finance": [
        'site:linkedin.com/in "CFP" "personal finance" ("author" OR "contributor" OR "writer")',
        'site:linkedin.com/in "financial planner" ("Forbes" OR "NerdWallet" OR "Bankrate")',
        'site:linkedin.com/in "CPA" "personal finance" ("columnist" OR "blogger")',
    ],
}


def extract_linkedin_url(text: str) -> str | None:
    """Extract linkedin.com/in/handle from text, including percent-encoded chars."""
    match = re.search(r'https?://(?:www\.)?linkedin\.com/in/[\w%.-]+', text)
    return match.group(0) if match else None


def extract_name_from_snippet(text: str) -> str:
    """Try to extract name from Google snippet of LinkedIn profile."""
    # Common pattern: "First Last - Title - Company | LinkedIn"
    match = re.match(r'^([A-Z][a-z]+ (?:[A-Z]\.? )?[A-Z][a-z]+)', text)
    if match:
        return match.group(1)
    # Fallback: first line before " - " or " | "
    parts = re.split(r' [-|–] ', text)
    if parts:
        name = parts[0].strip()
        if len(name) < 50 and len(name.split()) <= 4:
            return name
    return ""


def parse_search_results(raw_text: str) -> list[dict]:
    """Parse WebSearch-style results into candidate stubs."""
    candidates = []
    seen_urls = set()

    lines = raw_text.split('\n')
    for line in lines:
        url = extract_linkedin_url(line)
        if url and url not in seen_urls:
            seen_urls.add(url)
            # Use this line as the full context (title + snippet on same line)
            name = extract_name_from_snippet(line)
            candidates.append({
                "name": name,
                "linkedin_url": url,
                "scan_source": "google_search",
                "scan_timestamp": datetime.now(timezone.utc).isoformat(),
                "raw_snippet": line.strip()[:500],
            })

    return candidates


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Expert Hunter SCAN")
    parser.add_argument("--niche", choices=list(QUERIES.keys()), default=None,
                       help="Specific niche to scan (default: all)")
    parser.add_argument("--output", default="candidates_raw.json",
                       help="Output file path")
    parser.add_argument("--input-dir", default=None,
                       help="Directory with pre-fetched search results (for offline mode)")
    args = parser.parse_args()

    niches = [args.niche] if args.niche else list(QUERIES.keys())
    all_candidates = []
    seen_urls = set()

    for niche in niches:
        queries = QUERIES.get(niche, [])
        for q in queries:
            print(f"[SCAN] niche={niche} query={q[:60]}...")

            if args.input_dir:
                # Offline mode: read niche-specific files only
                import glob
                niche_pattern = f"{args.input_dir}/*{niche}*.txt"
                for f in glob.glob(niche_pattern):
                    with open(f) as fh:
                        results = parse_search_results(fh.read())
                        for r in results:
                            if r["linkedin_url"] not in seen_urls:
                                r["niche"] = niche
                                seen_urls.add(r["linkedin_url"])
                                all_candidates.append(r)
            else:
                print(f"  [INFO] Run WebSearch for this query in Claude Code, save results to --input-dir")

    # Dedup by URL
    final = []
    seen = set()
    for c in all_candidates:
        if c["linkedin_url"] not in seen:
            seen.add(c["linkedin_url"])
            final.append(c)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)

    print(f"[SCAN] Done. {len(final)} unique candidates -> {args.output}")


if __name__ == "__main__":
    main()
