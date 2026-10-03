"""Load the IPL datasets from the data/ folder."""

import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MATCHES_CSV = DATA_DIR / "matches.csv"
DELIVERIES_CSV = DATA_DIR / "deliveries.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read a CSV file into a list of row dicts keyed by column name."""
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def load_matches() -> list[dict[str, str]]:
    """Load one row per IPL match."""
    return read_csv(MATCHES_CSV)


def load_deliveries() -> list[dict[str, str]]:
    """Load one row per ball bowled across all IPL matches."""
    return read_csv(DELIVERIES_CSV)


def season_by_match_id(matches: list[dict[str, str]]) -> dict[str, str]:
    """Build a lookup from match id to season, e.g. {"1": "2017", ...}.

    Build it once, then look up each ball's season directly instead of
    searching through every match again for every ball.
    """
    seasons = {}
    for match in matches:
        seasons[match["id"]] = match["season"]
    return seasons
