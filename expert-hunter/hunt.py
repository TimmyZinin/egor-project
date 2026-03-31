#!/usr/bin/env python3
"""
Expert Hunter — Production Entrypoint.

Performs live search for finance experts via WebSearch queries,
enriches from snippets, scores, and exports CSV + JSON.

This is the PRIMARY user-facing flow. No hardcoded candidates.

Usage:
    python3 hunt.py --niche forex --geo US
    python3 hunt.py --niche stocks --geo US
    python3 hunt.py --niche crypto --geo US
    python3 hunt.py --niche personal_finance --geo US
    python3 hunt.py --niche forex --geo UK
    python3 hunt.py --all-niches --geo US

Test mode (uses saved fixtures, no internet):
    python3 hunt.py --niche forex --geo US --test-fixture fixtures/forex_us.json
"""

import argparse
import json
import subprocess
import sys
import os
import re
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from schema import ExpertCandidate, score_candidate, candidates_to_csv, candidates_to_json, shortlist

# --- Query templates ---

QUERY_TEMPLATES = {
    "forex": [
        'site:linkedin.com/in "CFA" ("forex" OR "FX" OR "currency") ("strategist" OR "analyst") {geo}',
        'site:linkedin.com/in "forex" ("author" OR "contributor") ("Bloomberg" OR "Reuters" OR "Forbes") {geo}',
        'site:linkedin.com/in ("currency strategist" OR "FX strategist") CFA {geo}',
    ],
    "stocks": [
        'site:linkedin.com/in "CFA" ("equity" OR "stock") ("analyst" OR "portfolio manager") ("author" OR "contributor") {geo}',
        'site:linkedin.com/in "investment" "CFA charterholder" ("writer" OR "columnist") ("Forbes" OR "Investopedia") {geo}',
        'site:linkedin.com/in "stock" "analyst" ("Bloomberg" OR "Motley Fool" OR "MarketWatch") {geo}',
    ],
    "crypto": [
        'site:linkedin.com/in ("crypto" OR "blockchain") "CFA" ("analyst" OR "researcher") {geo}',
        'site:linkedin.com/in "digital assets" ("CFA" OR "CFP") ("author" OR "contributor") {geo}',
        'site:linkedin.com/in ("bitcoin" OR "cryptocurrency") "finance" ("writer" OR "analyst") {geo}',
    ],
    "personal_finance": [
        'site:linkedin.com/in "CFP" "personal finance" ("author" OR "writer") ("NerdWallet" OR "Bankrate" OR "Forbes") {geo}',
        'site:linkedin.com/in "financial planner" "certified" ("author" OR "contributor") {geo}',
        'site:linkedin.com/in "CPA" "personal finance" ("columnist" OR "writer") {geo}',
    ],
}

GEO_FILTERS = {
    "US": "United States",
    "UK": "United Kingdom",
    "CA": "Canada",
    "AU": "Australia",
}

# --- Credential extraction ---

CREDENTIAL_PATTERNS = {
    "CFA": r'\bCFA\b',
    "CFP": r'\bCFP\b',
    "CPA": r'\bCPA\b',
    "CMT": r'\bCMT\b',
    "FRM": r'\bFRM\b',
    "CAIA": r'\bCAIA\b',
    "Series 7": r'\bSeries\s*7\b',
    "Series 3": r'\bSeries\s*3\b',
    "Series 65": r'\bSeries\s*65\b',
}

MEDIA_TIER1 = ["Bloomberg", "Forbes", "WSJ", "Wall Street Journal"]
MEDIA_TIER2 = ["CNBC", "Reuters", "MarketWatch", "Barron's", "Yahoo Finance"]
MEDIA_TIER3 = ["NerdWallet", "Bankrate", "Investopedia", "Motley Fool", "Kiplinger"]

SENIOR_PATTERNS = [r'\b(Chief|Head|Director|Senior|Lead|Managing|Partner|Professor)\b']


def extract_linkedin_urls(text: str) -> list[str]:
    return list(set(re.findall(r'https?://(?:www\.)?linkedin\.com/in/[\w%.-]+', text)))


