# IPL Project

A Python project for exploring and analyzing IPL (Indian Premier League) cricket data.

## Requirements

- Python 3.12+

## Setup

```bash
# 1. Clone the repo and enter the folder
git clone <repo-url>
cd ipl-project

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Each chart opens in its own window; close it to see the next one.

| Chart | Module |
|---|---|
| Total runs scored by each team | `src/total_runs_scored_by_team.py` |
| Top 10 batsmen for Royal Challengers Bangalore | `src/top_batsman_for_rcb.py` |

## Project Structure

```
ipl-project/
├── main.py                  # Entry point: loads data, shows each chart
├── data/
│   ├── matches.csv          # One row per match
│   └── deliveries.csv       # One row per ball bowled
├── src/
│   ├── data_loader.py       # Reads the CSVs
│   ├── plotting.py          # Shared chart helper
│   └── ...                  # One module per analysis
└── requirements.txt         # Python dependencies
```

## Adding Dependencies

When you install a new package, add it to `requirements.txt` so others get it too:

```bash
pip install <package>
pip freeze > requirements.txt
```
