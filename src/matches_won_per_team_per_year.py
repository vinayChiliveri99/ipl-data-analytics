""" Number of matches won per team per year in IPL.
Plot a stacked bar chart. """

import matplotlib.pyplot as plt

def plot_matches_won_per_team_per_year(matches: list[dict[str, str]]) -> None:
    """Plot a stacked bar chart of number of matches won per team per year."""
    # Count matches won by team by year
    counts = {}
    for match in matches:
        season = match["season"]
        winner = match["winner"]
        if season not in counts:
            counts[season] = {}
        if winner not in counts[season]:
            counts[season][winner] = 0
        counts[season][winner] += 1

    # Convert to a list of (season, team, count) tuples
    data = []
    for season, teams in counts.items():
        for team, count in teams.items():
            data.append((season, team, count))

    # Sort by season and then by team
    data.sort(key=lambda x: (x[0], x[1]))

    # Prepare data for plotting
    seasons = sorted(set(season for season, _, _ in data))
    teams = sorted(set(team for _, team, _ in data))
    values = {team: [0] * len(seasons) for team in teams}
    for season, team, count in data:
        season_index = seasons.index(season)
        values[team][season_index] = count

    # Plot the stacked bar chart
    _, ax = plt.subplots()
    bottom = [0] * len(seasons)
    for team in teams:
        ax.bar(seasons, values[team], bottom=bottom, label=team)
        bottom = [bottom[i] + values[team][i] for i in range(len(seasons))]

    ax.set_xlabel("Season")
    ax.set_ylabel("Number of Matches Won")
    ax.set_title("Number of Matches Won Per Team Per Year in IPL")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