def extract_name(text: str, url: str) -> str:
    # Try "Name, Credentials - Title" or "Name - Title" pattern
    # Split on " - " or " | " first, take the left part as name+creds
    name_part = re.split(r'\s+[-|–]\s+', text)[0].strip() if text else ""
    # Remove credential suffixes: CFA, CFP, CPA, CMT, FRM, MBA, PhD, etc.
    name_clean = re.sub(r',?\s*(?:CFA|CFP|CPA|CMT|FRM|CAIA|MBA|Ph\.?D\.?|®).*$', '', name_part).strip()
    if name_clean and len(name_clean.split()) >= 2 and len(name_clean) < 50:
        return name_clean
    # Fallback: extract from URL handle
    handle = url.rstrip('/').split('/')[-1]
    parts = re.sub(r'-\d+$', '', handle).replace('-', ' ').title()
    return parts if len(parts) < 50 else handle


def enrich_candidate(name: str, url: str, snippet: str, niche: str, geo: str) -> dict:
    text = f"{name} {snippet}"

    creds = [c for c, p in CREDENTIAL_PATTERNS.items() if re.search(p, text, re.IGNORECASE)]

    citability = "none"
    for outlet in MEDIA_TIER1:
        if outlet.lower() in text.lower():
            citability = "bloomberg_wsj_forbes"; break
    if citability == "none":
        for outlet in MEDIA_TIER2:
            if outlet.lower() in text.lower():
                citability = "cnbc_reuters"; break
    if citability == "none":
        for outlet in MEDIA_TIER3:
            if outlet.lower() in text.lower():
                citability = "niche_finance_media"; break

    experience = "5_9"
    for pat in SENIOR_PATTERNS:
        if re.search(pat, text):
            experience = "15_19"; break

    company = ""
    # Only extract company from "at Company" pattern — most reliable
    cm = re.search(r'\bat\s+([A-Z][A-Za-z\s&.]+?)(?:\s*[,|]|\s*$)', snippet)
    if cm:
        candidate_company = cm.group(1).strip()[:50]
        # Reject if it looks like a location (2 words or less, no uppercase mid-word)
        if len(candidate_company.split()) >= 2 or any(c.isupper() for c in candidate_company[1:]):
            company = candidate_company

    entity = "none"
    if len(text) > 100 and creds:
        entity = "basic_serp"
    if citability in ("bloomberg_wsj_forbes", "cnbc_reuters"):
        entity = "rich_serp_presence"

    # Normalize geo to scoring keys
    geo_to_scoring = {"US": "US", "UK": "UK", "CA": "Canada", "AU": "Australia"}
    scoring_location = geo_to_scoring.get(geo, "other")

    scoring = {
        "citability": citability,
        "credentials": creds,
        "google_entity": entity,
        "location": scoring_location,
        "native_english": "likely_native" if creds else "unclear",
        "experience_years": experience,
        "linkedin_activity": "5_to_10" if citability != "none" else "1_to_4",
    }
    if creds:
        first_cred = creds[0]
        if first_cred == "CFA":
            scoring["associations"] = "CFA_Institute"
        elif first_cred == "CFP":
            scoring["associations"] = "FPA"
        elif first_cred == "CPA":
            scoring["associations"] = "AICPA"

    return {
        "name": name,
        "linkedin_url": url,
        "primary_role": snippet[:80],
        "company": company,
        "location": geo,
        "niche_tags": niche,
        "credentials_claimed": ", ".join(creds),
        "credentials_verified_or_signal": f"{', '.join(creds)} in snippet; media={citability}" if creds else f"media={citability}",
        "evidence_links": url,
        "scoring": scoring,
    }


def generate_queries(niche: str, geo: str) -> list[str]:
    """Generate search queries for a niche+geo combination."""
    geo_label = GEO_FILTERS.get(geo, geo)
    templates = QUERY_TEMPLATES.get(niche, [])
    return [t.format(geo=geo_label) for t in templates]


def save_queries_file(queries: list[str], niche: str, geo: str, outdir: str = ".") -> str:
    """Save queries to a file for Claude Code operator to execute via WebSearch."""
    path = os.path.join(outdir, f"queries_{niche}_{geo.lower()}.txt")
    with open(path, "w") as f:
        for q in queries:
            f.write(q + "\n")
    return path


