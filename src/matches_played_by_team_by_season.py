"""Number of matches played by each team in each season, as a stacked bar chart."""

from src.plotting import plot_stacked_bar
from src.teams import TEAM_GROUPS, team_group


def matches_played_by_season(
    matches: list[dict[str, str]],
) -> dict[str, dict[str, int]]:
    """Count matches per season for each team group.

    Every match counts once for each of its two teams.
    """
    counts = {}
    for match in matches:
        season = match["season"]
        if season not in counts:
            counts[season] = {}

        for team in (match["team1"], match["team2"]):
            group = team_group(team)
            if group not in counts[season]:
                counts[season][group] = 0
            counts[season][group] += 1
    return counts


def plot_matches_played_by_team_by_season(matches: list[dict[str, str]]) -> None:
    """Plot a stacked bar chart of the number of matches played by team by season."""
    plot_stacked_bar(
        matches_played_by_season(matches),
        groups=TEAM_GROUPS,
        title="Matches Played by Each Team per Season",
        subtitle="Each match counts once for each of its two teams",
        xlabel="Season",
        ylabel="Matches played",
    )
