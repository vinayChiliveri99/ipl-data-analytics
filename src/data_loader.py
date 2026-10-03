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
