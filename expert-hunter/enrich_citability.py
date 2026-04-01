#!/usr/bin/env python3
"""
Sprint 1: Citability enrichment for expert-hunter candidates.

Takes derived_candidates JSON, generates WebSearch queries for each candidate,
processes saved search results, and updates citability scores.

Two modes:
  --generate <derived.json>   : Generate query file for operator to run
  --apply <derived.json> <citability_raw.json> : Apply citability data to candidates

Workflow:
  1. python3 enrich_citability.py --generate derived_candidates/forex_us.json
     -> Outputs: citability_queries_forex_us.txt (queries for operator)
  2. Operator runs WebSearch for each query, saves to citability_raw/forex_us.json
  3. python3 enrich_citability.py --apply derived_candidates/forex_us.json citability_raw/forex_us.json
     -> Updates: derived_candidates/forex_us.json (adds citability data)
     -> Outputs: candidates_forex_us_enriched.csv
"""

import json
import os
import re
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from schema import ExpertCandidate, score_candidate, candidates_to_csv, shortlist

MEDIA_TIER1 = ["Bloomberg", "Forbes", "WSJ", "Wall Street Journal"]
MEDIA_TIER2 = ["CNBC", "Reuters", "MarketWatch", "Barron's", "Yahoo Finance"]
MEDIA_TIER3 = ["NerdWallet", "Bankrate", "Investopedia", "Motley Fool", "Kiplinger", "FXStreet", "DailyFX", "InvestorPlace"]


