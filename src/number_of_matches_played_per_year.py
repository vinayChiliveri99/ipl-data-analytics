"""Number of matches played per year for all the years in the IPL."""

from src.plotting import plot_column_chart


def matches_per_season(matches: list[dict[str, str]]) -> dict[str, int]:
    """Count how many matches were played in each season."""
    counts = {}
    for match in matches:
        season = match["season"]
        if season not in counts:
            counts[season] = 0
        counts[season] += 1
    return counts


def plot_matches_played_per_year(matches: list[dict[str, str]]) -> None:
    """Plot a bar chart of the number of matches played per year."""
    counts = matches_per_season(matches)
    sorted_counts = sorted(counts.items(), key=lambda item: item[0])

    plot_column_chart(
        sorted_counts,
        title="Matches Played per IPL Season",
        subtitle="Number of matches in each season, 2008–2017",
        xlabel="Season",
        ylabel="Matches played",
    )
