"""Expert candidate schema and scoring logic for /expert-hunter skill."""

import csv
import json
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class ExpertCandidate:
    name: str
    linkedin_url: str
    primary_role: str = ""
    company: str = ""
    location: str = ""
    niche_tags: str = ""  # comma-separated
    credentials_claimed: str = ""  # comma-separated
    credentials_verified_or_signal: str = ""  # comma-separated
    evidence_links: str = ""  # comma-separated URLs
    fit_score: int = 0
    fit_notes: str = ""
    why_selected: str = ""
    confidence: str = "low"  # low | medium | high
    status: str = "candidate"  # candidate | shortlisted | rejected


# Scoring weights (raw points, max total = 100)
SCORING = {
    "citability": {
        "max": 25,
        "rules": {
            "bloomberg_wsj_forbes": 25,
            "cnbc_reuters": 20,
            "niche_finance_media": 15,
            "podcast_youtube": 10,
            "linkedin_articles_only": 5,
            "none": 0,
        },
    },
    "credentials": {
        "max": 20,
        "rules": {
            "CFA": 20,
            "CFP": 18,
            "CPA": 16,
            "CAIA": 15,
            "FRM": 15,
            "Series 7": 12,
            "Series 3": 12,
            "Series 65": 10,
            # multiple: max(single) + min(3 * extra, 5), hard cap 20
        },
    },
    "google_entity": {
        "max": 15,
        "rules": {
            "knowledge_panel": 15,
            "google_scholar_profile": 12,
            "ai_overview_cited": 10,
            "rich_serp_presence": 7,
            "basic_serp": 3,
            "none": 0,
        },
    },
    "associations": {
        "max": 10,
        "rules": {
            "CFA_Institute": 10,
            "NAPFA": 9,
            "FPA": 8,
            "AICPA": 8,
            "board_member_bonus": 2,  # additive
        },
    },
    "linkedin_activity": {
        "max": 10,
        "rules": {
            "10plus_posts_month": 8,
            "5_to_10": 6,
            "1_to_4": 3,
            "zero": 0,
            "articles_bonus": 2,  # additive, cap at 10
        },
    },
    "experience_years": {
        "max": 10,
        "rules": {
            "20plus": 10,
            "15_19": 8,
            "10_14": 6,
            "5_9": 4,
            "under_5": 2,
        },
    },
    "location": {
        "max": 5,
        "rules": {
            "US": 5,
            "UK": 5,
            "Canada": 3,
            "Australia": 3,
            "other_english": 2,
            "other": 0,
        },
    },
    "native_english": {
        "max": 5,
        "rules": {
            "confirmed_native": 5,
            "likely_native": 4,
            "fluent": 3,
            "unclear": 1,
        },
    },
}


def score_candidate(c: ExpertCandidate, scoring_details: dict) -> int:
    """Calculate fit_score from scoring_details dict.

    scoring_details keys match SCORING categories.
    Each value is the rule key that applies.
    Returns total score (0-100).
    """
    total = 0
    notes = []

    for category, rule_key in scoring_details.items():
        if category not in SCORING:
            continue
        cat = SCORING[category]
        if isinstance(rule_key, list):
            # multiple rules (e.g. credentials)
            points = 0
            for rk in rule_key:
                p = cat["rules"].get(rk, 0)
                points = max(points, p)
            # bonus for multiples
            if len(rule_key) > 1:
                extras = len(rule_key) - 1
                points += min(3 * extras, 5)
            points = min(points, cat["max"])
        else:
            points = min(cat["rules"].get(rule_key, 0), cat["max"])
        total += points
        if points > 0:
            notes.append(f"{category}={points}")

    total = min(total, 100)
    return total, ", ".join(notes)


def candidates_to_csv(candidates: list[ExpertCandidate], path: str):
    """Write candidates to CSV file."""
    if not candidates:
        return
    fieldnames = [
        "name", "linkedin_url", "primary_role", "company", "location",
        "niche_tags", "credentials_claimed", "credentials_verified_or_signal",
        "evidence_links", "fit_score", "fit_notes", "why_selected",
        "confidence", "status",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in candidates:
            writer.writerow(asdict(c))


def candidates_to_json(candidates: list[ExpertCandidate], path: str):
    """Write candidates to JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(c) for c in candidates], f, indent=2, ensure_ascii=False)


def shortlist(candidates: list[ExpertCandidate], top_n: int = 20) -> list[ExpertCandidate]:
    """Return top N candidates by fit_score, mark them as shortlisted."""
    ranked = sorted(candidates, key=lambda c: c.fit_score, reverse=True)
    result = []
    for c in ranked[:top_n]:
        c.status = "shortlisted"
        result.append(c)
    return result
