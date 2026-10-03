"""Extra runs conceded per team in the year 2016, as a bar chart."""

from src.data_loader import season_by_match_id
from src.plotting import plot_horizontal_bar


def extra_runs_by_bowling_team(
    deliveries: list[dict[str, str]], matches: list[dict[str, str]], year: str
) -> dict[str, int]:
    """Sum extra_runs given away by each bowling team in `year`."""
    seasons = season_by_match_id(matches)

    totals = {}
    for ball in deliveries:
        if seasons[ball["match_id"]] != year:
            continue
        team = ball["bowling_team"]
        if team not in totals:
            totals[team] = 0
        totals[team] += int(ball["extra_runs"])
    return totals


def plot_extra_runs_conceded_2016(
    deliveries: list[dict[str, str]], matches: list[dict[str, str]]
) -> None:
    """Plot a bar chart of extra runs conceded per team in the year 2016."""
    totals = extra_runs_by_bowling_team(deliveries, matches, year="2016")
    sorted_teams = sorted(totals.items(), key=lambda item: item[1], reverse=True)

    plot_horizontal_bar(
        sorted_teams,
        title="Extra Runs Conceded per Team, IPL 2016",
        subtitle="Wides, no-balls, byes and leg-byes given away while bowling",
        xlabel="Extra runs conceded",
        ylabel="Bowling team",
    )