def load_search_results(path: str) -> str:
    """Load raw search results text from file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_fixture(path: str) -> list[dict]:
    """Load test fixture JSON."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def hunt(niche: str, geo: str, test_fixture: str = None) -> list[ExpertCandidate]:
    """Main production hunt flow."""
    geo_label = GEO_FILTERS.get(geo, geo)
    print(f"\n[HUNT] niche={niche} geo={geo} ({geo_label})")

    raw_candidates = []
    seen_urls = set()

    if test_fixture:
        print(f"  [MODE] test-fixture: {test_fixture}")
        fixture_data = load_fixture(test_fixture)
        for entry in fixture_data:
            url = entry.get("linkedin_url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                enriched = enrich_candidate(
                    entry.get("name", ""),
                    url,
                    entry.get("raw_snippet", ""),
                    niche,
                    geo,
                )
                raw_candidates.append(enriched)
    else:
        # Production mode: load from raw_search/ JSON artifacts
        base = os.path.dirname(os.path.abspath(__file__))
        raw_dir = os.path.join(base, "raw_search")
        derived_dir = os.path.join(base, "derived_candidates")
        os.makedirs(derived_dir, exist_ok=True)

        # Find latest raw artifact for this niche+geo
        import glob as _glob
        pattern = os.path.join(raw_dir, f"{niche}_{geo.lower()}_*.json")
        raw_files = sorted(_glob.glob(pattern), reverse=True)

        if raw_files:
            raw_file = raw_files[0]  # latest
            print(f"  [MODE] production: loading raw artifact {os.path.basename(raw_file)}")
            with open(raw_file, "r", encoding="utf-8") as f:
                raw_artifact = json.load(f)

            raw_results = raw_artifact.get("raw_results", [])

            for idx, entry in enumerate(raw_results):
                url = entry.get("url", "")
                title = entry.get("title", "")
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                # Enrich from THIS result's title ONLY — no shared summary contamination
                per_result_snippet = entry.get("snippet", title)
                name = extract_name(title, url)
                enriched = enrich_candidate(name, url, per_result_snippet, niche, geo)
                # Trace: link back to raw artifact with result index
                enriched["raw_source_file"] = os.path.basename(raw_file)
                enriched["raw_source_index"] = idx
                enriched["raw_source_title"] = title
                enriched["raw_source_url"] = url
                raw_candidates.append(enriched)

            print(f"  [FOUND] {len(raw_candidates)} candidates from raw artifact")

            # Save derived candidates with trace
            derived_file = os.path.join(derived_dir, f"{niche}_{geo.lower()}.json")
            with open(derived_file, "w", encoding="utf-8") as f:
                json.dump(raw_candidates, f, indent=2, ensure_ascii=False)
            print(f"  [DERIVED] Saved to {derived_file}")
        else:
            # No raw artifact yet — generate queries for operator
            queries = generate_queries(niche, geo)
            qfile = save_queries_file(queries, niche, geo)
            print(f"  [MODE] production: no raw search artifact found in {raw_dir}")
            print(f"  [ACTION] Run these queries via WebSearch in Claude Code:")
            for i, q in enumerate(queries, 1):
                print(f"  [QUERY {i}] {q}")
            print(f"  [ACTION] Save ALL query results as ONE JSON to: raw_search/{niche}_{geo.lower()}_YYYYMMDD.json")
            print(f"  [FORMAT] {{\"query\": \"<all queries combined>\", \"timestamp\": \"...\", \"raw_results\": [{{\"title\": \"...\", \"url\": \"...\", \"snippet\": \"...\"}}]}}")
            print(f"  [NOTE] Combine results from ALL queries above into a single raw_results array")

    # Score candidates
    candidates = []
    for r in raw_candidates:
        c = ExpertCandidate(
            name=r["name"],
            linkedin_url=r["linkedin_url"],
            primary_role=r.get("primary_role", ""),
            company=r.get("company", ""),
            location=r.get("location", geo),
            niche_tags=r.get("niche_tags", niche),
            credentials_claimed=r.get("credentials_claimed", ""),
            credentials_verified_or_signal=r.get("credentials_verified_or_signal", ""),
            evidence_links=r.get("evidence_links", ""),
        )
        score, notes = score_candidate(c, r.get("scoring", {}))
        c.fit_score = score
        c.fit_notes = notes
        c.confidence = "high" if score >= 70 else ("medium" if score >= 50 else "low")

        parts = []
        if c.credentials_claimed:
            parts.append(f"Credentials: {c.credentials_claimed}")
        if "citability=25" in c.fit_notes or "citability=20" in c.fit_notes:
            parts.append("Cited in major financial media")
        elif "citability=15" in c.fit_notes:
            parts.append("Cited in niche financial media")
        if c.location in ("US", "UK"):
            parts.append(f"Location: {c.location}")
        if c.fit_score >= 70:
            parts.append(f"High fit ({c.fit_score})")
        c.why_selected = "; ".join(parts) if parts else "Meets criteria"

        candidates.append(c)

    candidates.sort(key=lambda x: x.fit_score, reverse=True)
    return candidates


