""" # Number of matches played per year for all the years in IPL.
# Plot a bar chart. """

import matplotlib.pyplot as plt

def plot_matches_played_per_year(matches: list[dict[str, str]]) -> None:
    """Plot a bar chart of number of matches played per year."""
    # Count matches played per year
    counts = {}
    for match in matches:
        season = match["season"]
        if season not in counts:
            counts[season] = 0
        counts[season] += 1

    # Sort by season
    sorted_counts = sorted(counts.items(), key=lambda item: item[0])

    # Prepare data for plotting
    seasons = [item[0] for item in sorted_counts]
    values = [item[1] for item in sorted_counts]

    # Plot the bar chart
    plt.bar(seasons, values)
    plt.xlabel("Season")
    plt.ylabel("Number of Matches Played")
    plt.title("Number of Matches Played Per Year in IPL")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
