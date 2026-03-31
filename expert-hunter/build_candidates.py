#!/usr/bin/env python3
"""Build candidate dataset from scan output or seed data, score, and export CSV + shortlist.

Modes:
  --from-scan <path>   : Read candidates_raw.json produced by scan.py (scan-backed mode)
  --seed               : Use built-in seed dataset (demo mode, default if no --from-scan)

Examples:
  python3 build_candidates.py --from-scan candidates_raw.json
  python3 build_candidates.py --seed
"""

import json
import os
import sys
import argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from schema import ExpertCandidate, score_candidate, candidates_to_csv, candidates_to_json, shortlist

# === SEED DATA (demo mode) ===
# Manually structured from WebSearch results executed 2026-03-30.
# This is a fallback for demo/development. Production path: --from-scan.

RAW = [
    # === FOREX / FX ===
    {
        "name": "Ye Xie, CFA",
        "linkedin_url": "https://www.linkedin.com/in/ye-xie-cfa-66783714/",
        "primary_role": "Chief FX Strategist",
        "company": "BMO Capital Markets",
        "location": "US",
        "niche_tags": "forex, FX, macro",
        "credentials_claimed": "CFA",
        "credentials_verified_or_signal": "CFA in LinkedIn title, Bloomberg bylines",
        "evidence_links": "https://www.linkedin.com/in/ye-xie-cfa-66783714/",
        "scoring": {"citability": "bloomberg_wsj_forbes", "credentials": ["CFA"], "google_entity": "rich_serp_presence", "location": "US", "native_english": "likely_native", "experience_years": "15_19", "linkedin_activity": "5_to_10", "associations": "CFA_Institute"},
    },
    {
        "name": "Sam Ro, CFA",
        "linkedin_url": "https://www.linkedin.com/in/sammyro/",
        "primary_role": "Founder & Editor",
        "company": "TKer (Substack)",
        "location": "US",
        "niche_tags": "stocks, macro, personal finance",
        "credentials_claimed": "CFA",
        "credentials_verified_or_signal": "CFA in title, Forbes contributor, Yahoo Finance alum",
        "evidence_links": "https://www.linkedin.com/in/sammyro/",
        "scoring": {"citability": "bloomberg_wsj_forbes", "credentials": ["CFA"], "google_entity": "rich_serp_presence", "location": "US", "native_english": "confirmed_native", "experience_years": "15_19", "linkedin_activity": "10plus_posts_month", "associations": "CFA_Institute"},
    },
    {
        "name": "Marta Norton, CFA",
        "linkedin_url": "https://www.linkedin.com/in/martaknorton/",
        "primary_role": "Chief Investment Strategist",
        "company": "Empower",
        "location": "US",
        "niche_tags": "investment, macro, retirement",
        "credentials_claimed": "CFA",
        "credentials_verified_or_signal": "CFA in title, frequent media quotes",
        "evidence_links": "https://www.linkedin.com/in/martaknorton/",
        "scoring": {"citability": "cnbc_reuters", "credentials": ["CFA"], "google_entity": "rich_serp_presence", "location": "US", "native_english": "confirmed_native", "experience_years": "20plus", "linkedin_activity": "5_to_10", "associations": "CFA_Institute"},
    },
    {
        "name": "Tom Garretson, CFA",
        "linkedin_url": "https://www.linkedin.com/in/tom-garretson-cfa-3774488/",
        "primary_role": "Fixed Income Portfolio Strategist",
        "company": "RBC Wealth Management",
        "location": "US",
        "niche_tags": "fixed income, bonds, macro",
        "credentials_claimed": "CFA",
        "credentials_verified_or_signal": "CFA in title, Bloomberg media appearances",
        "evidence_links": "https://www.linkedin.com/in/tom-garretson-cfa-3774488/",
        "scoring": {"citability": "bloomberg_wsj_forbes", "credentials": ["CFA"], "google_entity": "basic_serp", "location": "US", "native_english": "confirmed_native", "experience_years": "15_19", "linkedin_activity": "5_to_10", "associations": "CFA_Institute"},
    },
    {
        "name": "Blake Morrow",
        "linkedin_url": "https://www.linkedin.com/in/blake-morrow-322a47b3/",
        "primary_role": "Chief Currency Strategist",
        "company": "Forex Analytix",
        "location": "US",
        "niche_tags": "forex, FX, technical analysis",
        "credentials_claimed": "",
        "credentials_verified_or_signal": "No formal certs, but widely cited forex expert",
        "evidence_links": "https://www.linkedin.com/in/blake-morrow-322a47b3/",
        "scoring": {"citability": "niche_finance_media", "credentials": [], "google_entity": "basic_serp", "location": "US", "native_english": "confirmed_native", "experience_years": "20plus", "linkedin_activity": "10plus_posts_month"},
    },
    # === PERSONAL FINANCE / CFP ===
    {
        "name": "Liz Weston, CFP",
        "linkedin_url": "https://www.linkedin.com/in/lizweston/",
        "primary_role": "Personal Finance Columnist",
        "company": "Weston Studios (ex-NerdWallet)",
        "location": "US",
        "niche_tags": "personal finance, credit, debt",
        "credentials_claimed": "CFP",
        "credentials_verified_or_signal": "CFP in title, NerdWallet columnist, AP syndicated",
        "evidence_links": "https://www.linkedin.com/in/lizweston/",
        "scoring": {"citability": "bloomberg_wsj_forbes", "credentials": ["CFP"], "google_entity": "knowledge_panel", "location": "US", "native_english": "confirmed_native", "experience_years": "20plus", "linkedin_activity": "5_to_10", "associations": "FPA"},
    },
    {
        "name": "Hal M. Bundrick, CFP",
        "linkedin_url": "https://www.linkedin.com/in/halmbundrick/",
        "primary_role": "Senior Writer",
        "company": "Yahoo Finance (ex-NerdWallet)",
        "location": "US",
        "niche_tags": "personal finance, banking, credit",
        "credentials_claimed": "CFP",
        "credentials_verified_or_signal": "CFP in title, NerdWallet + Yahoo Finance bylines",
        "evidence_links": "https://www.linkedin.com/in/halmbundrick/",
        "scoring": {"citability": "bloomberg_wsj_forbes", "credentials": ["CFP"], "google_entity": "rich_serp_presence", "location": "US", "native_english": "confirmed_native", "experience_years": "20plus", "linkedin_activity": "5_to_10", "associations": "FPA"},
    },
    {
        "name": "Sean Pyles, CFP",
        "linkedin_url": "https://www.linkedin.com/in/seanloranpyles/",
        "primary_role": "Writer & Podcast Host",
        "company": "NerdWallet",
        "location": "US",
        "niche_tags": "personal finance, saving, budgeting",
        "credentials_claimed": "CFP",
        "credentials_verified_or_signal": "CFP in title, active NerdWallet writer, Smart Money podcast host",
        "evidence_links": "https://www.linkedin.com/in/seanloranpyles/",
        "scoring": {"citability": "niche_finance_media", "credentials": ["CFP"], "google_entity": "rich_serp_presence", "location": "US", "native_english": "confirmed_native", "experience_years": "10_14", "linkedin_activity": "10plus_posts_month"},
    },
    {
        "name": "Kelly Anne Smith",
        "linkedin_url": "https://www.linkedin.com/in/kelly-anne-smith/",
        "primary_role": "Writer",
        "company": "Forbes Advisor",
        "location": "US",
        "niche_tags": "personal finance, banking, credit cards",
        "credentials_claimed": "",
        "credentials_verified_or_signal": "No formal certs, Forbes Advisor byline",
        "evidence_links": "https://www.linkedin.com/in/kelly-anne-smith/",
        "scoring": {"citability": "bloomberg_wsj_forbes", "credentials": [], "google_entity": "basic_serp", "location": "US", "native_english": "confirmed_native", "experience_years": "5_9", "linkedin_activity": "5_to_10"},
    },
    {
        "name": "Christopher Burke, CFP",
        "linkedin_url": "https://www.linkedin.com/in/chris--burke/",
        "primary_role": "Financial Advisor",
        "company": "Merrill Lynch Wealth Management",
        "location": "US",
        "niche_tags": "personal finance, wealth management",
        "credentials_claimed": "CFP",
        "credentials_verified_or_signal": "CFP in title, Merrill Lynch (FINRA verifiable)",
        "evidence_links": "https://www.linkedin.com/in/chris--burke/",
        "scoring": {"citability": "none", "credentials": ["CFP"], "google_entity": "none", "location": "US", "native_english": "confirmed_native", "experience_years": "15_19", "linkedin_activity": "1_to_4"},
    },
    # === CRYPTO / DIGITAL ASSETS ===
    {
        "name": "Nik Bhatia, CFA, CMT",
        "linkedin_url": "https://www.linkedin.com/in/nik-bhatia-cfa-cmt-b549b858/",
        "primary_role": "Author & Adjunct Professor of Finance",
        "company": "The Bitcoin Layer",
        "location": "US",
        "niche_tags": "crypto, bitcoin, fixed income",
        "credentials_claimed": "CFA, CMT",
        "credentials_verified_or_signal": "CFA+CMT in title, published author (Layered Money), USC professor",
        "evidence_links": "https://www.linkedin.com/in/nik-bhatia-cfa-cmt-b549b858/",
        "scoring": {"citability": "bloomberg_wsj_forbes", "credentials": ["CFA"], "google_entity": "knowledge_panel", "location": "US", "native_english": "confirmed_native", "experience_years": "15_19", "linkedin_activity": "10plus_posts_month", "associations": "CFA_Institute"},
    },
    {
        "name": "Sofien Kaabar, CFA",
        "linkedin_url": "https://www.linkedin.com/in/sofienkaabar/",
        "primary_role": "Quantitative Researcher & Author",
        "company": "BBSP Research",
        "location": "Other",
        "niche_tags": "forex, crypto, quantitative",
        "credentials_claimed": "CFA",
        "credentials_verified_or_signal": "CFA in title, published multiple books on trading",
        "evidence_links": "https://www.linkedin.com/in/sofienkaabar/",
        "scoring": {"citability": "niche_finance_media", "credentials": ["CFA"], "google_entity": "rich_serp_presence", "location": "other", "native_english": "fluent", "experience_years": "10_14", "linkedin_activity": "10plus_posts_month", "associations": "CFA_Institute"},
    },
    {
        "name": "Bud Haslett, CFA, FRM",
        "linkedin_url": "https://www.linkedin.com/in/budhaslett",
        "primary_role": "Digital Assets Specialist",
        "company": "FOMO-FUD Digital Assets",
        "location": "US",
        "niche_tags": "crypto, risk management, digital assets",
        "credentials_claimed": "CFA, FRM",
        "credentials_verified_or_signal": "CFA+FRM in title, ex-CFA Institute staff",
        "evidence_links": "https://www.linkedin.com/in/budhaslett",
        "scoring": {"citability": "niche_finance_media", "credentials": ["CFA", "FRM"], "google_entity": "basic_serp", "location": "US", "native_english": "confirmed_native", "experience_years": "20plus", "linkedin_activity": "5_to_10", "associations": "CFA_Institute"},
    },
    {
        "name": "Kirk David Phillips, CPA",
        "linkedin_url": "https://www.linkedin.com/in/kirk-phillips-cpa/",
        "primary_role": "Crypto Tax & Accounting Expert",
        "company": "Crypto Bullseye Zone",
        "location": "US",
        "niche_tags": "crypto, tax, accounting",
        "credentials_claimed": "CPA, CMA, CFE",
        "credentials_verified_or_signal": "CPA in title, multiple accounting certs, published author",
        "evidence_links": "https://www.linkedin.com/in/kirk-phillips-cpa/",
        "scoring": {"citability": "niche_finance_media", "credentials": ["CPA"], "google_entity": "rich_serp_presence", "location": "US", "native_english": "confirmed_native", "experience_years": "20plus", "linkedin_activity": "5_to_10", "associations": "AICPA"},
    },
    # === STOCKS / EQUITY ===
    {
        "name": "Rachel L. Warren",
        "linkedin_url": "https://www.linkedin.com/in/rlw-8813/",
        "primary_role": "Contributing Stock Market Analyst",
        "company": "The Motley Fool",
        "location": "US",
        "niche_tags": "stocks, investing, healthcare",
        "credentials_claimed": "",
        "credentials_verified_or_signal": "No formal certs, Motley Fool contributor",
        "evidence_links": "https://www.linkedin.com/in/rlw-8813/",
        "scoring": {"citability": "niche_finance_media", "credentials": [], "google_entity": "basic_serp", "location": "US", "native_english": "confirmed_native", "experience_years": "5_9", "linkedin_activity": "5_to_10"},
    },
    {
        "name": "Vincent G. Piazza, CFA",
        "linkedin_url": "https://www.linkedin.com/in/vpiazzabloombergintelligence/",
        "primary_role": "Senior Energy Equity Analyst",
        "company": "Bloomberg Intelligence",
        "location": "US",
        "niche_tags": "stocks, energy, equity research",
        "credentials_claimed": "CFA",
        "credentials_verified_or_signal": "CFA in title, Bloomberg Intelligence analyst",
        "evidence_links": "https://www.linkedin.com/in/vpiazzabloombergintelligence/",
        "scoring": {"citability": "bloomberg_wsj_forbes", "credentials": ["CFA"], "google_entity": "basic_serp", "location": "US", "native_english": "confirmed_native", "experience_years": "20plus", "linkedin_activity": "1_to_4", "associations": "CFA_Institute"},
    },
    {
        "name": "Paul Katzeff",
        "linkedin_url": "https://www.linkedin.com/in/paul-katzeff-208115219/",
        "primary_role": "Writer",
        "company": "Investopedia",
        "location": "US",
        "niche_tags": "stocks, investing, markets",
        "credentials_claimed": "",
        "credentials_verified_or_signal": "Investopedia writer, MarketWatch contributor",
        "evidence_links": "https://www.linkedin.com/in/paul-katzeff-208115219/",
        "scoring": {"citability": "niche_finance_media", "credentials": [], "google_entity": "basic_serp", "location": "US", "native_english": "confirmed_native", "experience_years": "20plus", "linkedin_activity": "1_to_4"},
    },
    # === COMPETITOR EXPERTS (ForexBrokers / BrokerChooser) ===
    {
        "name": "Adam Nasli",
        "linkedin_url": "https://www.linkedin.com/in/adam-nasli/",
        "primary_role": "Head of Analyst Team",
        "company": "BrokerChooser",
        "location": "Other",
        "niche_tags": "forex, broker reviews, fintech",
        "credentials_claimed": "CFA-level knowledge",
        "credentials_verified_or_signal": "BrokerChooser lead analyst, ex-Citibank, 10+ years",
        "evidence_links": "https://www.linkedin.com/in/adam-nasli/",
        "scoring": {"citability": "niche_finance_media", "credentials": [], "google_entity": "basic_serp", "location": "other", "native_english": "fluent", "experience_years": "10_14", "linkedin_activity": "5_to_10"},
    },
    {
        "name": "Jacob Schroeder",
        "linkedin_url": "https://www.linkedin.com/in/jacob-schroeder/",
        "primary_role": "Financial Content Strategist",
        "company": "The Advisor Content Collective",
        "location": "US",
        "niche_tags": "personal finance, advisor content",
        "credentials_claimed": "",
        "credentials_verified_or_signal": "Kiplinger quoted, finance content specialist",
        "evidence_links": "https://www.linkedin.com/in/jacob-schroeder/",
        "scoring": {"citability": "niche_finance_media", "credentials": [], "google_entity": "none", "location": "US", "native_english": "confirmed_native", "experience_years": "10_14", "linkedin_activity": "10plus_posts_month"},
    },
    {
        "name": "Kim Clark",
        "linkedin_url": "https://www.linkedin.com/in/kimbclark/",
        "primary_role": "Writer",
        "company": "Kiplinger Personal Finance",
        "location": "US",
        "niche_tags": "personal finance, education, retirement",
        "credentials_claimed": "",
        "credentials_verified_or_signal": "Kiplinger staff writer",
        "evidence_links": "https://www.linkedin.com/in/kimbclark/",
        "scoring": {"citability": "niche_finance_media", "credentials": [], "google_entity": "basic_serp", "location": "US", "native_english": "confirmed_native", "experience_years": "20plus", "linkedin_activity": "1_to_4"},
    },
]


