"""Total runs scored by each team over the history of the IPL.

Uses the total_runs field, which includes extras.
"""

from src.plotting import plot_horizontal_bar


def runs_by_team(deliveries: list[dict[str, str]]) -> dict[str, int]:
    """Sum total_runs for every ball, grouped by batting team."""
    totals = {}
    for ball in deliveries:
        team = ball["batting_team"]
        if team not in totals:
            totals[team] = 0
        totals[team] += int(ball["total_runs"])
    return totals


def plot_total_runs_by_team(deliveries: list[dict[str, str]]) -> None:
    """Plot total IPL runs scored by each team."""
    totals = runs_by_team(deliveries)
    sorted_teams = sorted(totals.items(), key=lambda item: item[1], reverse=True)

    plot_horizontal_bar(
        sorted_teams,
        title="Total Runs Scored by IPL Teams",
        subtitle="All seasons, 2008–2017, including extras",
        xlabel="Total runs",
        ylabel="Team",
    )