def main():
    parser = argparse.ArgumentParser(description="Expert Hunter — Production Search")
    parser.add_argument("--niche", choices=list(QUERY_TEMPLATES.keys()),
                       help="Niche to search")
    parser.add_argument("--all-niches", action="store_true",
                       help="Search all niches")
    parser.add_argument("--geo", default="US",
                       help="Geography filter (US, UK, CA, AU)")
    parser.add_argument("--test-fixture", dest="fixture",
                       help="Path to test fixture JSON (no internet, for testing)")
    parser.add_argument("--output-dir", default=".", dest="outdir",
                       help="Output directory for CSV/JSON")
    args = parser.parse_args()

    niches = list(QUERY_TEMPLATES.keys()) if args.all_niches else [args.niche]
    if not args.all_niches and not args.niche:
        parser.error("Specify --niche or --all-niches")

    all_candidates = []
    base = os.path.dirname(os.path.abspath(__file__))
    for niche in niches:
        fixture = args.fixture
        if fixture and not os.path.exists(fixture):
            # Try niche-specific fixture in fixtures/ directory
            niche_fixture = os.path.join(base, "fixtures", f"{niche}_{args.geo.lower()}.json")
            if os.path.exists(niche_fixture):
                fixture = niche_fixture
            else:
                fixture = None  # no fixture for this niche, use production path
        result = hunt(niche, args.geo, fixture)
        all_candidates.extend(result)

    # Dedup by URL
    seen = set()
    deduped = []
    for c in all_candidates:
        if c.linkedin_url not in seen:
            seen.add(c.linkedin_url)
            deduped.append(c)
    deduped.sort(key=lambda x: x.fit_score, reverse=True)

    # Export
    tag = f"{args.geo.lower()}"
    if args.all_niches:
        tag = f"all_{tag}"
    elif args.niche:
        tag = f"{args.niche}_{tag}"

    if not deduped:
        print(f"\n[SKIP] No candidates found — skipping export to preserve previous data")
        return deduped

    os.makedirs(args.outdir, exist_ok=True)
    full_csv = os.path.join(args.outdir, f"candidates_{tag}.csv")
    full_json = os.path.join(args.outdir, f"candidates_{tag}.json")
    candidates_to_csv(deduped, full_csv)
    candidates_to_json(deduped, full_json)
    print(f"\n[EXPORT] {len(deduped)} candidates -> {full_csv}")

    top = shortlist(deduped, 20)
    short_csv = os.path.join(args.outdir, f"shortlist_{tag}.csv")
    candidates_to_csv(top, short_csv)
    print(f"[EXPORT] Shortlist {len(top)} -> {short_csv}")

    # Summary
    print(f"\n{'#':>2} {'Score':>5} {'Conf':>6} {'Name':<30} {'Creds':<15} {'Company':<30} {'Niche'}")
    print("-" * 110)
    for i, c in enumerate(deduped[:20], 1):
        print(f"{i:>2} {c.fit_score:>5} {c.confidence:>6} {c.name:<30} {c.credentials_claimed:<15} {c.company:<30} {c.niche_tags}")

    return deduped


if __name__ == "__main__":
    main()