"""
Scan-backed JSON input contract:
Each entry MUST have:
  - linkedin_url (str, required)
  - name (str, required)
Each entry MAY have:
  - raw_snippet (str) — used for enrichment heuristics
  - niche (str) — forex, stocks, crypto, personal_finance
  - scan_source (str) — google_search, finra, cfa_directory
  - scan_timestamp (str, ISO 8601)
"""

import re

# Known credential patterns to extract from snippets
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

# Known media outlets for citability detection
MEDIA_TIER1 = ["Bloomberg", "Forbes", "WSJ", "Wall Street Journal"]
MEDIA_TIER2 = ["CNBC", "Reuters", "MarketWatch", "Barron's", "Yahoo Finance"]
MEDIA_TIER3 = ["NerdWallet", "Bankrate", "Investopedia", "Motley Fool", "Kiplinger"]

# Company patterns suggesting seniority
SENIOR_PATTERNS = [
    r'\b(Chief|Head|Director|Senior|Lead|Managing|Partner|Professor)\b',
]


def enrich_from_snippet(entry: dict, default_location: str = "US") -> dict:
    """Extract structured signals from raw_snippet + name fields.

    This is lightweight enrichment that produces meaningful scoring
    differentiation from scan-level data alone.
    """
    snippet = entry.get("raw_snippet", "") + " " + entry.get("name", "")
    name = entry.get("name", "")

    # Extract credentials from name + snippet
    creds_found = []
    for cred, pattern in CREDENTIAL_PATTERNS.items():
        if re.search(pattern, snippet, re.IGNORECASE):
            creds_found.append(cred)

    # Extract company only from "at Company" pattern (reliable)
    company = ""
    company_match = re.search(r'\bat\s+([A-Z][A-Za-z\s&.]+?)(?:\s*[,|]|\s*$)', snippet)
    if company_match:
        company = company_match.group(1).strip()[:50]

    # Detect citability from media mentions
    citability = "none"
    for outlet in MEDIA_TIER1:
        if outlet.lower() in snippet.lower():
            citability = "bloomberg_wsj_forbes"
            break
    if citability == "none":
        for outlet in MEDIA_TIER2:
            if outlet.lower() in snippet.lower():
                citability = "cnbc_reuters"
                break
    if citability == "none":
        for outlet in MEDIA_TIER3:
            if outlet.lower() in snippet.lower():
                citability = "niche_finance_media"
                break

    # Detect seniority -> experience estimate
    experience = "5_9"
    for pat in SENIOR_PATTERNS:
        if re.search(pat, snippet):
            experience = "15_19"
            break

    # Detect google entity signal from snippet richness
    entity = "none"
    if len(snippet) > 150 and creds_found:
        entity = "basic_serp"
    if citability in ("bloomberg_wsj_forbes", "cnbc_reuters"):
        entity = "rich_serp_presence"

    # Build scoring dict
    scoring = {
        "citability": citability,
        "credentials": creds_found,
        "google_entity": entity,
        "location": default_location,
        "native_english": "likely_native" if creds_found else "unclear",
        "experience_years": experience,
        "linkedin_activity": "5_to_10" if citability != "none" else "1_to_4",
    }
    if creds_found:
        scoring["associations"] = "CFA_Institute" if "CFA" in creds_found else "FPA" if "CFP" in creds_found else "AICPA" if "CPA" in creds_found else ""

    creds_str = ", ".join(creds_found)
    verified_signal = f"{creds_str} detected in snippet" if creds_found else ""
    if citability != "none":
        verified_signal += f"; media signal: {citability}"

    return {
        "name": name,
        "linkedin_url": entry.get("linkedin_url", ""),
        "primary_role": entry.get("raw_snippet", "")[:80],
        "company": company,
        "location": default_location,
        "niche_tags": entry.get("niche", ""),
        "credentials_claimed": creds_str,
        "credentials_verified_or_signal": verified_signal,
        "evidence_links": entry.get("linkedin_url", ""),
        "scoring": scoring,
    }


