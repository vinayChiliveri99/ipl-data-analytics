"""Top batsmen for Royal Challengers Bangalore by runs scored for the team.

Considers only balls faced while RCB was batting, across the history of the IPL.
"""

from src.plotting import plot_horizontal_bar

RCB = "Royal Challengers Bangalore"


def runs_by_batsman(deliveries: list[dict[str, str]], team: str) -> dict[str, int]:
    """Sum batsman_runs for every batsman, counting only balls faced for `team`."""
    totals = {}
    for ball in deliveries:
        if ball["batting_team"] != team:
            continue
        batsman = ball["batsman"]
        if batsman not in totals:
            totals[batsman] = 0
        totals[batsman] += int(ball["batsman_runs"])
    return totals


def top_batsmen(
    deliveries: list[dict[str, str]], team: str, top_n: int
) -> list[tuple[str, int]]:
    """Return the top `top_n` (batsman, runs) pairs for `team`, highest first."""
    totals = runs_by_batsman(deliveries, team)
    sorted_batsmen = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    return sorted_batsmen[:top_n]

def plot_top_rcb_batsmen(deliveries: list[dict[str, str]], top_n: int = 10) -> None:
    """Plot the top `top_n` RCB batsmen by total runs scored."""
    plot_horizontal_bar(
        top_batsmen(deliveries, RCB, top_n),
        title=f"Top {top_n} Batsmen for {RCB} by Total Runs",
        xlabel="Total Runs",
        ylabel="Batsman",
    )
