"""Number of matches won by each team in each season, as a stacked bar chart."""

from src.plotting import plot_stacked_bar
from src.teams import TEAM_GROUPS, team_group


def matches_won_by_season(
    matches: list[dict[str, str]],
) -> dict[str, dict[str, int]]:
    """Count wins per season for each team group.

    Matches with no result have an empty winner and are skipped.
    """
    counts = {}
    for match in matches:
        winner = match["winner"]
        if winner == "":
            continue

        season = match["season"]
        if season not in counts:
            counts[season] = {}

        group = team_group(winner)
        if group not in counts[season]:
            counts[season][group] = 0
        counts[season][group] += 1
    return counts


def count_no_result_matches(matches: list[dict[str, str]]) -> int:
    """Count matches that ended without a winner."""
    count = 0
    for match in matches:
        if match["winner"] == "":
            count += 1
    return count


def plot_matches_won_per_team_per_year(matches: list[dict[str, str]]) -> None:
    """Plot a stacked bar chart of the number of matches won per team per year."""
    no_results = count_no_result_matches(matches)

    plot_stacked_bar(
        matches_won_by_season(matches),
        groups=TEAM_GROUPS,
        title="Matches Won by Each Team per Season",
        subtitle=f"Excludes {no_results} matches that ended with no result",
        xlabel="Season",
        ylabel="Matches won",
    )