def load_from_scan(path: str, default_location: str = "US") -> list[dict]:
    """Load candidates from scan JSON and enrich from snippets."""
    with open(path, "r", encoding="utf-8") as f:
        raw_scan = json.load(f)

    candidates = []
    for entry in raw_scan:
        if not entry.get("linkedin_url"):
            continue
        enriched = enrich_from_snippet(entry, default_location=default_location)
        candidates.append(enriched)
    return candidates


def build_all(source: str = "seed", scan_path: str = None):
    if source == "scan" and scan_path:
        raw_data = load_from_scan(scan_path)
        mode = "scan-backed"
        print(f"[MODE] scan-backed: loading from {scan_path}")
    else:
        raw_data = RAW
        mode = "seeded demo"
        print(f"[MODE] seeded demo: using built-in {len(RAW)} candidates")

    candidates = []

    for r in raw_data:
        scoring_input = r.get("scoring", {})
        c = ExpertCandidate(
            name=r["name"],
            linkedin_url=r["linkedin_url"],
            primary_role=r.get("primary_role", ""),
            company=r.get("company", ""),
            location=r.get("location", ""),
            niche_tags=r.get("niche_tags", ""),
            credentials_claimed=r.get("credentials_claimed", ""),
            credentials_verified_or_signal=r.get("credentials_verified_or_signal", ""),
            evidence_links=r.get("evidence_links", ""),
        )

        score, notes = score_candidate(c, scoring_input)
        c.fit_score = score
        c.fit_notes = notes
        c.confidence = "high" if score >= 70 else ("medium" if score >= 50 else "low")
        candidates.append(c)

    # Sort by score
    candidates.sort(key=lambda x: x.fit_score, reverse=True)

    # Generate why_selected for top candidates
    for c in candidates:
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
            parts.append(f"High fit score ({c.fit_score})")
        c.why_selected = "; ".join(parts) if parts else "Meets basic criteria"

    # Mode-specific output filenames to avoid cross-mode overwrites
    suffix = "scan" if source == "scan" else "seed"

    # Export full dataset
    full_csv = f"candidates_full.{suffix}.csv"
    full_json = f"candidates_full.{suffix}.json"
    candidates_to_csv(candidates, full_csv)
    candidates_to_json(candidates, full_json)
    print(f"Full dataset: {len(candidates)} candidates -> {full_csv} + {full_json}")

    # Shortlist top 20
    top = shortlist(candidates, 20)
    short_csv = f"candidates_shortlist.{suffix}.csv"
    short_json = f"candidates_shortlist.{suffix}.json"
    candidates_to_csv(top, short_csv)
    candidates_to_json(top, short_json)
    print(f"Shortlist: {len(top)} candidates -> {short_csv} + {short_json}")

    # Print summary
    print("\n=== SHORTLIST TOP 20 ===\n")
    print(f"{'#':>2} {'Score':>5} {'Conf':>6} {'Name':<30} {'Credentials':<15} {'Company':<30} {'Niche'}")
    print("-" * 120)
    for i, c in enumerate(top, 1):
        print(f"{i:>2} {c.fit_score:>5} {c.confidence:>6} {c.name:<30} {c.credentials_claimed:<15} {c.company:<30} {c.niche_tags}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build expert candidate dataset")
    parser.add_argument("--from-scan", dest="scan_path", default=None,
                       help="Path to candidates_raw.json from scan.py (scan-backed mode)")
    parser.add_argument("--seed", action="store_true", default=False,
                       help="Use built-in seed dataset (demo mode)")
    args = parser.parse_args()

    if args.scan_path:
        build_all(source="scan", scan_path=args.scan_path)
    else:
        build_all(source="seed")
