"""Main entry point for the IPL project application."""

from src.data_loader import load_deliveries, load_matches
from src.extra_runs_conceded_2016 import plot_extra_runs_conceded_2016
from src.matches_played_by_team_by_season import (
    plot_matches_played_by_team_by_season,
)
from src.matches_won_per_team_per_year import plot_matches_won_per_team_per_year
from src.number_of_matches_played_per_year import plot_matches_played_per_year
from src.top_10_economical_bowlers_2015 import plot_top_economical_bowlers
from src.top_batsman_for_rcb import plot_top_rcb_batsmen
from src.total_runs_scored_by_team import plot_total_runs_by_team


def main() -> None:
    """Load the data and show each chart in turn."""
    deliveries = load_deliveries()
    matches = load_matches()

    plot_total_runs_by_team(deliveries)
    plot_top_rcb_batsmen(deliveries, top_n=10)
    plot_matches_played_per_year(matches)
    plot_matches_played_by_team_by_season(matches)
    plot_matches_won_per_team_per_year(matches)
    plot_extra_runs_conceded_2016(deliveries, matches)
    plot_top_economical_bowlers(deliveries, matches, top_n=10, year="2015")


if __name__ == "__main__":
    main()