def generate_queries(derived_path: str):
    """Generate citability WebSearch queries for each candidate."""
    with open(derived_path, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    tag = os.path.basename(derived_path).replace(".json", "")
    query_file = f"citability_queries_{tag}.txt"

    queries = []
    for c in candidates:
        name = c.get("name", "")
        if not name or len(name) < 3:
            continue
        # Add first credential as disambiguator to reduce false matches on common names
        creds = c.get("credentials_claimed", "")
        first_cred = creds.split(",")[0].strip() if creds else ""
        disambig = f' "{first_cred}"' if first_cred else ""
        q = f'"{name}"{disambig} ("Forbes" OR "Bloomberg" OR "CNBC" OR "WSJ" OR "Reuters" OR "MarketWatch" OR "Investopedia" OR "NerdWallet" OR "FXStreet" OR "DailyFX" OR "InvestorPlace" OR "Kiplinger" OR "Motley Fool" OR "Bankrate")'
        linkedin_url = c.get("linkedin_url", "")
        queries.append({"name": name, "query": q, "linkedin_url": linkedin_url})

    with open(query_file, "w", encoding="utf-8") as f:
        for q in queries:
            f.write(f"# {q['name']} | {q['linkedin_url']}\n{q['query']}\n\n")

    print(f"[GENERATE] {len(queries)} queries -> {query_file}")
    print(f"[NEXT] Run each query via WebSearch in Claude Code")
    print(f"[NEXT] Save results to: citability_raw/{tag}.json")
    print(f"[FORMAT] Array of objects: {{\"name\": \"...\", \"linkedin_url\": \"...\", \"results\": [{{\"title\": \"...\", \"url\": \"...\", \"snippet\": \"...\"}}]}}")
    return queries


def detect_tier(text: str) -> tuple[str, list[str]]:
    """Detect media tier from text. Returns (tier_key, list of matched outlets)."""
    text_lower = text.lower()
    matched = []

    for outlet in MEDIA_TIER1:
        if outlet.lower() in text_lower:
            matched.append(outlet)
    if matched:
        return "bloomberg_wsj_forbes", matched

    for outlet in MEDIA_TIER2:
        if outlet.lower() in text_lower:
            matched.append(outlet)
    if matched:
        return "cnbc_reuters", matched

    for outlet in MEDIA_TIER3:
        if outlet.lower() in text_lower:
            matched.append(outlet)
    if matched:
        return "niche_finance_media", matched

    return "none", []


def apply_citability(derived_path: str, citability_raw_path: str):
    """Apply citability data from WebSearch results to derived candidates."""
    with open(derived_path, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    with open(citability_raw_path, "r", encoding="utf-8") as f:
        citability_data = json.load(f)

    # Index citability by linkedin_url (stable, preferred) and name (fallback)
    cit_by_url = {}
    cit_by_name = {}
    name_counts = {}
    for entry in citability_data:
        url = entry.get("linkedin_url", "")
        name = entry.get("name", "").lower()
        if url:
            cit_by_url[url] = entry
        if name:
            name_counts[name] = name_counts.get(name, 0) + 1
            cit_by_name[name] = entry
    # Only allow name fallback for unique names
    cit_by_unique_name = {n: e for n, e in cit_by_name.items() if name_counts.get(n, 0) == 1}

    updated = 0
    for c in candidates:
        url = c.get("linkedin_url", "")
        name_lower = c.get("name", "").lower()
        cit = cit_by_url.get(url) or cit_by_unique_name.get(name_lower)
        if not cit:
            # No citability data for this candidate — reset stale citability if present
            if c.get("citability_tier") and c.get("citability_raw_source") != os.path.basename(citability_raw_path):
                c["citability_tier"] = "none"
                c["citability_outlets"] = []
                c["citability_evidence_urls"] = []
                if "scoring" in c:
                    c["scoring"]["citability"] = "none"
            continue

        results = cit.get("results", [])
        if not results:
            # No search results — clear stale citability, set to none
            c["citability_tier"] = "none"
            c["citability_outlets"] = []
            c["citability_evidence_urls"] = []
            c["citability_raw_source"] = os.path.basename(citability_raw_path)
            if "scoring" in c:
                c["scoring"]["citability"] = "none"
            updated += 1
            continue

        all_text = " ".join(r.get("title", "") + " " + r.get("snippet", "") for r in results)
        evidence_urls = [r.get("url", "") for r in results if r.get("url")]

        tier, matched_outlets = detect_tier(all_text)

        # Only persist evidence if a media tier was actually matched
        c["citability_tier"] = tier
        c["citability_outlets"] = matched_outlets if tier != "none" else []
        c["citability_evidence_urls"] = evidence_urls[:5] if tier != "none" else []
        c["citability_raw_source"] = os.path.basename(citability_raw_path)

        # Update scoring
        if "scoring" in c:
            c["scoring"]["citability"] = tier

        # Keep credentials_verified_or_signal in sync
        existing_signal = c.get("credentials_verified_or_signal", "")
        # Remove any old media note
        existing_signal = re.sub(r';?\s*media:\s*[^;]*', '', existing_signal).strip('; ')
        if tier != "none" and matched_outlets:
            media_note = f"media: {', '.join(matched_outlets)}"
            c["credentials_verified_or_signal"] = f"{existing_signal}; {media_note}" if existing_signal else media_note
        else:
            c["credentials_verified_or_signal"] = existing_signal

        updated += 1

    # Save updated derived candidates
    with open(derived_path, "w", encoding="utf-8") as f:
        json.dump(candidates, f, indent=2, ensure_ascii=False)

    print(f"[APPLY] Updated {updated}/{len(candidates)} candidates with citability data")
    print(f"[SAVED] {derived_path}")

    # Re-score and export enriched CSV
    tag = os.path.basename(derived_path).replace(".json", "")
    enriched_candidates = []
    for c in candidates:
        ec = ExpertCandidate(
            name=c.get("name", ""),
            linkedin_url=c.get("linkedin_url", ""),
            primary_role=c.get("primary_role", ""),
            company=c.get("company", ""),
            location=c.get("location", ""),
            niche_tags=c.get("niche_tags", ""),
            credentials_claimed=c.get("credentials_claimed", ""),
            credentials_verified_or_signal=c.get("credentials_verified_or_signal", ""),
            evidence_links=", ".join(c.get("citability_evidence_urls", [])) or c.get("evidence_links", ""),
        )
        score, notes = score_candidate(ec, c.get("scoring", {}))
        ec.fit_score = score
        ec.fit_notes = notes
        ec.confidence = "high" if score >= 70 else ("medium" if score >= 50 else "low")

        parts = []
        if ec.credentials_claimed:
            parts.append(f"Credentials: {ec.credentials_claimed}")
        if "citability=25" in notes or "citability=20" in notes:
            parts.append(f"Media: {', '.join(c.get('citability_outlets', []))}")
        elif "citability=15" in notes:
            parts.append(f"Niche media: {', '.join(c.get('citability_outlets', []))}")
        if ec.location in ("US", "UK"):
            parts.append(f"Location: {ec.location}")
        if ec.fit_score >= 70:
            parts.append(f"High fit ({ec.fit_score})")
        ec.why_selected = "; ".join(parts) if parts else "Meets criteria"

        enriched_candidates.append(ec)

    enriched_candidates.sort(key=lambda x: x.fit_score, reverse=True)
    csv_path = f"candidates_{tag}_enriched.csv"
    candidates_to_csv(enriched_candidates, csv_path)
    print(f"[EXPORT] {len(enriched_candidates)} enriched candidates -> {csv_path}")

    # Print summary
    print(f"\n{'#':>2} {'Score':>5} {'Conf':>6} {'Name':<25} {'Citability':<20} {'Why'}")
    print("-" * 100)
    for i, ec in enumerate(enriched_candidates[:10], 1):
        cit = next((c for c in candidates if c["name"] == ec.name), {})
        tier = cit.get("citability_tier", "none")
        outlets = ", ".join(cit.get("citability_outlets", []))
        print(f"{i:>2} {ec.fit_score:>5} {ec.confidence:>6} {ec.name:<25} {tier:<20} {ec.why_selected[:50]}")


def main():
    parser = argparse.ArgumentParser(description="Citability Enrichment (Sprint 1)")
    parser.add_argument("--generate", metavar="DERIVED_JSON",
                       help="Generate WebSearch queries for citability check")
    parser.add_argument("--apply", nargs=2, metavar=("DERIVED_JSON", "CITABILITY_RAW_JSON"),
                       help="Apply citability data to derived candidates")
    args = parser.parse_args()

    if args.generate:
        generate_queries(args.generate)
    elif args.apply:
        apply_citability(args.apply[0], args.apply[1])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
