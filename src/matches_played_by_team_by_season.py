"""Plot a stacked bar chart of number of games played by team by season."""

import matplotlib.pyplot as plt

def plot_matches_played_by_team_by_season(matches: list[dict[str, str]]) -> None:
    """Plot a stacked bar chart of number of games played by team by season."""
    # Count matches played by team by season
    counts = {}
    for match in matches:
        season = match["season"]
        team1 = match["team1"]
        team2 = match["team2"]
        if season not in counts:
            counts[season] = {}
        if team1 not in counts[season]:
            counts[season][team1] = 0
        if team2 not in counts[season]:
            counts[season][team2] = 0
        counts[season][team1] += 1
        counts[season][team2] += 1

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
    ax.set_ylabel("Number of Matches Played")
    ax.set_title("Number of Matches Played by Team by Season")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
